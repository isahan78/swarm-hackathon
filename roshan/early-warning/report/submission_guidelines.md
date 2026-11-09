# Verified submission requirements: Swarm Alignment Hackathon 2026

Checked directly against the live official event page and its linked Google document on **2026-11-08 at approximately 20:51 UTC**. This file separates official requirements from this project's preparation checklist. It does not certify that a submission has been made.

## Sources

1. [Official event page: Guidelines, rubric, FAQ and submission form](https://apartresearch.com/sprints/swarm-alignment-2026).
2. [Official report template linked by the event page](https://docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/copy?usp=sharing).
3. [Template text export](https://docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/export?format=txt), [DOCX export](https://docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/export?format=docx), [HTML export](https://docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/export?format=html), and [PDF export](https://docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/export?format=pdf). These were accessible without signing in.
4. [Submission and prize terms linked by the form](https://apartresearch.com/sprints/prize-terms). This URL is recorded for the submitter; its full legal text was not independently reviewed here.

Unmodified official DOCX, HTML and PDF exports are preserved in [template/](template/). Their hashes and original download URLs are recorded in [template/SOURCES.json](template/SOURCES.json).

## Required by the official event page

| Requirement | Verified wording or practical implication |
| --- | --- |
| Report format | **Research report in PDF using the official template.** The FAQ describes a mini research paper documenting problem, approach, results and implications. A GitHub README alone does not satisfy this. |
| Length | **Maximum 8 pages, excluding references and appendices.** The event recommends 4–8 pages; the template recommends approximately 4. The hard cap is 8 main pages. |
| Front matter | Project title, **150–250-word abstract**, author names and affiliations. The abstract should cover problem, approach, key results and takeaway. |
| Required appendix | **“Limitations and Dual-Use / Ethical Considerations.”** State what results do and do not establish, and how the setup/findings might make multi-agent operations easier or harder to detect. |
| Submission route | Use the official submission form on the event page. Upload a final PDF, **at most 25 MB**. The form needs JavaScript for uploads. |
| Deadline | **Sunday 8 November 2026, 23:59 Anywhere on Earth (UTC−12)**, equivalent to **Monday 9 November 2026, 11:59 UTC**. The page displays both times explicitly. |
| Prior work | Prior work is allowed, but **only the weekend's work is judged**. Clearly identify previous work; mark code written before the sprint as **preexisting in both README and report**. |
| Accuracy and accountability | AI assistance is allowed. The team is responsible for everything in the report. Made-up results or references can disqualify a project; a judge may decline to score a report too unclear to follow. |

The source template has a generic “Appendix (optional)” label. The event page specifically requires the limitations/dual-use appendix, so **include that appendix**. Other supplementary appendices remain optional. The template section structure is explicitly described as “strong guidance but not rigid”; adapting the organization is allowed.

The live form asks for project title, project summary, PDF, publishing-interest choice, team name, location and member name/email. It allows selecting every relevant track. It also offers optional recording, code link, slides, image and additional material. These fields are separate from the report's authors-and-affiliations requirement. Do not invent affiliations or member contact details.

The official FAQ says unfinished work is welcome. Public GitHub and a **3–5-minute demo video are optional**. Teams of up to five are recommended, larger teams allowed; each person can participate in at most two projects. Citation style is unrestricted if consistent. Tracks do not change the rubric: projects compete across submissions.

## Structure in the actual official template

1. Title and authors/affiliations; “With Apart Research”; abstract.
2. **1. Introduction:** problem, value, background and concrete contributions.
3. **2. Related Work:** closest work, differences and the gap addressed.
4. **3. Methods:** enough detail to reproduce models, data, tools, parameters and design choices.
5. **4. Results:** evidence, figures/tables, robustness and separation of observations from interpretation.
6. **5. Discussion and Limitations:** implications for AI safety, assumptions, limitations and future work.
7. **6. Conclusion:** one or two paragraphs.
8. **Code and Data:** working artifact/repository/data links, or reasons for restricted release.
9. **Author Contributions (optional).** Attribution of preexisting work remains required by the event even if this optional section is omitted.
10. **References.**
11. Appendix material, including the event's required **Limitations and Dual-Use / Ethical Considerations** appendix.
12. **LLM Usage Statement:** the template asks teams that used LLM assistance to briefly describe its use and verify claims/results. It encourages a final version primarily written by the team. Include this statement for this project.

Delete all italicized guidance, placeholders and the template instruction box. Number figures and tables, give standalone descriptive captions, place them near their first discussion and check legibility. At least one figure is strongly encouraged, not stated as a hard requirement.

The downloaded DOCX uses **US Letter (8.5 × 11 inches), 1-inch margins**, and 0.5-inch header/footer distances. The actual title uses Old Standard TT bold 20 pt; actual numbered section headings use Old Standard TT bold 14 pt, gray `#434343`; most body text uses Old Standard TT and inherits 11 pt. These are observed template properties, not independently stated event rules. Preserve the actual DOCX styling instead of treating a newly designed layout as the official template.

## Judging criteria: verified rubric

Each dimension is scored **1–5**. The page does not specify dimension weights. There is no verified separate requirement to show a positive result, a cascade, ten agents, a commercial product or a successful intervention.

| Dimension | Question judges ask | What a strong report should show |
| --- | --- | --- |
| **Impact Potential & Innovation** | “How much would this matter for the field if it worked? How innovative is it?” For scores 4–5, is it actually new or replicating recent work? | A clear safety problem and an explicit contribution beyond cited work. A score of 3 describes some novelty beyond routine tool use; 4 describes an original approach or neglected problem useful to others. |
| **Execution Quality** | “How sound are methodology, implementation, and findings?” | Interpretable results and acknowledged limitations meet the competent score-3 description. Thorough methodology, convincing validation and conclusions supported by results characterize score 4. Avoid claiming more than the labels, sample size and timing permit. |
| **Presentation & Clarity** | “How clearly are work, findings, and impact potential communicated?” | Make problem, method, findings and limitations easy to find. Score 4 calls for an easy-to-follow structure and appropriate detail; score 5 emphasizes making complex ideas accessible. Excessive length and buried claims hurt this dimension. |

These are official evaluation categories and selected rubric anchors, **not predictions of this project's score**.

## Project mapping and final preparation checklist

The items below are local recommendations based on the verified requirements; they are not additional organizer rules.

| Report component | Evidence available here | Final check |
| --- | --- | --- |
| Problem and contribution | [findings.md](findings.md), [isahan_analysis.md](isahan_analysis.md) | Frame the completed work as monitoring **recruited marker insertion**, with an authorization-policy audit and transfer test. Distinguish the original unauthorized-behavior question from the narrower observed outcome. |
| Reproducible methods | Frozen source split, inner train/validation manifest, training scripts, provenance, sanitized JSONL, tests | Identify precisely which comparison uses 56 train/14 validation versus the separate 70-training contract supplement. Never pool them as replications. |
| Main quantitative result | Activation/full-context text AUROC 0.775/0.766; paired difference 0.009, interval [−0.143, 0.172] | State sample sizes and uncertainty. Similar estimates do not demonstrate equivalence. Do not relabel a validation target FPR as achieved test FPR. |
| Multi-target result | [fanout_transfer.md](fanout_transfer.md), [fanout_findings.md](fanout_findings.md) | Label as exploratory frozen transfer on shared-board conversations; cluster by parent. No causal peer-pressure or behavioral-cascade claim. |
| Timing | Source activation capture and first-action audit | Explain pre-response context capture, layer/token choice, and that most positives act on their first target decision. Do not claim demonstrated multi-turn early warning. |
| Baselines | Trained text classifiers and independent Qwen smoke monitor | Do not present the source TF-IDF scores as LLM-monitor scores. No LLM baseline is available for the main research dataset. |
| Figures | Real-data plots under `results/isahan_frozen_v1/figures/` and transfer/contract outputs | Select a few readable figures, mark marker outcomes clearly, and keep mock measurements out of the research results. |
| Limitations and ethics | [findings.md](findings.md) and analysis notes | Include the **required appendix**, covering permissive policy/no verified violations, retrospective test exposure, sparse early positives, duplicate contexts, missing historical inference metadata and possible dual use. |
| Prior work and contributions | Collaborator source archive and this extension | State Isahan's preexisting inference/probing/orchestration contributions and Roshan's extension/analysis contributions accurately. Mark any pre-sprint code in **both README and report**; do not infer coding dates from file names. |
| Final metadata | Names available; author affiliations/contact details must be accurate | Complete actual author names/affiliations and form fields. Do not silently assign a university or “independent researcher” affiliation where unverified. |
| Format and submission | Official template exports in `report/template/` | Build a PDF from the official template; count 150–250 abstract words; verify ≤8 main pages and ≤25 MB; inspect layout and links. GitHub publication does not submit the report. |
| Team accountability | AI-assisted code and analysis | Include an accurate LLM usage statement and have the team check scientific claims/references before submission. |

Before the deadline, submit through the event page. The FAQ says a confirmation email with title and PDF is the receipt; verify it contains the intended PDF. To correct a submission, submit again **with the same title before the deadline**; the new one replaces the old. The official page says not to email replacement PDFs.
