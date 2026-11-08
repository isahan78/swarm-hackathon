"""Adapt a collaborator's existing wrapper without changing its active runner."""
from .base import AgentBackend


class CallableBackendAdapter(AgentBackend):
    backend_kind = "adapter"

    def __init__(self, generate_fn, model_id="collaborator-unspecified", *, timing="unknown"):
        self.generate_fn = generate_fn
        self.model_id = model_id
        self.timing = timing

    def generate(self, agent_id, messages, capture_activations=True, *, context=None):
        # The callback owns any signature adaptation; one shared callback/model
        # is reused for B/C/D. Never invoke or mutate a remote active experiment.
        result = self.generate_fn(agent_id=agent_id, messages=messages,
                                  capture_activations=capture_activations,
                                  context=context or {})
        if not isinstance(result, dict) or not isinstance(result.get("text"), str):
            raise ValueError("Adapter callback must return a dict with text")
        result = dict(result)
        result.setdefault("tool_calls", [])
        result.setdefault("activation_ref", None)
        meta = dict(result.get("metadata") or {})
        activation_meta = dict(meta.get("activation_metadata") or {})
        activation_meta.setdefault("timing", self.timing)
        meta.update({"backend_kind": "adapter", "model_id": self.model_id,
                     "activation_metadata": activation_meta})
        result["metadata"] = meta
        return result


# Short alias for integration code.
IsahanBackendAdapter = CallableBackendAdapter
