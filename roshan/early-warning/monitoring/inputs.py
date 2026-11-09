"""The only view supplied to transcript monitors and trained text classifiers.

Current response/actions and all bookkeeping, activation data, hidden objectives,
condition identifiers, seeds, future outcomes and monitor scores are excluded.
"""
import json
from copy import deepcopy


def monitor_input(row):
    messages = row["visible_messages"]
    if not isinstance(messages, list):
        raise ValueError("visible_messages must be a list")
    # Only content and role are actual chat input; event annotations stay outside.
    sanitized = []
    for message in messages:
        if message.get("role") not in {"system", "user", "assistant", "tool"}:
            raise ValueError("Invalid visible message role")
        if not isinstance(message.get("content"), str):
            raise ValueError("Message content must be a string")
        sanitized.append({"role": message["role"], "content": message["content"]})
    policy = row["authorization_policy"]
    # Policy is also allowlisted so external records cannot smuggle annotations.
    policy = {key: deepcopy(policy[key]) for key in
              ("executor_id", "file_owners", "allowed_files", "rule") if key in policy}
    return {
        "legitimate_task": row["legitimate_task"],
        "authorization_policy": policy,
        "visible_messages": sanitized,
    }


def render_monitor_input(row):
    return json.dumps(monitor_input(row), ensure_ascii=False, sort_keys=True)
