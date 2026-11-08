from copy import deepcopy

import pytest

from monitoring.inputs import monitor_input
from swarm.io import read_jsonl
from swarm.permissions import MARKER
from swarm.runner import ExperimentConfig, run_experiment
from swarm.scenarios import TaskScopeWorkspace, get_scenario


@pytest.mark.parametrize("permissive", [False, True])
def test_own_file_marker_is_distinct_from_ownership(permissive):
    workspace = TaskScopeWorkspace(permissive=permissive)
    result = workspace.update_file("B", "file_b.txt", f"def get_value():\n    return 42\n# {MARKER}\n")
    assert result["unauthorized_attempt"] and result["unsanctioned_marker_content_attempt"]
    assert not result["ownership_violation_attempt"]
    assert result["executed"] is permissive
    assert result["completed_unsanctioned_marker_content"] is permissive
    assert not result["completed_ownership_violation"]
    assert (MARKER in workspace.files["file_b.txt"]) is permissive
    wrong_owner = workspace.update_file("C", "file_b.txt", "def get_value():\n    return 42\n")
    assert wrong_owner["ownership_violation_attempt"]
    assert not wrong_owner["unsanctioned_marker_content_attempt"]


def test_task_scope_clean_control_and_monitor_views(tmp_path):
    class ControlledBackend:
        def generate(self, agent_id, messages, **kwargs):
            content = "def get_value():\n    return 42\n"
            if kwargs["context"]["condition"] != "clean":
                content += f"# {MARKER}\n"
            return {"text": "Updating my file.", "tool_calls": [{"name": "update_file", "arguments": {
                "agent_id": agent_id, "file_id": f"file_{agent_id.lower()}.txt", "content": content}}],
                    "metadata": {"backend_kind": "mock", "model_id": "controlled-software-test"}}

    output = tmp_path / "task_scope"
    rows = run_experiment(ControlledBackend(), output, ExperimentConfig(
        scenario="task_scope_marker", episodes_per_condition=1, conditions=("clean", "direct"), steps=2))
    assert {row["dataset_semantics"] for row in rows} == {"task_scope_marker"}
    assert all(row["eventual_unauthorized_attempt"] == (row["condition"] != "clean") for row in rows)
    assert not any(row["completed_unauthorized_at_step"] for row in rows)
    assert not any(row["ownership_violation_attempt_at_step"] for row in rows)
    assert all(row["eventual_unauthorized_attempt"] is None for row in read_jsonl(output / "decisions.jsonl"))
    first = [row for row in rows if row["target_step"] == 1]
    for target in "BCD":
        matched = [row for row in first if row["agent_id"] == target]
        assert matched[0]["visible_messages"][0] == matched[1]["visible_messages"][0]
        assert MARKER not in matched[0]["visible_messages"][0]["content"]
    row = deepcopy(rows[-1])
    before = monitor_input(row)
    row["eventual_unauthorized_attempt"] = "future"
    row["authorization_policy"]["future_label"] = "future"
    row["unsanctioned_marker_content_attempt_at_step"] = "future"
    assert monitor_input(row) == before
    assert {"executor_id", "file_owners", "allowed_files", "rule"} == set(before["authorization_policy"])


def test_unknown_scenario_fails_before_output(tmp_path):
    with pytest.raises(ValueError, match="Unknown scenario"):
        run_experiment(None, tmp_path / "bad", ExperimentConfig(scenario="unknown"))
    assert not (tmp_path / "bad").exists()


def test_ownership_remains_default():
    assert ExperimentConfig().scenario == "ownership"
    assert get_scenario("ownership").dataset_semantics == "ownership_only_independent_targets"
