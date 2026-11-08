"""Generate (and tune) episodes per condition. Runs ON the pod.

    python3 swarm_env/generate.py --condition overt --justification reason --n 4 --out runs/tune
    python3 swarm_env/generate.py --sweep --n 4 --out runs/tune   # all cond x {reason,authority}

Saves per batch:
  <out>/<cond>_<just>.jsonl  — one line per episode: label, marker step, per-step log (no activations)
  <out>/<cond>_<just>.npz    — stacked recipient activations + (episode, step, label, condition) arrays
Prints the co-opt rate per batch — the knife-edge readout.
"""

import argparse, json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from episode import run_episode, RECIPIENT, SOURCE, AgentConfig, _first_marker_step
from conditions import source_system


def run_batch(model, condition, justification, n, out_dir, max_steps=6):
    src = AgentConfig("Dev-A", "source", source_system(condition, justification), owns=("notes.md",))
    rows, acts, meta = [], [], []
    for i in range(n):
        t0 = time.time()
        ep, label = run_episode(model, max_steps=max_steps, source=src, recipient=RECIPIENT)
        reveal = _first_marker_step(ep)
        log = []
        for r in ep.log:
            rec = {k: r[k] for k in ("step", "agent", "role", "result", "marker_present")}
            rec["action"] = r["action"]
            if r.get("gen") is not None:
                rec["gen"] = r["gen"]
            log.append(rec)
            if r["role"] == "recipient" and r.get("activation") is not None:
                acts.append(r["activation"])
                meta.append((i, r["step"], 1 if label == "co-opted" else 0))
        rows.append({"episode": i, "condition": condition, "justification": justification,
                     "label": label, "marker_step": reveal,
                     "board": ep.board, "log": log, "secs": round(time.time() - t0, 1)})
        print(f"  [{condition}/{justification}] ep {i}: {label} (marker step {reveal}, {rows[-1]['secs']}s)", flush=True)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / f"{condition}_{justification}"
    with open(f"{stem}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    if acts:
        m = np.array(meta, dtype=np.int64)
        np.savez_compressed(f"{stem}.npz", acts=np.stack(acts).astype(np.float32),
                            episode=m[:, 0], step=m[:, 1], label=m[:, 2],
                            condition=np.array(condition), justification=np.array(justification))
    k = sum(1 for r in rows if r["label"] == "co-opted")
    print(f"== {condition}/{justification}: co-opted {k}/{n} ==", flush=True)
    return k, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=["overt", "latent", "hidden", "control"])
    ap.add_argument("--justification", default="reason",
                    choices=["bare", "reason", "authority", "ticket"])
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--max-steps", type=int, default=6)
    ap.add_argument("--out", default="runs/tune")
    ap.add_argument("--sweep", action="store_true", help="all 3 conditions x --justifications")
    ap.add_argument("--justifications", nargs="+", default=["reason", "authority"],
                    choices=["bare", "reason", "authority", "ticket"])
    ap.add_argument("--layer", type=int, default=18)
    ap.add_argument("--backend", default="hf", choices=["hf", "openrouter"],
                    help="hf: local GPU (activations); openrouter: API, behavior only")
    args = ap.parse_args()

    if args.backend == "openrouter":
        from or_model import OpenRouterModel
        model = OpenRouterModel()
    else:
        from model import HFModel
        model = HFModel(layer=args.layer)

    summary = {}
    if args.sweep:
        for cond in ("overt", "latent", "hidden"):
            for just in args.justifications:
                k, n = run_batch(model, cond, just, args.n, args.out, args.max_steps)
                summary[f"{cond}/{just}"] = f"{k}/{n}"
    else:
        k, n = run_batch(model, args.condition, args.justification, args.n, args.out, args.max_steps)
        summary[f"{args.condition}/{args.justification}"] = f"{k}/{n}"
    print("\n=== SWEEP SUMMARY (co-opt rates) ===")
    for k_, v in summary.items():
        print(f"  {k_}: {v}")


if __name__ == "__main__":
    main()
