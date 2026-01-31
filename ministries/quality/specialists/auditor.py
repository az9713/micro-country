"""
Auditor Specialist - Quality Ministry

Responsible for security auditing and code quality review.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class SecurityFinding:
    """A security finding from an audit."""

    severity: str  # critical, high, medium, low
    category: str  # owasp category
    title: str
    description: str
    location: str
    remediation: str
    cwe_id: Optional[str] = None


@dataclass
class AuditReport:
    """A complete audit report."""

    scope: str
    findings: list[SecurityFinding] = field(default_factory=list)
    summary: str = ""
    risk_rating: str = "low"


class AuditorSpecialist:
    """
    The Auditor Specialist performs security and quality audits.

    Capabilities:
    - Identify security vulnerabilities
    - Check for OWASP Top 10 issues
    - Review code for quality issues
    - Assess risk levels
    """

    # OWASP Top 10 2021
    OWASP_TOP_10 = {
        "A01": "Broken Access Control",
        "A02": "Cryptographic Failures",
        "A03": "Injection",
        "A04": "Insecure Design",
        "A05": "Security Misconfiguration",
        "A06": "Vulnerable Components",
        "A07": "Auth Failures",
        "A08": "Data Integrity Failures",
        "A09": "Logging Failures",
        "A10": "SSRF",
    }

    # Common vulnerability patterns
    VULNERABILITY_PATTERNS = {
        "sql_injection": ["execute(", "query(", "SELECT", "INSERT", "UPDATE", "DELETE"],
        "xss": ["innerHTML", "document.write", "eval(", ".html("],
        "command_injection": ["exec(", "system(", "popen(", "subprocess.run(", "shell=True"],
        "path_traversal": ["../", "..\\", "open(", "file("],
        "hardcoded_secrets": ["password=", "api_key=", "secret=", "token="],
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "auditor"

    def get_system_prompt(self) -> str:
        """Get the auditor specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def quick_scan(self, code: str) -> list[dict]:
        """
        Quick scan for common vulnerability patterns.

        This is a simple pattern match - LLM analysis is more thorough.
        """
        findings = []

        code_lower = code.lower()

        for vuln_type, patterns in self.VULNERABILITY_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in code_lower:
                    findings.append({
                        "type": vuln_type,
                        "pattern": pattern,
                        "severity": "needs_review",
                        "note": f"Pattern '{pattern}' found - requires manual review",
                    })

        return findings

    def create_finding(
        self,
        severity: str,
        category: str,
        title: str,
        description: str,
        location: str,
        remediation: str,
    ) -> SecurityFinding:
        """Create a security finding."""
        return SecurityFinding(
            severity=severity,
            category=category,
            title=title,
            description=description,
            location=location,
            remediation=remediation,
        )

    def calculate_risk_rating(self, findings: list[SecurityFinding]) -> str:
        """Calculate overall risk rating from findings."""
        if not findings:
            return "low"

        severity_weights = {
            "critical": 10,
            "high": 5,
            "medium": 2,
            "low": 1,
        }

        total_weight = sum(
            severity_weights.get(f.severity, 0) for f in findings
        )

        if total_weight >= 15:
            return "critical"
        elif total_weight >= 8:
            return "high"
        elif total_weight >= 3:
            return "medium"
        else:
            return "low"

    def format_audit_request(
        self,
        code: str,
        context: str = None,
        focus_areas: list[str] = None,
    ) -> str:
        """Format an audit request for the LLM."""
        parts = [
            "# Security Audit Request",
            "",
            "## Code to Audit",
            "```",
            code,
            "```",
        ]

        if context:
            parts.extend([
                "",
                "## Context",
                context,
            ])

        if focus_areas:
            parts.extend([
                "",
                "## Focus Areas",
            ])
            for area in focus_areas:
                parts.append(f"- {area}")

        parts.extend([
            "",
            "## Check For",
        ])
        for code, name in self.OWASP_TOP_10.items():
            parts.append(f"- {code}: {name}")

        return "\n".join(parts)


def create_specialist() -> AuditorSpecialist:
    """Factory function to create the specialist."""
    return AuditorSpecialist()
