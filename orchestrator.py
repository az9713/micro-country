"""
Central Orchestrator - Head of State for the Micro-Country

The orchestrator is the central coordinator that:
- Connects to all ministry MCP servers
- Routes requests to appropriate ministries
- Aggregates context from multiple sources
- Manages the Ollama bridge for LLM inference
- Coordinates debates and cross-ministry collaboration
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field

import yaml

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from bridge.ollama_bridge import OllamaBridge, OllamaConfig, Message, ToolDefinition
from genius import GeniusProtocol, EvidenceCourt, Evidence, EvidenceType


@dataclass
class MinistryConnection:
    """Represents a connection to a ministry server."""

    name: str
    path: str
    specialists: list[str]
    session: Optional[ClientSession] = None
    tools: list[dict] = field(default_factory=list)
    resources: list[dict] = field(default_factory=list)


@dataclass
class Request:
    """A request to be processed."""

    content: str
    ministry: Optional[str] = None
    specialist: Optional[str] = None
    context: dict = field(default_factory=dict)


@dataclass
class Response:
    """A response from processing."""

    content: str
    ministry: str
    specialist: Optional[str] = None
    reasoning_trace: Optional[dict] = None
    tool_calls: list[dict] = field(default_factory=list)


class Orchestrator:
    """
    Central Orchestrator for the Micro-Country of Geniuses.

    Responsibilities:
    - Connect to ministry MCP servers
    - Route requests to appropriate ministries
    - Coordinate cross-ministry collaboration
    - Manage debates and conflict resolution
    - Provide unified interface for users
    """

    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path(__file__).parent / "config.yaml"
        self.config = self._load_config()

        # Initialize components
        self.genius = GeniusProtocol(
            prompts_dir=Path(__file__).parent / "genius" / "prompts"
        )
        self.court = EvidenceCourt()

        # Initialize Ollama bridge
        ollama_cfg = OllamaConfig(
            host=self.config["ollama"]["host"],
            model=self.config["ollama"]["model"],
            timeout=self.config["ollama"]["timeout"],
        )
        self.ollama = OllamaBridge(ollama_cfg, self.genius)

        # Ministry connections
        self.ministries: dict[str, MinistryConnection] = {}
        self._setup_ministries()

        # Knowledge server connection
        self.knowledge_session: Optional[ClientSession] = None

    def _load_config(self) -> dict:
        """Load configuration from YAML."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        return {
            "ollama": {
                "host": "http://localhost:11434",
                "model": "mistral:7b",
                "timeout": 300,
            },
            "ministries": {},
            "database": {"path": "data/country.db"},
        }

    def _setup_ministries(self):
        """Initialize ministry connection definitions."""
        for name, cfg in self.config.get("ministries", {}).items():
            self.ministries[name] = MinistryConnection(
                name=name,
                path=cfg["path"],
                specialists=cfg.get("specialists", []),
            )

    async def connect_to_ministry(self, ministry_name: str) -> bool:
        """
        Connect to a ministry's MCP server.

        Args:
            ministry_name: Name of the ministry to connect to

        Returns:
            True if connection successful
        """
        if ministry_name not in self.ministries:
            return False

        ministry = self.ministries[ministry_name]
        ministry_path = Path(__file__).parent / ministry.path

        if not ministry_path.exists():
            print(f"Warning: Ministry server not found at {ministry_path}")
            return False

        try:
            server_params = StdioServerParameters(
                command=sys.executable,
                args=[str(ministry_path)],
            )

            # This would normally use the MCP client to connect
            # For now, we'll set up the structure for future connection
            print(f"Ministry {ministry_name} ready for connection at {ministry_path}")
            return True

        except Exception as e:
            print(f"Error connecting to {ministry_name}: {e}")
            return False

    async def connect_to_knowledge_server(self) -> bool:
        """Connect to the shared knowledge server."""
        knowledge_path = Path(__file__).parent / "shared" / "knowledge_server.py"

        if not knowledge_path.exists():
            print(f"Warning: Knowledge server not found at {knowledge_path}")
            return False

        try:
            print(f"Knowledge server ready for connection at {knowledge_path}")
            return True
        except Exception as e:
            print(f"Error connecting to knowledge server: {e}")
            return False

    async def startup(self):
        """Start the orchestrator and connect to all servers."""
        print("Starting Micro-Country Orchestrator...")

        # Check Ollama connection
        async with self.ollama:
            connected = await self.ollama.check_connection()
            if connected:
                print(f"[OK] Connected to Ollama at {self.config['ollama']['host']}")
                models = await self.ollama.list_models()
                configured_model = self.config["ollama"]["model"].split(":")[0]
                if configured_model in [m.split(":")[0] for m in models]:
                    print(f"[OK] Model {self.config['ollama']['model']} available")
                else:
                    print(f"[WARNING] Model {self.config['ollama']['model']} not found in: {models}")
            else:
                print(f"[ERROR] Could not connect to Ollama at {self.config['ollama']['host']}")

        # Connect to knowledge server
        await self.connect_to_knowledge_server()

        # Connect to ministries
        for ministry_name in self.ministries:
            await self.connect_to_ministry(ministry_name)

        print("\nOrchestrator ready!")

    def route_request(self, request: Request) -> str:
        """
        Determine which ministry should handle a request.

        Uses simple keyword matching. In production, would use LLM classification.
        """
        content_lower = request.content.lower()

        # If ministry explicitly specified, use it
        if request.ministry:
            return request.ministry

        # Keyword-based routing
        routing_rules = {
            "code": ["implement", "code", "function", "class", "debug", "fix bug", "refactor", "architecture", "design"],
            "research": ["search", "find", "research", "analyze", "document", "write"],
            "quality": ["test", "security", "audit", "review", "validate", "verify"],
            "operations": ["file", "directory", "run", "execute", "deploy", "shell"],
            "archives": ["remember", "recall", "history", "decision", "knowledge", "store"],
            "communications": ["notify", "message", "schedule", "calendar", "alert"],
        }

        for ministry, keywords in routing_rules.items():
            if any(kw in content_lower for kw in keywords):
                return ministry

        # Default to code ministry
        return "code"

    def select_specialist(self, ministry: str, request: Request) -> str:
        """
        Select the best specialist within a ministry for a request.

        Uses simple keyword matching. In production, would use LLM classification.
        """
        if request.specialist:
            return request.specialist

        if ministry not in self.ministries:
            return None

        specialists = self.ministries[ministry].specialists
        if not specialists:
            return None

        content_lower = request.content.lower()

        # Specialist selection rules
        specialist_rules = {
            # Code ministry
            "architect": ["design", "architecture", "system", "api", "structure"],
            "coder": ["implement", "code", "function", "class", "write"],
            "debugger": ["debug", "fix", "bug", "error", "issue"],
            # Research ministry
            "analyst": ["analyze", "data", "insight", "pattern"],
            "writer": ["document", "write", "explain", "tutorial"],
            "searcher": ["search", "find", "research", "look up"],
            # Quality ministry
            "tester": ["test", "coverage", "unit", "integration"],
            "auditor": ["security", "audit", "vulnerability", "review"],
            "validator": ["validate", "verify", "check", "confirm"],
            # Operations ministry
            "file_manager": ["file", "directory", "folder", "path"],
            "shell_runner": ["run", "execute", "command", "shell"],
            "deployer": ["deploy", "release", "production", "staging"],
            # Archives ministry
            "memory": ["remember", "store", "save", "record"],
            "indexer": ["index", "organize", "categorize", "search"],
            # Communications ministry
            "messenger": ["message", "notify", "alert", "send"],
            "scheduler": ["schedule", "calendar", "time", "deadline"],
        }

        for specialist in specialists:
            if specialist in specialist_rules:
                keywords = specialist_rules[specialist]
                if any(kw in content_lower for kw in keywords):
                    return specialist

        # Return first specialist as default
        return specialists[0]

    async def process_request(self, request: Request) -> Response:
        """
        Process a request through the appropriate ministry.

        Steps:
        1. Route to ministry
        2. Select specialist
        3. Generate response with genius protocol
        4. Return structured response
        """
        # Route request
        ministry = self.route_request(request)
        specialist = self.select_specialist(ministry, request)

        # Build context
        context = {
            "ministry": ministry,
            "specialist": specialist,
            "user_context": request.context,
        }

        # Generate response using Ollama with genius protocol
        async with self.ollama:
            output, trace = await self.ollama.generate_with_reasoning(
                prompt=request.content,
                specialist=specialist,
            )

        return Response(
            content=output,
            ministry=ministry,
            specialist=specialist,
            reasoning_trace=trace.to_dict() if trace else None,
        )

    async def coordinate_debate(
        self,
        topic: str,
        participants: list[str] = None,
        max_rounds: int = 1,
    ) -> dict:
        """
        Coordinate a debate between specialists.

        Args:
            topic: The topic to debate
            participants: List of specialist names (default: architect, coder)
            max_rounds: Number of debate rounds (default: 1 for faster response)

        Returns:
            Debate result with synthesis
        """
        if participants is None:
            # Use 2 participants by default for faster debates
            participants = ["architect", "coder"]

        async with self.ollama:
            result = await self.ollama.debate(
                topic=topic,
                participants=participants,
                max_rounds=max_rounds,
            )

        return result

    async def resolve_conflict(
        self,
        topic: str,
        positions: list[dict],
    ) -> dict:
        """
        Resolve a conflict using the Evidence Court.

        Args:
            topic: What the conflict is about
            positions: List of positions with evidence

        Returns:
            Court ruling
        """
        # Convert positions to court format
        court_positions = []
        for pos in positions:
            evidence_list = []
            for ev in pos.get("evidence", []):
                evidence_list.append(
                    Evidence(
                        evidence_type=EvidenceType[ev.get("type", "THEORETICAL").upper()],
                        description=ev.get("description", ""),
                        source=ev.get("source", "unknown"),
                        confidence=ev.get("confidence", 0.7),
                    )
                )

            court_positions.append(
                self.court.create_position(
                    advocate=pos["advocate"],
                    position=pos["position"],
                    arguments=pos.get("arguments", []),
                    evidence=evidence_list,
                )
            )

        # Create judge prompt
        judge_prompt = self.court.create_case_prompt(topic, court_positions)

        # Get ruling from LLM (Archives ministry acts as judge)
        async with self.ollama:
            ruling_response = await self.ollama.generate(
                prompt=judge_prompt,
                specialist="memory",  # Archives/memory as judge
            )

        # Parse the ruling
        ruling = self.court.parse_ruling_response(
            ruling_response,
            topic,
            court_positions,
        )

        return ruling.to_dict()

    async def adversarial_review(
        self,
        output: str,
        output_type: str,
        context: str,
    ) -> dict:
        """
        Have output reviewed adversarially.

        Args:
            output: The output to review
            output_type: Type of output
            context: Context for review

        Returns:
            Review result
        """
        async with self.ollama:
            return await self.ollama.adversarial_review(
                output=output,
                output_type=output_type,
                context=context,
                reviewer="auditor",
            )

    async def run_interactive(self):
        """Run an interactive session."""
        await self.startup()

        print("\n" + "=" * 60)
        print("Welcome to the Micro-Country of Geniuses")
        print("=" * 60)
        print("\nCommands:")
        print("  /debate <topic>  - Start a debate on a topic")
        print("  /review <text>   - Adversarial review of text")
        print("  /ministry <name> - Direct request to ministry")
        print("  /quit            - Exit")
        print("\nOr just type your request.\n")

        while True:
            try:
                user_input = input("\n> ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "/quit":
                    print("Goodbye from the Micro-Country!")
                    break

                if user_input.startswith("/debate "):
                    topic = user_input[8:].strip()
                    print(f"\nStarting debate on: {topic}")
                    print("Participants: architect, coder")
                    print("(Progress will be shown as each participant responds)")
                    result = await self.coordinate_debate(topic)

                    # Display individual positions
                    print("\n" + "=" * 50)
                    print("DEBATE POSITIONS")
                    print("=" * 50)
                    for pos in result.get("positions", []):
                        print(f"\n--- {pos.get('participant', 'unknown')} (Round {pos.get('round', 1)}) ---")
                        print(pos.get("position", ""))

                    # Display synthesis
                    print("\n" + "=" * 50)
                    print("SYNTHESIS")
                    print("=" * 50)
                    print(result.get("synthesis", "No synthesis available"))

                elif user_input.startswith("/review "):
                    text = user_input[8:].strip()
                    print(f"\nReviewing: {text[:100]}...")
                    result = await self.adversarial_review(
                        output=text,
                        output_type="general",
                        context="User submitted for review",
                    )
                    print(f"\nVerdict: {result['verdict']}")
                    if result["issues"]:
                        print("Issues:")
                        for issue in result["issues"]:
                            print(f"  - {issue}")

                elif user_input.startswith("/ministry "):
                    parts = user_input[10:].split(" ", 1)
                    ministry = parts[0]
                    content = parts[1] if len(parts) > 1 else ""
                    request = Request(content=content, ministry=ministry)
                    response = await self.process_request(request)
                    print(f"\n[{response.ministry}/{response.specialist}]")
                    print(response.content)

                else:
                    request = Request(content=user_input)
                    response = await self.process_request(request)
                    print(f"\n[{response.ministry}/{response.specialist}]")
                    print(response.content)

            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                import traceback
                print(f"\nError: {e}")
                traceback.print_exc()


async def main():
    """Main entry point."""
    orchestrator = Orchestrator()
    await orchestrator.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
