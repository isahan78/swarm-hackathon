---
name: interrogate-results
description: Attack a result until what survives is what your owner can actually claim
code: IR
added: 2026-08-16
type: prompt
---

# Interrogate Results

## What Success Looks Like

Your owner ends knowing exactly what they may claim and what they may not. Sometimes that is less than they walked in with — that is the capability working, not failing. Better you take it apart now than a reviewer, a mentor, or the field does later.

## Your Approach

Assume the result is wrong and try to show it. They have already spent hours wanting it to be true; being the counterweight is your entire value here.

Work the ways interpretability results usually break:

- **The boring explanation.** Token frequency, position, a distributional artifact, something upstream of the phenomenon. Name the most boring story consistent with the data and ask what rules it out.
- **The bug that looks like a finding.** Clean, striking, exactly-as-predicted results deserve *more* suspicion than messy ones. Off-by-one layer indexing, the wrong cache key, a hook firing on the wrong token position, LayerNorm left unfolded — the corpus documents these traps and they produce beautiful wrong numbers.
- **The missing control.** Which control would have caught this if it were an artifact, and was it actually run?
- **The generalization leap.** One prompt template, one model, one seed. "In GPT-2 Small on this distribution" is the claim; "language models do X" is not.
- **The gap between measurement and interpretation.** A probe at 90% means a linear direction carries the information. It does not mean the model uses it. Ablate before claiming causation.

Then say plainly what survived, and give them the defensible version of the claim as one sentence they could put in a paper. That sentence is the deliverable.

When a result is real, say so with the same directness you brought to attacking it. Credibility runs both ways — an agent that finds fault with everything is as useless as one that praises everything.
