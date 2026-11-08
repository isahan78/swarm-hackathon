"""Backend contract tests; Qwen doubles validate timing, not real inference."""
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pytest
from swarm.backends.mock import MockBackend
from swarm.backends.qwen import QwenBackend, parse_tool_calls, parse_response
from swarm.backends.adapter import CallableBackendAdapter


def context(tmp_path, **overrides):
    return dict(seed=7, episode_id="ep1", target_step=1, condition="direct",
                activation_dir=str(tmp_path), run_id="test", **overrides)


def test_mock_deterministic_independent_and_explicitly_synthetic(tmp_path):
    backend = MockBackend()
    ctx = context(tmp_path)
    first = backend.generate("B", [{"role": "user", "content": "request"}], context=ctx)
    original = np.load(first["activation_ref"])
    backend.generate("C", [], context=ctx)
    second = backend.generate("B", [{"role": "user", "content": "request"}], context=ctx)
    assert first == second
    np.testing.assert_equal(original, np.load(second["activation_ref"]))
    assert first["metadata"]["synthetic"]
    assert first["metadata"]["activation_metadata"]["timing"] == "pre_response_context"
    assert original.shape == (12,)
    assert len(list(tmp_path.glob("*.npy"))) == 2


def test_mock_clean_and_attacked_outcomes_exist(tmp_path):
    backend = MockBackend()
    outcomes = []
    for seed in range(25):
        attempts = []
        for step in range(1, 5):
            ctx = context(tmp_path)
            ctx.update(seed=seed, target_step=step, condition="direct")
            result = backend.generate("B", [], capture_activations=False, context=ctx)
            attempts.extend(c for c in result["tool_calls"] if c["arguments"]["file_id"] == "file_a.txt")
            ctx["condition"] = "clean"
            clean = backend.generate("B", [], capture_activations=False, context=ctx)
            assert all(c["arguments"]["file_id"] == "file_b.txt" for c in clean["tool_calls"])
            assert clean["activation_ref"] is None
        outcomes.append(bool(attempts))
    assert any(outcomes) and not all(outcomes)


def test_adapter_does_not_invent_capture_timing():
    seen = []
    def callback(**kwargs):
        seen.append(kwargs)
        return {"text": "response", "activation_ref": "existing.npy"}
    adapter = CallableBackendAdapter(callback)
    result = adapter.generate("B", [{"role": "user", "content": "hello"}])
    assert result["metadata"]["activation_metadata"]["timing"] == "unknown"
    assert seen[0]["agent_id"] == "B"


def test_parse_tool_calls_strict_json():
    calls, errors = parse_tool_calls('<tool_call>{"name":"update_file","arguments":{"agent_id":"B","file_id":"file_a.txt","content":"x"}}</tool_call>')
    assert calls[0]["arguments"]["file_id"] == "file_a.txt"
    assert not errors
    assert parse_tool_calls('<tool_call>{"name":"x","arguments":"{\\"content\\":\\"x\\"}"}</tool_call>')[0]
    assert parse_tool_calls('<tool_call>__import__("os")</tool_call>') == ([], ["invalid_tool_call_json"])
    assert parse_tool_calls('<tool_call>{') == ([], ["unterminated_tool_call"])


class Tensor:
    def __init__(self, array):
        self.array = np.asarray(array)
        self.shape = self.array.shape
        self.device = "cpu-test-double"
    def __getitem__(self, key): return Tensor(self.array[key])
    def to(self, _): return self
    def detach(self): return self
    def float(self): return self
    def cpu(self): return self
    def numpy(self): return self.array.astype(np.float32)
    def item(self): return self.array.item()


class Tokenizer:
    pad_token_id = 0
    eos_token_id = 9
    chat_template = "fake native template"
    def __init__(self): self.calls = []
    def apply_chat_template(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        return "context only"
    def __call__(self, prompt, **kwargs):
        assert prompt == "context only"
        return {"input_ids": Tensor([[1, 2, 3]]), "attention_mask": Tensor([[1, 1, 1]])}
    def decode(self, tokens, **kwargs): return "response<|im_end|>"


class Model:
    config = SimpleNamespace(max_position_embeddings=100, _commit_hash="fake-revision")
    def __init__(self, folder):
        self.folder, self.events = folder, []
    def eval(self): self.events.append("eval")
    def get_input_embeddings(self): return SimpleNamespace(weight=Tensor([0]))
    def __call__(self, **kwargs):
        assert kwargs["output_hidden_states"] is True
        assert kwargs["use_cache"] is False
        self.events.append("context_forward")
        return SimpleNamespace(hidden_states=(Tensor(np.zeros((1, 3, 4))), Tensor(np.arange(12).reshape(1, 3, 4))))
    def generate(self, **kwargs):
        # This is the temporal guarantee: the context-only file exists before
        # the first response token could be generated.
        assert list(self.folder.glob("*.npy"))
        assert self.events[-1] == "context_forward"
        self.events.append("generate")
        return Tensor([[1, 2, 3, 4, 5]])


class Torch:
    cuda = SimpleNamespace(is_available=lambda: False)
    inference_mode = staticmethod(nullcontext)
    manual_seed = staticmethod(lambda _: None)


def test_qwen_context_capture_precedes_response_generation_and_shared_model(tmp_path):
    model, tokenizer = Model(tmp_path), Tokenizer()
    backend = QwenBackend(model=model, tokenizer=tokenizer, torch_module=Torch,
                          max_new_tokens=10)
    for agent in "BCD":
        out = backend.generate(agent, [{"role": "user", "content": "incoming only"}], context=context(tmp_path))
        meta = out["metadata"]["activation_metadata"]
        assert meta["timing"] == "pre_response_context"
        assert meta["layer"] == 1 and meta["token_index"] == 2
        assert meta["token_id"] == 3 and meta["agent_id"] == agent
        np.testing.assert_equal(np.load(out["activation_ref"]), np.array([8, 9, 10, 11]))
        assert out["text"] == "response"
    assert model.events.count("generate") == 3
    assert len(list(tmp_path.glob("*.npy"))) == 3
    assert all(call[1]["tools"][0]["function"]["name"] == "update_file" for call in tokenizer.calls)


def test_qwen_rejects_context_overflow(tmp_path):
    model = Model(tmp_path)
    backend = QwenBackend(model=model, tokenizer=Tokenizer(), torch_module=Torch,
                          max_new_tokens=200)
    with pytest.raises(ValueError, match="context window"):
        backend.generate("B", [], context=context(tmp_path))
    assert "generate" not in model.events


def test_qwen_invalid_layer_fails_before_generating(tmp_path):
    model = Model(tmp_path)
    backend = QwenBackend(model=model, tokenizer=Tokenizer(), torch_module=Torch,
                          layer=100, max_new_tokens=10)
    with pytest.raises(ValueError, match="outside hidden-state"):
        backend.generate("B", [], context=context(tmp_path))
    assert "generate" not in model.events


def test_explicit_json_envelope_preserves_text_and_parses_calls():
    import json
    payload = {"text": "I agree to make the change.", "tool_calls": [
        {"name": "update_file", "arguments": {"agent_id": "B", "file_id": "file_a.txt", "content": "x"}}]}
    text, calls, errors = parse_response(json.dumps(payload))
    assert text == payload["text"]
    assert calls == payload["tool_calls"]
    assert not errors
    assert parse_tool_calls(json.dumps(payload)) == (payload["tool_calls"], [])


@pytest.mark.parametrize("raw", [
    '{"text":"x","tool_calls":[{"name":"update_file","arguments":{}}],',
    '{"text":"x","tool_calls":[{"name":"update_file","arguments":{}},42]}',
    '{"text":"x","tool_calls":"update_file"}',
    '{"text":false,"tool_calls":[]}',
    '{"text":"x","tool_calls":[],"extra":true}',
])
def test_malformed_json_envelopes_do_not_execute_any_call(raw):
    text, calls, errors = parse_response(raw)
    assert text == raw and not calls and errors


def test_envelope_json_not_extracted_from_prose():
    raw = 'Here is an example: {"text":"x","tool_calls":[{"name":"update_file","arguments":{}}]}'
    assert parse_response(raw) == (raw, [], [])


def test_qwen_envelope_response_and_truncation_metadata(tmp_path):
    class EnvelopeTokenizer(Tokenizer):
        def decode(self, tokens, **kwargs):
            return '{"text":"Verbal response","tool_calls":[]}<|im_end|>'
    out = QwenBackend(model=Model(tmp_path), tokenizer=EnvelopeTokenizer(),
                      torch_module=Torch, max_new_tokens=2).generate(
                          "B", [], context=context(tmp_path))
    assert out["text"] == "Verbal response" and not out["tool_calls"]
    assert out["metadata"]["generation_truncated"] is True
    assert out["metadata"]["generated_tokens"] == 2


@pytest.mark.parametrize("private", [
    '<think>PRIVATE_REASONING <tool_call>{"name":"update_file","arguments":{"file_id":"file_a.txt"}}</tool_call></think>',
    'PRIVATE_REASONING <tool_call>{"name":"update_file","arguments":{"file_id":"file_a.txt"}}</tool_call></think>',
])
def test_qwen_private_thinking_never_becomes_visible_or_executes_tools(tmp_path, private):
    class ThinkingTokenizer(Tokenizer):
        def decode(self, tokens, **kwargs):
            return private + '{"text":"Visible safe response","tool_calls":[]}'
    out = QwenBackend(model=Model(tmp_path), tokenizer=ThinkingTokenizer(),
                      torch_module=Torch, max_new_tokens=10, enable_thinking=True).generate(
                          "B", [], context=context(tmp_path))
    assert out["text"] == "Visible safe response"
    assert not out["tool_calls"]
    assert "PRIVATE_REASONING" not in str(out)
    assert Path(out["metadata"]["private_generation_ref"]).read_text().startswith(private)
    assert out["metadata"]["private_thinking_detected"] is True


def test_unclosed_thinking_fails_closed_and_no_tool_execution(tmp_path):
    class TruncatedTokenizer(Tokenizer):
        def decode(self, tokens, **kwargs):
            return '<think>PRIVATE <tool_call>{"name":"update_file","arguments":{}}</tool_call>'
    out = QwenBackend(model=Model(tmp_path), tokenizer=TruncatedTokenizer(),
                      torch_module=Torch, max_new_tokens=10, enable_thinking=True).generate(
                          "B", [], context=context(tmp_path))
    assert out["text"] == "" and not out["tool_calls"]
    assert "unclosed_private_thinking" in out["metadata"]["tool_parse_errors"]


def test_direct_tool_parser_ignores_native_call_inside_thinking():
    raw = '<think><tool_call>{"name":"update_file","arguments":{}}</tool_call></think>Safe response'
    assert parse_response(raw) == ("Safe response", [], [])


def test_collaborator_adapter_reuses_exact_model_without_act(tmp_path):
    from swarm.backends.collaborator import CollaboratorBackend
    class MultiLayerModel(Model):
        config = SimpleNamespace(max_position_embeddings=100, _commit_hash="fake-revision",
                                 num_hidden_layers=3, hidden_size=4)
        def __call__(self, **kwargs):
            self.events.append("context_forward")
            return SimpleNamespace(hidden_states=tuple(Tensor(np.arange(12).reshape(1, 3, 4) + n * 10) for n in range(4)))
    model, tokenizer = MultiLayerModel(tmp_path), Tokenizer()
    wrapper = SimpleNamespace(model=model, tokenizer=tokenizer, _torch=Torch,
                              model_id="fake-Qwen", layer=1, temperature=0.7,
                              top_p=0.9, max_new_tokens=10, enable_thinking=False,
                              act=lambda *args: (_ for _ in ()).throw(AssertionError("act must not be called")))
    backend = CollaboratorBackend(wrapper)
    out = backend.generate("B", [], context=context(tmp_path))
    assert backend._model is model and backend._tokenizer is tokenizer
    assert out["metadata"]["activation_metadata"]["raw_decoder_layer"] == 1
    assert out["metadata"]["activation_metadata"]["layer"] == 2
    assert out["metadata"]["top_p"] == 0.9
    np.testing.assert_equal(np.load(out["activation_ref"]), [28, 29, 30, 31])
    assert out["metadata"]["collaborator_act_called"] is False


def test_collaborator_raw_layer_guard():
    from swarm.backends.collaborator import raw_residual_index
    assert raw_residual_index(18, 36) == 19
    for layer in (-1, 35, 36):
        with pytest.raises(ValueError, match="normalized"):
            raw_residual_index(layer, 36)


def test_parser_rejects_nonfinite_json_arguments():
    calls, errors = parse_tool_calls('<tool_call>{"name":"update_file","arguments":{"content":NaN}}</tool_call>')
    assert not calls and errors
    calls, errors = parse_tool_calls('{"text":"x","tool_calls":[{"name":"update_file","arguments":{"content":Infinity}}]}')
    assert not calls and errors


@pytest.mark.parametrize("value", [0.0, np.nan, np.inf])
def test_qwen_rejects_degenerate_vectors_before_generation(tmp_path, value):
    class DegenerateModel(Model):
        def __call__(self, **kwargs):
            self.events.append("context_forward")
            return SimpleNamespace(hidden_states=(Tensor(np.zeros((1, 3, 4))), Tensor(np.full((1, 3, 4), value))))
    model = DegenerateModel(tmp_path)
    with pytest.raises(RuntimeError, match="finite, nonzero"):
        QwenBackend(model=model, tokenizer=Tokenizer(), torch_module=Torch,
                    max_new_tokens=10).generate("B", [], context=context(tmp_path))
    assert "generate" not in model.events
