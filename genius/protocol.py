"""
Genius Protocol Implementation

The 7-step reasoning loop that makes every agent a genius:
1. OBSERVE - Read context, understand request
2. THINK - Chain-of-thought reasoning
3. REFLECT - "Am I on the right track?"
4. CRITIQUE - "What could go wrong?"
5. REFINE - Adjust approach based on critique
6. ACT - Execute with confidence
7. VERIFY - Check result matches intent
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from pathlib import Path
import json


@dataclass
class ReasoningTrace:
    """A complete trace of the 7-step genius reasoning process."""

    specialist: str
    task_id: Optional[str] = None

    # The 7 steps
    observe: str = ""
    think: str = ""
    reflect: str = ""
    critique: str = ""
    refine: str = ""
    act: str = ""
    verify: str = ""

    # Quality assessment
    quality_score: float = 0.0
    quality_issues: list[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        """Check if all reasoning steps are filled."""
        return all([
            self.observe,
            self.think,
            self.reflect,
            self.critique,
            self.refine,
            self.act,
            self.verify,
        ])

    def to_dict(self) -> dict:
        """Convert trace to dictionary."""
        return {
            "specialist": self.specialist,
            "task_id": self.task_id,
            "steps": {
                "observe": self.observe,
                "think": self.think,
                "reflect": self.reflect,
                "critique": self.critique,
                "refine": self.refine,
                "act": self.act,
                "verify": self.verify,
            },
            "quality_score": self.quality_score,
            "quality_issues": self.quality_issues,
        }

    def format_for_prompt(self) -> str:
        """Format trace for inclusion in prompts."""
        return f"""## Reasoning Trace

### 1. OBSERVE
{self.observe}

### 2. THINK
{self.think}

### 3. REFLECT
{self.reflect}

### 4. CRITIQUE
{self.critique}

### 5. REFINE
{self.refine}

### 6. ACT
{self.act}

### 7. VERIFY
{self.verify}

Quality Score: {self.quality_score:.2f}
"""


class GeniusProtocol:
    """
    The Genius Protocol enforces rigorous reasoning on every agent.

    Each specialist uses this protocol to:
    - Think deeply before acting
    - Self-critique their reasoning
    - Verify their outputs meet quality thresholds
    """

    STEPS = ["observe", "think", "reflect", "critique", "refine", "act", "verify"]

    STEP_PROMPTS = {
        "observe": """## Step 1: OBSERVE
Read the context carefully. What exactly is being asked?
What information do you have? What's missing?
State your observations clearly.""",

        "think": """## Step 2: THINK
Now reason through the problem step by step.
What are the key considerations?
What approaches could work?
Show your chain of thought.""",

        "reflect": """## Step 3: REFLECT
Pause and reflect. Am I on the right track?
Have I understood the request correctly?
Are my assumptions valid?
What am I uncertain about?""",

        "critique": """## Step 4: CRITIQUE
Now critique your own thinking ruthlessly.
What could go wrong with my approach?
What are the risks and edge cases?
What am I missing?
Play devil's advocate.""",

        "refine": """## Step 5: REFINE
Based on your critique, how should you adjust?
Improve your approach to address the issues found.
Strengthen weak points.
This is your refined plan.""",

        "act": """## Step 6: ACT
Execute with confidence.
Provide your actual output/recommendation/solution.
Be clear and complete.""",

        "verify": """## Step 7: VERIFY
Check your output against the original request.
Does it actually address what was asked?
Have you met the quality threshold?
- Rationale explained? ✓/✗
- Trade-offs identified? ✓/✗
- Evidence cited? ✓/✗""",
    }

    def __init__(self, prompts_dir: Path = None):
        """Initialize the protocol with prompt templates."""
        self.prompts_dir = prompts_dir or Path(__file__).parent / "prompts"
        self._prompt_cache: dict[str, str] = {}

    def load_base_prompt(self) -> str:
        """Load the base genius prompt template."""
        if "base" not in self._prompt_cache:
            base_path = self.prompts_dir / "base_genius.txt"
            if base_path.exists():
                self._prompt_cache["base"] = base_path.read_text()
            else:
                self._prompt_cache["base"] = self._default_base_prompt()
        return self._prompt_cache["base"]

    def load_specialist_prompt(self, specialist: str) -> str:
        """Load a specialist-specific prompt."""
        if specialist not in self._prompt_cache:
            specialist_path = self.prompts_dir / f"{specialist}.txt"
            if specialist_path.exists():
                self._prompt_cache[specialist] = specialist_path.read_text()
            else:
                self._prompt_cache[specialist] = ""
        return self._prompt_cache[specialist]

    def build_genius_prompt(
        self,
        specialist: str,
        task_context: str,
        include_reasoning_template: bool = True,
    ) -> str:
        """
        Build a complete genius prompt for a specialist.

        Combines:
        - Base genius reasoning protocol
        - Specialist domain expertise
        - Task-specific context
        - Reasoning template (if needed)
        """
        parts = []

        # Base genius protocol
        base = self.load_base_prompt()
        if base:
            parts.append(base)

        # Specialist expertise
        specialist_prompt = self.load_specialist_prompt(specialist)
        if specialist_prompt:
            parts.append(specialist_prompt)

        # Task context
        parts.append(f"\n## Current Task\n\n{task_context}")

        # Reasoning template
        if include_reasoning_template:
            parts.append(self._reasoning_template())

        return "\n\n".join(parts)

    def _reasoning_template(self) -> str:
        """Get the reasoning template agents must follow."""
        return """
## Your Response Format

You MUST structure your response with these 7 sections:

### 1. OBSERVE
[What you observe about the request and context]

### 2. THINK
[Your chain-of-thought reasoning]

### 3. REFLECT
[Self-reflection on your understanding and approach]

### 4. CRITIQUE
[Critical analysis of potential flaws]

### 5. REFINE
[Refined approach based on critique]

### 6. ACT
[Your actual output/solution]

### 7. VERIFY
[Verification that output meets requirements]
- Rationale explained: [Yes/No]
- Trade-offs identified: [Yes/No]
- Evidence cited: [Yes/No]
"""

    def parse_reasoning_trace(
        self, response: str, specialist: str, task_id: str = None
    ) -> ReasoningTrace:
        """Parse an LLM response into a ReasoningTrace."""
        trace = ReasoningTrace(specialist=specialist, task_id=task_id)

        # Parse each section
        current_step = None
        current_content = []

        for line in response.split("\n"):
            # Check if this is a step header
            step_found = None
            for step in self.STEPS:
                markers = [
                    f"### {step.upper()}",
                    f"## {step.upper()}",
                    f"**{step.upper()}**",
                    f"{step.upper()}:",
                    f"### 1. {step.upper()}" if step == "observe" else None,
                    f"### 2. {step.upper()}" if step == "think" else None,
                    f"### 3. {step.upper()}" if step == "reflect" else None,
                    f"### 4. {step.upper()}" if step == "critique" else None,
                    f"### 5. {step.upper()}" if step == "refine" else None,
                    f"### 6. {step.upper()}" if step == "act" else None,
                    f"### 7. {step.upper()}" if step == "verify" else None,
                ]
                if any(m and m.lower() in line.lower() for m in markers if m):
                    step_found = step
                    break

            if step_found:
                # Save previous step content
                if current_step:
                    setattr(trace, current_step, "\n".join(current_content).strip())
                current_step = step_found
                current_content = []
            elif current_step:
                current_content.append(line)

        # Save last step
        if current_step:
            setattr(trace, current_step, "\n".join(current_content).strip())

        # Calculate quality score
        trace.quality_score, trace.quality_issues = self.assess_quality(trace)

        return trace

    def assess_quality(self, trace: ReasoningTrace) -> tuple[float, list[str]]:
        """
        Assess the quality of a reasoning trace.

        Returns (score: 0.0-1.0, issues: list of problems found)
        """
        score = 1.0
        issues = []

        # Check completeness
        for step in self.STEPS:
            content = getattr(trace, step, "")
            if not content:
                score -= 0.1
                issues.append(f"Missing {step.upper()} step")
            elif len(content) < 20:
                score -= 0.05
                issues.append(f"{step.upper()} step is too brief")

        # Check for quality markers in VERIFY step
        verify_lower = trace.verify.lower()
        quality_markers = ["rationale", "trade-off", "evidence"]
        for marker in quality_markers:
            if marker not in verify_lower:
                score -= 0.05
                issues.append(f"VERIFY step missing '{marker}' check")

        # Check for actual reasoning (not just placeholders)
        placeholder_patterns = ["[your", "[insert", "[todo", "[tbd"]
        for step in self.STEPS:
            content = getattr(trace, step, "").lower()
            if any(p in content for p in placeholder_patterns):
                score -= 0.1
                issues.append(f"{step.upper()} contains placeholder text")

        return max(0.0, score), issues

    def meets_quality_threshold(
        self, trace: ReasoningTrace, threshold: float = 0.7
    ) -> bool:
        """Check if a trace meets the quality threshold."""
        return trace.quality_score >= threshold

    def _default_base_prompt(self) -> str:
        """Default base prompt if file not found."""
        return """# Genius Protocol

You are a genius-level specialist. Every response must demonstrate:
- Deep understanding of the problem
- Rigorous reasoning
- Self-awareness and critique
- Quality verification

## Core Principles

1. **Think before acting** - Never output without reasoning
2. **Critique yourself** - Find flaws before others do
3. **Verify quality** - Check your work meets standards
4. **Cite evidence** - Back claims with data or precedent
5. **Acknowledge uncertainty** - Be honest about what you don't know

## Quality Threshold

Your output is NOT ready until you can:
- Explain WHY, not just WHAT
- Identify at least 2 trade-offs you considered
- State what evidence supports your recommendation
"""


class DebateProtocol:
    """
    Protocol for multi-agent debates to reach consensus.

    Pattern:
    1. Architect proposes
    2. Coder critiques
    3. Tester critiques
    4. Architect synthesizes
    5. Repeat until consensus
    """

    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds

    def create_debate_prompt(
        self,
        topic: str,
        positions: list[dict],
        round_num: int,
        role: str,
    ) -> str:
        """
        Create a prompt for a debate participant.

        Args:
            topic: What's being debated
            positions: List of {specialist, position, arguments}
            round_num: Current debate round
            role: 'proposer', 'critic', or 'synthesizer'
        """
        positions_text = "\n\n".join(
            f"**{p['specialist']}**: {p['position']}\nArguments: {p['arguments']}"
            for p in positions
        )

        if role == "proposer":
            return f"""## Debate Topic: {topic}

You are proposing a position. State your position clearly and provide strong arguments.

Consider:
- What evidence supports your position?
- What are the strongest counter-arguments?
- What trade-offs are you accepting?
"""
        elif role == "critic":
            return f"""## Debate Topic: {topic}

### Current Positions
{positions_text}

You are critiquing these positions. Your job is to:
1. Find weaknesses in the arguments
2. Identify unstated assumptions
3. Point out missing considerations
4. Suggest improvements

Be constructive but rigorous. Weak arguments waste everyone's time.
"""
        else:  # synthesizer
            return f"""## Debate Topic: {topic}

### Debate Round {round_num}

{positions_text}

You are synthesizing these positions into a final recommendation.

Consider:
- Where do the positions agree?
- Which critiques were most valid?
- What's the strongest combined position?
- What remains uncertain?

Produce a final recommendation that addresses the valid critiques.
"""

    def check_consensus(self, positions: list[dict]) -> tuple[bool, str]:
        """
        Check if positions have reached consensus.

        Returns (reached_consensus, summary)
        """
        if len(positions) < 2:
            return False, "Not enough positions to evaluate consensus"

        # Simple heuristic: check if latest positions agree on key points
        # In practice, this would use the LLM to evaluate
        return False, "Consensus check requires LLM evaluation"


class AdversarialReview:
    """
    Adversarial review protocol where every output is challenged.

    Every significant output gets reviewed by a skeptic before acceptance.
    """

    def create_review_prompt(
        self,
        output_type: str,
        output: str,
        context: str,
    ) -> str:
        """Create a prompt for adversarial review."""
        return f"""## Adversarial Review

You are the skeptic. Your job is to find problems with this output.

### Output Type: {output_type}

### Context
{context}

### Output to Review
{output}

### Your Task

1. **Find Flaws**: What's wrong with this output?
2. **Challenge Assumptions**: What assumptions were made? Are they valid?
3. **Identify Risks**: What could go wrong if we use this?
4. **Check Completeness**: What's missing?
5. **Verify Claims**: Are all claims supported by evidence?

Be thorough but fair. The goal is improvement, not obstruction.

### Your Review

Rate the output: [ACCEPT / NEEDS_REVISION / REJECT]

Issues found:
- [List each issue]

Recommended changes:
- [List specific improvements]
"""

    def parse_review_result(self, review: str) -> dict:
        """Parse a review response."""
        result = {
            "verdict": "NEEDS_REVISION",  # default
            "issues": [],
            "recommendations": [],
        }

        # Extract verdict
        for verdict in ["ACCEPT", "NEEDS_REVISION", "REJECT"]:
            if verdict in review.upper():
                result["verdict"] = verdict
                break

        # Extract issues (simple heuristic)
        in_issues = False
        in_recommendations = False

        for line in review.split("\n"):
            line = line.strip()
            if "issues found" in line.lower():
                in_issues = True
                in_recommendations = False
            elif "recommended" in line.lower() or "improvements" in line.lower():
                in_issues = False
                in_recommendations = True
            elif line.startswith("- ") or line.startswith("* "):
                item = line[2:].strip()
                if in_issues:
                    result["issues"].append(item)
                elif in_recommendations:
                    result["recommendations"].append(item)

        return result
