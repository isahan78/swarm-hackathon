# PRD & Build Log — Co-opted from the inside

Living document. Product requirements up top, a running record of everything
done below. See [PROJECT.md](PROJECT.md) for the why. Last updated: 2026-11-07.

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
| Model interface: StubModel (+ HFModel for Qwen3-8B later) | `swarm_env/model.py` | **built (stub)** |
| Episode loop, AgentConfig, CLI | `swarm_env/episode.py` | **built, runs** |
| Activation capture hook (Qwen3-8B) | `swarm_env/model.py` (HFModel) | TODO (on RunPod) |
| Probe train/eval | reuse `ais-research/experiment/train_probe.py`, `cross_fit.py` | reuse |
| Text monitor | reuse text baseline / LLM judge | reuse |
| Figures | reuse `make_figures.py` | reuse |

## 4. Build log (what we've done)

### 2026-11-06 — framing & design
- Converted 4 hackathon talks + chats into `docs/talks/`; cross-talk synthesis in `docs/overview.md`.
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

## 5. To-do (weekend plan)
- [x] Design the task + hidden objective (the unsanctioned marker).
- [x] Env state + actions (`env.py`).
- [x] Prompts + model interface + episode loop; run Stub end-to-end (clean / co-opted / latent).
- [ ] Stand up Qwen3-8B on RunPod behind the same interface.
- [ ] Activation capture in the loop (fixed layer, last-token).
- [ ] Generate dataset; TUNE so co-opted and clean rates are both non-trivial (knife-edge).
- [ ] Faithfulness judge pass.
- [ ] Train probe (held-out by objective) + run transcript monitor.
- [ ] Analysis: detection vs faithfulness; detection latency. Two figures.
- [ ] CEILING: scale to N agents (cascade), if floor is solid.
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
