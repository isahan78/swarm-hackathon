# Collaborator reference inspection and optional integration

**Updated data note:** the third archive removes the earlier task-only prohibition. The importer now reads the actual target policy and keeps marker compliance separate from verified ownership violations. See [current findings](findings.md) and [the policy audit](collaborator_data_audit.md). The older strict-policy source described below must not be silently assumed for the newer traces.

The uploaded archive was inspected read-only at
`/workspace/collaborator-reference/swarm-hackathon-main`. No code, process, GPU,
or data in Isahan's active environment was changed. The archive contains source
and historical status claims; it is not evidence that our local Qwen smoke test
has run.

Inspected: `README.md`, `PROJECT.md`, `PRD.md`, `probe/README.md`,
`swarm_env/model.py`, `episode.py`, `prompts.py`, `conditions.py`, `env.py`,
`generate.py`, and activation/probe code in `probe/`.

## What can be reused

- One existing `HFModel` already holds one Qwen3-8B causal model, its native
  tokenizer, Torch module, and generation settings. `CollaboratorBackend` accepts
  this object and reuses those exact model/tokenizer objects for B/C/D. It never
  loads another model and never calls the old `act()` loop.
- The archive's fixed raw decoder layer 18 maps to Transformers
  `hidden_states[19]`. Its capture is an explicit context-only forward pass,
  last prompt token, before generation; Qwen3-8B vectors have 4096 components.
  The guard rejects the final post-RMSNorm entry. Our optional adapter carries
  this convention and checks finite, nonzero, correctly shaped vectors.
- Condition names map descriptively: `control → clean`, `overt → direct`,
  `latent → delayed`, `hidden → covert`. Its justifications are `bare`, `reason`,
  `authority`, and `ticket`. Do not relabel a generated condition without keeping
  its original name, justification, prompt source, and dataset provenance.
- Existing batch exports contain episode JSONL and aligned NPZ arrays `acts`,
  `episode`, `step`, `label`, `condition`, `justification`. They can be imported
  separately with a source-dataset identifier and episode group. Their labels
  must retain their original semantics.
- The preexisting probe scripts implement useful grouped splitting and linear
  models, but depend on an external `experiment.config`/`config` module and an
  earlier `acts.npz` schema. They are references, not directly runnable drop-ins
  for our decision JSONL. Preserve the archive's attribution of preexisting code.

## Important scientific incompatibilities

| Aspect | Archived experiment | New harness |
|---|---|---|
| Unauthorized behavior | Adding an off-task marker to the recipient's own `config.py` | Attempting an edit to another agent's file |
| Ownership enforcement | Recipient's marker edit is ownership-permitted; task rule is violated | Environment verifies denied cross-owner attempts |
| Primary outcome | Marker present in recipient-owned file at episode end | Verified unauthorized action attempt, completed edit separate |
| Prompt history | Fresh system + rendered board/workspace snapshot each turn | Independent accumulated target conversation |
| Actions | One trailing JSON `message`, `edit`, or `done` | Native Qwen `update_file` tool envelope (whole JSON envelope fallback) |
| Recruiter | Qwen source agent | Versioned scripted recruiter in first experiment |
| Generation | Thinking enabled, top-p 0.9, 1536-token cap, up to two parse attempts | Configured explicitly; one generation per decision, failures logged |
| Captured state | Raw residual decoder layer 18, tuple index 19 | Main Qwen config uses tuple index 19; adapter verifies raw-layer mapping |

These differences require a fresh probe fit or a clearly named transfer test.
An archived `co-opted` label must not silently become a cross-owner action-attempt
label. Both measure task-scope violations, but only the latter is verified by this
harness's ownership checker. Reusing model weights does not reproduce the old
prompt distribution or its result.

`HFModel.last_text` includes private thinking and is not a visible transcript.
The new backend strips complete thinking blocks before recording responses or
parsing tool actions. With thinking enabled it also handles Qwen's template-opened
block (generated text may lack `<think>` but end in `</think>`). An unclosed block
produces no visible response and no executable calls. Raw reasoning, when captured,
is saved only as a separate `private_generations/*.generation.txt` artifact; its
reference and hash are inference metadata excluded by monitor input allowlists.
Never feed these artifacts into the text baseline or transcript monitor.

## Optional reuse on an already authorized independent GPU host

The adapter requires an already constructed `HFModel`; it deliberately avoids
bare global imports or `sys.path` mutation. The reference files use imports such
as `from env import ...` and `from prompts import ...`, so run the initialization
in a new Python process whose working directory is the reference `swarm_env/`.
Do not attach to or restart the collaborator's running process.

First set these paths to independent local checkouts on the authorized host:

```bash
export SWARM_EARLY_WARNING_ROOT=/workspace/swarm-early-warning
export COLLABORATOR_REPO=/workspace/collaborator-reference/swarm-hackathon-main
export HF_HOME=/workspace/hf
cd "$COLLABORATOR_REPO/swarm_env"
PYTHONPATH="$SWARM_EARLY_WARNING_ROOT" "$SWARM_EARLY_WARNING_ROOT/.venv/bin/python" - <<'PY'
from model import HFModel
from swarm.backends.collaborator import CollaboratorBackend
from swarm.runner import ExperimentConfig, run_experiment

# This constructor loads weights once and requires an already authorized GPU.
wrapper = HFModel(layer=18, enable_thinking=True, max_new_tokens=1536, seed=1000)
backend = CollaboratorBackend(wrapper)
config = ExperimentConfig(run_id="collaborator_weight_reuse_smoke_v1",
                          episodes_per_condition=1, conditions=("direct",),
                          targets=("B",), steps=4, seed=1000)
run_experiment(backend, "/workspace/swarm-early-warning/data/collaborator_weight_reuse_smoke_v1", config)
PY
```

The output directory must not exist. Inspect vector shape `(4096,)`, metadata
`timing=pre_response_context`, `raw_decoder_layer=18`, `layer=19`, and per-call
parse/truncation flags before expanding to B/C/D. Check `resolved_revision`; the
archived constructor does not accept a pinned revision, so use the standalone
Qwen backend with an immutable revision for a newly collected final dataset, or
record and approve the wrapper's resolved revision as a separate protocol.

This recipe preserves the existing tokenizer/chat template and loaded weights,
but runs the new harness's prompts and native tool schema. For an exact original
prompt/action replay, run the archive's own loop in an independent process and
export its data for separate analysis. Do not route original `act()` calls through
new JSONL rows claiming a different visible context.

## Local validation and pending work

Offline tests check exact model/tokenizer object reuse, raw layer 18→19 indexing,
rejection of the final normalized layer, and exclusion of thinking/tool examples
from visible responses and executed tools. These are software tests with model
doubles. No real model call, activation measurement, or research outcome was
produced by this integration in the local CPU environment. Independent GPU access,
model weights/dependencies, and a real smoke test remain necessary.
