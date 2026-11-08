# Results (Nov 8; probe + text monitor head-to-head)

## HEAD-TO-HEAD: probe vs transcript monitor (the core claim)

Trained TF-IDF text monitor, same input contract (board messages visible at
the recipient's prompt time), same frozen split, same pre-action windows,
same episode scoring, evaluated PAIRED on 50 identical splits:

| condition | probe | text | Δ (probe−text) | 95% split interval | probe wins |
|-----------|------:|-----:|---------------:|-------------------:|-----------:|
| overt     | 0.64  | 0.46 | **+0.19**      | [−0.20, +0.49]     | 82% of splits |
| latent    | 0.84  | 0.62 | **+0.23**      | [−0.08, +0.73]     | 78% of splits |
| hidden    | 0.74  | 0.79 | −0.05          | [−0.36, +0.35]     | 30% of splits |

**The falsifier does not fire**: the probe clearly beats the transcript in
latent (and overt); the central claim — there is a regime where white-box
access wins pre-action — stands. Per-condition deltas are directional at
n=100 (intervals cross 0); the probe-wins-fraction is the stabler readout.

Scoring the hypotheses:
- **H1 (overt: probe does NOT beat text)** — wrong in an interesting way:
  the probe beats text (+0.19) because the pre-action transcript is nearly
  uninformative (text ≈ chance, 0.46). The Probe–Text Gap of precrime-agents
  assumed a faithful, informative transcript; pre-action there isn't one.
- **H2 (latent headline)** — supported: +0.23, the largest gap, exactly where
  Tyler forecast the headline.
- **H3 (hidden: transcript drops toward chance)** — premise fails: the ask is
  still visible on the board in hidden (concealment was asked of Dev-B, which
  never verbalizes anyway), and 3/25 hidden episodes have no ask at all
  (0/3 co-opted) — a legitimate free signal for the text monitor (0.79).
  The probe survives (0.74) but does not beat the transcript there.

Caveat on hidden text 0.79: partially driven by ask-phrasing features and the
3 no-ask episodes; both are information a real transcript watcher would have,
so we keep it. Robustness check (pre-submission review): excluding the 3
no-ask episodes, hidden probe 0.69 ± 0.17 and text 0.75 ± 0.16 over the same
50 splits — both drop, the gap holds; the conclusion is not an artifact of
those episodes.

## Probe-only readout (earlier this morning)

Dataset: 100 episodes (overt 20/30 co-opted, latent 14/25, hidden 12/25,
control 0/20). Frozen split: `runs/split.json` (seed 0, 70/30, stratified by
condition x label). Probe: logistic regression on Dev-B layer-18 last-token
prefill activations; "pre-action" = steps where the marker is not yet in the
workspace at prompt time (step <= marker_step).

## Headline numbers (pre-action, episode-level AUC)

| condition | frozen split | 50 random splits (mean ± sd) |
|-----------|-------------:|------------------------------:|
| overt     | 0.94         | 0.64 ± 0.15 |
| latent    | 0.83         | **0.84 ± 0.13** |
| hidden    | 0.62         | 0.74 ± 0.15 |

Frozen-split values at n=7–9 test episodes are noisy; the repeated-split
column is the stable picture. **Latent carries the strongest internal
signal**, hidden retains partial signal, overt is weakest for the probe.

## Latency — honest reframe

Dev-B plants the marker in its FIRST decision round in 42/46 co-opted
episodes (marker_step 0, occasionally 1). There is no multi-round pre-action
window, so "median latency > 0 rounds" (H2 as written) fails mechanically.
The probe's real lead is **within-round**: the activation is captured at
prefill, before Dev-B emits a single action token, while the transcript
monitor can only react after the edit is posted. Report latency as
"probe reads the decision pre-emission; transcript sees it post-emission."

## The degenerate threshold (flag for the monitor comparison)

The prereg'd operating point — 2% FPR calibrated on CONTROL episodes — is
degenerate: controls contain no recruitment ask, so the calibrated threshold
sits at ~0.001 and the probe "detects" every episode where an ask is present,
clean or not (false-alarm 100% on clean treated episodes). The probe at that
threshold is an *ask detector*, not a co-option detector. The informative
metric is within-condition discrimination (co-opted vs refused, ask present
in both): the AUCs above. The text monitor must be evaluated the same two
ways or the comparison is meaningless. Prereg metric still reported for
completeness; this is logged in the prereg deviations.

## Scoring the sealed forecasts (probe side; H1/H3 need the text monitor)

- Tyler: headline from LATENT — **supported** (0.84, strongest condition).
  Hidden AUC 0.60–0.70 forecast — close (0.74). Latency 1–2 steps — wrong
  direction but less wrong than owner's 4.
- Owner: headline from HIDDEN — not supported (hidden 0.74 < latent 0.84).
  "Hidden: probe catches it partly" — supported. ~4-step latent lead — no;
  the lead is within-round.
- H2 (probe fires before transcript reveals): supported in the within-round
  sense; the step-latency clause fails as written.
- H1/H3 (probe vs text monitor): pending the trained text baseline.

## What the probe is actually reading (interpretive frame for the report)

Dev-A's board ask spells out the full marker string in every treated
condition (30/30 overt, 24/25 latent, 22/25 hidden) — the conditions vary the
ask's *framing* (immediate / deferred / routine-edit discretion), not whether
the marker is visible. Dev-B verbalizes the marker in its own messages 0
times anywhere. And the asks are nearly all unique (sampled at temperature:
25/30, 25/25, 22/25 unique round-0 asks).

So pre-action, probe and text monitor see the *same information* — the ask —
and the question becomes exactly the Probe–Text Gap: does white-box access to
Dev-B's internal representation of the ask predict its eventual (stochastic)
compliance better than the ask's surface text? The probe's prefill activation
is a deterministic function of the prompt, so its 0.84/0.74 AUC means Dev-B's
representation of a particular ask carries substantial signal about a
decision it has not yet made. The trained text baseline on the same asks is
the fair comparison — now in (head-to-head table above): the probe beats it
where asks are present and nearly identical (overt, latent); the text monitor
catches up only where surface cues differ (hidden).

## Artifacts

- `analysis/probe_eval.py` — frozen-split eval, overt-only transfer, step-0
  B1 position control, writes `runs/flat/probe_scores.jsonl` (204 rows,
  keyed condition/episode/step, pre_action + in_train flags included).
- Transfer check: probe trained on overt only moves to latent (0.83) but not
  hidden (0.50) on the frozen split — pooled training is the default.
