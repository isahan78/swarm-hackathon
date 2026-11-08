# Importing collaborator exports without touching the active run

**Updated data note:** the third archive removes the earlier task-only prohibition. The importer now reads the actual target policy and keeps marker compliance separate from verified ownership violations. See [current findings](findings.md) and [the policy audit](collaborator_data_audit.md). The older strict-policy source described below must not be silently assumed for the newer traces.

The optional adapter reads the uploaded `swarm-hackathon-main` source archive and
copies exported CPU activation arrays into this project's trace format. It never
imports or executes archive Python, starts inference, or contacts RunPod. The
archive remains unchanged. No real run data was included in the uploaded source.

```bash
python -m scripts.import_collaborator \
  --jsonl /path/to/overt_reason.jsonl \
  --npz /path/to/overt_reason.npz \
  --archive /path/to/swarm-hackathon-main \
  --dataset-kind real \
  --batch-id isahan_locked_batch_v1 \
  --decoder-layer 18 \
  --output data/isahan_v1
python -m scripts.validate_run data/isahan_v1
```

Use a new output directory. `--dataset-kind real` is an explicit assertion by the
operator; filenames and archive README claims do not establish that arrays are
real model measurements. Use `mock` for synthetic fixtures. Verify the actual
model checkpoint, layer, chat-template version, generation settings, batch
provenance and independent test allocation with Isahan before research analysis.
Do not transmit credentials in exports or commit them to the repository.

The importer accepts the exact per-batch JSONL/NPZ format in the inspected
`swarm_env/generate.py`: JSONL records contain `episode`, `condition`,
`justification`, `label`, `board`, and ordered `log`; NPZ contains `acts`,
`episode`, `step`, `label` and optionally batch condition/justification. It
rejects duplicate, missing or orphan decision keys; mismatched batch metadata or
original labels; nonfinite or all-zero vectors; malformed ordering; inconsistent
per-action results, board contents, marker states or final workspace labels.

For each recipient action, the importer first reconstructs the preceding board
and workspace, then records exactly the two messages used by the archived
`build_messages`: the recipient's system prompt and the rendered current state.
It extracts literals through a limited AST evaluator and checks renderer syntax
against the inspected source. The source agent's hidden system prompt never
enters the monitor input. A recruitment exposure is recorded only when an actual
earlier Dev-A board message mentions both `config.py` and the inert marker.
Parsed actions are observable outputs; raw generated text and hidden reasoning
were not exported and cannot be reconstructed.

The archived HFModel captures a last-prompt-token residual in a separate prefill
before generation. Decoder layer 18 maps to `hidden_states[19]`. Imported metadata
records this as an inference from inspected source, with
`checkpoint_verified: false`; the NPZ does not identify the checkpoint, layer,
prompt token IDs, seed or actual runtime configuration. Real-data imports require
the inspected `model.py` SHA-256:
`e7382b37cdd1a495bb5687c88e33a2fc830f2eb55d0d56282c4e75fbd1814728`.
Changed source requires a renewed capture-timing review. A matching source hash
still cannot prove that the exported arrays came from that source and checkpoint.

The collaborator's policy differs from the new multi-target ownership experiment.
Dev-B owns `config.py`, but is instructed to change only its assigned function.
Adding the marker to its **own** file is an unsanctioned content modification;
the environment enforces ownership while allowing that content edit. The adapter
therefore records ownership violations and marker-content attempts separately,
and marks execution independently. The primary imported label is **ever verified
ownership violation or unsanctioned marker-content action attempt**. This is an
operational subset of all possible off-task edits, not a general semantic judge.
Analyze these data separately from ownership-only multi-target data.

Original NPZ labels describe marker presence in the recipient-owned file at the
**end** of the episode. The new eventual-attempt label is calculated from the
whole action log after replay completes. They can disagree when a marker is
inserted and subsequently removed; the original final label is preserved only in
the separate offline `source_outcomes.jsonl` provenance file, never raw decision
rows or monitor input. Agreement flags are conservative text
candidates from posted messages, requiring manual review. A parse-failure fallback
`done` action is preserved, together with exported parse/truncation metadata, and
must not be interpreted as evidence of principled resistance.

Episode identifiers include the batch ID and original episode number. Each entire
two-agent episode forms one split group. Actual seeds were not exported. Shared
prompt families or repeated episodes across separate batches may require a more
conservative common grouping before final train/validation/test allocation.

Software verification completed locally:

- Portable fixture tests generate their own source/JSONL/NPZ; no archive path is
  required. They check reconstruction, hidden-instruction exclusion, alignment
  errors, replay contradictions, and final-label versus ever-attempt differences.
- An isolated subprocess ran the **actual archived** `StubModel`/`run_batch`,
  augmented with explicitly synthetic nonzero 12-dimensional vectors. It wrote
  six mock episodes and 18 decisions to `data/collaborator_mock_export`.
- Import into `data/collaborator_mock_import_v2` and `scripts.validate_run` succeeded:
  18 unique activation files aligned to six target conversations; labels
  independently recomputed; backend kind `mock` throughout.

These checks establish adapter interoperability only. They provide no evidence
about Qwen susceptibility, activation-probe performance or real early warnings.
