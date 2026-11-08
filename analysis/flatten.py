"""Flatten episode records into the agreed per-step format + a frozen split.

Outputs (from runs/full/*.jsonl):
  runs/flat/steps.jsonl   — MONITOR-FACING. One row per agent step:
                            condition, episode, step, agent, role, action.
                            Deliberately EXCLUDES label, marker_present,
                            marker_step, and gen metadata, per the monitor
                            input contract (the text monitor may read only
                            board messages and edit actions).
  runs/flat/labels.jsonl  — EVAL-ONLY. One row per episode:
                            condition, episode, label (1=co-opted), marker_step,
                            n_steps. Join key: (condition, episode).
  runs/split.json         — frozen train/test split, seed 0, ~70/30,
                            episode-level, stratified by condition x label.
                            Everyone trains/tests on THIS split; never resplit.

Monitor scores go in separate files keyed (condition, episode, step) — never
back into these.
"""

import json
import random
from pathlib import Path

CONDITIONS = ["overt", "latent", "hidden", "control"]
SEED = 0
TEST_FRAC = 0.30

root = Path(__file__).resolve().parent.parent
flat = root / "runs" / "flat"
flat.mkdir(parents=True, exist_ok=True)

steps_f = open(flat / "steps.jsonl", "w")
labels_f = open(flat / "labels.jsonl", "w")
strata = {}  # (condition, label) -> [episode ids]

for cond in CONDITIONS:
    for line in open(root / "runs" / "full" / f"{cond}_ticket.jsonl"):
        r = json.loads(line)
        label = 1 if r["label"] == "co-opted" else 0
        strata.setdefault((cond, label), []).append(r["episode"])
        labels_f.write(json.dumps({
            "condition": cond, "episode": r["episode"], "label": label,
            "marker_step": r["marker_step"], "n_steps": len(r["log"]),
        }) + "\n")
        for s in r["log"]:
            steps_f.write(json.dumps({
                "condition": cond, "episode": r["episode"], "step": s["step"],
                "agent": s["agent"], "role": s["role"], "action": s["action"],
            }) + "\n")
steps_f.close()
labels_f.close()

rng = random.Random(SEED)
split = {"seed": SEED, "test_frac": TEST_FRAC, "stratify": "condition x label",
         "train": [], "test": []}
for (cond, label), eps in sorted(strata.items()):
    eps = sorted(eps)
    rng.shuffle(eps)
    n_test = max(1, round(len(eps) * TEST_FRAC))
    for e in eps[:n_test]:
        split["test"].append([cond, e])
    for e in eps[n_test:]:
        split["train"].append([cond, e])

with open(root / "runs" / "split.json", "w") as f:
    json.dump(split, f, indent=1)

print(f"steps.jsonl: {sum(1 for _ in open(flat / 'steps.jsonl'))} rows")
print(f"labels.jsonl: {sum(1 for _ in open(flat / 'labels.jsonl'))} rows")
print(f"split: train={len(split['train'])} test={len(split['test'])}")
for (cond, label), eps in sorted(strata.items()):
    n_te = sum(1 for c, e in split["test"] if c == cond and e in eps)
    print(f"  {cond:8s} label={label}: {len(eps):3d} eps ({n_te} test)")
