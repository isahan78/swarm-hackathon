"""Build and check a PDF using the event's unmodified DOCX as reference.

Requires pandoc, LibreOffice, python-docx and pypdf. The report's claims remain
in Markdown; this script changes layout only and records build verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile


def build(project: Path, output: Path) -> dict:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt, RGBColor
    from lxml import etree as ET
    from pypdf import PdfReader

    source = project / "report/submission_report.md"
    reference = project / "report/template/swarm_alignment_official_template.docx"
    text = source.read_text()
    title = text.splitlines()[0].removeprefix("# ")
    abstract = text.split("## Abstract\n", 1)[1].split("\n## ", 1)[0].strip()
    words = len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", abstract))
    if not 150 <= words <= 250:
        raise ValueError(f"Abstract has {words} words; expected 150–250")
    required = "Appendix A. Limitations and Dual-Use / Ethical Considerations"
    if required not in text:
        raise ValueError("Missing required limitations/ethics appendix")
    for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if not (source.parent / target).resolve().is_file():
            raise FileNotFoundError(target)
    for executable in ("pandoc", "soffice"):
        if not shutil.which(executable):
            raise RuntimeError(f"Install {executable} before building the report")
    output.mkdir(parents=True, exist_ok=True)
    docx_path = output / "submission_report.docx"
    with tempfile.TemporaryDirectory(prefix="swarm-report-") as directory:
        temporary = Path(directory)
        # Google Docs omits some styles that Pandoc's generated body uses.
        # Add only missing structural styles from Pandoc's default reference;
        # preserve every existing official-template style and section setting.
        fallback = subprocess.run(["pandoc", "--print-default-data-file=reference.docx"],
                                  check=True, capture_output=True).stdout
        from io import BytesIO
        with zipfile.ZipFile(reference) as archive:
            ref_parts = {name: archive.read(name) for name in archive.namelist()}
        with zipfile.ZipFile(BytesIO(fallback)) as archive:
            fallback_styles = ET.fromstring(archive.read("word/styles.xml"))
        official_styles = ET.fromstring(ref_parts["word/styles.xml"])
        w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        identifiers = {style.attrib.get(w + "styleId") for style in official_styles}
        for style in fallback_styles:
            identifier = style.attrib.get(w + "styleId")
            if identifier and identifier not in identifiers:
                official_styles.append(style)
        ref_parts["word/styles.xml"] = ET.tostring(official_styles, encoding="utf-8", xml_declaration=True)
        derived_reference = temporary / "official-with-structural-styles.docx"
        with zipfile.ZipFile(derived_reference, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in ref_parts.items():
                archive.writestr(name, data)
        md = temporary / "body.md"
        md.write_text(text.split("\n", 1)[1])
        subprocess.run([
            "pandoc", str(md), "--from=markdown", "--to=docx",
            "--standalone", "--shift-heading-level-by=-1",
            f"--metadata=title:{title}", f"--reference-doc={derived_reference}",
            f"--resource-path={source.parent}:{project}", "-o", str(docx_path),
        ], check=True)
        # Pandoc 3.1 retains the Google template's embedded TTF parts but can
        # omit their MIME entry. Repair only the generated package, never the
        # original downloaded template, before python-docx reads it.
        with zipfile.ZipFile(docx_path) as archive:
            parts = {name: archive.read(name) for name in archive.namelist()}
        changed = False
        # Some Pandoc versions keep the font relationships but drop the
        # embedded font files themselves; restore them from the reference.
        for name, data in ref_parts.items():
            if name.startswith("word/fonts/") and name not in parts:
                parts[name] = data
                changed = True
        types = ET.fromstring(parts["[Content_Types].xml"])
        namespace = "{http://schemas.openxmlformats.org/package/2006/content-types}"
        if any(name.endswith(".ttf") for name in parts) and not any(
                item.attrib.get("Extension") == "ttf" for item in types):
            ET.SubElement(types, namespace + "Default", {
                "Extension": "ttf", "ContentType": "application/x-font-ttf"})
            parts["[Content_Types].xml"] = ET.tostring(types, encoding="utf-8", xml_declaration=True)
            changed = True
        if changed:
            with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for name, data in parts.items():
                    archive.writestr(name, data)
        document = Document(docx_path)
        # The reference template applies these properties directly to its
        # guidance paragraphs. Transfer those same properties to report styles.
        for section in document.sections:
            section.page_width, section.page_height = Inches(8.5), Inches(11)
            section.top_margin = section.bottom_margin = Inches(1)
            section.left_margin = section.right_margin = Inches(1)
            section.header_distance = section.footer_distance = Inches(0.5)
        for name in ("Normal", "normal", "Body Text", "BodyText", "First Paragraph", "Compact"):
            if name in document.styles:
                style = document.styles[name]
                style.font.name = "Old Standard TT"
                style.font.size = Pt(11)
                style.paragraph_format.line_spacing = 1.15
                style.paragraph_format.space_after = Pt(6)
                if name in ("Body Text", "BodyText", "First Paragraph", "Compact"):
                    style.base_style = document.styles["Normal"]
        for name, size in (("Title", 20), ("Heading 1", 14),
                           ("Heading 2", 13), ("Heading 3", 12)):
            if name in document.styles:
                style = document.styles[name]
                style.font.name = "Old Standard TT"
                style.font.size = Pt(size)
                style.font.bold = True
                style.font.color.rgb = RGBColor.from_string("434343")
                style.paragraph_format.keep_with_next = True
        for name in ("Caption", "Image Caption", "Table Caption"):
            if name in document.styles:
                document.styles[name].font.name = "Old Standard TT"
                document.styles[name].font.size = Pt(10)
        before_abstract = True
        for paragraph in document.paragraphs:
            if paragraph.text == "Abstract":
                before_abstract = False
            if before_abstract or paragraph.text == "Abstract":
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if paragraph.text == "References" or paragraph.text.startswith("Appendix "):
                paragraph.paragraph_format.page_break_before = True
            # Keep the manually numbered explanatory caption with its picture.
            if paragraph._p.xpath(".//w:drawing"):
                paragraph.paragraph_format.keep_with_next = True
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Replace the template's literal page placeholder with a real PAGE field.
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        for section in document.sections:
            for paragraph in section.footer.paragraphs:
                if paragraph.text.strip() == "X":
                    paragraph.clear()
                    field = OxmlElement("w:fldSimple")
                    field.set(qn("w:instr"), "PAGE")
                    paragraph._p.append(field)
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        paragraph.paragraph_format.space_after = Pt(3)
                        paragraph.paragraph_format.line_spacing = 1.0
                        for run in paragraph.runs:
                            run.font.name = "Old Standard TT"
                            run.font.size = Pt(10)
        document.save(docx_path)
        fonts = project / "report/template/fonts"
        font_config = temporary / "fonts.conf"
        from xml.sax.saxutils import escape
        font_config.write_text(
            '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">'
            '<fontconfig><include ignore_missing="yes">/etc/fonts/fonts.conf</include>'
            f'<dir>{escape(str(fonts))}</dir>'
            f'<cachedir>{escape(str(temporary / "font-cache"))}</cachedir></fontconfig>'
        )
        environment = os.environ.copy()
        environment["FONTCONFIG_FILE"] = str(font_config)
        environment["XDG_CACHE_HOME"] = str(temporary / "cache")
        subprocess.run([
            "soffice", f"-env:UserInstallation={(temporary / 'lo').as_uri()}",
            "--headless", "--convert-to", "pdf", "--outdir", str(output),
            str(docx_path),
        ], check=True, env=environment, timeout=120)
    pdf = output / "submission_report.pdf"
    reader = PdfReader(pdf)
    pages = [page.extract_text() or "" for page in reader.pages]
    reference_page = next(
        (i for i, page in enumerate(pages) if re.search(r"(?m)^References\s*$", page)), None
    )
    if reference_page is None:
        raise ValueError("Could not locate References page for main-text page count")
    if reference_page > 8:
        raise ValueError(f"Main report uses {reference_page} pages (maximum eight)")
    if pdf.stat().st_size > 25_000_000:
        raise ValueError("PDF exceeds upload limit")
    verification = {
        "format": "Official DOCX reference template, same paper/margins/font sizing",
        "template_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
        "markdown_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "abstract_words": words,
        "main_pages_before_references": reference_page,
        "total_pages": len(pages),
        "pdf_bytes": pdf.stat().st_size,
        "required_ethics_appendix_present": required in text,
        "affiliations_supplied": "not yet supplied" not in text,
        "publication_verified": False,
        "publication_verification_note": "The PDF build does not check GitHub publication; verify the remote branch separately.",
        "submission_made": False,
    }
    (output / "submission_build.json").write_text(json.dumps(verification, indent=2) + "\n")
    return verification


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    print(json.dumps(build(project, (args.output or project / "report").resolve()), indent=2))


if __name__ == "__main__":
    main()
