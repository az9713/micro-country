"""
Ministry of Archives - MCP Server

The Archives Ministry is responsible for:
- Storing and retrieving decisions
- Managing domain knowledge
- Indexing and organizing information
- Serving as judge in the Evidence Court

Tools:
- store_decision: Record a decision with rationale
- recall_context: Retrieve relevant historical context
- index_knowledge: Organize and index information

Resources:
- decision_log: Historical decisions
- project_history: Project evolution

Specialists:
- memory: Storage and retrieval
- indexer: Organization and search
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    ResourceContents,
    TextResourceContents,
    Tool,
    TextContent,
)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.database import Database
from genius import GeniusProtocol, EvidenceCourt, Evidence, EvidenceType


class ArchivesMinistry:
    """
    MCP Server for the Ministry of Archives.

    Also serves as the judge for the Evidence Court.
    """

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.court = EvidenceCourt()
        self.server = Server("archives-ministry")
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="archives://decision-log",
                    name="Decision Log",
                    description="Historical decisions with rationale",
                    mimeType="application/json",
                ),
                Resource(
                    uri="archives://project-history",
                    name="Project History",
                    description="Project evolution and milestones",
                    mimeType="application/json",
                ),
                Resource(
                    uri="archives://knowledge-base",
                    name="Knowledge Base",
                    description="Accumulated domain knowledge",
                    mimeType="application/json",
                ),
                Resource(
                    uri="archives://court-precedents",
                    name="Court Precedents",
                    description="Evidence Court rulings and precedents",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a resource."""
            if uri == "archives://decision-log":
                data = await self.db.get_decisions(limit=100)
            elif uri == "archives://project-history":
                data = await self.db.get_task_history(limit=100)
            elif uri == "archives://knowledge-base":
                data = await self.db.search_knowledge(limit=100)
            elif uri == "archives://court-precedents":
                data = await self.db.get_court_precedents(limit=50)
            else:
                raise ValueError(f"Unknown resource: {uri}")

            return [
                TextResourceContents(
                    uri=uri,
                    mimeType="application/json",
                    text=json.dumps(data, indent=2, default=str),
                )
            ]

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                # Memory specialist tools
                Tool(
                    name="store_decision",
                    description="Store a decision with full context and rationale. Use when a significant decision is made that should be remembered.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ministry": {
                                "type": "string",
                                "description": "Which ministry made this decision",
                            },
                            "decision_type": {
                                "type": "string",
                                "description": "Type: design, implementation, configuration, process",
                            },
                            "context": {
                                "type": "object",
                                "description": "What led to this decision",
                            },
                            "decision": {
                                "type": "string",
                                "description": "The actual decision",
                            },
                            "rationale": {
                                "type": "string",
                                "description": "Why this decision was made",
                            },
                            "alternatives_considered": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Other options that were evaluated",
                            },
                            "evidence": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"},
                                        "description": {"type": "string"},
                                        "source": {"type": "string"},
                                    },
                                },
                                "description": "Evidence supporting the decision",
                            },
                        },
                        "required": ["ministry", "decision_type", "context", "decision", "rationale"],
                    },
                ),
                Tool(
                    name="recall_context",
                    description="Recall relevant historical context for a given topic or situation.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "What topic to recall context for",
                            },
                            "include_decisions": {
                                "type": "boolean",
                                "default": True,
                                "description": "Include relevant decisions",
                            },
                            "include_knowledge": {
                                "type": "boolean",
                                "default": True,
                                "description": "Include domain knowledge",
                            },
                            "include_precedents": {
                                "type": "boolean",
                                "default": False,
                                "description": "Include court precedents",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 10,
                            },
                        },
                        "required": ["topic"],
                    },
                ),
                Tool(
                    name="store_lesson",
                    description="Store a lesson learned from experience.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "description": "Knowledge domain",
                            },
                            "topic": {
                                "type": "string",
                                "description": "Specific topic",
                            },
                            "lesson": {
                                "type": "string",
                                "description": "What was learned",
                            },
                            "context": {
                                "type": "string",
                                "description": "Context where this was learned",
                            },
                            "confidence": {
                                "type": "number",
                                "default": 0.8,
                                "description": "Confidence level 0.0-1.0",
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["domain", "topic", "lesson"],
                    },
                ),
                # Indexer specialist tools
                Tool(
                    name="index_knowledge",
                    description="Index and categorize a piece of knowledge for easy retrieval.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content to index",
                            },
                            "domain": {
                                "type": "string",
                                "description": "Primary domain category",
                            },
                            "topics": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Related topics",
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Tags for search",
                            },
                            "related_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "IDs of related knowledge",
                            },
                        },
                        "required": ["content", "domain"],
                    },
                ),
                Tool(
                    name="search_archives",
                    description="Search the archives for relevant information.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query",
                            },
                            "domains": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Domains to search",
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                            },
                        },
                        "required": ["query"],
                    },
                ),
                # Evidence Court tools (judge role)
                Tool(
                    name="adjudicate_conflict",
                    description="Adjudicate a conflict between positions using evidence-based reasoning. This is the Evidence Court.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "What the conflict is about",
                            },
                            "positions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "advocate": {"type": "string"},
                                        "position": {"type": "string"},
                                        "arguments": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                        "evidence": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "type": {
                                                        "type": "string",
                                                        "enum": ["EMPIRICAL", "PRECEDENT", "CONSENSUS", "THEORETICAL", "INTUITION"],
                                                    },
                                                    "description": {"type": "string"},
                                                    "source": {"type": "string"},
                                                    "confidence": {"type": "number"},
                                                },
                                            },
                                        },
                                    },
                                },
                                "description": "The conflicting positions with evidence",
                            },
                        },
                        "required": ["topic", "positions"],
                    },
                ),
                Tool(
                    name="get_precedent",
                    description="Get relevant precedents for a topic.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic to find precedents for",
                            },
                            "limit": {
                                "type": "integer",
                                "default": 5,
                            },
                        },
                        "required": ["topic"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            try:
                result = await self._execute_tool(name, arguments)
                return [TextContent(type="text", text=json.dumps(result, default=str))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    async def _execute_tool(self, name: str, args: dict[str, Any]) -> Any:
        """Execute a tool."""

        if name == "store_decision":
            decision_id = await self.db.log_decision(
                ministry=args["ministry"],
                decision_type=args["decision_type"],
                context=args["context"],
                decision=args["decision"],
                rationale=args["rationale"],
                options_considered=args.get("alternatives_considered"),
                evidence=args.get("evidence"),
            )
            return {
                "success": True,
                "decision_id": decision_id,
                "message": f"Decision recorded: {args['decision'][:100]}...",
            }

        elif name == "recall_context":
            context = {"topic": args["topic"], "results": []}

            if args.get("include_decisions", True):
                decisions = await self.db.get_decisions(limit=args.get("limit", 10))
                # Filter by topic relevance (simple keyword match)
                topic_lower = args["topic"].lower()
                relevant = [
                    d for d in decisions
                    if topic_lower in str(d).lower()
                ][:5]
                if relevant:
                    context["results"].append({
                        "type": "decisions",
                        "items": relevant,
                    })

            if args.get("include_knowledge", True):
                knowledge = await self.db.search_knowledge(
                    query=args["topic"],
                    limit=args.get("limit", 10),
                )
                if knowledge:
                    context["results"].append({
                        "type": "knowledge",
                        "items": knowledge,
                    })

            if args.get("include_precedents", False):
                precedents = await self.db.get_court_precedents(
                    topic_query=args["topic"],
                    limit=5,
                )
                if precedents:
                    context["results"].append({
                        "type": "precedents",
                        "items": precedents,
                    })

            return context

        elif name == "store_lesson":
            knowledge_id = await self.db.store_knowledge(
                domain=args["domain"],
                topic=args["topic"],
                content=args["lesson"],
                source=args.get("context", "experience"),
                confidence=args.get("confidence", 0.8),
                tags=args.get("tags"),
            )
            return {
                "success": True,
                "knowledge_id": knowledge_id,
                "message": f"Lesson stored in {args['domain']}/{args['topic']}",
            }

        elif name == "index_knowledge":
            # Store with enhanced metadata
            knowledge_id = await self.db.store_knowledge(
                domain=args["domain"],
                topic=args.get("topics", ["general"])[0] if args.get("topics") else "general",
                content=args["content"],
                source="indexed",
                tags=args.get("tags"),
            )
            return {
                "success": True,
                "knowledge_id": knowledge_id,
                "indexed_in": args["domain"],
                "tags": args.get("tags", []),
            }

        elif name == "search_archives":
            results = []

            # Search knowledge
            if args.get("domains"):
                for domain in args["domains"]:
                    knowledge = await self.db.search_knowledge(
                        domain=domain,
                        query=args["query"],
                        tags=args.get("tags"),
                        limit=args.get("limit", 20) // len(args["domains"]),
                    )
                    results.extend(knowledge)
            else:
                results = await self.db.search_knowledge(
                    query=args["query"],
                    tags=args.get("tags"),
                    limit=args.get("limit", 20),
                )

            return {
                "query": args["query"],
                "count": len(results),
                "results": results,
            }

        elif name == "adjudicate_conflict":
            # Convert input to court positions
            court_positions = []
            for pos in args["positions"]:
                evidence_list = []
                for ev in pos.get("evidence", []):
                    evidence_list.append(
                        Evidence(
                            evidence_type=EvidenceType[ev.get("type", "THEORETICAL")],
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

            # Evaluate evidence
            analysis = self.court.evaluate_positions(court_positions)

            # Determine winner
            winner, losers = self.court.determine_winner(court_positions)

            # Build ruling
            ruling = {
                "topic": args["topic"],
                "ruling": f"Position by {winner.advocate} prevails",
                "winning_position": {
                    "advocate": winner.advocate,
                    "position": winner.position,
                    "evidence_strength": winner.total_evidence_strength(),
                },
                "rationale": f"Based on evidence strength analysis. {winner.advocate}'s position has the strongest evidential support with a strength score of {winner.total_evidence_strength():.2f}.",
                "evidence_analysis": analysis,
                "losing_positions": [
                    {
                        "advocate": p.advocate,
                        "position": p.position,
                        "evidence_strength": p.total_evidence_strength(),
                    }
                    for p in losers
                ],
            }

            # Record the case
            case_id = await self.db.record_court_case(
                topic=args["topic"],
                advocates=[{"advocate": p.advocate, "position": p.position} for p in court_positions],
                evidence_presented=[
                    {"advocate": p.advocate, "evidence": [e.to_dict() for e in p.evidence]}
                    for p in court_positions
                ],
                ruling=ruling["ruling"],
                ruling_rationale=ruling["rationale"],
                evidence_analysis=analysis,
            )

            ruling["case_id"] = case_id
            return ruling

        elif name == "get_precedent":
            precedents = await self.db.get_court_precedents(
                topic_query=args["topic"],
                limit=args.get("limit", 5),
            )
            return {
                "topic": args["topic"],
                "count": len(precedents),
                "precedents": precedents,
            }

        else:
            raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        await self.db.initialize()
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


async def main():
    """Main entry point."""
    import yaml

    # Load config
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        db_path = Path(__file__).parent.parent.parent / config["database"]["path"]
    else:
        db_path = Path(__file__).parent.parent.parent / "data" / "country.db"

    ministry = ArchivesMinistry(db_path)
    await ministry.run()


if __name__ == "__main__":
    asyncio.run(main())
