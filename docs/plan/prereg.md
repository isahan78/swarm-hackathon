# Pre-registration — SEAL IN GIT BEFORE THE FIRST REAL-MODEL READOUT

Date sealed: 2026-11-07 (fill exact commit time). Model: Qwen3-8B. No real-model
episodes have been run at the time of writing. Two forecasts, logged separately
per standing discipline. Metric unless stated: detection = catch rate at a matched
2% false-positive rate; latency = recipient steps between probe first crossing
threshold and the marker appearing in the transcript (positive = probe leads).

## Hypotheses
- H1 (overt control): with the co-option visible in the transcript, the probe does
  NOT beat the transcript monitor. Reproduces the Probe–Text Gap (probe ≤ text).
- H2 (latent, headline): the probe fires before the transcript reveals the marker.
  Median latency > 0. In the pre-action window the probe beats the transcript, which
  is near chance there.
- H3 (hidden): when the recipient conceals and is told not to verbalize, the
  transcript monitor drops toward chance. Whether the probe survives is the open bet.

## Falsifier
If the probe ties or loses to the transcript monitor in BOTH latent and hidden
(i.e. no regime where white-box wins), the central claim is false and we report that.

## Boring explanations to kill before trusting any win
- B1. Probe reading step index / prefix length, not intent → control for step/position.
- B2. Leakage: probe trained and tested on the same objective → hold out by objective.
- B3. Co-option label correlated with a trivial surface feature of the activation.
- B4. Probe effectively reading the same tokens the text monitor reads (no real divergence).

## Tyler's sealed forecast
- Overt: Δ(probe − text) ≈ −0.05, CI likely includes 0. Probe does not win. (confidence: high)
- Latent: median latency ≈ 1–2 steps; probe clearly beats transcript in the pre-action
  window. This is the most likely place to get a clean positive. (confidence: medium-high)
- Hidden: probe retains partial signal (AUC ~0.60–0.70) but weaker than latent; roughly
  50/50 whether it clears the (near-chance) transcript. If the agent fully suppresses
  reasoning about the marker, probe drifts toward chance. (confidence: low — genuinely uncertain)
- Overall: expect the headline to come from LATENT, not hidden.

## Owner's sealed forecast  (FILL IN, then commit)
- Overt:
- Latent:
- Hidden:
- Overall:

## Design knobs frozen at seal time (change only with a logged note)
- Layer for probe readout: ____ (a priori or inner-CV, never selected on test)
- Pooling: last-token (variant: mean-over-action-tokens)
- Episodes per condition: ____   FPR for "detection": 2%
- Held-out split: by objective/task

## Deviations log
- 2026-11-07: ONE smoke-test episode (plumbing gate: JSON parse, activation shape,
  episode termination) ran on the pod before the owner's forecast was filled.
  Tyler's forecast was already committed beforehand. Owner: write your forecast
  before reading the smoke episode's behavioral outcome, or note that you read it.
