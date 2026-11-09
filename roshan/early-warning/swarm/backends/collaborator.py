"""Reuse an already loaded Isahan HFModel's weights in the independent harness.

This intentionally does NOT call HFModel.act(): act rebuilds a different state
snapshot prompt and parses a different action protocol. Reusing its model and
native tokenizer avoids a second 8B model copy while maintaining this harness's
actual visible history. See report/collaborator_integration.md.
"""
import hashlib
import inspect
from pathlib import Path
import numpy as np
from .qwen import QwenBackend


def raw_residual_index(decoder_layer, num_decoder_layers):
    """Match reference model.residual_index, rejecting final post-RMSNorm."""
    layer = int(decoder_layer)
    if layer < 0 or layer + 1 >= int(num_decoder_layers):
        raise ValueError("Raw decoder layer maps to final normalized entry or lies outside model")
    return layer + 1


class CollaboratorBackend(QwenBackend):
    """Accept one HFModel object constructed in a separate authorized process.

    No collaborator code is imported here and no global import paths are changed.
    Native tokenizer/template and inference parameters are inherited. The new
    harness's tasks/tool protocol remain a separate experiment and require a new
    probe fit or explicit transfer evaluation; old probe weights are not reused.
    """
    def __init__(self, wrapper):
        for name in ("model", "tokenizer", "_torch", "layer", "model_id"):
            if not hasattr(wrapper, name):
                raise TypeError(f"HFModel wrapper missing {name}")
        config = wrapper.model.config
        if not hasattr(config, "num_hidden_layers"):
            raise ValueError("Need model.config.num_hidden_layers to verify raw residual index")
        self.raw_decoder_layer = int(wrapper.layer)
        index = raw_residual_index(self.raw_decoder_layer, config.num_hidden_layers)
        self.wrapper = wrapper
        self.reference_model_sha256 = None
        try:
            source = Path(inspect.getfile(type(wrapper)))
            if source.is_file():
                self.reference_model_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
        except (TypeError, OSError):
            pass
        super().__init__(model_id=wrapper.model_id, revision="inherited-wrapper",
                         device=str(getattr(wrapper.model, "device", "inherited")),
                         dtype="bfloat16", layer=index,
                         max_new_tokens=getattr(wrapper, "max_new_tokens", 1536),
                         temperature=getattr(wrapper, "temperature", 0.7),
                         top_p=getattr(wrapper, "top_p", 0.9),
                         enable_thinking=getattr(wrapper, "enable_thinking", True),
                         model=wrapper.model, tokenizer=wrapper.tokenizer,
                         torch_module=wrapper._torch)

    def generate(self, agent_id, messages, capture_activations=True, *, context=None):
        result = super().generate(agent_id, messages, capture_activations, context=context)
        if capture_activations:
            vector = np.load(result["activation_ref"], allow_pickle=False)
            hidden_size = getattr(self.wrapper.model.config, "hidden_size", None)
            if vector.ndim != 1 or (hidden_size is not None and vector.shape != (hidden_size,)):
                raise RuntimeError("Collaborator activation shape does not match hidden_size")
            if not np.isfinite(vector).all() or not np.any(vector):
                raise RuntimeError("Collaborator activation is nonfinite or all zero")
            result["metadata"]["activation_metadata"].update({
                "raw_decoder_layer": self.raw_decoder_layer,
                "layer_convention": "Raw residual after zero-based decoder L at hidden_states[L+1]; final normalized entry forbidden"})
        result["metadata"].update({
            "weight_source": "already_loaded_collaborator_HFModel",
            "reference_model_sha256": self.reference_model_sha256,
            "protocol_compatibility": "new_multi_target_update_file_protocol_not_original_act_snapshot",
            "collaborator_act_called": False,
            "reference_retry_behavior": "not_reused: one generation per decision; parse failures logged"})
        return result
