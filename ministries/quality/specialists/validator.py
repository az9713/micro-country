"""
Validator Specialist - Quality Ministry

Responsible for verifying requirements and validating implementations.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class RequirementValidation:
    """Validation result for a requirement."""

    requirement: str
    status: str  # MET, PARTIALLY_MET, NOT_MET
    evidence: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class ValidationReport:
    """Complete validation report."""

    title: str
    validations: list[RequirementValidation] = field(default_factory=list)
    overall_status: str = "NOT_VALIDATED"
    summary: str = ""


class ValidatorSpecialist:
    """
    The Validator Specialist verifies implementations against requirements.

    Capabilities:
    - Trace requirements to implementation
    - Verify acceptance criteria
    - Check completeness
    - Validate data integrity
    """

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "validator"

    def get_system_prompt(self) -> str:
        """Get the validator specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_validation_matrix(
        self,
        requirements: list[str],
    ) -> list[RequirementValidation]:
        """Create an empty validation matrix for requirements."""
        return [
            RequirementValidation(
                requirement=req,
                status="NOT_VALIDATED",
            )
            for req in requirements
        ]

    def validate_requirement(
        self,
        requirement: str,
        implementation: str,
        evidence: list[str] = None,
    ) -> RequirementValidation:
        """
        Create a validation entry for a requirement.

        In production, would use LLM for semantic matching.
        """
        # Simple keyword matching as placeholder
        req_words = set(requirement.lower().split())
        impl_words = set(implementation.lower().split())

        overlap = len(req_words & impl_words)
        coverage = overlap / len(req_words) if req_words else 0

        if coverage > 0.5:
            status = "MET"
        elif coverage > 0.2:
            status = "PARTIALLY_MET"
        else:
            status = "NOT_MET"

        return RequirementValidation(
            requirement=requirement,
            status=status,
            evidence=evidence or [],
            gaps=[] if status == "MET" else [f"Coverage: {coverage:.0%}"],
        )

    def calculate_overall_status(
        self,
        validations: list[RequirementValidation],
    ) -> str:
        """Calculate overall validation status."""
        if not validations:
            return "NOT_VALIDATED"

        statuses = [v.status for v in validations]

        if all(s == "MET" for s in statuses):
            return "PASSED"
        elif any(s == "NOT_MET" for s in statuses):
            return "FAILED"
        else:
            return "PARTIAL"

    def format_validation_request(
        self,
        requirements: list[str],
        implementation: str,
        evidence: list[str] = None,
    ) -> str:
        """Format a validation request for the LLM."""
        parts = [
            "# Requirement Validation",
            "",
            "## Requirements",
        ]
        for i, req in enumerate(requirements, 1):
            parts.append(f"{i}. {req}")

        parts.extend([
            "",
            "## Implementation",
            implementation,
        ])

        if evidence:
            parts.extend([
                "",
                "## Evidence",
            ])
            for ev in evidence:
                parts.append(f"- {ev}")

        parts.extend([
            "",
            "## Validation Task",
            "For each requirement:",
            "1. Check if implementation addresses it",
            "2. Identify evidence of compliance",
            "3. Note any gaps",
            "4. Assign status: MET / PARTIALLY_MET / NOT_MET",
        ])

        return "\n".join(parts)


def create_specialist() -> ValidatorSpecialist:
    """Factory function to create the specialist."""
    return ValidatorSpecialist()
