"""Small inference contract; implementations share one model across agents."""
from abc import ABC, abstractmethod
from typing import Any


class AgentBackend(ABC):
    backend_kind = "unknown"
    model_id = "unknown"

    @abstractmethod
    def generate(self, agent_id: str, messages: list[dict],
                 capture_activations: bool = True, *, context: dict | None = None) -> dict:
        """Return text, tool_calls, activation_ref, metadata.

        Messages are the agent-visible chat history. Context contains inference
        bookkeeping only and MUST NOT contain eventual outcomes. Activations must
        identify their timing; an unknown timing never establishes pre-response.
        """
        raise NotImplementedError


def activation_path(context: dict, agent_id: str):
    """Construct a collision-resistant local artifact name from identifiers."""
    import hashlib
    from pathlib import Path
    folder = Path(context.get("activation_dir", "activations")).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    identity = "|".join(str(context.get(k, "")) for k in
                        ("run_id", "episode_id", "target_step")) + "|" + agent_id
    return folder / (hashlib.sha256(identity.encode()).hexdigest()[:24] + ".npy")
