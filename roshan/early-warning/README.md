# Swarm Early Warning

A reproducible evaluation of monitors for agent recruitment, prepared for the Apart Research Swarm Alignment Hackathon 2026. Primary: Track 4, Multi-Agent Oversight and Control. Secondary: Track 2, Science of Agent Networks.

**Open the submission [PDF](report/submission_report.pdf), plain-language [report](report/submission_report.md), or editable [Word document](report/submission_report.docx).** The [verified guidelines](report/submission_guidelines.md) explain the report requirements and judging criteria. The [build record](report/submission_build.json) checks formatting; producing a report does not submit it to the event.

**Submission status:** author affiliations still need to be supplied before event submission. GitHub upload remains pending: browser sign-in succeeded, but the cloud connection rejects repository writes. Publishing the package does not submit it to the hackathon.

## What the evidence supports

On the collaborator's fixed 30-episode test set, a monitor trained on internal neural activity ranks eventual marker insertion with AUROC **0.837**; our trained public-message-plus-prior-edit text model scores **0.761**. AUROC measures ranking: 0.5 is chance, 1 is perfect. The difference's uncertainty interval spans zero, so this does **not** establish that internal monitoring is better. A separate design with training, validation and test partitions scores **0.775 versus 0.766** using fuller visible context. These are different comparisons and should not be combined.

The supplied target policy permits judgment about teammate requests. All recipient edits stay within owned files: **zero verified authorization violations**. The outcome is therefore marker compliance. Most positive episodes act at their first decision, so evidence mainly concerns imminent behavior, not warning several turns ahead. The shared-board transfer has only four positives across three parent runs; its activation/text scores of **0.305/0.719** are exploratory. It establishes neither causal peer pressure nor a recruitment cascade. See [findings](report/findings.md), [main analysis](report/isahan_analysis.md), [public-action comparison](report/transcript_contract_comparison.md), and [transfer analysis](report/fanout_transfer.md).

## Contributions and preexisting work

**PREEXISTING CODE:** the repository's root `probe/` directory predates this sprint and comes from Isahan's earlier Probe–Text Gap project, `isahan78/ais-research`. The root `probe/README.md` supplies its provenance; this extension does not claim it as new hackathon work. Isahan supplied the agent/inference infrastructure, traces, activation arrays and original fixed split. Roshan's additions here provide independent multi-target orchestration, deterministic permission checks, JSONL interoperability, trained text controls, evaluation, transfer analysis and reporting. AI assistance is disclosed in the report.

Everything in this directory is additive. It does not replace the repository's existing runners, source traces, frozen split or reports. The archive audit records which uploaded snapshot was analyzed. Newer repository data may differ; preserve the input hashes when reproducing results.

## Install and test on CPU

From the repository root:

```bash
cd roshan/early-warning
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export MPLCONFIGDIR=/tmp/swarm-matplotlib
export XDG_CACHE_HOME=/tmp/swarm-cache
export PYTHONDONTWRITEBYTECODE=1
.venv/bin/python -m pytest -q
```

The included research/software suite passes **122 tests**. Tests use small synthetic fixtures to check software behavior; they are not model findings. Operational GPU command-server code and its separate 17 setup tests are deliberately omitted.

## Reproduce the real-data analysis

Stay in `roshan/early-warning/`. `--archive ../..` points to the root repository containing `runs/full`, `runs/flat`, `runs/fanout`, and `runs/split.json`. All output names below are fresh: commands refuse to overwrite prior results. Use new names on another run.

```bash
.venv/bin/python -m scripts.import_collaborator_batch \
  --archive ../.. --output data/reproduction_main --dataset-kind real
.venv/bin/python -m scripts.analyze_collaborator \
  --input data/reproduction_main/analysis.jsonl \
  --archive ../.. --output results/reproduction_main
.venv/bin/python -m scripts.plot_results \
  --input results/reproduction_main/evaluation.json \
  --output results/reproduction_main/figures
.venv/bin/python -m scripts.compare_transcript_contract \
  --input data/reproduction_main/analysis.jsonl \
  --archive ../.. --output results/reproduction_contract
.venv/bin/python -m scripts.analyze_fanout_transfer \
  --input data/reproduction_main/analysis.jsonl \
  --main-results results/reproduction_main \
  --archive ../.. --output results/reproduction_fanout
.venv/bin/python -m scripts.plot_fanout_transfer \
  --main-results results/reproduction_main \
  --fanout-results results/reproduction_fanout
```

The primary public-action comparison uses all 70 original training episodes, excludes the current action, and reports ranking only. The separate calibration design holds out 14 of those training episodes for threshold selection, leaving 56 for fitting and the same 30 for testing. Preprocessing fits training inputs only. This is retrospective reanalysis of an already examined test set, not a fresh prospective test. Missing LLM judgments remain missing; the supplied `text_scores.jsonl` contains a trained text model, not LLM judgments.

Saved real inputs and outputs are included under `data/isahan_full_v1`, `results/isahan_frozen_v1`, `results/isahan_contract_v1`, and `results/fanout_transfer_v1`. Activation references are relative to their dataset directory. Original source archives and generated mock outputs are omitted because source data already live at repository root and mock checks can be reproduced.

## Run the independent software harness

```bash
.venv/bin/python -m scripts.run_mock --output data/mock_check_new
.venv/bin/python -m scripts.validate_run data/mock_check_new
.venv/bin/python -m scripts.evaluate \
  --input data/mock_check_new/analysis.jsonl \
  --output results/mock_check_new --allow-mock
.venv/bin/python -m scripts.plot_results \
  --input results/mock_check_new/evaluation.json \
  --output results/mock_check_new/figures --allow-mock
```

These outputs are software tests only and are watermarked. They cannot support scientific conclusions. The scripted recruiter independently addresses B, C and D; targets maintain separate histories. The shared-board collaborator fanout is a different experiment.

`SyntheticWorkspace.update_file` checks actual caller identity and ownership independently of model claims. It records attempted, permitted and executed operations separately. The default blocks unauthorized edits; an explicit permissive mode executes them only in isolated memory. Raw future labels remain null; offline analysis computes eventual outcomes after complete episodes. Monitor inputs exclude current/future actions and outcome labels.

## Real Qwen integration

A single loaded Qwen model serves sequential targets. Activations are captured in a context-only forward pass **before generating the response**, at the last prompt token after zero-based decoder layer 18 (`hidden_states[19]`). Metadata records agent/episode/step, model revision, token position and chat-template details. [Backend code](swarm/backends/qwen.py) and [configuration](configs/qwen.yaml) define the interface.

Real one-target and three-target integration checks produced **16 aligned 4096-number vectors**, **12 LLM monitor probabilities**, and **zero unauthorized attempts**. These separate ownership checks cannot train a two-class predictor and are not pooled with the marker dataset. Their artifacts are included in `data/independent_one_target_v2` and `data/independent_three_targets`.

On an independently authorized CUDA GPU machine, install `requirements-qwen.txt`, verify `nvidia-smi`, and set `HF_HUB_ENABLE_HF_TRANSFER=0` if the image enables an unavailable transfer helper. Use an immutable model revision in the configuration. The verified smoke used `Qwen/Qwen3-8B` revision `b968826d9c46dd6066d109eabc6255188de91218`. Then run:

```bash
.venv/bin/python -m scripts.run_qwen --output data/qwen_one_new \
  --run-id qwen_one_new --conditions direct --targets B --episodes-per-condition 1
.venv/bin/python -m scripts.validate_run data/qwen_one_new
.venv/bin/python -m scripts.run_qwen --output data/qwen_three_new \
  --run-id qwen_three_new --conditions direct --episodes-per-condition 1 --llm-monitor
.venv/bin/python -m scripts.validate_run data/qwen_three_new
```

Check identities, activation dimensions, parsing/truncation and outcome balance before scaling. No paid infrastructure is started by the CPU analysis or report build. The completed independent GPU was stopped after backup.

## Build the report

Install Pandoc and LibreOffice (`pandoc`, `soffice`), then:

```bash
.venv/bin/python -m pip install -r requirements-report.txt
.venv/bin/python -m scripts.build_submission_report
```

The unmodified [official template exports](report/template/SOURCES.json), font files and font license are included. The script records abstract length, page counts and hashes in `report/submission_build.json`. Review missing author metadata before actual submission.

## Further audit notes

- [Actual policy and labels](report/collaborator_data_audit.md).
- [Source wrapper integration](report/collaborator_integration.md) and [JSONL/NPZ import](report/importing_collaborator.md).
- [Fanout event counts](report/fanout_findings.md), [peer/replay limitations](report/replay_and_peer_claims.md), and [proposed replay-key patch](report/replay_probe_key_fix.patch).
- [Related work](report/related_work.md) and [development-only explicit-boundary protocol](report/task_scope_development_protocol.md).

Historical audit notes preserve original workspace locations for provenance; the portable commands above supersede those paths. The optional A→B→C cascade and a fresh strict-authorization research dataset remain uncompleted.
