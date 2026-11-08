"""OpenRouter backend behind the same .act() interface as HFModel/StubModel.

BEHAVIOR-ONLY: returns activation None (no internals over an API). Used for
the group-size scaling sweep; activations for these episodes are recovered
afterwards by replaying logged prompts through the local model (prefill is a
deterministic function of the prompt — see analysis/replay_probe.py).

Sampling parity with the pod HFModel: temperature 0.7, top_p 0.9,
max_tokens 1536, thinking left to the provider default for qwen3.
The responding provider is recorded per call in last_meta for the fidelity
audit (quantization / serving drift is the known risk; the anchor arm
checks it behaviorally).

Key: read from the OPENROUTER_API_KEY environment variable. Never logged,
never written to disk.
"""

import json
import os
import time
import urllib.request

from model import parse_action_or_none
from prompts import build_messages

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "qwen/qwen3-8b"


class OpenRouterModel:
    def __init__(self, model_id=MODEL_ID, temperature=0.7, top_p=0.9,
                 max_tokens=1536, timeout=180):
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if not key:
            raise RuntimeError("Set OPENROUTER_API_KEY in the environment.")
        self._key = key
        self.model_id = model_id
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.last_meta = None

    def _call(self, messages):
        body = json.dumps({
            "model": self.model_id,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
        }).encode()
        req = urllib.request.Request(API_URL, data=body, headers={
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
        })
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read())

    def act(self, agent, ep, step):
        messages = build_messages(agent, ep)
        action, meta = None, {}
        for attempt in range(1, 4):  # one extra retry vs pod (network errors)
            try:
                resp = self._call(messages)
            except Exception as e:  # noqa: BLE001 — network/HTTP: back off, retry
                meta = {"parse_ok": False, "error": type(e).__name__,
                        "attempt": attempt}
                time.sleep(min(10 * attempt, 30))
                continue
            choice = (resp.get("choices") or [{}])[0]
            msg = choice.get("message", {})
            # Some providers put Qwen3 thinking in `reasoning`; the action JSON
            # is in content. Fall back to reasoning text if content is empty.
            text = msg.get("content") or msg.get("reasoning") or ""
            action = parse_action_or_none(text)
            meta = {
                "parse_ok": action is not None,
                "attempt": attempt,
                "provider": resp.get("provider"),
                "or_model": resp.get("model"),
                "finish": choice.get("finish_reason"),
                "new_tokens": (resp.get("usage") or {}).get("completion_tokens"),
            }
            if action is not None:
                break
        self.last_meta = meta
        return action or {"type": "done"}, None
