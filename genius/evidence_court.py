"""
Evidence Court - Conflict Resolution for the Micro-Country

When geniuses disagree, evidence decides.

Evidence Strength (ranked):
1. Empirical - Benchmarks, tests, data (strongest)
2. Precedent - What worked before
3. Consensus - Multiple specialists agree
4. Theoretical - Logical arguments
5. Intuition - Gut feeling (weakest)
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional
import json


class EvidenceType(IntEnum):
    """Evidence types ranked by strength (lower = stronger)."""

    EMPIRICAL = 1  # Benchmarks, tests, measurable data
    PRECEDENT = 2  # What worked before in similar situations
    CONSENSUS = 3  # Multiple specialists agree
    THEORETICAL = 4  # Logical arguments and reasoning
    INTUITION = 5  # Gut feeling, heuristics


@dataclass
class Evidence:
    """A piece of evidence supporting a position."""

    evidence_type: EvidenceType
    description: str
    source: str  # Where this evidence comes from
    data: Optional[dict] = None  # Actual data if applicable
    confidence: float = 0.8  # 0.0 to 1.0

    def strength_score(self) -> float:
        """
        Calculate overall strength score.

        Combines type ranking with confidence.
        """
        # Type contributes 60%, confidence 40%
        type_score = (6 - self.evidence_type) / 5  # 1.0 for EMPIRICAL, 0.2 for INTUITION
        return (type_score * 0.6) + (self.confidence * 0.4)

    def to_dict(self) -> dict:
        return {
            "type": self.evidence_type.name,
            "description": self.description,
            "source": self.source,
            "data": self.data,
            "confidence": self.confidence,
            "strength_score": self.strength_score(),
        }


@dataclass
class Position:
    """A position in a court case."""

    advocate: str  # Who is advocating (ministry/specialist)
    position: str  # The actual position/claim
    arguments: list[str]  # Supporting arguments
    evidence: list[Evidence] = field(default_factory=list)

    def total_evidence_strength(self) -> float:
        """Calculate total evidence strength for this position."""
        if not self.evidence:
            return 0.0
        return sum(e.strength_score() for e in self.evidence) / len(self.evidence)

    def to_dict(self) -> dict:
        return {
            "advocate": self.advocate,
            "position": self.position,
            "arguments": self.arguments,
            "evidence": [e.to_dict() for e in self.evidence],
            "total_strength": self.total_evidence_strength(),
        }


@dataclass
class CourtRuling:
    """The result of an Evidence Court case."""

    case_id: str
    topic: str
    ruling: str
    rationale: str
    winning_position: Position
    losing_positions: list[Position]
    evidence_analysis: dict
    precedent_set: Optional[str] = None
    dissenting_opinions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "topic": self.topic,
            "ruling": self.ruling,
            "rationale": self.rationale,
            "winning_position": self.winning_position.to_dict(),
            "losing_positions": [p.to_dict() for p in self.losing_positions],
            "evidence_analysis": self.evidence_analysis,
            "precedent_set": self.precedent_set,
            "dissenting_opinions": self.dissenting_opinions,
        }


class EvidenceCourt:
    """
    The Evidence Court resolves conflicts between geniuses.

    Process:
    1. Advocates present positions with evidence
    2. Judge (Archives Ministry) evaluates evidence strength
    3. Strongest evidence wins
    4. Decision recorded with full rationale
    """

    def __init__(self):
        self._case_counter = 0

    def create_case_prompt(self, topic: str, positions: list[Position]) -> str:
        """
        Create a prompt for the judge (Archives Ministry) to evaluate.

        The judge must:
        1. Analyze each position's evidence
        2. Rank evidence by type and quality
        3. Determine which position has strongest support
        4. Write a ruling with full rationale
        """
        positions_text = self._format_positions(positions)

        return f"""## EVIDENCE COURT CASE

### Topic Under Dispute
{topic}

### Positions Presented

{positions_text}

### Evidence Strength Hierarchy
1. **EMPIRICAL** (strongest) - Benchmarks, tests, measurable data
2. **PRECEDENT** - What worked before in similar situations
3. **CONSENSUS** - Multiple specialists agree
4. **THEORETICAL** - Logical arguments and reasoning
5. **INTUITION** (weakest) - Gut feeling, heuristics

### Your Task as Judge

1. **Analyze Evidence**: For each position, evaluate the quality and type of evidence
2. **Rank Positions**: Determine which has the strongest evidential support
3. **Issue Ruling**: State which position prevails and why
4. **Set Precedent**: What principle does this establish for future cases?

### Your Ruling

Format your response as:

#### Evidence Analysis
[Analyze each piece of evidence]

#### Ruling
[State which position wins]

#### Rationale
[Explain why, citing the evidence hierarchy]

#### Precedent Set
[What principle this establishes]

#### Dissenting Considerations
[Any valid points from losing positions worth noting]
"""

    def _format_positions(self, positions: list[Position]) -> str:
        """Format positions for the court prompt."""
        parts = []
        for i, pos in enumerate(positions, 1):
            evidence_text = "\n".join(
                f"  - [{e.evidence_type.name}] {e.description} (confidence: {e.confidence})"
                for e in pos.evidence
            ) or "  - No formal evidence presented"

            parts.append(f"""#### Position {i}: {pos.advocate}

**Claim**: {pos.position}

**Arguments**:
{chr(10).join(f'- {arg}' for arg in pos.arguments)}

**Evidence**:
{evidence_text}
""")
        return "\n".join(parts)

    def evaluate_positions(self, positions: list[Position]) -> dict:
        """
        Evaluate positions based on evidence strength.

        Returns analysis of each position's evidential support.
        """
        analysis = {}

        for pos in positions:
            evidence_by_type = {}
            for e in pos.evidence:
                type_name = e.evidence_type.name
                if type_name not in evidence_by_type:
                    evidence_by_type[type_name] = []
                evidence_by_type[type_name].append({
                    "description": e.description,
                    "source": e.source,
                    "confidence": e.confidence,
                    "strength": e.strength_score(),
                })

            analysis[pos.advocate] = {
                "position": pos.position,
                "evidence_count": len(pos.evidence),
                "evidence_by_type": evidence_by_type,
                "total_strength": pos.total_evidence_strength(),
                "strongest_evidence_type": (
                    min((e.evidence_type for e in pos.evidence), default=EvidenceType.INTUITION).name
                    if pos.evidence else "NONE"
                ),
            }

        return analysis

    def determine_winner(self, positions: list[Position]) -> tuple[Position, list[Position]]:
        """
        Determine winning position based on evidence.

        Returns (winner, losers)
        """
        if not positions:
            raise ValueError("No positions to evaluate")

        # Sort by total evidence strength (descending)
        sorted_positions = sorted(
            positions,
            key=lambda p: p.total_evidence_strength(),
            reverse=True,
        )

        winner = sorted_positions[0]
        losers = sorted_positions[1:]

        return winner, losers

    def parse_ruling_response(
        self,
        response: str,
        topic: str,
        positions: list[Position],
    ) -> CourtRuling:
        """Parse the judge's response into a CourtRuling."""
        self._case_counter += 1
        case_id = f"case_{self._case_counter:04d}"

        # Extract sections from response
        ruling = self._extract_section(response, "Ruling", "Rationale")
        rationale = self._extract_section(response, "Rationale", "Precedent")
        precedent = self._extract_section(response, "Precedent", "Dissenting")
        dissenting = self._extract_section(response, "Dissenting", None)

        # Determine winner based on evidence (backup if not clear from ruling)
        winner, losers = self.determine_winner(positions)

        # Try to match ruling text to a position
        for pos in positions:
            if pos.advocate.lower() in ruling.lower():
                winner = pos
                losers = [p for p in positions if p != pos]
                break

        return CourtRuling(
            case_id=case_id,
            topic=topic,
            ruling=ruling.strip(),
            rationale=rationale.strip(),
            winning_position=winner,
            losing_positions=losers,
            evidence_analysis=self.evaluate_positions(positions),
            precedent_set=precedent.strip() if precedent else None,
            dissenting_opinions=[d.strip() for d in dissenting.split("\n") if d.strip()]
            if dissenting else [],
        )

    def _extract_section(
        self, text: str, start_marker: str, end_marker: Optional[str]
    ) -> str:
        """Extract a section from the response text."""
        text_lower = text.lower()
        start_markers = [
            f"#### {start_marker.lower()}",
            f"### {start_marker.lower()}",
            f"**{start_marker.lower()}**",
            f"{start_marker.lower()}:",
        ]

        start_idx = -1
        for marker in start_markers:
            idx = text_lower.find(marker)
            if idx != -1:
                start_idx = idx + len(marker)
                break

        if start_idx == -1:
            return ""

        if end_marker:
            end_markers = [
                f"#### {end_marker.lower()}",
                f"### {end_marker.lower()}",
                f"**{end_marker.lower()}**",
                f"{end_marker.lower()}:",
            ]
            end_idx = len(text)
            for marker in end_markers:
                idx = text_lower.find(marker, start_idx)
                if idx != -1 and idx < end_idx:
                    end_idx = idx
            return text[start_idx:end_idx]
        else:
            return text[start_idx:]

    def create_evidence(
        self,
        evidence_type: str | EvidenceType,
        description: str,
        source: str,
        data: dict = None,
        confidence: float = 0.8,
    ) -> Evidence:
        """Helper to create evidence with string type."""
        if isinstance(evidence_type, str):
            evidence_type = EvidenceType[evidence_type.upper()]
        return Evidence(
            evidence_type=evidence_type,
            description=description,
            source=source,
            data=data,
            confidence=confidence,
        )

    def create_position(
        self,
        advocate: str,
        position: str,
        arguments: list[str],
        evidence: list[Evidence] = None,
    ) -> Position:
        """Helper to create a position."""
        return Position(
            advocate=advocate,
            position=position,
            arguments=arguments,
            evidence=evidence or [],
        )


# Convenience functions for common evidence types
def empirical_evidence(description: str, source: str, data: dict = None, confidence: float = 0.9) -> Evidence:
    """Create empirical evidence (benchmarks, tests, data)."""
    return Evidence(EvidenceType.EMPIRICAL, description, source, data, confidence)


def precedent_evidence(description: str, source: str, confidence: float = 0.8) -> Evidence:
    """Create precedent evidence (what worked before)."""
    return Evidence(EvidenceType.PRECEDENT, description, source, None, confidence)


def consensus_evidence(description: str, source: str, confidence: float = 0.75) -> Evidence:
    """Create consensus evidence (multiple specialists agree)."""
    return Evidence(EvidenceType.CONSENSUS, description, source, None, confidence)


def theoretical_evidence(description: str, source: str, confidence: float = 0.7) -> Evidence:
    """Create theoretical evidence (logical arguments)."""
    return Evidence(EvidenceType.THEORETICAL, description, source, None, confidence)


def intuition_evidence(description: str, source: str, confidence: float = 0.5) -> Evidence:
    """Create intuition evidence (gut feeling)."""
    return Evidence(EvidenceType.INTUITION, description, source, None, confidence)
