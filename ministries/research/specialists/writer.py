"""
Writer Specialist - Research Ministry

Responsible for clear, effective technical communication.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class Document:
    """A document being written."""

    title: str
    doc_type: str
    audience: str
    sections: list[dict] = field(default_factory=list)
    status: str = "draft"


class WriterSpecialist:
    """
    The Writer Specialist creates clear technical documentation.

    Capabilities:
    - Write various documentation types
    - Explain complex concepts simply
    - Structure information for audiences
    - Create tutorials and guides
    """

    # Document templates
    DOC_TEMPLATES = {
        "api": {
            "sections": ["Overview", "Authentication", "Endpoints", "Examples", "Errors"],
            "focus": "Reference and practical usage",
        },
        "tutorial": {
            "sections": ["Prerequisites", "Introduction", "Steps", "Verification", "Next Steps"],
            "focus": "Step-by-step learning",
        },
        "reference": {
            "sections": ["Overview", "Features", "Configuration", "API", "Troubleshooting"],
            "focus": "Comprehensive coverage",
        },
        "guide": {
            "sections": ["Introduction", "Concepts", "Best Practices", "Examples", "Summary"],
            "focus": "Understanding and application",
        },
        "adr": {
            "sections": ["Context", "Decision", "Status", "Consequences", "Alternatives"],
            "focus": "Decision documentation",
        },
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "writer"

    def get_system_prompt(self) -> str:
        """Get the writer specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_document(
        self,
        title: str,
        doc_type: str,
        audience: str,
    ) -> Document:
        """Create a new document with template structure."""
        template = self.DOC_TEMPLATES.get(doc_type, self.DOC_TEMPLATES["guide"])

        sections = [
            {"title": s, "content": ""}
            for s in template["sections"]
        ]

        return Document(
            title=title,
            doc_type=doc_type,
            audience=audience,
            sections=sections,
        )

    def get_template_for_type(self, doc_type: str) -> dict:
        """Get the template for a document type."""
        return self.DOC_TEMPLATES.get(doc_type, self.DOC_TEMPLATES["guide"])

    def adjust_for_audience(self, content: str, audience: str) -> str:
        """
        Adjust content complexity for target audience.

        This is a placeholder - real implementation would use LLM.
        """
        guidelines = {
            "beginner": "Use simple terms, avoid jargon, include analogies",
            "intermediate": "Technical terms OK, explain complex concepts",
            "expert": "Assume domain knowledge, focus on nuances",
        }
        return f"[Adjust for {audience}: {guidelines.get(audience, 'general')}]\n\n{content}"


def create_specialist() -> WriterSpecialist:
    """Factory function to create the specialist."""
    return WriterSpecialist()
