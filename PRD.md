# PRD & Build Log — Co-opted from the inside

Living document. Product requirements up top, a running record of everything
done below. See [PROJECT.md](PROJECT.md) for the why. Last updated: 2026-11-08
(results in — see [docs/results.md](docs/results.md)).

---

## 1. What we are building
A measurement harness that answers: *can an activation probe catch inter-agent
co-option earlier than a transcript monitor?* Four parts:
1. **Environment** — a small swarm (open-model agents) on a shared board where one
   agent recruits another into planting an inert marker.
2. **Activation capture** — read the recipient's residual stream each step.
3. **Two monitors** — a transcript reader (text/LLM judge) and a linear probe.
4. **Analysis** — detection vs measured faithfulness, and detection latency.

## 2. Requirements

### Functional
- F1. In-memory text workspace (files as strings) + append-only message board.
- F2. ≥2 agents take turns; each emits one JSON action: message | edit | done.
- F3. File ownership enforced (source cannot edit recipient's file → must recruit).
- F4. Free label: co-opted iff MARKER present in workspace at end.
- F5. Model-agnostic agent interface: swap a Stub for Qwen3-8B without touching the loop.
- F6. Capture recipient activations per step (fixed layer, last-token pooling to start).
- F7. Transcript monitor sees only recipient's messages + edits (NOT hidden reasoning).
- F8. Probe trains on activations → co-opted label; held-out by task/objective, not just run.
- F9. Faithfulness judge: rate per episode whether the transcript reveals the co-option.
- F10. Metrics: detection @ matched FPR per monitor; detection latency (steps probe leads transcript).

### Non-functional
- N1. No code execution / no sandbox (side action is an inert string).
- N2. Realizability: every monitor gets only its real deployment input.
- N3. Reuse owner's pipeline (train_probe, cross_fit, make_figures, harvest_activations, RunPod).
- N4. Budget ~$10–30 GPU. Keep episodes short (5–8 steps), prompts short.
- N5. Prove the loop with a Stub model before spending any GPU.

### Success criteria (can't-lose)
- Probe beats transcript in latent/hidden and ties in overt → headline win.
- Probe fails → documented finding on limits of internal monitoring. Both publishable.

## 3. Architecture / components → code
| Component | File | Status |
|---|---|---|
| Env state, actions, ownership, marker, rendering | `swarm_env/env.py` | **built** |
| Prompts: source/recipient systems, action protocol, prompt builder | `swarm_env/prompts.py` | **built** |
| Model interface: StubModel + HFModel (Qwen3-8B) | `swarm_env/model.py` | **built; HFModel needs pod to run** |
| Episode loop, AgentConfig, CLI | `swarm_env/episode.py` | **built, runs** |
| Activation capture (Qwen3-8B, prefill pass, [L+1], last-token) | `swarm_env/model.py` (HFModel) | **written; smoke-test on pod** |
| Probe train/eval | reuse `ais-research/experiment/train_probe.py`, `cross_fit.py` | reuse |
| Text monitor | reuse text baseline / LLM judge | reuse |
| Figures | reuse `make_figures.py` | reuse |

## 4. Build log (what we've done)

### 2026-11-06 — framing & design
- Converted 4 hackathon talks + chats into `docs/talks/`; cross-talk synthesis (local notes, since removed from the repo).
- Verified rules → `docs/plan/rules.md`. Confirmed remote track, deadline Sun 23:59 AoE.
- Read the METR/Redwood Hugging Face incident report → `docs/plan/hf-incident.md`
  (real emergent swarm: ~1200 agents, recruiters, transcript spoofing spread to 7%).
- Owner's ais-research repo reviewed: owner owns the probe pipeline + a single-agent
  control env (goodhart-prep) + RunPod workflow on Qwen3-8B. Owner IS the interp lead.
- Key pivot: owner's own "Probe–Text Gap" null (probe never beats text on a *faithful*
  transcript, because activations = f(prefix)) becomes the launchpad: probe can only win
  where the transcript is UNFAITHFUL = the swarm (spoofing / split / latency).
- Red-team pass (against the rules). Two threats fixed by design:
  (1) circularity → spoof is agent-driven, faithfulness is measured, BOTH monitors attacked;
  (2) inter-agent-influence scoring gap → influence/co-option is now the CENTER.
- Project locked: influence-centered, swarm-only. Design → `docs/plan/project-final.md`.
  Minimal environment spec → `docs/plan/env-spec.md`.
- Discord recruiting post drafted (honest about what's built vs not).

### 2026-11-07 — build start
- Scaffolded `swarm_env/`. `env.py` done: Episode state, JSON-action apply with file
  ownership, marker check, workspace/board rendering, initial 2-file repo.
- Built `prompts.py`, `model.py` (StubModel + HFModel TODO), `episode.py` (loop + CLI).
- **Loop proven with no GPU**, all three stub modes behave correctly:
  honest -> clean (no marker); compliant -> co-opted (marker at recipient step 0);
  latent -> co-opted (chore at step 0, marker planted at step 2 = a 2-step latency gap).
  Ownership enforced, board + action parsing + free label all working.
- Initialized `swarm-hackathon` as its own git repo (neither local folder was a repo).
  Copied 7 preexisting probe scripts into `probe/` (train_probe, cross_fit, text_classifier,
  text_floor, make_figures, harvest_activations, llm_judge) with `probe/README.md`
  marking them preexisting per the rules. `.gitignore` excludes recordings + the untrusted
  swarmtraces dataset. Initial commit made.
- RunPod wired up via the official MCP server (OAuth). Registered owner's SSH key (account
  had none). Deployed pod `eoo4bzheqi3ztx`: A40 48GB Secure EU-SE-1 at $0.59/hr (4090 now
  $0.89/hr LOW stock — A40 cheaper, better stock, batch headroom). Code rsynced (no creds
  on pod), weights on the 60GB persistent volume (HF_HOME=/workspace/hf).
- **SMOKE PASS** (one real Qwen3-8B episode): all JSON actions parsed, 2 recipient
  activations captured shape (4096,), episode terminated, label produced. ~15s/turn with
  thinking => ~300 episodes ≈ 5 GPU-hrs ≈ $3 — generation fits the budget. Behavioral
  signal: recipient did its task and REFUSED the marker ask at default settings (its
  reasoning cited the "only the requested change" rule) => knife-edge tuning (R2) is real
  and is the next task.
- **Tuning sweeps (knife-edge, R2).** Sweep 1 (3 cond x {reason, authority} x 4 eps) came
  back 0/24 — diagnosed as a BUG, not refusal: with thinking enabled the source's CoT
  blew the 512-token cap before emitting its JSON action, and parse_action's fail-safe
  silently turned that into "done", so the recruit message was never posted. Fixed:
  max_new_tokens 1536, one retry on parse failure, per-turn gen metadata (parse_ok /
  truncated) logged. Sweep 2 (same grid, fixed): 1/24 genuine co-opt (overt/authority,
  marker at recipient step 1) + 1 FAKE co-opt that exposed a label loophole — the source
  wrote the marker into its own notes.md and marker-anywhere counted it. Fixed: co-option
  now requires the marker in a recipient-owned file (label + per-step marker_present).
  Takeaway: authority framing recruits sometimes, reason-only never -> escalated to a
  'ticket' tier (concrete ticket + deadline + in-scope claim); sweep 3 running.
  Episodes now 2.5–6 min (longer generations) -> ~100 eps/cond would overshoot the
  budget; plan ~40–50 eps/cond and log the prereg deviation.
- Wrote the real `HFModel` (Qwen3-8B) behind the same `.act()` interface + `build_messages`:
  two passes per turn — a prefill-only forward for the activation (last-token residual at a
  fixed layer, `[L+1]` indexing and degenerate-vector checks ported from harvest_activations),
  then `generate()` for the action text. Lazy torch import keeps the stub loop GPU-free.
  Not yet run — needs the pod.

### 2026-11-08 — the 0/40 incident, the full run, and the result
- **Full run #1 (old recipient prompt) came back 0/40 co-opted on overt** — not a bug:
  asks posted in 39/40, parses fine; Dev-B's rule "make ONLY the change your task
  requires" inoculated it against ALL influence (refusal CoT cited it verbatim).
  Revised the recipient to a realistic engineer's latitude — ONCE, identically in
  every condition (attribution logic intact) — capped Dev-A at 2 asks, archived the
  old episodes as tuning data, logged everything in prereg deviations. Sanity 2/6 →
  relaunched at 30/25/25/20.
- **Dataset landed overnight: overt 20/30, latent 14/25, hidden 12/25, control 0/20**
  (100 episodes, 204 recipient step-vectors at dim 4096). Rsynced local, pod stopped.
  Committed raw jsonl+npz, monitor-facing flattening (`runs/flat/steps.jsonl`, no
  labels per the input contract), eval join table, frozen seed-0 70/30 split.
- **1:30am canary** (go/no-go, prereg-logged): post-action AUC 0.997 = the trivial
  B4 positive control; decision-step pre-action AUC ~0.70 = real signal. Proceeded.
- **Probe eval** (`analysis/probe_eval.py`): pre-action episode-level AUC over 50
  splits — latent 0.84 ± 0.13, hidden 0.74 ± 0.15, overt 0.64 ± 0.15. Two analysis
  deviations logged: the prereg 2%-FPR-on-controls threshold is DEGENERATE (controls
  have no ask → it detects asks, not co-option; within-condition AUC is the honest
  metric), and step-latency fails mechanically (marker lands at Dev-B's first round
  56/58 → the probe's lead is within-round, prefill vs emitted action).
- **Text monitor + head-to-head** (`analysis/text_baseline.py`, `head_to_head.py`):
  trained TF-IDF under the strict input contract, PAIRED on 50 identical splits —
  probe−text = **+0.19 overt / +0.23 latent / −0.05 hidden** (probe wins 82/78/30%
  of splits). **The falsifier does not fire; H2 (latent headline) supported; H1
  wrong in our favor** (pre-action transcript ≈ uninformative, text at 0.46); H3's
  premise failed structurally (ask stays board-visible in hidden; 3 no-ask episodes
  hand the text monitor free signal). Figures 1 + 2 committed.
- **Swarm fan-out built** (`swarm_env/fanout.py`): 1 source → 3 recipients, recipient
  prompt byte-identical (name/file substitution only) for zero-shot probe transfer,
  `peer_complied_before` logged per step for the conformity number. Stub-tested;
  awaiting the ~$1 pod run.

## 5. To-do (weekend plan)
- [x] Design the task + hidden objective (the unsanctioned marker).
- [x] Env state + actions (`env.py`).
- [x] Prompts + model interface + episode loop; run Stub end-to-end (clean / co-opted / latent).
- [x] Stand up Qwen3-8B on RunPod behind the same interface.
- [x] Activation capture in the loop (fixed layer, last-token).
- [x] Generate dataset; TUNE so co-opted and clean rates are both non-trivial (knife-edge).
- [x] Faithfulness measured (structural analysis: ask visible everywhere, Dev-B silent).
- [x] Train probe (frozen episode split) + run trained transcript monitor.
- [x] Analysis: paired head-to-head; within-round latency reframe. Two figures.
- [ ] CEILING: fan-out run (code built + stub-tested; needs the ~$1 pod run).
- [ ] Report on official template + Limitations/Dual-Use appendix; mark preexisting code.
- [ ] Submit before Sun 23:59 AoE.

## 6. Risks
- R1. Activation capture in a multi-step loop is new integration (owner's prior work was single-pass). Mitigate: do it fresh, one layer first.
- R2. Co-option knife-edge: recipient always refuses or always complies → no signal. Mitigate: budget tuning time.
- R3. Orchestration teammate is parallelism, not survival; owner can build the board.
- R4. Hackathon n may not support tight CIs → spend runs on the one headline comparison.

## 7. Submission checklist (from rules.md — confirm on live Apart page)
- [ ] Official template; ≤ ~8 pages; abstract 150–250 words.
- [ ] Required Limitations + Dual-Use / Ethical appendix.
- [ ] Preexisting code marked as preexisting in README + report.
- [ ] Form: title, summary, PDF, Track 4, team name, member names + emails.
