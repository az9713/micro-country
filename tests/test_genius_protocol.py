"""Tests for the Genius Protocol."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from genius.protocol import GeniusProtocol, ReasoningTrace, DebateProtocol, AdversarialReview
from genius.evidence_court import (
    EvidenceCourt,
    Evidence,
    EvidenceType,
    Position,
    empirical_evidence,
    precedent_evidence,
    theoretical_evidence,
)


class TestReasoningTrace:
    """Tests for ReasoningTrace."""

    def test_create_trace(self):
        trace = ReasoningTrace(specialist="architect")
        assert trace.specialist == "architect"
        assert not trace.is_complete()

    def test_complete_trace(self):
        trace = ReasoningTrace(
            specialist="architect",
            observe="Observed the problem",
            think="Thought about solutions",
            reflect="Reflected on approach",
            critique="Found potential issues",
            refine="Refined the solution",
            act="Implemented the solution",
            verify="Verified it works",
        )
        assert trace.is_complete()

    def test_trace_to_dict(self):
        trace = ReasoningTrace(specialist="coder", observe="test")
        d = trace.to_dict()
        assert d["specialist"] == "coder"
        assert d["steps"]["observe"] == "test"


class TestGeniusProtocol:
    """Tests for GeniusProtocol."""

    def test_create_protocol(self):
        protocol = GeniusProtocol()
        assert protocol.STEPS == ["observe", "think", "reflect", "critique", "refine", "act", "verify"]

    def test_load_base_prompt(self):
        protocol = GeniusProtocol()
        prompt = protocol.load_base_prompt()
        assert "Genius Protocol" in prompt or len(prompt) > 0

    def test_build_genius_prompt(self):
        protocol = GeniusProtocol()
        prompt = protocol.build_genius_prompt(
            specialist="architect",
            task_context="Design a simple API",
        )
        assert "Design a simple API" in prompt

    def test_parse_reasoning_trace(self):
        protocol = GeniusProtocol()
        response = """
### 1. OBSERVE
I see a request for an API design.

### 2. THINK
The key considerations are scalability and simplicity.

### 3. REFLECT
I believe I understand the requirements correctly.

### 4. CRITIQUE
I might be missing security considerations.

### 5. REFINE
Let me add authentication to the design.

### 6. ACT
Here is my API design: GET /users, POST /users

### 7. VERIFY
This design meets the requirements.
- Rationale explained: Yes
- Trade-offs identified: Yes
- Evidence cited: Yes
"""
        trace = protocol.parse_reasoning_trace(response, "architect")
        assert trace.specialist == "architect"
        assert "API design" in trace.observe
        assert "scalability" in trace.think.lower()

    def test_assess_quality(self):
        protocol = GeniusProtocol()
        trace = ReasoningTrace(
            specialist="architect",
            observe="Good observation with details",
            think="Thorough reasoning process",
            reflect="Careful reflection",
            critique="Identified several issues",
            refine="Made improvements",
            act="Clear output provided",
            verify="Rationale explained, Trade-offs identified, Evidence cited",
        )
        score, issues = protocol.assess_quality(trace)
        assert score > 0.5
        assert len(issues) < 5


class TestEvidenceCourt:
    """Tests for Evidence Court."""

    def test_evidence_types(self):
        assert EvidenceType.EMPIRICAL < EvidenceType.PRECEDENT
        assert EvidenceType.PRECEDENT < EvidenceType.CONSENSUS
        assert EvidenceType.THEORETICAL < EvidenceType.INTUITION

    def test_evidence_strength(self):
        empirical = Evidence(
            EvidenceType.EMPIRICAL,
            "Benchmark shows 100 req/s",
            "load test",
            confidence=0.9,
        )
        intuition = Evidence(
            EvidenceType.INTUITION,
            "This feels right",
            "gut feeling",
            confidence=0.5,
        )
        assert empirical.strength_score() > intuition.strength_score()

    def test_convenience_functions(self):
        emp = empirical_evidence("Test result", "unit test")
        assert emp.evidence_type == EvidenceType.EMPIRICAL

        prec = precedent_evidence("Previous success", "project X")
        assert prec.evidence_type == EvidenceType.PRECEDENT

        theo = theoretical_evidence("Logical argument", "reasoning")
        assert theo.evidence_type == EvidenceType.THEORETICAL

    def test_position_strength(self):
        pos = Position(
            advocate="architect",
            position="Use microservices",
            arguments=["Scalability", "Independence"],
            evidence=[
                empirical_evidence("Benchmark: 10x throughput", "test"),
                precedent_evidence("Netflix uses this", "case study"),
            ],
        )
        assert pos.total_evidence_strength() > 0.5

    def test_court_determine_winner(self):
        court = EvidenceCourt()

        pos1 = Position(
            advocate="architect",
            position="Use microservices",
            arguments=["Scalable"],
            evidence=[empirical_evidence("Benchmark data", "test", confidence=0.9)],
        )
        pos2 = Position(
            advocate="coder",
            position="Use monolith",
            arguments=["Simple"],
            evidence=[theoretical_evidence("Easier to develop", "reasoning", confidence=0.7)],
        )

        winner, losers = court.determine_winner([pos1, pos2])
        assert winner.advocate == "architect"
        assert len(losers) == 1

    def test_evaluate_positions(self):
        court = EvidenceCourt()

        positions = [
            Position(
                advocate="analyst",
                position="Option A",
                arguments=["Good"],
                evidence=[empirical_evidence("Data shows it works", "study")],
            )
        ]

        analysis = court.evaluate_positions(positions)
        assert "analyst" in analysis
        assert analysis["analyst"]["evidence_count"] == 1


class TestDebateProtocol:
    """Tests for Debate Protocol."""

    def test_create_debate_prompt(self):
        debate = DebateProtocol()

        positions = [
            {"specialist": "architect", "position": "Use REST", "arguments": "Standard and simple"},
        ]

        prompt = debate.create_debate_prompt(
            topic="API design",
            positions=positions,
            round_num=1,
            role="critic",
        )

        assert "API design" in prompt
        assert "REST" in prompt


class TestAdversarialReview:
    """Tests for Adversarial Review."""

    def test_create_review_prompt(self):
        review = AdversarialReview()

        prompt = review.create_review_prompt(
            output_type="code",
            output="def foo(): pass",
            context="Simple function",
        )

        assert "code" in prompt.lower()
        assert "def foo" in prompt

    def test_parse_review_result(self):
        review = AdversarialReview()

        response = """
Rating: NEEDS_REVISION

Issues found:
- No error handling
- Missing docstring

Recommended changes:
- Add try/except
- Add documentation
"""

        result = review.parse_review_result(response)
        assert result["verdict"] == "NEEDS_REVISION"
        assert len(result["issues"]) >= 1
        assert len(result["recommendations"]) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
