"""Append-only message board with recipient-specific delivery."""
from copy import deepcopy


class MessageBoard:
    def __init__(self):
        self.events = []

    def post(self, *, episode_id, sender, recipient, content, target_step, kind):
        event = {
            "episode_id": episode_id, "message_order": len(self.events) + 1,
            "sender": sender, "recipient": recipient, "content": content,
            "target_step": target_step, "kind": kind,
        }
        self.events.append(event)
        return deepcopy(event)

    def for_target(self, target):
        return deepcopy([event for event in self.events if event["recipient"] == target])
