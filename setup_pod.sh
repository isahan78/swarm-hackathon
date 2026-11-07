#!/usr/bin/env bash
# Pod setup — run ON the RunPod box after the code is rsynced to ~/swarm-hackathon.
# From the local machine the whole flow is:
#   rsync -az --exclude .git --exclude '*.m4a' --exclude '*.mp4' --exclude data \
#       /Users/IsahanKhan/swarm-hackathon/  <pod>:~/swarm-hackathon/
#   ssh <pod> 'cd ~/swarm-hackathon && bash setup_pod.sh'
set -euo pipefail
cd "$(dirname "$0")"

echo "== python/env =="
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip -q install --upgrade pip
pip -q install -r requirements.txt

echo "== GPU check =="
python3 - <<'PY'
import torch
assert torch.cuda.is_available(), "No CUDA GPU visible"
print("cuda OK:", torch.cuda.get_device_name(0),
      f"{torch.cuda.get_device_properties(0).total_memory/1e9:.0f} GB")
PY

echo "== prefetch Qwen3-8B weights (resumable; ~16 GB) =="
hf download Qwen/Qwen3-8B --exclude "*.gguf" || \
  huggingface-cli download Qwen/Qwen3-8B --exclude "*.gguf"

echo "== done. Smoke test: =="
echo "   source .venv/bin/activate && python3 swarm_env/smoke_test.py"
