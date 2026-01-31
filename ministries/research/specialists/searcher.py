"""
Searcher Specialist - Research Ministry

Responsible for finding and evaluating information.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class SearchResult:
    """A search result."""

    title: str
    source: str
    url: Optional[str] = None
    snippet: str = ""
    relevance: float = 0.8
    credibility: float = 0.8
    recency: Optional[str] = None


@dataclass
class SourceEvaluation:
    """Evaluation of a source."""

    source: str
    currency: str  # How recent
    relevance: str  # How relevant
    authority: str  # How credible
    accuracy: str  # How accurate
    purpose: str  # Why was it written
    overall_score: float = 0.8


class SearcherSpecialist:
    """
    The Searcher Specialist finds and evaluates information.

    Capabilities:
    - Formulate effective search queries
    - Evaluate source credibility
    - Find authoritative sources
    - Track information provenance
    """

    # Source credibility rankings
    SOURCE_TIERS = {
        "tier1": ["official docs", "academic papers", "rfc", "specs"],
        "tier2": ["reputable tech blogs", "conference talks", "books"],
        "tier3": ["stackoverflow", "github issues", "tutorials"],
        "tier4": ["forums", "reddit", "blog posts"],
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "searcher"

    def get_system_prompt(self) -> str:
        """Get the searcher specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def formulate_query(
        self,
        topic: str,
        context: str = None,
    ) -> list[str]:
        """Formulate search queries for a topic."""
        queries = [topic]

        # Add variations
        queries.append(f"{topic} best practices")
        queries.append(f"{topic} tutorial")
        queries.append(f"{topic} documentation")

        if context:
            queries.append(f"{topic} {context}")

        return queries

    def evaluate_source(
        self,
        source: str,
        url: str = None,
    ) -> SourceEvaluation:
        """
        Evaluate a source's credibility.

        This is a simple heuristic - real implementation would be more sophisticated.
        """
        tier = "tier4"  # Default
        for t, sources in self.SOURCE_TIERS.items():
            if any(s in source.lower() for s in sources):
                tier = t
                break

        tier_scores = {"tier1": 0.95, "tier2": 0.8, "tier3": 0.6, "tier4": 0.4}

        return SourceEvaluation(
            source=source,
            currency="Unknown",
            relevance="Needs evaluation",
            authority=tier,
            accuracy="Needs verification",
            purpose="Unknown",
            overall_score=tier_scores.get(tier, 0.5),
        )

    def prioritize_sources(
        self,
        sources: list[str],
    ) -> list[str]:
        """Prioritize sources by credibility."""
        evaluated = [(s, self.evaluate_source(s).overall_score) for s in sources]
        evaluated.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in evaluated]


def create_specialist() -> SearcherSpecialist:
    """Factory function to create the specialist."""
    return SearcherSpecialist()
