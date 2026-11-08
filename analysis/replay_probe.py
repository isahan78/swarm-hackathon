"""Replay probing: recover prefill activations from logged transcripts.

The probe reads the layer-18 residual at PREFILL — a deterministic function
of the prompt — and our traces log everything the prompt is built from (board
messages and workspace edits, in execution order). So for episodes generated
WITHOUT activation capture (the OpenRouter sweep), we rebuild each recipient's
exact prompt at each decision and run Pass 1 of the pod model over it. This
is the same code path that produced every stored activation.

Runs ON THE POD.

  # self-validation: replay pod episodes and compare to their stored npz
  python3 analysis/replay_probe.py runs/full/overt_ticket.jsonl \
      --validate runs/full/overt_ticket.npz

  # recover activations for an OpenRouter batch
  python3 analysis/replay_probe.py runs/or/fanout_overt_ticket_n10.jsonl \
      --out runs/or/fanout_overt_ticket_n10_replay.npz
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "swarm_env"))

import numpy as np

from env import Episode, initial_workspace
from episode import RECIPIENT, AgentConfig
from fanout import fanout_workspace, make_recipient


def agent_configs(rec):
    """Recipient AgentConfigs + initial workspace for one episode record."""
    if "labels" in rec:  # fan-out episode
        names = sorted(rec["labels"])
        rfiles = {n: f"config_{n.split('-')[1].lower()}.py" for n in names}
        return ({n: make_recipient(n, f) for n, f in rfiles.items()},
                fanout_workspace(rfiles))
    return {"Dev-B": RECIPIENT}, initial_workspace()


def replay_episode(model, rec):
    """Yield (step, agent, prefill_vec) for each recipient decision, by
    replaying the log in execution order."""
    import torch
    from model import check_activation, residual_index
    from prompts import build_messages

    recipients, ws = agent_configs(rec)
    ep = Episode(workspace=ws)
    for r in rec["log"]:
        agent_name, action = r["agent"], r["action"]
        if r["role"] == "recipient":
            cfg = recipients[agent_name]
            messages = build_messages(cfg, ep)
            text_in = model.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
                enable_thinking=True)
            inputs = model.tokenizer(text_in, return_tensors="pt").to(model.model.device)
            with torch.inference_mode():
                out = model.model(**inputs, output_hidden_states=True, use_cache=False)
            hs = out.hidden_states
            vec = hs[residual_index(model.layer, len(hs))][0, -1, :].float()
            vec = vec.cpu().numpy().astype(np.float32)
            check_activation(vec)
            yield r["step"], agent_name, vec
            del out, hs
        # apply the logged action to advance state
        if action["type"] == "message":
            ep.post(r["step"], agent_name, action.get("text", ""))
        elif action["type"] == "edit" and str(r.get("result", "")).startswith("edited"):
            ep.workspace[action["file"]] = action.get("content", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", help="write replayed activations to this .npz")
    ap.add_argument("--validate", help="stored .npz to compare against (pod data)")
    ap.add_argument("--layer", type=int, default=18)
    ap.add_argument("--limit", type=int, help="replay only the first N episodes")
    args = ap.parse_args()

    from model import HFModel
    model = HFModel(layer=args.layer)

    acts, eps, steps, agents, labels = [], [], [], [], []
    n_done = 0
    for line in open(args.jsonl):
        rec = json.loads(line)
        if args.limit and n_done >= args.limit:
            break
        lab = rec.get("labels") or {"Dev-B": rec["label"]}
        for step, agent, vec in replay_episode(model, rec):
            acts.append(vec)
            eps.append(rec["episode"]); steps.append(step); agents.append(agent)
            labels.append(1 if lab[agent] == "co-opted" else 0)
        n_done += 1
        print(f"  replayed ep {rec['episode']} ({len(acts)} vecs total)", flush=True)

    acts = np.stack(acts)
    if args.validate:
        d = np.load(args.validate, allow_pickle=True)
        stored = {(int(e), int(s)): d["acts"][i]
                  for i, (e, s) in enumerate(zip(d["episode"], d["step"]))}
        cos, mad = [], []
        for i, (e, s) in enumerate(zip(eps, steps)):
            if (e, s) in stored:
                a, b = acts[i], stored[(e, s)]
                cos.append(float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))))
                mad.append(float(np.max(np.abs(a - b))))
        cos, mad = np.array(cos), np.array(mad)
        print(f"VALIDATION vs {args.validate}: {len(cos)} matched vectors")
        print(f"  cosine: min {cos.min():.6f}  mean {cos.mean():.6f}")
        print(f"  max-abs-diff: median {np.median(mad):.4f}  max {mad.max():.4f}")
        print("  VERDICT:", "EXACT-ENOUGH (replay sound)" if cos.min() > 0.999
              else "MISMATCH — debug prompt reconstruction before trusting replay")
    if args.out:
        np.savez_compressed(args.out, acts=acts,
                            episode=np.array(eps), step=np.array(steps),
                            agent=np.array(agents), label=np.array(labels))
        print(f"wrote {args.out} ({len(acts)} vectors)")


if __name__ == "__main__":
    main()
