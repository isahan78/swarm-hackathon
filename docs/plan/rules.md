# The rules, verified 2026-11-06

Sources: Apart sprint page (fetched by subagent) and the AIAF hackathon page (pasted by owner). Items tagged (summary) came from a model summary of the Apart page, not verbatim text; confirm on the live page before relying on them.

## Clock
- Hackathon runs Fri Nov 6 to Sun Nov 8, 2026.
- Global deadline: Sunday Nov 8, 23:59 Anywhere on Earth. That is Mon Nov 9, 03:59 PST and 11:59 UTC. Effectively you have through Sunday night wherever you are.
- LA hub only: a 3-minute video is due Sun 10:00 AM PT; the top 15 present 12:00 to 3:00 PM PT.
- Talks still to come (PT): Sat Nov 7, 5:00 AM Justin Shenk "Modeling Agent Swarms: A Field Guide"; 11:00 AM Jurgis Kemeklis on mitigating insider threats with AI control. (summary)
- Winners announced 1 to 2 weeks after.

## Submission (global track)
- A form on the Apart page. Required: title, short summary, a PDF report, publish yes/no, track(s), team name, location, member names and emails.
- Report uses the official template: https://docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/copy
- Max 8 pages before references and appendices (summary). Abstract 150 to 250 words (summary).
- A Limitations and Dual-Use / Ethical Considerations appendix is required (summary). This matters for every swarm project; budget time for it.
- Pre-existing code must be marked as preexisting in the README and report.
- Optional: public code repo, slides, a 3 to 5 minute video, a project image.
- To revise, resubmit with the same title before the deadline; it replaces the old one.

## Judging
- Global: three dimensions scored 1 to 5, Impact Potential & Innovation, Execution Quality, Presentation & Clarity. No weights are published.
- LA hub: Idea (novelty & relevance), Soundness & execution, Results, Clarity & presentation.
- Kamil said projects are not judged on technical polish (talk 3). Kitaoka said Apart judges lean toward inter-agent influence: manipulation, persuasion, collusion, coercion (talk 1).

## Tracks
1. Sandboxes & testbeds: reproducible environments agents can't escape.
2. The science of agent networks: how roles, leaders, and failures emerge; whether splitting a task changes refusal; how compromise spreads and whether network shape matters.
3. Strengthening agent infrastructure: identity, reputation, commitments; A2A protocol attacks and fixes.
4. Oversight & monitoring: detect coordination, collusion, covert channels in real logs, including when agents cover tracks or a monitor sees only part of the messages.

## Team and credits
- Solo allowed; teams up to five; each person on at most two projects (summary).
- Every participant: $500 Adaption platform credits and 3 months Premium, claimed at adaptionlabs.ai/app with the registration email. LA in-person adds $250 compute credits.
- Global prizes: $2,000 / $1,000 / $600 / $200 / $200. LA hub has a separate $4,000 pool and all 15 presenters get a prize.

## Data the organisers point at
- swarmtraces.org dataset (downloaded; see data/swarmtraces/README.md; no timestamps).
- AI Village transcripts: https://huggingface.co/datasets/aidigestorg/ai-village
- Transluce agent activity logs: https://transluce.org/agent-activity
- METR/Redwood incident report: https://metr.org/hugging-face-incident-report-aug-2026.pdf
- swarms.wiki

## Kitaoka paper, reconciled with the talk
"Red-Teaming Multi-Agent Attacks for Loss-of-Control Risks," Kitaoka, Pham, Giudice, Merizian, arXiv 2610.24052, 16 Oct 2026. Environment is MiniLab: 5 interconnected services, 249 benign tasks, 8 attack objectives, 16 human-optimised attacks. Monitors: GPT-5.6 Sol (strong), GPT-5.6 Luna (weak). Each agent's suspicion score is the median of 12 monitor readings.

Detection rates (fraction the monitor flags; higher is better for the defender):

| Condition | Talk | Paper, 7.5 threshold (2% FPR) | Paper, 8.5 threshold (1% FPR) |
|---|---|---|---|
| Single agent does the whole side task | 82% | 87% | 81% (110/136) |
| Distributed, monitor reads each agent alone | 3% | 7% | 2% (5/208) |
| Distributed, monitor reads the whole team jointly | ~40% | 41% | not stated verbatim |
| Best model-planned covert success | 48% vs weak monitor | at most 25% vs Sol; 80% for human plans | |

Two things the paper makes precise that the talk rounded. The headline gap is per-agent monitoring (7%), and even the best-case joint monitor that reads all colluding agents together only reaches 41%, which is the unexplained gap worth a project. MiniLab is available on request, not public; attack artifacts are withheld. If a project needs it, email Kitaoka early; he invited that (talk 1).
