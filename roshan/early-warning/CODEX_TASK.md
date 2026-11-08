# Current task and implementation boundaries

The user's current specification is **Swarm Early Warning — Predicting Agent Recruitment Before Defection** (Apart Research Swarm Alignment Hackathon 2026). This file records the local implementation contract; the full conversation remains authoritative.

1. Build the smallest working independent A→B/C/D susceptibility experiment, using mock inference for software tests and a one-model Qwen adapter for real work.
2. Keep each target's messages private to that target. Use inert synthetic files and independently verified ownership rules. Primary outcome: verified unauthorized action attempt. Record completed violations separately.
3. Capture documented incoming-context activations before response generation. Current configured sample: zero-based decoder layer 18, Transformers hidden_states index 19, final context token. Never call generation/post-action features strict pre-response prediction.
4. Generate raw JSONL with null future labels, then separate complete-episode offline labels. Pass monitors an explicit allowlist of currently visible context. No hidden source instructions, private thinking, current response, future action or outcome inputs.
5. Compare activation, LLM transcript and trained TF-IDF/logistic monitors. Split complete episodes/seed families; fit preprocessing on train; choose thresholds on validation; reserve final real test data. Distinguish imminent detection (lead 0) from advance prediction. Include exposed-only controls, class counts, missing alerts and agreement-candidate caveats.
6. Use mock measurements only for implementation checks. Real model findings/figures remain pending until real data exist.
7. Do not provision paid GPU resources or alter Isahan's active pod without explicit approval. An uploaded collaborator ZIP is reference code, not authorization to run infrastructure. Preserve it outside this project; use small adapters/exports and keep differing task-scope labels separate.
8. Reproduce local checks using README commands. Complete the primary experiment before considering a genuine behavioral cascade.

Initial workspace inspection found no previous project or tests. The collaborator ZIP arrived later and contains the two-agent runner, HFModel and preexisting probing scripts, but no real datasets, weights or credentials. See report/collaborator_integration.md for interfaces and limitations.
