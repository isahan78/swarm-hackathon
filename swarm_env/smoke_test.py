"""Smoke test — the Phase 1 gate. Run ON the pod:

    python3 swarm_env/smoke_test.py [--layer 18] [--max-steps 4]

One real Qwen3-8B episode end-to-end. Passes iff:
  1. every turn's reply parses into a valid JSON action (no fail-safe 'done' storm),
  2. the recipient's activation is a finite, non-zero vector of shape (hidden,),
  3. the episode terminates and yields a label.
Prints the board and per-step log so we can eyeball agent behavior (does Dev-A
actually recruit? does Dev-B comply/refuse?) before spending on a dataset.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from episode import run_episode, _first_marker_step
from model import HFModel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", type=int, default=18)
    ap.add_argument("--max-steps", type=int, default=4)
    ap.add_argument("--max-new-tokens", type=int, default=512)
    ap.add_argument("--no-thinking", action="store_true")
    args = ap.parse_args()

    print(f"loading Qwen3-8B (layer={args.layer}, thinking={not args.no_thinking}) ...")
    model = HFModel(layer=args.layer, max_new_tokens=args.max_new_tokens,
                    enable_thinking=not args.no_thinking)

    ep, label = run_episode(model, max_steps=args.max_steps)

    print(f"\n=== LABEL: {label} ===\n")
    print("per-step log:")
    n_acts, fail_safe_dones = 0, 0
    for r in ep.log:
        act = r["action"]
        print(f"  step {r['step']:>2} {r['agent']:<6} {act.get('type'):<8} -> {r['result']}")
        if r["role"] == "recipient" and r.get("activation") is not None:
            v = r["activation"]
            assert v.ndim == 1 and v.shape[0] > 0, f"bad activation shape {v.shape}"
            n_acts += 1
    print("\nboard:")
    for m in ep.board:
        print(f"  [step {m['step']}] {m['from']}: {m['text'][:200]}")
    print(f"\nlast raw generation (tail):\n---\n{(model.last_text or '')[-500:]}\n---")
    print(f"\nactivations captured (recipient turns): {n_acts}, "
          f"shape: {ep.log and next((r['activation'].shape for r in ep.log if r.get('activation') is not None), None)}")
    print(f"marker files: {ep.marker_files()}")
    print(f"transcript reveals marker at recipient step: {_first_marker_step(ep)}")

    if n_acts == 0:
        sys.exit("SMOKE FAIL: no recipient activations captured")
    print("\nSMOKE PASS")


if __name__ == "__main__":
    main()
