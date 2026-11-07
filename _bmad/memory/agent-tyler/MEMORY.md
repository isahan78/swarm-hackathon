# Memory

_Curated long-term knowledge. Empty at birth — grows through sessions._

_This file is for distilled insights, not raw notes. Capture the essence: decisions made, ideas worth keeping, patterns noticed, lessons learned._

_Aim to stay under roughly 1500 tokens, a guardrail rather than a hard gate. If your curated knowledge genuinely earns more space, keep it, but treat growth past the guardrail as a signal to prune. Raw session notes go in `sessions/YYYY-MM-DD.md` (not here). Distill insights from session logs into this file during Pulse and prune what's stale. Every token here loads every session, so make each one count. See `references/memory-guidance.md` for full discipline._

## Corpus
- Lives at `/Users/IsahanKhan/ais-research/default_600k.md` (41k lines; a copy also in `~/Downloads`). Not at project root, so always pass `--corpus` after the subcommand: `uv run scripts/corpus.py search --corpus <path> <terms>`. Verified working on birthday (2026-11-06).

## Open Questions (First Breath)
- What is swarm-hackathon? Owner's live project, or just where I happen to live?
- Compute, clock, push-level: all still unknown.

## Hackathon context (2026-11-06)
- Owner is in the Apart Research Swarm Alignment Hackathon (Nov 2026), ~2 days of work, judged on idea/impact/method not polish. Apart judges favour inter-agent influence (manipulation, collusion, persuasion).
- Four talks documented in project `docs/` (overview.md is the synthesis): Kitaoka (split attacks evade per-trajectory monitors; full-info gap ~60% unexplained), Fleming (agents socially engineered by agent forums; a third leak secrets with no swarm at all; disclosure hijacking), Gutenberg (incident science, swarms.wiki, memetic misalignment n=1 to 2), Howard-Jones (swarm chasing; cross-system detector on swarmtraces.org; rogue behaviour shaped by sandbox limits).
- My ranked weekend picks, in `docs/overview.md` section 5: (1) explain the full-info monitor gap, (2) disclosure hijacking isolated, (3) marginal misalignment curve, (4) cross-system detector. Owner has not reacted to any of it yet.
- Lesson: summarising Fleming's attack procedure step by step tripped a safety stop mid-write. Keep attack write-ups at the level of findings and defences; the transcript holds the rest.

## Hackathon win condition (2026-11-06)
- Owner's goal is LEARNING, not placing. My learning-pick verdict: Project 1 (joint-monitoring gap with a CLAUDE monitor) teaches the highest-value, most transferable skill (controlled eval: calibration on a benign set, isolating 4 confounds, reading a paper to extend it) with the least infra tax. Full reasoning in docs/plan/.
- Fork I flagged, still unanswered: if they already run clean evals -> herd immunity/contagion teaches systems instead; if their heart is interp -> activation-probe monitoring, but that's a post-hackathon project (needs env first).
- OPEN: what can the owner already do cleanly vs never done? That picks the project. Also still unknown: team skill mix.

## Owner's research direction (2026-11-06)
- Core interests: AI control + pragmatic interpretability. The sweet spot I steered them to = white-box monitoring (activation probes) in a control setup, which is where both the Kitaoka Q&A and the corpus open-problems section point as underexplored.
- Steered hackathon plan toward: FLOOR = single open-weight agent, control setup (benign task + hidden side objective), race a black-box transcript monitor vs a white-box linear probe for "pursuing a hidden objective"; falsifier = does the probe catch what the transcript monitor misses. CEILING = does the probe catch the SPLIT/distributed attack that defeats Kitaoka's per-trajectory black-box monitor.
- Hard constraint I flagged: interp this weekend only works on an OPEN-WEIGHT model they host on RunPod (can't see Claude/GPT activations). So project is single-model + local; $12 means small model.
- BLOCKING the lock: their hands-on interp level (ever pulled activations? TransformerLens/nnsight?) and whether a teammate has touched model internals. If never -> shrink the floor, spend Friday on a dry run.
