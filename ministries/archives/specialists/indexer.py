"""
Indexer Specialist - Archives Ministry

Responsible for organizing, categorizing, and making knowledge searchable.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class IndexEntry:
    """An entry in the knowledge index."""

    entry_id: str
    domain: str
    category: str
    subcategory: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    related_entries: list[str] = field(default_factory=list)
    search_terms: list[str] = field(default_factory=list)


class IndexerSpecialist:
    """
    The Indexer Specialist organizes and indexes knowledge.

    Capabilities:
    - Categorize knowledge into domains
    - Create searchable indexes
    - Build knowledge graphs
    - Optimize retrieval
    """

    # Standard domain taxonomy
    DOMAINS = {
        "architecture": ["system-design", "api-design", "data-modeling", "patterns"],
        "security": ["authentication", "authorization", "encryption", "vulnerabilities"],
        "testing": ["unit-tests", "integration-tests", "e2e-tests", "test-strategies"],
        "operations": ["deployment", "monitoring", "infrastructure", "automation"],
        "process": ["decisions", "reviews", "planning", "retrospectives"],
        "domain-knowledge": ["business-logic", "requirements", "constraints"],
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "indexer"

    def get_system_prompt(self) -> str:
        """Get the indexer specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def classify_content(self, content: str) -> dict:
        """
        Classify content into domain and category.

        Returns suggested classification based on keywords.
        In production, would use LLM for smarter classification.
        """
        content_lower = content.lower()

        # Simple keyword-based classification
        domain_scores = {}
        for domain, categories in self.DOMAINS.items():
            score = 0
            if domain in content_lower:
                score += 2
            for cat in categories:
                if cat.replace("-", " ") in content_lower or cat in content_lower:
                    score += 1
            if score > 0:
                domain_scores[domain] = score

        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            return {
                "domain": best_domain,
                "categories": self.DOMAINS[best_domain],
                "confidence": min(domain_scores[best_domain] / 5, 1.0),
            }

        return {
            "domain": "domain-knowledge",
            "categories": ["general"],
            "confidence": 0.3,
        }

    def extract_search_terms(self, content: str) -> list[str]:
        """Extract search terms from content."""
        # Simple word extraction - in production would use NLP
        words = content.lower().split()
        # Filter out common words and keep meaningful terms
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                      "being", "have", "has", "had", "do", "does", "did", "will",
                      "would", "could", "should", "may", "might", "must", "shall",
                      "can", "need", "dare", "ought", "used", "to", "of", "in",
                      "for", "on", "with", "at", "by", "from", "as", "into",
                      "through", "during", "before", "after", "above", "below",
                      "between", "under", "again", "further", "then", "once",
                      "here", "there", "when", "where", "why", "how", "all",
                      "each", "few", "more", "most", "other", "some", "such",
                      "no", "nor", "not", "only", "own", "same", "so", "than",
                      "too", "very", "just", "and", "but", "if", "or", "because",
                      "until", "while", "this", "that", "these", "those"}

        terms = [w for w in words if w not in stop_words and len(w) > 2]
        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)

        return unique_terms[:20]  # Limit to 20 terms

    def suggest_tags(self, content: str, domain: str) -> list[str]:
        """Suggest tags based on content and domain."""
        tags = []

        # Add domain as tag
        tags.append(domain)

        # Extract key terms as potential tags
        terms = self.extract_search_terms(content)
        tags.extend(terms[:5])

        return list(set(tags))

    def build_index_entry(
        self,
        content: str,
        entry_id: str,
        domain: str = None,
    ) -> IndexEntry:
        """Build a complete index entry for content."""
        if not domain:
            classification = self.classify_content(content)
            domain = classification["domain"]

        return IndexEntry(
            entry_id=entry_id,
            domain=domain,
            category=self.DOMAINS.get(domain, ["general"])[0],
            tags=self.suggest_tags(content, domain),
            search_terms=self.extract_search_terms(content),
        )


def create_specialist() -> IndexerSpecialist:
    """Factory function to create the specialist."""
    return IndexerSpecialist()
