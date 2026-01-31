"""
Analyst Specialist - Research Ministry

Responsible for deep analysis, pattern recognition, and insight generation.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class AnalysisResult:
    """Result of an analysis."""

    topic: str
    key_findings: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    confidence: float = 0.8


class AnalystSpecialist:
    """
    The Analyst Specialist performs deep analysis and generates insights.

    Capabilities:
    - Analyze documents and data
    - Identify patterns and trends
    - Generate insights
    - Compare options objectively
    """

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "analyst"

    def get_system_prompt(self) -> str:
        """Get the analyst specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_analysis_framework(self, topic: str) -> dict:
        """Create a framework for structured analysis."""
        return {
            "topic": topic,
            "framework": {
                "context": "What is the situation?",
                "data": "What evidence do we have?",
                "patterns": "What patterns emerge?",
                "implications": "What does this mean?",
                "recommendations": "What should we do?",
            },
        }

    def format_comparison_matrix(
        self,
        options: list[dict],
        criteria: list[str],
    ) -> str:
        """Format a comparison matrix for display."""
        if not options or not criteria:
            return "No options or criteria provided"

        # Header
        header = "| Criteria | " + " | ".join(o.get("name", "?") for o in options) + " |"
        separator = "|" + "---|" * (len(options) + 1)

        rows = [header, separator]
        for criterion in criteria:
            row = f"| {criterion} | " + " | ".join("?" for _ in options) + " |"
            rows.append(row)

        return "\n".join(rows)


def create_specialist() -> AnalystSpecialist:
    """Factory function to create the specialist."""
    return AnalystSpecialist()
