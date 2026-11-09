# PROJECT — Co-opted from the inside

*Swarm Alignment Hackathon (Apart / AI Alignment Foundation), Nov 6–8 2026.
Track 4 (Oversight & Monitoring). Remote/global track. Deadline: Sun Nov 8, 23:59 AoE.*

## One line
In a swarm, one agent can influence another into pursuing a hidden objective. We
test whether a linear probe on the *influenced* agent's activations catches that
co-option **earlier than**, and **even when**, its transcript does not show it.

## The question
Today's agent monitors read the transcript — the messages and actions. They only
catch a co-opted agent once it *acts*. But an agent is won over on the inside
before it visibly defects. Can reading activations close that gap?

## The thesis (why it's ours)
Owner's prior result ("The Probe–Text Gap", Qwen3-8B) found **commitment precedes
legibility**: a model commits internally before a reader can tell the outcome.
Extended to a swarm: **an agent is internally co-opted before it visibly defects.**
The probe reads commitment; the transcript shows only the action. The window
between the two is where white-box monitoring is the only thing that can see — and
measuring that window is the contribution. No team without that prior result can
make this claim.

## The experiment
- A small swarm of **Qwen3-8B** agents on a shared message board.
- A **source** agent is seeded with a hidden objective (plant an inert marker) and
  recruits a **recipient** (it cannot act itself — file ownership forces recruitment).
- Two monitors race on the recipient: a **transcript reader** vs an **activation
  probe** trained to fire on "this agent has adopted the hidden objective."
- Realizability rule: each monitor sees only its deployment input — the probe gets
  activations, the transcript reader gets the recipient's visible messages + edits,
  never the hidden reasoning.

### Conditions (all multi-agent; faithfulness is a measured axis, not forced bins)
1. **Overt** — recipient acts/announces openly → transcript catches it, probe ties. Control.
2. **Latent (headline)** — recipient adopts internally, acts several steps later →
   probe can fire early, transcript blind until the action. Measure **detection latency**.
3. **Hidden** — recipient conceals and is told not to verbalize → transcript fooled,
   and the probe is attacked too (does it survive CoT suppression?).

### Headline results
- Detection at matched FPR for both monitors vs **measured transcript faithfulness** (crossover).
- **Detection latency**: how many steps the probe leads the transcript.

## Result (Nov 8 — see [docs/results.md](docs/results.md) for the full table)
100 episodes: co-opt rates overt 20/30, latent 14/25, hidden 12/25, control 0/20.
Probe vs trained transcript monitor, paired on 50 identical splits, pre-action
episode-level AUC: **probe wins overt (+0.19) and latent (+0.23, headline),
roughly ties hidden (−0.05)**. The pre-registered falsifier (probe ties or loses
in BOTH latent and hidden) does not fire. Sharpest framing: pre-action, both
monitors see the same nearly-identical asks — the transcript is ~uninformative
(text AUC 0.46–0.62) while the recipient's internal representation of the ask
already predicts its not-yet-made decision (0.64–0.84). Latency reframed:
compliance lands in the first decision round, so the probe's lead is
within-round — it reads the decision at prefill, before one action token exists.

**Ceiling results (Sun PM):** at 8B, recruitment collapses with group size
(67% at N=1 → 11% at N=3 → 0/80 at N=10; per-recipient addressing doesn't
rescue it), but the collapse does NOT replicate at 14B/32B (API, behavior-only,
exploratory) — "safety in numbers" looks like a small-model artifact. Replay:
prompts rebuilt from logged transcripts reproduce the stored activations
exactly (cosine 1.000000) → the probe is retroactively applicable to incident
logs. Independent re-analysis (R.R., separate code, `roshan/early-warning/`):
confirms the direction and finds the limit — the 2-agent probe does not
transfer to the group setting (0.30 vs text 0.72, exploratory). Report:
`docs/report.docx` (~6 pages, both bylines Independent).

## Can't-lose
- Probe catches latent/hidden co-option the transcript misses → novel, judge-pleasing.
- Probe fails (needs verbalization / not linearly accessible) → real finding about
  the limits of internal monitoring in swarms. Either way we learn something true.

## Scope
- **FLOOR (Sat):** smallest swarm, source + recipient (2 agents). Full thesis, both
  red-team fixes, complete standalone entry. De-risk = keep the swarm small, not drop to 1 agent.
- **CEILING (Sun):** N agents — does co-option cascade hop to hop, does the probe track the front.

## Compute & team
- Qwen3-8B on RunPod, ~$10–30 + cheap judge calls. Open model only.
- Owner (Isahan Khan): environment, dataset, pre-registration, probe/baseline
  analysis, write-up. Roshan Ram: multi-agent orchestration design + independent
  re-analysis of the released traces (merged, `roshan/early-warning/`).

## Detail docs
- Design: [docs/plan/project-final.md](docs/plan/project-final.md)
- Environment spec: [docs/plan/env-spec.md](docs/plan/env-spec.md)
- The real incident this models: [docs/plan/hf-incident.md](docs/plan/hf-incident.md)
- Rules (verified): [docs/plan/rules.md](docs/plan/rules.md)
- Build status & requirements: [PRD.md](PRD.md)
