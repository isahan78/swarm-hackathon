# CHECKLIST — live task tracker

Ordered by dependency. Tick as you finish. See [PROJECT.md](PROJECT.md) for the
why, [PRD.md](PRD.md) for requirements, [docs/plan/env-spec.md](docs/plan/env-spec.md)
for the build spec. ★ = critical path.  **← YOU ARE HERE** marks current front.

## Phase 0 — Setup
- [x] Design task + hidden objective (unsanctioned marker)
- [x] Build env skeleton + episode loop, proven with stub (honest/compliant/latent)
- [x] PROJECT.md + PRD.md
- [x] Init git repo; copy preexisting probe scripts into `probe/` (marked preexisting)
- [ ] **Seal the pre-registration** — fill owner's forecast in docs/plan/prereg.md and
      commit BEFORE any GPU: overt = probe ties text; latent = probe leads text; hidden = ?
- [ ] Post Discord recruit — Naveen is in (orchestration + report); confirm & lock team
- [ ] Confirm live Apart page: page limit, abstract length, required appendix

## Phase 1 — Wire Qwen3-8B (Sat AM, on RunPod) ★
- [x] ★ Implement `HFModel.act`: build_messages → generate → parse_action (swarm_env/model.py)
- [x] ★ Add activation capture: prefill pass, fixed layer, last-token, [L+1] indexing
- [ ] ★ Stand up Qwen3-8B on RunPod (reuse pod_overnight workflow)  **← YOU ARE HERE**
- [ ] Smoke test: 1 real episode end-to-end; confirm JSON parses + activation shape is (hidden,)

## Phase 2 — Generate data + tune (Sat midday) ★
- [ ] Define the 3 condition framings (overt / latent / hidden evasion pressure)
- [ ] ★ TUNE prompts so BOTH co-opted and clean rates are non-trivial (the knife-edge)
- [ ] Generate N episodes/condition; store transcript + per-step activations + free label
- [ ] Generate clean no-recruit control episodes (probe false-positive floor)

## Phase 3 — Monitors + faithfulness (Sat PM)
- [ ] Faithfulness judge pass: rate per episode whether transcript reveals the co-option
- [ ] Train probe (held-out by objective, not just run) — reuse train_probe.py
- [ ] Run transcript monitor (text baseline / LLM judge) on the same episodes

## Phase 4 — Analysis = the result (Sat night)
- [ ] Detection @ matched FPR, both monitors, vs MEASURED faithfulness → crossover plot
- [ ] Detection latency: steps the probe leads the transcript (latent episodes)
- [ ] Controls: probe FPR floor on clean; compare vs imported single-agent baseline
- [ ] Two headline figures — reuse make_figures.py

## Phase 5 — Ceiling (Sun AM, only if floor is solid)
- [ ] Scale to N agents; does co-option cascade hop to hop; does the probe track the front

## Phase 6 — Write-up + submit (Sun)
- [ ] Report on official template (abstract 150–250w, thesis, setup, results, limitations)
- [ ] Limitations + Dual-Use appendix (address circularity head-on; no novel harm)
- [ ] Mark preexisting code as preexisting in README + report
- [ ] Submit form before Sun Nov 8 23:59 AoE (title, summary, PDF, Track 4, team, emails)

---
### Immediate next 3 actions
1. Seal the pre-registration and commit it.
2. Get the RunPod up with Qwen3-8B.
3. I write `HFModel` + the activation hook the moment the pod is live.
