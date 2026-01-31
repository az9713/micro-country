"""
Ollama Bridge - LLM Integration for the Micro-Country

This module provides the interface between the Micro-Country and Ollama
for local LLM inference. It:
- Injects genius prompts into requests
- Manages conversation context
- Handles tool calling
- Parses structured responses
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Optional, Callable, AsyncIterator
from dataclasses import dataclass, field

import httpx

from genius.protocol import GeniusProtocol, ReasoningTrace


@dataclass
class Message:
    """A message in a conversation."""

    role: str  # 'system', 'user', 'assistant'
    content: str
    tool_calls: list[dict] = field(default_factory=list)
    tool_call_id: Optional[str] = None


@dataclass
class ToolDefinition:
    """Definition of a tool the LLM can call."""

    name: str
    description: str
    parameters: dict


@dataclass
class OllamaConfig:
    """Configuration for Ollama connection."""

    host: str = "http://localhost:11434"
    model: str = "qwen2.5:14b"
    timeout: int = 120
    temperature: float = 0.7
    num_ctx: int = 8192


class OllamaBridge:
    """
    Bridge between the Micro-Country and Ollama for LLM inference.

    Features:
    - Automatic genius prompt injection
    - Tool calling support
    - Streaming responses
    - Response parsing for reasoning traces
    """

    def __init__(
        self,
        config: OllamaConfig = None,
        genius_protocol: GeniusProtocol = None,
    ):
        self.config = config or OllamaConfig()
        self.genius = genius_protocol or GeniusProtocol()
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self._client

    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = await self.client.get(f"{self.config.host}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """List available models."""
        try:
            response = await self.client.get(f"{self.config.host}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            pass
        return []

    async def generate(
        self,
        prompt: str,
        system: str = None,
        specialist: str = None,
        include_reasoning_template: bool = True,
        **kwargs,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: The user prompt
            system: Custom system prompt (overrides genius prompt)
            specialist: Specialist name for genius prompt injection
            include_reasoning_template: Whether to include 7-step template
            **kwargs: Additional Ollama parameters

        Returns:
            The generated response text
        """
        # Build system prompt
        if system is None and specialist:
            system = self.genius.build_genius_prompt(
                specialist=specialist,
                task_context=prompt,
                include_reasoning_template=include_reasoning_template,
            )

        # Prepare request
        request_data = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_ctx": kwargs.get("num_ctx", self.config.num_ctx),
            },
        }

        if system:
            request_data["system"] = system

        # Make request
        response = await self.client.post(
            f"{self.config.host}/api/generate",
            json=request_data,
        )
        response.raise_for_status()

        data = response.json()
        return data.get("response", "")

    async def generate_stream(
        self,
        prompt: str,
        system: str = None,
        specialist: str = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        """
        Generate a streaming response from the LLM.

        Yields chunks of text as they're generated.
        """
        # Build system prompt
        if system is None and specialist:
            system = self.genius.build_genius_prompt(
                specialist=specialist,
                task_context=prompt,
                include_reasoning_template=True,
            )

        request_data = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_ctx": kwargs.get("num_ctx", self.config.num_ctx),
            },
        }

        if system:
            request_data["system"] = system

        async with self.client.stream(
            "POST",
            f"{self.config.host}/api/generate",
            json=request_data,
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
                    except json.JSONDecodeError:
                        continue

    async def chat(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] = None,
        specialist: str = None,
        **kwargs,
    ) -> tuple[str, list[dict]]:
        """
        Have a chat conversation with the LLM.

        Args:
            messages: List of conversation messages
            tools: Available tools for the LLM to call
            specialist: Specialist for genius prompt injection
            **kwargs: Additional parameters

        Returns:
            Tuple of (response text, tool calls)
        """
        # Convert messages to Ollama format
        ollama_messages = []

        # Inject genius system prompt if specialist specified
        if specialist:
            # Find or create system message
            has_system = any(m.role == "system" for m in messages)
            if not has_system:
                genius_prompt = self.genius.build_genius_prompt(
                    specialist=specialist,
                    task_context="",
                    include_reasoning_template=True,
                )
                ollama_messages.append({"role": "system", "content": genius_prompt})

        for msg in messages:
            ollama_msg = {"role": msg.role, "content": msg.content}
            if msg.tool_calls:
                ollama_msg["tool_calls"] = msg.tool_calls
            ollama_messages.append(ollama_msg)

        # Prepare tools
        ollama_tools = None
        if tools:
            ollama_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in tools
            ]

        # Make request
        request_data = {
            "model": self.config.model,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_ctx": kwargs.get("num_ctx", self.config.num_ctx),
            },
        }

        if ollama_tools:
            request_data["tools"] = ollama_tools

        response = await self.client.post(
            f"{self.config.host}/api/chat",
            json=request_data,
        )
        response.raise_for_status()

        data = response.json()
        message = data.get("message", {})

        return message.get("content", ""), message.get("tool_calls", [])

    async def generate_with_reasoning(
        self,
        prompt: str,
        specialist: str,
        task_id: str = None,
    ) -> tuple[str, ReasoningTrace]:
        """
        Generate a response with parsed reasoning trace.

        Args:
            prompt: The task/question
            specialist: Which specialist is responding
            task_id: Optional task ID for tracking

        Returns:
            Tuple of (final output, reasoning trace)
        """
        response = await self.generate(
            prompt=prompt,
            specialist=specialist,
            include_reasoning_template=True,
        )

        # Parse the reasoning trace
        trace = self.genius.parse_reasoning_trace(
            response=response,
            specialist=specialist,
            task_id=task_id,
        )

        # Extract the ACT section as the final output
        final_output = trace.act if trace.act else response

        return final_output, trace

    async def debate(
        self,
        topic: str,
        participants: list[str],
        max_rounds: int = 1,
        progress_callback=None,
    ) -> dict:
        """
        Run a debate between specialists.

        Args:
            topic: What to debate
            participants: List of specialist names
            max_rounds: Maximum debate rounds (default 1 for faster response)
            progress_callback: Optional callback(message) for progress updates

        Returns:
            Debate result with positions and synthesis
        """
        def progress(msg):
            if progress_callback:
                progress_callback(msg)
            else:
                print(msg, flush=True)

        positions = []
        total_steps = len(participants) * max_rounds + 1  # +1 for synthesis
        current_step = 0

        # Round 1: Each participant states their position
        progress(f"\n[Round 1/{max_rounds}] Gathering initial positions...")
        for participant in participants:
            current_step += 1
            progress(f"  [{current_step}/{total_steps}] {participant} is thinking...")

            prompt = f"""Topic: {topic}

State your position concisely (2-3 paragraphs max) with key arguments."""

            response = await self.generate(
                prompt=prompt,
                specialist=participant,
            )
            positions.append({
                "participant": participant,
                "position": response,
                "round": 1,
            })
            progress(f"  [{current_step}/{total_steps}] {participant} done.")

        # Round 2+: Critique and refine (if more rounds requested)
        for round_num in range(2, max_rounds + 1):
            progress(f"\n[Round {round_num}/{max_rounds}] Critique and refine...")
            positions_text = "\n".join(
                f"- {p['participant']}: {p['position'][:200]}..."
                for p in positions
                if p["round"] == round_num - 1
            )

            for participant in participants:
                current_step += 1
                progress(f"  [{current_step}/{total_steps}] {participant} refining...")

                prompt = f"""Topic: {topic}

Previous positions (summarized):
{positions_text}

Briefly critique others and refine your position (2 paragraphs max)."""

                response = await self.generate(
                    prompt=prompt,
                    specialist=participant,
                )
                positions.append({
                    "participant": participant,
                    "position": response,
                    "round": round_num,
                })
                progress(f"  [{current_step}/{total_steps}] {participant} done.")

        # Final synthesis
        current_step += 1
        progress(f"\n[Synthesis] Creating final summary...")
        progress(f"  [{current_step}/{total_steps}] Synthesizing all positions...")

        final_positions = "\n".join(
            f"- {p['participant']}: {p['position'][:300]}"
            for p in positions
            if p["round"] == max_rounds
        )

        synthesis_prompt = f"""Topic: {topic}

Final positions:
{final_positions}

Provide a brief synthesis (3-4 sentences): key agreements, disagreements, and recommendation."""

        synthesis = await self.generate(
            prompt=synthesis_prompt,
            specialist="architect",
        )
        progress(f"  [{current_step}/{total_steps}] Synthesis complete!")

        return {
            "topic": topic,
            "participants": participants,
            "positions": positions,
            "synthesis": synthesis,
            "rounds": max_rounds,
        }

    async def adversarial_review(
        self,
        output: str,
        output_type: str,
        context: str,
        reviewer: str = "auditor",
    ) -> dict:
        """
        Have a specialist review output adversarially.

        Args:
            output: The output to review
            output_type: Type of output (code, design, etc.)
            context: Context for the review
            reviewer: Which specialist reviews

        Returns:
            Review result with verdict and issues
        """
        # Truncate output if too long for faster processing
        output_preview = output[:500] + "..." if len(output) > 500 else output

        prompt = f"""Review this {output_type} critically.

Context: {context}

Output:
{output_preview}

Verdict: ACCEPT, NEEDS_REVISION, or REJECT

Issues found:
- (list issues briefly)

Recommended changes:
- (list fixes briefly)
"""

        response = await self.generate(
            prompt=prompt,
            specialist=reviewer,
        )

        # Parse verdict
        verdict = "NEEDS_REVISION"
        for v in ["ACCEPT", "NEEDS_REVISION", "REJECT"]:
            if v in response.upper():
                verdict = v
                break

        # Extract issues (simple parsing)
        issues = []
        recommendations = []
        in_issues = False
        in_recommendations = False

        for line in response.split("\n"):
            line = line.strip()
            if "issues found" in line.lower():
                in_issues = True
                in_recommendations = False
            elif "recommended" in line.lower():
                in_issues = False
                in_recommendations = True
            elif line.startswith("- ") or line.startswith("* "):
                item = line[2:].strip()
                if in_issues:
                    issues.append(item)
                elif in_recommendations:
                    recommendations.append(item)

        return {
            "verdict": verdict,
            "issues": issues,
            "recommendations": recommendations,
            "full_review": response,
        }


async def main():
    """Test the Ollama bridge."""
    import yaml

    # Load config
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        ollama_cfg = OllamaConfig(
            host=cfg["ollama"]["host"],
            model=cfg["ollama"]["model"],
            timeout=cfg["ollama"]["timeout"],
        )
    else:
        ollama_cfg = OllamaConfig()

    async with OllamaBridge(ollama_cfg) as bridge:
        # Check connection
        connected = await bridge.check_connection()
        print(f"Ollama connected: {connected}")

        if connected:
            # List models
            models = await bridge.list_models()
            print(f"Available models: {models}")

            # Test generation with genius protocol
            print("\n--- Testing Architect Genius ---\n")
            output, trace = await bridge.generate_with_reasoning(
                prompt="Design a simple rate limiting system for an API",
                specialist="architect",
            )
            print(f"Quality Score: {trace.quality_score}")
            print(f"Output:\n{output[:500]}...")


if __name__ == "__main__":
    asyncio.run(main())
