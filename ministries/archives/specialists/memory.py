"""
Memory Specialist - Archives Ministry

Responsible for storing and retrieving knowledge, decisions, and context.
"""

from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class MemoryEntry:
    """A single memory entry."""

    entry_id: str
    content: str
    context: dict
    tags: list[str]
    confidence: float
    source: str


class MemorySpecialist:
    """
    The Memory Specialist stores and retrieves knowledge.

    Capabilities:
    - Store decisions with rationale
    - Preserve context for future reference
    - Recall relevant historical information
    - Link related memories
    """

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "memory"

    def get_system_prompt(self) -> str:
        """Get the memory specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def format_for_storage(
        self,
        content: str,
        context: dict,
        tags: list[str] = None,
        source: str = None,
    ) -> dict:
        """Format content for storage in the knowledge base."""
        return {
            "content": content,
            "context": context,
            "tags": tags or [],
            "source": source or "memory_specialist",
            "metadata": {
                "specialist": self.specialist_name,
                "ministry": "archives",
            },
        }

    def format_decision_for_storage(
        self,
        decision: str,
        rationale: str,
        context: dict,
        alternatives: list[str] = None,
        evidence: list[dict] = None,
    ) -> dict:
        """Format a decision for storage."""
        return {
            "decision": decision,
            "rationale": rationale,
            "context": context,
            "alternatives_considered": alternatives or [],
            "evidence": evidence or [],
            "metadata": {
                "specialist": self.specialist_name,
                "ministry": "archives",
                "type": "decision",
            },
        }

    def build_recall_query(
        self,
        topic: str,
        include_decisions: bool = True,
        include_lessons: bool = True,
        include_context: bool = True,
    ) -> dict:
        """Build a query for recalling relevant information."""
        return {
            "topic": topic,
            "filters": {
                "include_decisions": include_decisions,
                "include_lessons": include_lessons,
                "include_context": include_context,
            },
        }


def create_specialist() -> MemorySpecialist:
    """Factory function to create the specialist."""
    return MemorySpecialist()
