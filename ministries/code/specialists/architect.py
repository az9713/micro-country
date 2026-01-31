"""
Architect Specialist - Code Ministry

Responsible for system design, architecture decisions, and technical vision.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class DesignDocument:
    """A design document produced by the architect."""

    feature: str
    overview: str
    components: list[dict] = field(default_factory=list)
    data_flow: list[dict] = field(default_factory=list)
    api_design: Optional[dict] = None
    trade_offs: list[dict] = field(default_factory=list)
    decision: str = ""
    rationale: str = ""


@dataclass
class TradeOff:
    """A trade-off consideration."""

    option_a: str
    option_b: str
    criteria: str
    chosen: str
    rationale: str


class ArchitectSpecialist:
    """
    The Architect Specialist designs systems and makes architectural decisions.

    Capabilities:
    - Design system architecture
    - Analyze trade-offs
    - Define APIs and data models
    - Review and critique designs
    - Document architectural decisions
    """

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "architect"

    def get_system_prompt(self) -> str:
        """Get the architect specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_design_template(self, feature: str, requirements: list[str]) -> DesignDocument:
        """Create an empty design document template."""
        return DesignDocument(
            feature=feature,
            overview=f"Architecture design for {feature}",
            components=[],
            data_flow=[],
            trade_offs=[],
        )

    def format_design_request(
        self,
        feature: str,
        requirements: list[str],
        constraints: list[str] = None,
        context: str = None,
    ) -> str:
        """Format a design request for the LLM."""
        parts = [
            f"# Design Request: {feature}",
            "",
            "## Requirements",
        ]
        for req in requirements:
            parts.append(f"- {req}")

        if constraints:
            parts.append("")
            parts.append("## Constraints")
            for con in constraints:
                parts.append(f"- {con}")

        if context:
            parts.append("")
            parts.append("## Context")
            parts.append(context)

        parts.extend([
            "",
            "## Expected Output",
            "1. Architecture overview",
            "2. Component breakdown",
            "3. Data flow diagram (text)",
            "4. API design (if applicable)",
            "5. At least 2 trade-offs considered",
            "6. Final recommendation with rationale",
        ])

        return "\n".join(parts)

    def analyze_trade_off(
        self,
        option_a: str,
        option_b: str,
        criteria: list[str],
    ) -> dict:
        """Create a trade-off analysis structure."""
        return {
            "options": [option_a, option_b],
            "criteria": criteria,
            "analysis": {criterion: {"option_a": "", "option_b": ""} for criterion in criteria},
            "recommendation": "",
            "rationale": "",
        }


def create_specialist() -> ArchitectSpecialist:
    """Factory function to create the specialist."""
    return ArchitectSpecialist()
