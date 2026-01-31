"""
Shared Knowledge Server - MCP Server for the Micro-Country

This MCP server provides access to the shared knowledge base:
- Constitution (core rules and values)
- Decision log (historical decisions)
- Project context (current state)
- Domain knowledge (accumulated expertise)
- Task history (what was attempted)

All ministries connect to this server to read and write shared knowledge.
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

from .database import Database


class KnowledgeServer:
    """MCP Server for shared knowledge access."""

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.server = Server("knowledge-server")
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available knowledge resources."""
            return [
                Resource(
                    uri="knowledge://constitution",
                    name="Constitution",
                    description="Core rules and values that govern the Micro-Country",
                    mimeType="application/json",
                ),
                Resource(
                    uri="knowledge://decisions",
                    name="Decision Log",
                    description="Historical decisions with full rationale",
                    mimeType="application/json",
                ),
                Resource(
                    uri="knowledge://projects",
                    name="Project Context",
                    description="Current state of all projects",
                    mimeType="application/json",
                ),
                Resource(
                    uri="knowledge://domain",
                    name="Domain Knowledge",
                    description="Accumulated expertise by domain",
                    mimeType="application/json",
                ),
                Resource(
                    uri="knowledge://tasks",
                    name="Task History",
                    description="What was attempted, what worked",
                    mimeType="application/json",
                ),
                Resource(
                    uri="knowledge://court-cases",
                    name="Evidence Court Cases",
                    description="Conflict resolution records",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a knowledge resource."""
            if uri == "knowledge://constitution":
                data = await self.db.get_constitution()
            elif uri == "knowledge://decisions":
                data = await self.db.get_decisions(limit=100)
            elif uri == "knowledge://projects":
                # Get all projects (simplified - in real impl would have list method)
                async with self.db.connection() as conn:
                    cursor = await conn.execute(
                        "SELECT * FROM project_context ORDER BY updated_at DESC LIMIT 50"
                    )
                    rows = await cursor.fetchall()
                    data = [dict(row) for row in rows]
            elif uri == "knowledge://domain":
                data = await self.db.search_knowledge(limit=100)
            elif uri == "knowledge://tasks":
                data = await self.db.get_task_history(limit=100)
            elif uri == "knowledge://court-cases":
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
            """List available knowledge tools."""
            return [
                # Decision tools
                Tool(
                    name="log_decision",
                    description="Log a decision with full context and rationale",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ministry": {
                                "type": "string",
                                "description": "Which ministry made this decision",
                            },
                            "decision_type": {
                                "type": "string",
                                "description": "Type of decision (design, implementation, etc.)",
                            },
                            "context": {
                                "type": "object",
                                "description": "Context that led to this decision",
                            },
                            "decision": {
                                "type": "string",
                                "description": "The actual decision made",
                            },
                            "rationale": {
                                "type": "string",
                                "description": "Why this decision was made",
                            },
                            "specialist": {
                                "type": "string",
                                "description": "Specific specialist who made the decision",
                            },
                            "options_considered": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Alternatives that were evaluated",
                            },
                            "evidence": {
                                "type": "array",
                                "items": {"type": "object"},
                                "description": "Evidence supporting the decision",
                            },
                        },
                        "required": ["ministry", "decision_type", "context", "decision", "rationale"],
                    },
                ),
                Tool(
                    name="search_decisions",
                    description="Search for past decisions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ministry": {
                                "type": "string",
                                "description": "Filter by ministry",
                            },
                            "decision_type": {
                                "type": "string",
                                "description": "Filter by decision type",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum results to return",
                                "default": 20,
                            },
                        },
                    },
                ),
                # Project tools
                Tool(
                    name="create_project",
                    description="Create a new project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Project name",
                            },
                            "description": {
                                "type": "string",
                                "description": "Project description",
                            },
                            "goals": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Project goals",
                            },
                            "constraints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Project constraints",
                            },
                            "tech_stack": {
                                "type": "object",
                                "description": "Technologies in use",
                            },
                        },
                        "required": ["name"],
                    },
                ),
                Tool(
                    name="get_project",
                    description="Get a project by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_id": {
                                "type": "string",
                                "description": "The project ID",
                            },
                        },
                        "required": ["project_id"],
                    },
                ),
                Tool(
                    name="update_project",
                    description="Update a project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_id": {
                                "type": "string",
                                "description": "The project ID",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["active", "paused", "completed", "archived"],
                            },
                            "current_phase": {"type": "string"},
                            "goals": {"type": "array", "items": {"type": "string"}},
                            "constraints": {"type": "array", "items": {"type": "string"}},
                            "tech_stack": {"type": "object"},
                            "file_structure": {"type": "object"},
                        },
                        "required": ["project_id"],
                    },
                ),
                # Knowledge tools
                Tool(
                    name="store_knowledge",
                    description="Store domain knowledge",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "description": "Knowledge domain (architecture, security, etc.)",
                            },
                            "topic": {
                                "type": "string",
                                "description": "Specific topic",
                            },
                            "content": {
                                "type": "string",
                                "description": "The knowledge content",
                            },
                            "source": {
                                "type": "string",
                                "description": "Where this knowledge came from",
                            },
                            "confidence": {
                                "type": "number",
                                "description": "Confidence level (0.0-1.0)",
                                "default": 0.8,
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Tags for categorization",
                            },
                        },
                        "required": ["domain", "topic", "content"],
                    },
                ),
                Tool(
                    name="search_knowledge",
                    description="Search domain knowledge",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "description": "Filter by domain",
                            },
                            "query": {
                                "type": "string",
                                "description": "Search query",
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
                    },
                ),
                # Task tools
                Tool(
                    name="create_task",
                    description="Create a new task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ministry": {
                                "type": "string",
                                "description": "Which ministry owns this task",
                            },
                            "task_type": {
                                "type": "string",
                                "description": "Type of task",
                            },
                            "description": {
                                "type": "string",
                                "description": "Task description",
                            },
                            "specialist": {
                                "type": "string",
                                "description": "Assigned specialist",
                            },
                            "project_id": {
                                "type": "string",
                                "description": "Associated project",
                            },
                            "input_context": {
                                "type": "object",
                                "description": "Input context for the task",
                            },
                        },
                        "required": ["ministry", "task_type", "description"],
                    },
                ),
                Tool(
                    name="update_task",
                    description="Update a task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The task ID",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed", "failed"],
                            },
                            "approach": {"type": "string"},
                            "output": {"type": "object"},
                            "success": {"type": "boolean"},
                            "lessons_learned": {"type": "string"},
                            "duration_ms": {"type": "integer"},
                        },
                        "required": ["task_id"],
                    },
                ),
                Tool(
                    name="get_task_history",
                    description="Get task history",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ministry": {"type": "string"},
                            "project_id": {"type": "string"},
                            "status": {"type": "string"},
                            "limit": {"type": "integer", "default": 50},
                        },
                    },
                ),
                # Court case tools
                Tool(
                    name="record_court_case",
                    description="Record an Evidence Court case",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "What the conflict is about",
                            },
                            "advocates": {
                                "type": "array",
                                "items": {"type": "object"},
                                "description": "Positions and their advocates",
                            },
                            "evidence_presented": {
                                "type": "array",
                                "items": {"type": "object"},
                                "description": "Evidence for each position",
                            },
                            "ruling": {
                                "type": "string",
                                "description": "The court's decision",
                            },
                            "ruling_rationale": {
                                "type": "string",
                                "description": "Why this ruling",
                            },
                            "evidence_analysis": {"type": "object"},
                            "dissenting_opinions": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "precedent_set": {"type": "string"},
                        },
                        "required": ["topic", "advocates", "evidence_presented", "ruling", "ruling_rationale"],
                    },
                ),
                Tool(
                    name="search_precedents",
                    description="Search for court precedents",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic_query": {
                                "type": "string",
                                "description": "Search query for topic or precedent",
                            },
                            "limit": {"type": "integer", "default": 10},
                        },
                    },
                ),
                # Reasoning trace tools
                Tool(
                    name="save_reasoning_trace",
                    description="Save a genius reasoning trace",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "specialist": {"type": "string"},
                            "observe": {"type": "string"},
                            "think": {"type": "string"},
                            "reflect": {"type": "string"},
                            "critique": {"type": "string"},
                            "refine": {"type": "string"},
                            "act": {"type": "string"},
                            "verify": {"type": "string"},
                            "task_id": {"type": "string"},
                            "quality_score": {"type": "number"},
                        },
                        "required": ["specialist", "observe", "think", "reflect", "critique", "refine", "act", "verify"],
                    },
                ),
                # Cross-ministry request tools
                Tool(
                    name="create_cross_ministry_request",
                    description="Create a request to another ministry",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "from_ministry": {"type": "string"},
                            "to_ministry": {"type": "string"},
                            "request_type": {"type": "string"},
                            "request_content": {"type": "object"},
                        },
                        "required": ["from_ministry", "to_ministry", "request_type", "request_content"],
                    },
                ),
                Tool(
                    name="respond_to_request",
                    description="Respond to a cross-ministry request",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "request_id": {"type": "string"},
                            "response_content": {"type": "object"},
                            "status": {
                                "type": "string",
                                "enum": ["completed", "failed"],
                                "default": "completed",
                            },
                        },
                        "required": ["request_id", "response_content"],
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
        """Execute a tool and return the result."""
        if name == "log_decision":
            decision_id = await self.db.log_decision(
                ministry=args["ministry"],
                decision_type=args["decision_type"],
                context=args["context"],
                decision=args["decision"],
                rationale=args["rationale"],
                specialist=args.get("specialist"),
                options_considered=args.get("options_considered"),
                evidence=args.get("evidence"),
            )
            return {"success": True, "decision_id": decision_id}

        elif name == "search_decisions":
            return await self.db.get_decisions(
                ministry=args.get("ministry"),
                decision_type=args.get("decision_type"),
                limit=args.get("limit", 20),
            )

        elif name == "create_project":
            project_id = await self.db.create_project(
                name=args["name"],
                description=args.get("description"),
                goals=args.get("goals"),
                constraints=args.get("constraints"),
                tech_stack=args.get("tech_stack"),
            )
            return {"success": True, "project_id": project_id}

        elif name == "get_project":
            project = await self.db.get_project(args["project_id"])
            if project:
                return project
            return {"error": "Project not found"}

        elif name == "update_project":
            project_id = args.pop("project_id")
            success = await self.db.update_project(project_id, **args)
            return {"success": success}

        elif name == "store_knowledge":
            knowledge_id = await self.db.store_knowledge(
                domain=args["domain"],
                topic=args["topic"],
                content=args["content"],
                source=args.get("source"),
                confidence=args.get("confidence", 0.8),
                tags=args.get("tags"),
            )
            return {"success": True, "knowledge_id": knowledge_id}

        elif name == "search_knowledge":
            return await self.db.search_knowledge(
                domain=args.get("domain"),
                query=args.get("query"),
                tags=args.get("tags"),
                limit=args.get("limit", 20),
            )

        elif name == "create_task":
            task_id = await self.db.create_task(
                ministry=args["ministry"],
                task_type=args["task_type"],
                description=args["description"],
                specialist=args.get("specialist"),
                project_id=args.get("project_id"),
                input_context=args.get("input_context"),
            )
            return {"success": True, "task_id": task_id}

        elif name == "update_task":
            task_id = args.pop("task_id")
            success = await self.db.update_task(task_id, **args)
            return {"success": success}

        elif name == "get_task_history":
            return await self.db.get_task_history(
                ministry=args.get("ministry"),
                project_id=args.get("project_id"),
                status=args.get("status"),
                limit=args.get("limit", 50),
            )

        elif name == "record_court_case":
            case_id = await self.db.record_court_case(
                topic=args["topic"],
                advocates=args["advocates"],
                evidence_presented=args["evidence_presented"],
                ruling=args["ruling"],
                ruling_rationale=args["ruling_rationale"],
                evidence_analysis=args.get("evidence_analysis"),
                dissenting_opinions=args.get("dissenting_opinions"),
                precedent_set=args.get("precedent_set"),
            )
            return {"success": True, "case_id": case_id}

        elif name == "search_precedents":
            return await self.db.get_court_precedents(
                topic_query=args.get("topic_query"),
                limit=args.get("limit", 10),
            )

        elif name == "save_reasoning_trace":
            trace_id = await self.db.save_reasoning_trace(
                specialist=args["specialist"],
                observe=args["observe"],
                think=args["think"],
                reflect=args["reflect"],
                critique=args["critique"],
                refine=args["refine"],
                act=args["act"],
                verify=args["verify"],
                task_id=args.get("task_id"),
                quality_score=args.get("quality_score"),
            )
            return {"success": True, "trace_id": trace_id}

        elif name == "create_cross_ministry_request":
            request_id = await self.db.create_cross_ministry_request(
                from_ministry=args["from_ministry"],
                to_ministry=args["to_ministry"],
                request_type=args["request_type"],
                request_content=args["request_content"],
            )
            return {"success": True, "request_id": request_id}

        elif name == "respond_to_request":
            success = await self.db.respond_to_request(
                request_id=args["request_id"],
                response_content=args["response_content"],
                status=args.get("status", "completed"),
            )
            return {"success": success}

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
    import sys
    import yaml

    # Load config
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        db_path = Path(__file__).parent.parent / config["database"]["path"]
    else:
        db_path = Path(__file__).parent.parent / "data" / "country.db"

    server = KnowledgeServer(db_path)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
