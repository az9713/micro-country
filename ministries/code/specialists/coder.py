"""
Coder Specialist - Code Ministry

Responsible for writing clean, tested, maintainable code.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class CodeOutput:
    """Output from the coder specialist."""

    code: str
    language: str
    file_path: Optional[str] = None
    description: str = ""
    tests: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


class CoderSpecialist:
    """
    The Coder Specialist writes high-quality code.

    Capabilities:
    - Implement features from specifications
    - Write clean, readable code
    - Refactor existing code
    - Add tests alongside code
    - Follow coding conventions
    """

    # Supported languages and their conventions
    LANGUAGES = {
        "python": {
            "indent": 4,
            "naming": "snake_case",
            "docstring": '"""',
        },
        "javascript": {
            "indent": 2,
            "naming": "camelCase",
            "docstring": "/**",
        },
        "typescript": {
            "indent": 2,
            "naming": "camelCase",
            "docstring": "/**",
        },
        "go": {
            "indent": "\t",
            "naming": "camelCase",
            "docstring": "//",
        },
        "rust": {
            "indent": 4,
            "naming": "snake_case",
            "docstring": "///",
        },
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "coder"

    def get_system_prompt(self) -> str:
        """Get the coder specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def format_implementation_request(
        self,
        feature: str,
        language: str,
        design: str = None,
        existing_code: str = None,
    ) -> str:
        """Format an implementation request for the LLM."""
        parts = [
            f"# Implementation Request: {feature}",
            "",
            f"## Language: {language}",
        ]

        conventions = self.LANGUAGES.get(language, self.LANGUAGES["python"])
        parts.extend([
            "",
            "## Conventions",
            f"- Indent: {conventions['indent']} spaces" if isinstance(conventions['indent'], int) else f"- Indent: tabs",
            f"- Naming: {conventions['naming']}",
        ])

        if design:
            parts.extend([
                "",
                "## Design/Specification",
                design,
            ])

        if existing_code:
            parts.extend([
                "",
                "## Existing Code to Integrate With",
                "```",
                existing_code,
                "```",
            ])

        parts.extend([
            "",
            "## Requirements",
            "- Write clean, readable code",
            "- Include error handling",
            "- Add comments for complex logic only",
            "- Follow the conventions above",
            "- Include basic test cases",
        ])

        return "\n".join(parts)

    def format_refactor_request(
        self,
        code: str,
        goals: list[str],
        constraints: list[str] = None,
    ) -> str:
        """Format a refactoring request."""
        parts = [
            "# Refactoring Request",
            "",
            "## Original Code",
            "```",
            code,
            "```",
            "",
            "## Goals",
        ]
        for goal in goals:
            parts.append(f"- {goal}")

        if constraints:
            parts.extend([
                "",
                "## Constraints (must preserve)",
            ])
            for con in constraints:
                parts.append(f"- {con}")

        parts.extend([
            "",
            "## Output Expected",
            "1. Refactored code",
            "2. List of changes made",
            "3. Explanation of improvements",
        ])

        return "\n".join(parts)

    def validate_code_quality(self, code: str, language: str) -> dict:
        """
        Basic code quality validation.

        Returns dict with validation results.
        """
        results = {
            "has_code": bool(code.strip()),
            "line_count": len(code.split("\n")),
            "has_comments": False,
            "has_error_handling": False,
            "issues": [],
        }

        # Check for comments
        comment_markers = ["#", "//", "/*", '"""', "'''"]
        results["has_comments"] = any(m in code for m in comment_markers)

        # Check for error handling
        error_patterns = ["try:", "try {", "catch", "except", "Error", "panic"]
        results["has_error_handling"] = any(p in code for p in error_patterns)

        # Basic issues detection
        if results["line_count"] > 200:
            results["issues"].append("Function/file may be too long")

        if not results["has_error_handling"] and results["line_count"] > 20:
            results["issues"].append("Consider adding error handling")

        return results


def create_specialist() -> CoderSpecialist:
    """Factory function to create the specialist."""
    return CoderSpecialist()
