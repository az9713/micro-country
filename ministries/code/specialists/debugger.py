"""
Debugger Specialist - Code Ministry

Responsible for investigating, diagnosing, and fixing bugs.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class BugReport:
    """A structured bug report."""

    description: str
    error_message: Optional[str] = None
    expected_behavior: Optional[str] = None
    actual_behavior: Optional[str] = None
    reproduction_steps: list[str] = field(default_factory=list)
    code_context: Optional[str] = None
    environment: dict = field(default_factory=dict)


@dataclass
class DebugAnalysis:
    """Analysis of a bug."""

    hypotheses: list[dict] = field(default_factory=list)
    diagnostic_steps: list[str] = field(default_factory=list)
    root_cause: Optional[str] = None
    confidence: float = 0.0
    recommended_fix: Optional[str] = None


class DebuggerSpecialist:
    """
    The Debugger Specialist investigates and fixes bugs.

    Capabilities:
    - Analyze error messages and stack traces
    - Form hypotheses about root causes
    - Design diagnostic steps
    - Propose fixes with verification
    - Document findings for future reference
    """

    # Common error patterns and likely causes
    ERROR_PATTERNS = {
        "TypeError": ["wrong type passed", "null/undefined access", "missing import"],
        "ValueError": ["invalid input", "out of range", "wrong format"],
        "KeyError": ["missing key", "typo in key name", "uninitialized dict"],
        "IndexError": ["off-by-one", "empty collection", "wrong loop bounds"],
        "AttributeError": ["typo in attribute", "wrong object type", "uninitialized"],
        "ImportError": ["missing package", "wrong path", "circular import"],
        "ConnectionError": ["network issue", "wrong URL", "timeout"],
        "PermissionError": ["file permissions", "admin required", "path issue"],
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "debugger"

    def get_system_prompt(self) -> str:
        """Get the debugger specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def parse_error_type(self, error_message: str) -> list[str]:
        """Extract likely causes from error message."""
        causes = []
        for error_type, likely_causes in self.ERROR_PATTERNS.items():
            if error_type in error_message:
                causes.extend(likely_causes)
        return causes if causes else ["Unknown error type - needs investigation"]

    def format_debug_request(self, bug: BugReport) -> str:
        """Format a debugging request for the LLM."""
        parts = [
            "# Bug Investigation",
            "",
            f"## Description: {bug.description}",
        ]

        if bug.error_message:
            parts.extend([
                "",
                "## Error Message",
                "```",
                bug.error_message,
                "```",
            ])

        if bug.expected_behavior:
            parts.extend([
                "",
                f"## Expected Behavior: {bug.expected_behavior}",
            ])

        if bug.actual_behavior:
            parts.extend([
                "",
                f"## Actual Behavior: {bug.actual_behavior}",
            ])

        if bug.reproduction_steps:
            parts.extend([
                "",
                "## Reproduction Steps",
            ])
            for i, step in enumerate(bug.reproduction_steps, 1):
                parts.append(f"{i}. {step}")

        if bug.code_context:
            parts.extend([
                "",
                "## Code Context",
                "```",
                bug.code_context,
                "```",
            ])

        parts.extend([
            "",
            "## Debugging Protocol",
            "1. Form hypotheses about root cause",
            "2. Design steps to test each hypothesis",
            "3. Identify the most likely cause",
            "4. Propose a fix",
            "5. Explain how to verify the fix",
        ])

        return "\n".join(parts)

    def create_hypothesis(
        self,
        description: str,
        likelihood: str,
        test: str,
    ) -> dict:
        """Create a hypothesis structure."""
        return {
            "description": description,
            "likelihood": likelihood,  # "high", "medium", "low"
            "test": test,
            "verified": False,
            "result": None,
        }

    def format_fix_proposal(
        self,
        root_cause: str,
        fix_code: str,
        verification_steps: list[str],
    ) -> str:
        """Format a fix proposal."""
        parts = [
            "# Bug Fix Proposal",
            "",
            f"## Root Cause: {root_cause}",
            "",
            "## Fix",
            "```",
            fix_code,
            "```",
            "",
            "## Verification",
        ]
        for i, step in enumerate(verification_steps, 1):
            parts.append(f"{i}. {step}")

        return "\n".join(parts)


def create_specialist() -> DebuggerSpecialist:
    """Factory function to create the specialist."""
    return DebuggerSpecialist()
