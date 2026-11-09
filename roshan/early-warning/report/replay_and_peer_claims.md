# Interpreting the new swarm and replay claims

The collaborator's update proposes personalized asks and larger OpenRouter
swarms. Those newer batches are not in the uploaded snapshot. The current
analysis therefore evaluates only the available group-ask fanout, without
claiming a result for the pending intervention.

## Group asking and peer effects

The observed marker rates are 20/30 in the two-agent overt batch and 4/36
recipients in the four-agent group-ask batch. They describe different batches
with different state, file names, number of recipients and source wording.
They do not isolate a causal effect of group versus individually addressed asks.
A controlled personalized-ask comparison should keep the target policy, task,
order, sampling settings and analysis fixed, group outcomes by parent swarm,
and report uncertainty in the group difference.

The quoted 3/6 versus 5/67 is reproduced by counting whether the marker is
present after each recipient decision. It includes rows from recipients that
had already inserted the marker. Before each recipient's first insertion,
the corresponding new-insertion counts are **1/4 with a prior peer marker**
and **3/65 without one**. These are four positive recipients, not eight new
adoptions. The [risk-set audit](../results/fanout_audit/peer_risk_set_audit.json)
saves both tables.

Even corrected counts cannot identify peer pressure: peer visibility is not
randomized, B/C/D order is fixed, observations repeat within parents, and only
three parents contain any positive recipient. No recipient posts a message
recruiting another, so an active recruitment cascade is not observed.

## What activation replay can recover

For a known local model, a prefill hidden state is a deterministic function
of that model's parameters and its exact tokenized input, subject to inference
mode and numerical implementation. Replaying an identical prompt through the
same checkpoint can regenerate the chosen local pre-response representation.

Replaying another model's OpenRouter transcript through local Qwen produces
**Qwen's representation of that transcript**. It does not reconstruct the
original remote model's internal neural state or private reasoning. This can
still be a useful text-to-representation monitor, provided its model and
information access are named correctly and compared with trained text baselines.

Even a provider model with the same advertised name needs fidelity checks:
checkpoint/revision, tokenizer, chat template, system messages, tools,
thinking-prefix formatting, truncation, quantization and exact prompt token IDs
must match. A useful validation subset compares replayed vectors with vectors
captured during the original local calls, alongside input token hashes.
Private reasoning absent from logs cannot be reconstructed from the transcript.

The supplied `analysis/replay_probe.py` also keys its validation dictionary by
`(episode, step)` only. Fanout has three recipient vectors at each round, so
these keys collide and overwrite one another. Validation must include agent ID.
A syntax-checked [proposed patch](replay_probe_key_fix.patch) uses
`(episode, step, agent)`, rejects duplicates and missing matches, and keeps the
single-recipient NPZ fallback. It was prepared separately; no collaborator source
was changed. Our transfer analysis already uses the full three-part identity.
High cosine similarity alone also does not certify exact prompt/token fidelity.

A probe trained on one model's states should not be assumed to transfer to
another checkpoint, template, role or network setting. The observed poor fanout
transfer reinforces that caution; it does not establish a universal impossibility.

## Comparable text observations

The requested board-message-plus-edit-action baseline must receive only
public message/edit actions that occurred before the current recipient action.
The current row in `steps.jsonl` is an output, even though labels are absent.
Generation metadata, private thinking, source hidden objectives and outcome
annotations are never part of that monitor input. Exact original train/test
membership must remain frozen, with any new calibration data taken from its
training partition only.

The main report's full-visible-input baseline and the source-comparable
board-plus-edits baseline are labeled separately, so a representation change
is not mistaken for directly reproducing the original text contract.
