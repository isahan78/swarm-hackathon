"""Local Qwen inference, with a separate context-only forward before generation.

No model is downloaded or GPU allocated until generate() is first called. The
hidden-state index follows Transformers: 0=embeddings, 1=first block output,
-1=final block output (usually post final norm). No generation-token activation
is used. One instance owns one model and serves all agents sequentially.
"""
import hashlib
import importlib.metadata
import json
import math
import time
import numpy as np
from .base import AgentBackend, activation_path

TOOLS = [{"type": "function", "function": {
    "name": "update_file", "description": "Update a simulated file subject to ownership checks.",
    "parameters": {"type": "object", "properties": {
        "agent_id": {"type": "string"}, "file_id": {"type": "string"},
        "content": {"type": "string"}},
        "required": ["agent_id", "file_id", "content"], "additionalProperties": False}}}]


def strip_private_thinking(text, *, expected=False):
    """Separate generated thinking from deployable output, failing closed.

    With thinking enabled, Qwen's template may already end with the opening
    <think> token, so generated reasoning can have only a closing </think>.
    Neither a complete nor a truncated private block may invoke tools.
    """
    visible = text
    found = False
    if expected or "</think>" in visible or "<think>" in visible:
        found = True
        if "</think>" not in visible:
            return "", True, ["unclosed_private_thinking"]
        # Everything through the first close is private. This covers both
        # template-opened and model-emitted opening tags.
        visible = visible.split("</think>", 1)[1]
        while "<think>" in visible or "</think>" in visible:
            if "<think>" not in visible or "</think>" not in visible:
                return "", True, ["unclosed_private_thinking"]
            before, rest = visible.split("<think>", 1)
            if "</think>" not in rest:
                return "", True, ["unclosed_private_thinking"]
            _, after = rest.split("</think>", 1)
            visible = before + after
    return visible.strip() if found else visible, found, []


def _reject_nonfinite_constant(value):
    raise ValueError(f"Nonfinite JSON constant: {value}")


def _validated_call(call):
    if not isinstance(call, dict) or not isinstance(call.get("name"), str) or not call["name"]:
        raise ValueError("Invalid tool call object")
    arguments = call.get("arguments", {})
    if isinstance(arguments, str):
        arguments = json.loads(arguments, parse_constant=_reject_nonfinite_constant)
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object")
    return {"name": call["name"], "arguments": arguments}


def parse_response(text):
    """Parse native tool tags or one complete JSON response envelope.

    The fallback requires the entire response to be a JSON object with exactly
    text/tool_calls fields. We never extract JSON substrings from prose or execute
    code. Malformed whole-response envelopes yield no tool calls, including when
    only one of several calls is malformed.
    """
    text, _, thinking_errors = strip_private_thinking(text)
    if thinking_errors:
        return text, [], thinking_errors
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            envelope = json.loads(stripped, parse_constant=_reject_nonfinite_constant)
        except (ValueError, TypeError):
            return text, [], ["invalid_response_json"]
        if isinstance(envelope, dict) and "tool_calls" in envelope:
            try:
                if set(envelope) != {"text", "tool_calls"}:
                    raise ValueError("Response envelope must contain only text and tool_calls")
                if not isinstance(envelope["text"], str) or not isinstance(envelope["tool_calls"], list):
                    raise ValueError("Invalid response envelope fields")
                calls = [_validated_call(call) for call in envelope["tool_calls"]]
            except (ValueError, TypeError):
                return text, [], ["invalid_response_envelope"]
            return envelope["text"], calls, []
        # Ordinary complete JSON (for example a transcript probability) is text.
        return text, [], []
    calls, errors = [], []
    remainder = text
    while "<tool_call>" in remainder:
        _, tail = remainder.split("<tool_call>", 1)
        if "</tool_call>" not in tail:
            errors.append("unterminated_tool_call")
            break
        payload, remainder = tail.split("</tool_call>", 1)
        try:
            calls.append(_validated_call(json.loads(payload.strip(), parse_constant=_reject_nonfinite_constant)))
        except (ValueError, TypeError):
            errors.append("invalid_tool_call_json")
    return text, calls, errors


def parse_tool_calls(text):
    """Compatibility helper returning calls/errors without changing text."""
    _, calls, errors = parse_response(text)
    return calls, errors


class QwenBackend(AgentBackend):
    backend_kind = "qwen"

    def __init__(self, model_id="Qwen/Qwen3-8B", revision="main", device="auto",
                 dtype="bfloat16", layer=-1, max_new_tokens=256, temperature=0.0,
                 enable_thinking=False, top_p=None, *, model=None, tokenizer=None, torch_module=None):
        if not math.isfinite(float(temperature)) or not 0 <= float(temperature):
            raise ValueError("temperature must be nonnegative")
        if int(max_new_tokens) < 1:
            raise ValueError("max_new_tokens must be positive")
        self.model_id, self.revision, self.device = model_id, revision, device
        self.dtype, self.layer = dtype, int(layer)
        self.max_new_tokens, self.temperature = int(max_new_tokens), float(temperature)
        self.enable_thinking = bool(enable_thinking)
        if top_p is not None and (not math.isfinite(float(top_p)) or not 0 < float(top_p) <= 1):
            raise ValueError("top_p must be in (0, 1]")
        self.top_p = None if top_p is None else float(top_p)
        self._model, self._tokenizer, self._torch = model, tokenizer, torch_module

    def _ensure_loaded(self):
        if self._torch is None:
            try:
                import torch
            except ImportError as exc:
                raise RuntimeError("Qwen requires torch; install requirements-qwen.txt on an authorized GPU host") from exc
            self._torch = torch
        if self._model is None or self._tokenizer is None:
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
            except ImportError as exc:
                raise RuntimeError("Qwen requires transformers; install requirements-qwen.txt") from exc
            if self.device == "auto" and not self._torch.cuda.is_available():
                raise RuntimeError("No CUDA GPU available; run on an authorized independent GPU host (or explicitly set device=cpu)")
            dtype = getattr(self._torch, self.dtype, None)
            if dtype is None:
                raise ValueError(f"Unknown torch dtype: {self.dtype}")
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_id, revision=self.revision)
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_id, revision=self.revision, torch_dtype=dtype,
                device_map=self.device if self.device == "auto" else {"": self.device},
                trust_remote_code=False)
        self._model.eval()

    def generate(self, agent_id, messages, capture_activations=True, *, context=None):
        context = context or {}
        self._ensure_loaded()
        torch, model, tokenizer = self._torch, self._model, self._tokenizer
        seed = int(context.get("seed", 0))
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        # Keep tool schema/native chat template unchanged for target inference;
        # transcript-monitor calls use plain chat and cannot invoke workspace tools.
        kwargs = {"tokenize": False, "add_generation_prompt": True,
                  "enable_thinking": self.enable_thinking}
        if context.get("purpose") != "transcript_monitor":
            kwargs["tools"] = TOOLS
        prompt = tokenizer.apply_chat_template(messages, **kwargs)
        encoded = tokenizer(prompt, return_tensors="pt")
        input_device = model.get_input_embeddings().weight.device
        encoded = {key: value.to(input_device) for key, value in encoded.items()}
        prompt_length = int(encoded["input_ids"].shape[1])
        if prompt_length == 0:
            raise ValueError("Chat template produced an empty context")
        context_limit = getattr(model.config, "max_position_embeddings", None)
        if context_limit and prompt_length + self.max_new_tokens > context_limit:
            raise ValueError("Prompt plus response exceeds context window; never silently truncate monitored history")
        activation_ref, activation_meta = None, None
        start = time.perf_counter()
        with torch.inference_mode():
            if capture_activations:
                # This forward is finished and saved BEFORE model.generate starts.
                outputs = model(**encoded, output_hidden_states=True, use_cache=False,
                                return_dict=True)
                states = outputs.hidden_states
                if not -len(states) <= self.layer < len(states):
                    raise ValueError(f"layer {self.layer} outside hidden-state tuple of length {len(states)}")
                resolved_layer = self.layer % len(states)
                vector = states[self.layer][0, -1, :].detach().float().cpu().numpy()
                if vector.ndim != 1 or not np.isfinite(vector).all() or not np.any(vector):
                    raise RuntimeError("Activation must be a finite, nonzero one-dimensional vector")
                path = activation_path(context, agent_id)
                np.save(path, vector)
                activation_ref = str(path)
                activation_meta = {
                    "timing": "pre_response_context", "layer": resolved_layer,
                    "requested_layer": self.layer,
                    "layer_convention": "Transformers hidden_states: 0 embeddings; n block n output",
                    "token_position": "last_context_token", "token_index": prompt_length - 1,
                    "token_id": int(encoded["input_ids"][0, -1].item()),
                    "shape": list(vector.shape), "synthetic": False,
                    "agent_id": agent_id, "episode_id": context.get("episode_id"),
                    "target_step": context.get("target_step")}
                del states, outputs
            gen_kwargs = {"max_new_tokens": self.max_new_tokens,
                          "do_sample": self.temperature > 0,
                          "pad_token_id": tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id}
            if self.temperature > 0:
                gen_kwargs["temperature"] = self.temperature
                if self.top_p is not None:
                    gen_kwargs["top_p"] = self.top_p
            sequence = model.generate(**encoded, **gen_kwargs)
        new_tokens = sequence[0, prompt_length:]
        text = tokenizer.decode(new_tokens, skip_special_tokens=False)
        # Preserve native <tool_call> tags while removing completion boundary tokens.
        for boundary in ("<|im_end|>", "<|endoftext|>"):
            text = text.replace(boundary, "")
        raw_generation = text
        text, private_thinking, thinking_errors = strip_private_thinking(
            text, expected=self.enable_thinking)
        private_ref = None
        if private_thinking and context.get("activation_dir"):
            folder = activation_path(context, agent_id).parent.parent / "private_generations"
            folder.mkdir(parents=True, exist_ok=True)
            private_path = folder / activation_path(context, agent_id).with_suffix(".generation.txt").name
            private_path.write_text(raw_generation, encoding="utf-8")
            private_ref = str(private_path)
        text, calls, parse_errors = parse_response(text)
        parse_errors = thinking_errors + parse_errors
        versions = {}
        for package in ("torch", "transformers", "numpy", "accelerate"):
            try:
                versions[package] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                versions[package] = "not-installed-or-injected-test-double"
        metadata = {
            "backend_kind": self.backend_kind, "model_id": self.model_id,
            "requested_revision": self.revision,
            "resolved_revision": getattr(model.config, "_commit_hash", None),
            "seed": seed, "temperature": self.temperature,
            "top_p": self.top_p if self.top_p is not None else getattr(getattr(model, "generation_config", None), "top_p", None),
            "max_new_tokens": self.max_new_tokens, "enable_thinking": self.enable_thinking,
            "dtype": self.dtype, "device": str(input_device),
            "cuda_version": getattr(getattr(torch, "version", None), "cuda", None),
            "gpu_name": torch.cuda.get_device_name() if torch.cuda.is_available() else None,
            "prompt_tokens": prompt_length, "generated_tokens": int(new_tokens.shape[0]),
            "generation_truncated": int(new_tokens.shape[0]) >= self.max_new_tokens,
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "chat_template_sha256": hashlib.sha256(str(tokenizer.chat_template).encode()).hexdigest(),
            "activation_metadata": activation_meta, "package_versions": versions,
            "elapsed_seconds": time.perf_counter() - start, "tool_parse_errors": parse_errors,
            "private_thinking_detected": private_thinking,
            "private_generation_ref": private_ref,
            "raw_generation_sha256": hashlib.sha256(raw_generation.encode()).hexdigest(),
            "gpu_peak_allocated_bytes": torch.cuda.max_memory_allocated() if torch.cuda.is_available() else None,
            "determinism_note": "Seeds fixed; cross-device/kernel bitwise determinism is not guaranteed."}
        return {"text": text, "tool_calls": calls, "activation_ref": activation_ref,
                "metadata": metadata}
