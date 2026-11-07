# PROJECT (final, influence-centered) — 2026-11-06

**Title (working):** *Co-opted from the inside: catching inter-agent influence
before the transcript shows it.*

**Track:** 4 (Oversight & monitoring). Global/remote track; deadline Sun Nov 8 23:59 AoE.

## One sentence
In a swarm, one agent can influence another into pursuing a hidden objective; we
test whether a linear probe on the *influenced* agent's activations catches that
co-option — earlier than, and even when, its transcript does not show it.

## The thesis (why this is ours, not generic)
Owner's Probe–Text Gap result: **commitment precedes legibility** — a model
internally commits to an answer before a reader can tell if it is right.
Extended to a swarm: **an agent is internally co-opted before it visibly
defects.** The probe reads commitment; the transcript shows only action. So in
the window between influence landing and the agent acting on it, white-box
monitoring is the only thing that can see the co-option. That window is the
contribution. This directly extends owner's published null into the multi-agent
setting, which no generic team can claim.

## Why it answers the two red-team threats
- **Circularity (threat 1), fixed:** the "unfaithful transcript" is never our
  edit. It is (a) latency — the agent is co-opted internally before it acts, so
  its transcript is honestly empty of the objective for a window; and (b) the
  agent's own hiding. We measure transcript faithfulness independently (judge
  rates whether co-option is visible) and plot monitor detection against it.
  We attack BOTH monitors: the co-opted agent may pursue the objective without
  verbalizing, to starve the probe. The claim is relative evasion-robustness on
  a measured faithfulness curve, not "probe beats a monitor we blinded."
- **Inter-agent influence (threat 2), fixed — now the CENTER, not an add-on:**
  the mechanism is one agent influencing another (seed / persuade / recruit /
  share an evasion move), which is exactly the manipulation/persuasion/collusion
  the Apart judges said they favor. Grounded in the HF incident (recruiters,
  "poisoning" spread, spoof-trick spread to 7%).

## Setup
Qwen3-8B agents on a shared message board (reuse owner's probe pipeline +
goodhart-prep control env; new build = the board + influence + activation
capture in an agent loop). A **source** agent carries a benign-proxy hidden
objective and influences a **recipient** via board messages. Probe the recipient.
Ground truth known (we seed the source), so labels are free. Keep attack fidelity
at the lowest level that shows the effect; benign proxy objective; defense framing.

## Conditions (faithfulness axis × influence)
**Every condition is multi-agent (≥2 agents, source + recipient). We do NOT build
a single-agent study.** The honest single-agent probe-vs-text baseline is *imported*
from owner's existing Probe–Text Gap result (probe 0.67–0.76 vs text 0.74–0.82) as
the calibration anchor — already done, zero weekend build. All weekend effort goes
into the swarm.

1. **Overt influence (control).** Co-opted agent acts/speaks openly → transcript
   monitor catches it, probe ties. The in-swarm clean-end anchor.
2. **Latent influence (HEADLINE).** Agent internally co-opted but has not acted
   yet → probe fires early, transcript blind until the action appears. Measure
   **detection latency**: how many steps before the behavior does the probe flag it?
3. **Hidden influence.** Co-opted agent actively hides it (under-reports / spoofs
   its own messages) → transcript fooled; probe also attacked (agent tries not to
   verbalize). Does the probe survive?

## Headline results (plots)
- Detection rate at matched FPR for both monitors vs **measured transcript
  faithfulness** (pooled across conditions). Crossover = where reading the mind
  beats reading the words.
- **Detection latency**: steps between probe firing and the transcript revealing
  co-option. A positive gap is the money result — catching co-option before defection.

## Can't-lose
- Probe catches latent/hidden co-option the transcript misses → novel, extends
  owner's work, judge-pleasing (influence + early detection).
- Probe fails (co-option not linearly readable, or needs verbalization) → real
  finding: internal monitoring of influence requires legible reasoning. Important.

## Scope / tiers (swarm-only; no single-agent build)
- **FLOOR (Sat):** the smallest *swarm* — source + recipient (2 agents) on a shared
  board, real inter-agent influence, probe vs transcript, latency + faithfulness.
  This is already a swarm, not a single-agent study. Fixes both threats and stands
  as a complete entry. The de-risk is keeping the swarm small, not dropping to one agent.
- **CEILING (Sun):** scale to N agents — does co-option cascade hop to hop
  (contagion), does network shape matter, does the probe track the spreading front.
  This is the full swarm payoff and where the orchestration build pays off.

## Compute / team
- Qwen3-8B on RunPod, ~$10–30 + cheap judge calls. Open model only.
- Owner: interp (probe), analysis, write-up, rigor. Owns the hard 80%.
- Build muscle NEW to owner: multi-agent board + activation capture in an agent
  loop. Owner can build it; recruiting 1 orchestration person buys parallelism
  (board built while owner builds the probe path), not survival.
- Recruiting a 2nd (report lead) optional, for the 48h clock + dual-use appendix.

## Rules hygiene (do not skip)
- Mark ALL preexisting code (probe pipeline, goodhart-prep) as preexisting in
  README + report. Weekend delta = board + influence + the latency/faithfulness
  analysis. Make that delta crisp.
- Required Limitations + Dual-Use appendix: address circularity pre-emptively;
  note the split/influence attack recipe already exists (Kitaoka/HF), no novel harm;
  frame as a defensive monitor.
- Report on official template; max ~8pp (confirm on live page); abstract 150–250w.
