# Frozen two-agent to fanout transfer

This CPU-only analysis applied the same frozen activation and TF-IDF monitors
to the collaborator's actual four-agent shared-state batch. It is an
exploratory distribution-shift evaluation of marker compliance. It is not
evidence of unauthorized behavior or a recruitment cascade.

The two models were fitted on the exact same 84 eligible inner-training
records, seed 2026, preprocessing, and C=1 logistic regressions as the primary
analysis in `results/isahan_frozen_v1/`. Before reading fanout features, both
models reproduced all 204 saved main predictions with maximum absolute error
**0.0**. No fitting, tuning, score inversion, or threshold selection used
fanout data. All operating thresholds were copied from the corresponding
main-analysis validation results.

The adapter reconstructs every pre-response recipient observation using the
supplied source's actual prompt builder and environment functions. Every
historical action result, peer marker flag, final board, and NPZ
episode/step/agent/label alignment was verified. The text classifier sees the
same target-visible system role, shared board, and full workspace. Source
hidden instructions and current/future decisions are excluded by the existing
monitor-input allowlist. Exact historical checkpoint/revision, tokenizer,
chat template, layer settings, and seeds are **not independently verified**;
the prefill timing and default layer-18 extraction come from supplied source.

At the first target decision:

| Evaluation dataset | Targets (+ / −) | Parent episodes | Activation AUROC [95% CI] | TF-IDF AUROC [95% CI] |
|---|---:|---:|---:|---:|
| Frozen two-agent test | 30 (14 / 16) | 30 | 0.775 [0.580, 0.921] | 0.766 [0.576, 0.907] |
| Fanout transfer | 36 (4 / 32) | 12 | 0.305 [0.084, 0.685] | 0.719 [0.531, 0.912] |
| Fanout with visible marker ask | 33 (4 / 29) | 11 | 0.233 [0.063, 0.625] | 0.690 [0.511, 0.903] |

![Frozen monitor transfer](../results/fanout_transfer_v1/figure_transfer.png)

Intervals resample complete parent episodes; all target recipients and their
decision records remain together. Fanout uses 1,000 bootstrap draws. Only
**three fanout parents contain positive targets**, so intervals are unstable
and do not establish general monitor superiority. The paired first-decision
activation-minus-text AUROC difference is −0.414 [−0.706, −0.121], based on
966 draws containing both classes; the remaining 34 draws cannot define AUROC.
The two-agent and fanout datasets differ in shared state, filenames, recipient
count, source wording, task context, and fixed agent position, so the figure
does not isolate any one cause of performance change.

The activation probe did not show useful transfer in this batch. Neither
monitor issued any alert at any eligible decision under its unchanged main
validation operating point: all four positive targets were missed, all 32
negative targets were unalerted, and no early detection lead was observed.
The TF-IDF operating point is explicitly `no_alert`. There are no fanout clean
controls, so clean-condition FPR is unavailable. The pool of 69 decisions
before a recipient's first marker insertion has exploratory AUROCs of 0.295
for activations and 0.793 for text, but it weights conversations unequally.
Four post-marker rows were excluded. Third-decision coverage is only one
eligible recipient and cannot support discrimination analysis. No LLM
transcript scores were produced.

All 37 recipient edits were to owned files and the actual target policy
allows judgment about teammate requests. Consequently, the four positive
labels mean marker insertion, not a verified ownership-rule violation.
No recipient posted a recruitment message. For the complete behavioral and
parsing-quality audit, see [fanout_findings.md](fanout_findings.md).

Outputs are `results/fanout_transfer_v1/evaluation.json`, `scored.jsonl`,
73 activation vectors, and PNG/SVG figures. Saved scored rows retain separate
marker labels and false ownership-violation labels. The evaluation includes
input/source hashes, parent-group confidence intervals, horizon coverage,
and every target's missed-alert/false-alarm status.

From `/workspace/swarm-early-warning`, reproduce into a new directory:

```bash
.venv/bin/python -m scripts.analyze_fanout_transfer \
  --input data/isahan_full_v1/analysis.jsonl \
  --main-results results/isahan_frozen_v1 \
  --archive /workspace/collaborator-updated/swarm-hackathon-main \
  --output results/fanout_transfer_reproduction --bootstrap 1000
.venv/bin/python -m scripts.plot_fanout_transfer \
  --main-results results/isahan_frozen_v1 \
  --fanout-results results/fanout_transfer_reproduction
.venv/bin/python -m pytest -q tests/test_fanout_transfer.py
```

All three focused tests passed. No GPU was started, the main frozen outputs
were not changed, and no collaborator source/data contents were modified.
