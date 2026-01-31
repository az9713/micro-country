"""
Messenger Specialist - Communications Ministry

Responsible for message composition and delivery.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class Message:
    """A message."""

    subject: str
    body: str
    to: str
    priority: str = "normal"
    action_required: bool = False


class MessengerSpecialist:
    """
    The Messenger Specialist handles message composition and delivery.

    Capabilities:
    - Compose clear messages
    - Route to appropriate recipients
    - Track delivery status
    - Manage priorities
    """

    PRIORITY_LEVELS = {
        "critical": {"escalation_time": 5, "notify_on_failure": True},
        "high": {"escalation_time": 60, "notify_on_failure": True},
        "normal": {"escalation_time": 1440, "notify_on_failure": False},
        "low": {"escalation_time": None, "notify_on_failure": False},
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "messenger"

    def get_system_prompt(self) -> str:
        """Get the messenger specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def compose_message(
        self,
        to: str,
        subject: str,
        body: str,
        priority: str = "normal",
    ) -> Message:
        """Compose a message."""
        return Message(
            subject=subject,
            body=body,
            to=to,
            priority=priority,
        )

    def format_for_delivery(self, message: Message) -> str:
        """Format a message for delivery."""
        return f"""
TO: {message.to}
PRIORITY: {message.priority.upper()}
SUBJECT: {message.subject}

{message.body}

---
Action Required: {'Yes' if message.action_required else 'No'}
"""


def create_specialist() -> MessengerSpecialist:
    """Factory function to create the specialist."""
    return MessengerSpecialist()
