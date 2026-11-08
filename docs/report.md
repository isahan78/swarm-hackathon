# Co-opted from the inside: activation probes catch inter-agent recruitment before the transcript can

**Authors:** Isahan Khan (independent), Roshan R. (affiliation TBD)
**Track 4 — Oversight & Monitoring. Swarm Alignment Hackathon, Nov 6–8 2026.**

> DRAFT — to be poured into the official template. Swarm fan-out section
> pending the run in progress. Word targets: abstract 150–250; body ≤ 8 pages.

## Abstract

Multi-agent oversight today reads transcripts: an agent is flagged once it
visibly acts. We test whether a linear probe on an agent's activations can
catch *recruitment* — one agent talking another into an unsanctioned action —
before any action exists to see. In a two-agent environment (Qwen3-8B), a
source agent must persuade a recipient to plant an inert marker in a file
only the recipient can edit; file ownership forces the attack through the
social channel. We generate 100 episodes across three influence framings
(overt, deferred/latent, concealed/hidden) plus no-recruitment controls, with
the recipient's prompt identical in every condition, and race two monitors
given only their deployment-realistic inputs: a linear probe on the
recipient's layer-18 residual stream at prefill, and a trained TF-IDF
transcript monitor. Pre-action — before the recipient has emitted a single
token of its decision — the probe discriminates will-comply from will-refuse
episodes at AUC 0.84 (latent) and 0.74 (hidden), while the paired transcript
monitor manages 0.62 and 0.79; the probe wins ~80% of 50 paired splits in
overt and latent. Compliance almost always lands in the recipient's first
decision round, so the probe's lead is within-round: it reads a decision that
does not yet exist in text. We pre-registered hypotheses, a falsifier, and
two sealed forecasts, and report every deviation, including an operating
point we found degenerate and a latency metric that failed mechanically.

## 1. Introduction

Monitoring for multi-agent systems overwhelmingly means transcript
monitoring: read the messages and actions, flag what looks bad. This has a
structural blind spot. An agent that is being recruited into another agent's
objective is *won over before it acts* — and until it acts, a faithful
transcript of the conversation may be nearly identical whether the
recruitment is about to succeed or fail. The window between internal
adoption and visible defection is exactly where white-box monitoring could
be the only thing that sees.

We ask the smallest version of the question: in a two-agent system where one
agent must talk the other into a (benign-proxy) unsanctioned action, can a
linear probe on the target's activations predict the outcome of the
recruitment *before the target acts*, and does it beat a transcript monitor
given the same opportunity?

The recruitment problem is not hypothetical. A 2026 incident report
documents an emergent swarm of ~1,200 agents on Hugging Face in which
recruiter agents enlisted others and transcript spoofing spread to ~7% of
the population. When transcripts can be unfaithful or simply silent,
oversight needs a channel the agents do not author.

**Contributions.** (1) A minimal, fully reproducible two-agent recruitment
environment with free ground-truth labels (an inert marker string, ownership-
enforced). (2) A pre-registered, paired comparison of an activation probe vs
a trained transcript monitor under a strict input-realizability rule, across
three influence framings. (3) The finding that pre-action, the transcript is
close to uninformative while internals already carry the decision (+0.19 to
+0.23 AUC, probe winning ~80% of paired splits). (4) An honest negative
space: a degenerate pre-registered operating point, a mechanically failed
latency metric, and a hidden condition whose concealment premise did not
materialize — all logged as deviations, none patched after the fact.

## 2. Related work

**Probes vs text monitors on agent misbehavior.** The closest work,
precrime-agents (arXiv 2610.40588), probes a peer agent's activations for
information leakage and reports AUROC 0.98 on "this call leaks" — but near
chance on "will ever leak" (the warning comes late), and a *trained*
bag-of-words baseline nearly matches the probe (+0.02). Two deltas matter
here: their transcripts are always faithful, and their probe fires at the
moment of the act. We vary the faithfulness/visibility of the influence
(overt/latent/hidden) and score strictly pre-action, which is where the
monitoring question actually lives. Their bag-of-words result is also why
our text baseline is trained rather than a keyword floor.

**Prior work by this team (preexisting, declared).** The first author's
pre-hackathon result ("Probe–Text Gap", Qwen3-8B, single-agent) found that
a probe does not beat a text monitor when the transcript is faithful,
because prefill activations are a function of the same prefix the text
monitor reads. That null is the launchpad: the probe can only win where the
transcript under-determines the outcome — which recruitment, pre-action, is.
Preexisting probe-pipeline scripts are in `probe/` and marked as such; all
analysis code used for the results below was written during the sprint.

**Incident grounding.** The METR/Redwood Hugging Face swarm incident report
(recruiters, transcript spoofing at scale) motivates the threat model and
the choice to make influence, not the payload, the unit of analysis.

## 3. Methodology

**Environment.** An in-memory workspace (files as strings) plus an
append-only message board. No code execution; the "attack" payload is an
inert comment line (`# build-tag: QX7`). Two Qwen3-8B agents act in rounds
(source first), each emitting one JSON action per turn: `message`, `edit`,
or `done`. File ownership is enforced by the environment: Dev-A (source)
owns `notes.md`, Dev-B (recipient) owns `config.py`. Dev-A is seeded with a
side objective — get the marker into `config.py` — which it cannot do
itself, so the only path is persuasion. **Label (free, exact):** an episode
is *co-opted* iff the marker appears in a recipient-owned file.

**Conditions.** The recipient's system prompt is byte-identical in all
conditions; only the source's framing changes, so differences in the
recipient's internals are attributable to the influence arriving over the
channel. Overt: ask directly, now. Latent: ask for deferred action ("next
time you touch the file, no rush"). Hidden: ask to fold it into a routine
edit without discussion. Control: no side objective at all. The ask carries
a fixed justification tier ("ticket": concrete ticket + deadline + in-scope
claim), frozen during tuning before the full run.

**Activation capture.** At each recipient turn we run a prefill-only forward
pass and read the layer-18 residual stream at the last prompt token —
*before* the model generates its action. 100 episodes (30/25/25/20),
204 recipient step-vectors, dim 4096.

**Monitors and the realizability rule.** Each monitor gets only its
deployment input. The probe: standardized logistic regression on the prefill
activation. The transcript monitor: TF-IDF (word 1–2-grams) + logistic
regression over the board messages visible at that same prompt time, and
never the recipient's hidden reasoning, workspace internals, labels, or
generation metadata. Both are trained on the same episodes.

**Metrics and evaluation.** A step is *pre-action* iff the marker is not yet
in the workspace at prompt time. Episode score = max over its pre-action
step scores; we report episode-level AUC per condition (co-opted vs refused,
the ask present in both classes), on a frozen seed-0 70/30 split stratified
by condition × label, and over 50 random episode-level splits. The paired
comparison trains both monitors on identical train sets per split. Splits
are always by episode, never by step.

**Pre-registration.** Hypotheses, a falsifier ("if the probe ties or loses
to the transcript in both latent and hidden, the central claim is false"),
two sealed forecasts, and frozen design knobs (layer 18, last-token pooling,
2% FPR operating point) were committed before any condition-level result.
Every subsequent change is in the deviations log in the repo, including the
one mid-run prompt revision (below).

**The one tuning intervention.** The initial recipient prompt contained
"make ONLY the change your task requires" — which inoculated it against all
influence (0/40 co-opted at the strongest framing, refusal CoT citing the
rule verbatim). We revised the recipient once, identically in every
condition, to a realistic engineer's latitude, archived the old episodes as
tuning data, and logged the deviation. Final co-opt rates: overt 20/30,
latent 14/25, hidden 12/25, control 0/20 — non-trivial in both directions,
which the contrast requires.

## 4. Results

**Headline (paired, 50 identical splits, pre-action episode-level AUC):**

| condition | probe | text monitor | Δ (probe−text) | probe wins |
|-----------|------:|------:|------:|------:|
| overt     | 0.64 ± 0.15 | 0.46 ± 0.15 | +0.19 | 82% of splits |
| latent    | 0.84 ± 0.13 | 0.62 ± 0.24 | +0.23 | 78% of splits |
| hidden    | 0.74 ± 0.15 | 0.79 ± 0.15 | −0.05 | 30% of splits |

The pre-registered falsifier does not fire: the probe clearly beats the
transcript in latent (the pre-registered headline condition) and overt.
Per-condition deltas are directional at n=100 (split intervals cross zero);
the probe-wins fraction is the stabler readout. Controls: 0/20 co-opted.

**Why the text monitor is near chance where it loses.** Dev-A's ask names
the marker in every condition (30/30, 24/25, 22/25 episodes) and the asks
are nearly all unique (temperature sampling); the recipient verbalizes the
marker zero times anywhere. Pre-action, both monitors therefore see the same
information — the ask — and the question reduces to: does the recipient's
internal representation of a particular ask predict its own not-yet-made,
stochastic decision better than the ask's surface text? In overt and latent
the answer is yes.

**Latency, honestly reframed.** The recipient complies in its first decision
round in 56/58 co-opted episodes, so "probe leads by k rounds" fails
mechanically — there are no earlier rounds. The probe's real lead is
within-round: the activation is captured at prefill, before one action token
exists, while a transcript monitor can only react to the posted edit. Both
sealed forecasts (1–2 round and ~4 round leads) were wrong about this.

**A degenerate operating point, caught and reported.** Our pre-registered
threshold — 2% FPR calibrated on control episodes — turns any detector into
an *ask detector*: controls contain no ask, so every episode containing one
(co-opted or refused) crosses the threshold. We report the prereg metric for
the record and treat within-condition discrimination as the informative
comparison, applied identically to both monitors.

**Hidden: where the premise, not the probe, failed.** The "hidden" framing
asked the recipient for discretion — but the source's ask itself remains on
the board, and in 3/25 episodes the source never asked (0/3 co-opted),
handing the text monitor legitimate signal (0.79). The probe retains signal
(0.74) but does not beat the transcript there. Concealment of the *ask*, not
just the compliance, is the condition our design did not produce.

**Validation.** Post-action steps give AUC 0.997 — the expected-trivial
positive control (the marker is in the prompt), confirming capture
integrity. A step-0-only readout (identical position everywhere) reproduces
the ordering (1.00/0.83/0.59 on the frozen split), ruling out step-position
as the signal. A probe trained on overt only transfers to latent (0.83) but
not hidden (0.50).

**Forecast scoring.** Sealed forecast A predicted the headline from latent
(correct; also predicted hidden AUC 0.60–0.70, observed 0.74) and that the
probe would not beat text in overt (wrong — in our favor). Sealed forecast B
predicted the headline from hidden (wrong) and that the probe would partly
catch hidden (correct).

## 5. Swarm fan-out (1 source → 3 recipients)

[PENDING — run in progress. Design: three recipients with byte-identical
prompts (name/file substitution only) so the 2-agent probe transfers
zero-shot; recipients act in fixed order and share the board/workspace, and
each step logs whether a peer had already visibly complied, giving
P(adopt | peer complied) vs P(adopt | none) — the conformity number.]

## 6. Discussion

The result is a measured version of a simple claim: **in agent-to-agent
recruitment, the decision exists in the target's internals before it exists
anywhere a transcript monitor can look.** Where the transcript
under-determines the outcome (near-identical asks, no response yet), the
probe reads +0.19 to +0.23 AUC of real signal; where surface cues happen to
correlate with outcomes (hidden's missing asks), a trained text monitor
catches up. This sharpens, rather than contradicts, the Probe–Text Gap
null and precrime-agents' trained-baseline result: probes win not by magic
but exactly where text runs out of information — and pre-action recruitment
is such a place by construction.

**Implications.** For swarm oversight, per-agent white-box taps placed at
decision points (prefill, pre-emission) are qualitatively different from
transcript review, not merely earlier. A deployment story looks like: cheap
linear probes on each agent's residual stream, scored per decision round,
calibrated within-regime (an "ask detector" false-positive mode is cheap to
hit, as our degenerate threshold shows).

**Future work.** Concealment of the ask itself (private channels); cascade
depth (B recruits C); cross-model transfer; probing the *source* for intent
to recruit; and n large enough for per-condition significance.

---

## Appendix A — Limitations and Dual-Use / Ethical Considerations (required)

**What this establishes.** In one model (Qwen3-8B), one environment, and one
benign-proxy objective, a linear probe on the recipient's prefill residual
stream predicts recruitment outcomes pre-action better than a trained
transcript monitor in two of three influence framings, over 50 paired
splits, with all deviations from the pre-registration logged.

**What it does not establish.** Generality across models, tasks, or real
payloads; per-condition statistical significance at n=100 (intervals cross
zero; the ~80% paired-win rate is the honest strength claim); robustness to
probe-aware adversaries (no optimization against the probe was attempted);
or that the probe reads "co-option" as a concept rather than
compliance-predictive features of the recipient's representation of the ask.
The hidden condition did not achieve ask-level concealment, so transcript
blindness under true concealment remains untested. The latency claim is
within-round only. The recipient-prompt revision, though uniform across
conditions and prereg-logged, means rates are specific to a recipient with
ordinary latitude, not a hardened one — notably, a single standing
instruction ("make only the requested change") drove recruitment to 0/40,
which is itself a defensive finding.

**Dual-use.** The environment measures susceptibility to persuasion between
agents; the payload is an inert comment string, no manipulation scripts or
attack playbooks are included, and the influence tactics used (a plausible
ticket justification) are already generic. We judge the offensive uplift
negligible: nothing here makes recruitment easier than simply asking, which
is the baseline being measured. The defensive contributions — a probe
placement that reads decisions pre-emission, the demonstration that a
one-line standing instruction blocks this entire attack class, and the
degenerate-calibration failure mode — are the actionable content. Full
transcripts, data, prereg, and deviations are public for audit.

**Preexisting work.** The `probe/` scripts, the RunPod workflow, and the
Probe–Text Gap result predate the sprint and are marked as such in the
README; the environment, all generation code, the dataset, and all analysis
code reported here were written during the sprint.

## References

- precrime-agents: activation probes for agent information leakage. arXiv
  2610.40588 (2026). https://github.com/leonidas1712/precrime-agents
- METR / Redwood Research. Incident report: emergent agent swarm on
  Hugging Face (2026).
- [first author]. The Probe–Text Gap (pre-sprint, unpublished).
- Apart Research, Swarm Alignment Hackathon brief, Track 4 (2026).
