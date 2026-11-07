#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Corpus — navigate the AI safety research corpus without loading it.

The corpus is far larger than any context window, so it is never read whole.
This script is the reading apparatus: find the relevant sections, then pull
only those lines.

    toc       Print the curated outline at the top of the corpus
    outline   List headings with line numbers (optionally scoped or depth-limited)
    search    Rank sections by relevance to query terms, with matching snippets
    read      Print a slice, either by line range or by section heading

Every result carries line numbers so a `search` hit feeds straight into `read`,
and so citations point at something the owner can open themselves.

Fenced code blocks are tracked, so `# comment` lines inside notebook code are
not mistaken for markdown headings.

Usage:
    uv run scripts/corpus.py toc
    uv run scripts/corpus.py outline --depth 2 --under "Superposition"
    uv run scripts/corpus.py search activation patching --limit 5
    uv run scripts/corpus.py read --lines 9979-10040
    uv run scripts/corpus.py read --section "Cultivating Research Taste"

Exit codes: 0 = results, 1 = no results, 2 = error.
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_CORPUS_NAME = "default_600k.md"
# Exactly one space after the hashes: real markdown headings use one, while
# indented code comments ("#     title=...") in the corpus's notebooks do not.
HEADING_RE = re.compile(r"^(#{1,6}) (\S.*?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# Strip markdown link syntax so headings read cleanly: [Title](url) -> Title
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+-]*")


def find_corpus(explicit: str | None) -> Path:
    """Resolve the corpus path, searching upward from cwd when not given."""
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"corpus not found: {path}")
        return path
    here = Path.cwd().resolve()
    for directory in [here, *here.parents][:6]:
        candidate = directory / DEFAULT_CORPUS_NAME
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"could not find {DEFAULT_CORPUS_NAME} in {here} or its parents; "
        f"pass --corpus PATH"
    )


def load(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def clean_title(raw: str) -> str:
    return LINK_RE.sub(r"\1", raw).replace("**", "").strip()


def parse_headings(lines: list[str]) -> list[dict]:
    """Return [{line, level, title}], skipping anything inside a code fence."""
    headings: list[dict] = []
    in_fence = False
    for index, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append({
                "line": index,
                "level": len(match.group(1)),
                "title": clean_title(match.group(2)),
            })
    return headings


def section_bounds(headings: list[dict], position: int, total: int) -> int:
    """End line of the section starting at headings[position] (inclusive)."""
    level = headings[position]["level"]
    for following in headings[position + 1:]:
        if following["level"] <= level:
            return following["line"] - 1
    return total


def ancestry(headings: list[dict], position: int) -> list[str]:
    """Heading titles above headings[position], outermost first."""
    trail: list[str] = []
    level = headings[position]["level"]
    for previous in reversed(headings[:position]):
        if previous["level"] < level:
            trail.append(previous["title"])
            level = previous["level"]
            if level == 1:
                break
    return list(reversed(trail))


def cmd_toc(lines: list[str], args) -> int:
    """Print the hand-written outline that precedes the first h1/h2."""
    end = len(lines)
    for index, line in enumerate(lines, start=1):
        if re.match(r"^#{1,2}\s+\S", line):
            end = index - 1
            break
    end = min(end, args.max_lines)
    emit_lines(lines, 1, end, args)
    return 0


def cmd_outline(lines: list[str], args) -> int:
    headings = parse_headings(lines)
    start, stop = 1, len(lines)
    if args.under:
        needle = args.under.lower()
        match = next(
            (i for i, h in enumerate(headings) if needle in h["title"].lower()), None
        )
        if match is None:
            print(f"no heading matching {args.under!r}", file=sys.stderr)
            return 1
        start = headings[match]["line"]
        stop = section_bounds(headings, match, len(lines))
    selected = [
        h for h in headings
        if start <= h["line"] <= stop and h["level"] <= args.depth
    ]
    if not selected:
        print("no headings matched", file=sys.stderr)
        return 1
    selected = selected[: args.limit]
    if args.json:
        print(json.dumps({"headings": selected}, indent=2))
    else:
        for h in selected:
            print(f"{h['line']:>6}  {'  ' * (h['level'] - 1)}{h['title']}")
    return 0


def cmd_search(lines: list[str], args) -> int:
    terms = [t.lower() for t in args.terms]
    headings = parse_headings(lines)
    if not headings:
        print("corpus has no headings to search", file=sys.stderr)
        return 1
    total = len(lines)

    # Line numbers where any term appears, once, reused for every span below.
    hit_lines: list[int] = []
    hit_terms: dict[int, set[str]] = {}
    for offset, line in enumerate(lines, start=1):
        low = line.lower()
        present = {term for term in terms if term in low}
        if present:
            hit_lines.append(offset)
            hit_terms[offset] = present

    if not hit_lines:
        print(f"no matches for {' '.join(terms)}", file=sys.stderr)
        return 1

    results = []
    for position, heading in enumerate(headings):
        # Score the leaf span — this heading up to the next heading of any level.
        start = heading["line"]
        end = headings[position + 1]["line"] - 1 if position + 1 < len(headings) else total
        span_hits = [n for n in hit_lines if start <= n <= end]
        if not span_hits:
            continue
        covered = set().union(*(hit_terms[n] for n in span_hits))
        # Every term must appear somewhere in the span when several were given.
        if len(covered) < len(terms):
            continue

        window_start, window_end, density = densest_window(span_hits, start, end, args.window)
        title = heading["title"].lower()
        # Density beats raw volume, so an 8000-line unheaded blob cannot outrank
        # the section actually about the query just by being enormous.
        score = density + 25 * sum(1 for term in terms if term in title)
        results.append({
            "score": score,
            "hits": len(span_hits),
            "heading_line": start,
            "section_end": section_bounds(headings, position, total),
            "read_start": window_start,
            "read_end": window_end,
            "title": heading["title"],
            "path": ancestry(headings, position),
            "snippets": [
                (n, trim(lines[n - 1])) for n in span_hits[: args.snippets]
            ],
        })

    if not results:
        print(f"no section contains all of: {' '.join(terms)}", file=sys.stderr)
        return 1

    results.sort(key=lambda r: (-r["score"], r["heading_line"]))
    results = results[: args.limit]

    if args.json:
        print(json.dumps({"terms": terms, "results": results}, indent=2))
        return 0

    for result in results:
        trail = " > ".join(result["path"]) if result["path"] else "(top level)"
        print(f"\n{result['title']}  [heading at line {result['heading_line']}]")
        print(f"    in: {trail}")
        print(f"    {result['hits']} hits; read --lines {result['read_start']}-{result['read_end']}")
        for line_number, text in result["snippets"]:
            print(f"    {line_number:>6}: {text}")
    return 0


def densest_window(hits: list[int], start: int, end: int, width: int):
    """Smallest readable window covering the tightest cluster of hits."""
    if end - start + 1 <= width:
        return start, end, len(hits)
    best_count, best_at = 0, hits[0]
    for index, first in enumerate(hits):
        count = 0
        for later in hits[index:]:
            if later - first >= width:
                break
            count += 1
        if count > best_count:
            best_count, best_at = count, first
    window_start = max(start, best_at - width // 8)
    return window_start, min(end, window_start + width - 1), best_count


def trim(text: str, limit: int = 160) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def cmd_read(lines: list[str], args) -> int:
    if args.section:
        headings = parse_headings(lines)
        needle = args.section.lower()
        match = next(
            (i for i, h in enumerate(headings) if needle in h["title"].lower()), None
        )
        if match is None:
            print(f"no heading matching {args.section!r}", file=sys.stderr)
            return 1
        start = headings[match]["line"]
        end = section_bounds(headings, match, len(lines))
    else:
        bounds = re.fullmatch(r"(\d+)-(\d+)", args.lines or "")
        if not bounds:
            print("--lines expects START-END, e.g. --lines 120-260", file=sys.stderr)
            return 2
        start, end = int(bounds.group(1)), int(bounds.group(2))
        if start > end:
            print("--lines START must not exceed END", file=sys.stderr)
            return 2
    emit_lines(lines, start, end, args)
    return 0


def emit_lines(lines: list[str], start: int, end: int, args) -> None:
    start = max(1, start)
    end = min(end, len(lines))
    truncated = False
    if end - start + 1 > args.max_lines:
        end = start + args.max_lines - 1
        truncated = True
    body = lines[start - 1:end]
    if args.json:
        print(json.dumps(
            {"start": start, "end": end, "truncated": truncated, "text": "\n".join(body)},
            indent=2,
        ))
        return
    print(f"===== lines {start}-{end} =====")
    print("\n".join(body))
    if truncated:
        print(
            f"\n[truncated at {args.max_lines} lines — continue with --lines {end + 1}-...]",
            file=sys.stderr,
        )


def build_parser() -> argparse.ArgumentParser:
    # Shared options, attached to both the top level and every subcommand, so
    # `--json read ...` and `read --json ...` both work.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--corpus", help=f"path to the corpus (default: nearest {DEFAULT_CORPUS_NAME})")
    common.add_argument("--json", action="store_true", help="emit JSON instead of text")
    common.add_argument("--max-lines", type=int, default=400, help="cap on printed lines (default 400)")
    common.add_argument("--verbose", action="store_true", help="report the resolved corpus path")

    parser = argparse.ArgumentParser(
        prog="corpus.py",
        parents=[common],
        description="Search and read the AI safety research corpus.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("toc", parents=[common], help="print the curated outline at the top of the corpus")

    outline = sub.add_parser("outline", parents=[common], help="list headings with line numbers")
    outline.add_argument("--depth", type=int, default=3, help="max heading level to show (default 3)")
    outline.add_argument("--under", help="only headings inside the section matching this text")
    outline.add_argument("--limit", type=int, default=200, help="max headings to print (default 200)")

    search = sub.add_parser("search", parents=[common], help="rank sections by relevance to terms")
    search.add_argument("terms", nargs="+", help="one or more search terms")
    search.add_argument("--limit", type=int, default=8, help="max sections to report (default 8)")
    search.add_argument("--snippets", type=int, default=3, help="matching lines per section (default 3)")
    search.add_argument("--window", type=int, default=200, help="readable window size around hits (default 200)")

    read = sub.add_parser("read", parents=[common], help="print a slice by line range or section")
    group = read.add_mutually_exclusive_group(required=True)
    group.add_argument("--lines", help="line range, e.g. 120-260")
    group.add_argument("--section", help="heading text to read (to the end of that section)")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        path = find_corpus(args.corpus)
    except FileNotFoundError as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.verbose:
        print(f"corpus: {path}", file=sys.stderr)
    lines = load(path)
    return {
        "toc": cmd_toc,
        "outline": cmd_outline,
        "search": cmd_search,
        "read": cmd_read,
    }[args.command](lines, args)


if __name__ == "__main__":
    raise SystemExit(main())
