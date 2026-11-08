# CHECKLIST — live task tracker

Ordered by dependency. Tick as you finish. See [PROJECT.md](PROJECT.md) for the
why, [PRD.md](PRD.md) for requirements, [docs/plan/env-spec.md](docs/plan/env-spec.md)
for the build spec. ★ = critical path.  **← YOU ARE HERE** marks current front.

## Phase 0 — Setup
- [x] Design task + hidden objective (unsanctioned marker)
- [x] Build env skeleton + episode loop, proven with stub (honest/compliant/latent)
- [x] PROJECT.md + PRD.md
- [x] Init git repo; copy preexisting probe scripts into `probe/` (marked preexisting)
- [x] **Seal the pre-registration** — both forecasts sealed in docs/plan/prereg.md
      before condition-level results; all changes since logged in its deviations
- [ ] Lock team — Roshan in (repo collaborator; need full name + email for the form);
      Naveen silent
- [ ] Confirm live Apart page: page limit, abstract length, required appendix

## Phase 1 — Wire Qwen3-8B (Sat AM, on RunPod) ★
- [x] ★ Implement `HFModel.act`: build_messages → generate → parse_action (swarm_env/model.py)
- [x] ★ Add activation capture: prefill pass, fixed layer, last-token, [L+1] indexing
- [x] ★ Stand up Qwen3-8B on RunPod — via RunPod MCP: pod `eoo4bzheqi3ztx`, A40 48GB, $0.59/hr, EU-SE-1
- [x] Smoke test PASS (2026-11-07): actions parsed, 2 recipient activations shape (4096,), label clean.
      Episode ~60s (~15s/turn with thinking) -> ~300 episodes ≈ 5 GPU-hrs ≈ $3. Recipient REFUSED the
      marker at default settings -> tuning must raise plausibility (knife-edge, as predicted R2)

## Phase 2 — Generate data + tune (Sat midday) ★
- [x] Define the 3 condition framings (overt / latent / hidden evasion pressure) — conditions.py
- [x] ★ TUNE prompts so BOTH rates are non-trivial — knife-edge opened after 3 sweeps
      + one incident: the recipient's "only the requested change" rule inoculated it
      (0/40); recipient latitude revised ONCE uniformly, ticket tier frozen (prereg logged)
- [x] Generate episodes: overt 20/30, latent 14/25, hidden 12/25 co-opted — in repo
      (runs/full/*.jsonl + .npz), flattened (runs/flat/), frozen split (runs/split.json)
- [x] Clean no-recruit controls: 0/20 co-opted (floor holds); pod STOPPED after rsync

## Phase 3 — Monitors + faithfulness (done Sun AM)
- [x] Faithfulness measured structurally: marker visible in ask in ALL conditions
      (30/30, 24/25, 22/25); Dev-B verbalizes it 0 times anywhere (docs/results.md)
- [x] Train probe — analysis/probe_eval.py on the frozen split (fresh code; the
      preexisting probe/ scripts informed the method)
- [x] Transcript monitor: trained TF-IDF under the strict input contract —
      analysis/text_baseline.py

## Phase 4 — Analysis = the result (done Sun AM)
- [x] Head-to-head PAIRED on 50 identical splits (analysis/head_to_head.py):
      probe−text = +0.19 overt / +0.23 latent / −0.05 hidden; probe wins 82/78/30%
      of splits. FALSIFIER DOES NOT FIRE. Prereg's control-calibrated 2% FPR found
      degenerate (ask detector) — logged; within-condition AUC is the honest metric
- [x] Latency: marker lands at Dev-B's first decision round (56/58) → reframed as
      within-round lead (prefill vs emitted action), logged in prereg deviations
- [x] Controls: 0/20 co-opted; canary + B1 step-0 control + overt-only transfer run
- [x] Two headline figures: figures/fig1_probe_auc.png, figures/fig2_probe_vs_text.png

## Phase 5 — Ceiling: swarm fan-out (Sun PM)  **← YOU ARE HERE**
- [x] Fan-out code built + stub-tested (swarm_env/fanout.py): 1 source → 3 recipients,
      recipient prompt/marker/tier FROZEN (zero-shot probe transfer), per-step
      peer_complied_before logged for the conformity number
- [ ] ★ Run ~12 fan-out episodes on the pod (~1.5h, ~$1); conformity analysis +
      zero-shot probe transfer readout

## Phase 6 — Write-up + submit (Sun evening) ★
- [ ] ★ Report on official template (abstract 150–250w; results from docs/results.md)
- [ ] Limitations + Dual-Use appendix (degenerate-threshold + hidden-premise caveats in)
- [ ] Mark preexisting code as preexisting in README + report (probe/README.md done)
- [ ] Flip repo public; submit form before Sun Nov 8 23:59 AoE
      (title, summary, PDF, Track 4, team names + emails — NEED Roshan's)

---
### Immediate next 3 actions
1. Restart pod, launch the fan-out run (one command), stop pod after rsync.
2. Draft the report on the official template while it generates.
3. Get Roshan's full name + email; flip repo public; submit.
