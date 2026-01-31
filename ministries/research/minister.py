"""
Ministry of Research - MCP Server

The Research Ministry is responsible for:
- Information gathering and search
- Analysis and synthesis
- Documentation and writing

Tools:
- search_web: Search for information
- analyze_document: Analyze a document
- synthesize_findings: Combine multiple sources

Resources:
- research_cache: Cached research results
- source_index: Index of sources

Specialists:
- analyst: Deep analysis and pattern recognition
- writer: Documentation and technical writing
- searcher: Information retrieval
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
from genius import GeniusProtocol


class ResearchMinistry:
    """MCP Server for the Ministry of Research."""

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("research-ministry")

        # Ministry state
        self.research_cache = {}
        self.source_index = {}

        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="research://cache",
                    name="Research Cache",
                    description="Cached research results",
                    mimeType="application/json",
                ),
                Resource(
                    uri="research://sources",
                    name="Source Index",
                    description="Index of information sources",
                    mimeType="application/json",
                ),
                Resource(
                    uri="research://findings",
                    name="Research Findings",
                    description="Synthesized research findings",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a resource."""
            if uri == "research://cache":
                data = self.research_cache
            elif uri == "research://sources":
                data = self.source_index
            elif uri == "research://findings":
                # Get recent research from knowledge base
                knowledge = await self.db.search_knowledge(
                    domain="research",
                    limit=50,
                )
                data = {"findings": knowledge}
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
                # Searcher tools
                Tool(
                    name="search_web",
                    description="Search the web for information on a topic.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query",
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Preferred sources (e.g., 'official docs', 'github', 'stackoverflow')",
                            },
                            "recency": {
                                "type": "string",
                                "enum": ["any", "recent", "last_year"],
                                "description": "How recent should sources be",
                            },
                        },
                        "required": ["query"],
                    },
                ),
                Tool(
                    name="search_codebase",
                    description="Search a codebase for patterns or implementations.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "What to search for",
                            },
                            "file_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "File extensions to search (e.g., '.py', '.js')",
                            },
                            "path": {
                                "type": "string",
                                "description": "Path to search in",
                            },
                        },
                        "required": ["pattern"],
                    },
                ),
                # Analyst tools
                Tool(
                    name="analyze_document",
                    description="Analyze a document and extract key information.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Document content to analyze",
                            },
                            "focus": {
                                "type": "string",
                                "description": "What aspect to focus on",
                            },
                            "questions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific questions to answer",
                            },
                        },
                        "required": ["content"],
                    },
                ),
                Tool(
                    name="compare_options",
                    description="Compare multiple options or solutions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "options": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                    },
                                },
                                "description": "Options to compare",
                            },
                            "criteria": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Criteria for comparison",
                            },
                            "context": {
                                "type": "string",
                                "description": "Context for the comparison",
                            },
                        },
                        "required": ["options", "criteria"],
                    },
                ),
                Tool(
                    name="synthesize_findings",
                    description="Synthesize findings from multiple sources into a coherent summary.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "findings": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "source": {"type": "string"},
                                        "content": {"type": "string"},
                                    },
                                },
                                "description": "Findings to synthesize",
                            },
                            "question": {
                                "type": "string",
                                "description": "Question to answer with synthesis",
                            },
                        },
                        "required": ["findings"],
                    },
                ),
                # Writer tools
                Tool(
                    name="write_documentation",
                    description="Write documentation for a feature or system.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "What to document",
                            },
                            "audience": {
                                "type": "string",
                                "description": "Target audience",
                            },
                            "doc_type": {
                                "type": "string",
                                "enum": ["api", "tutorial", "reference", "guide", "adr"],
                                "description": "Type of documentation",
                            },
                            "content_source": {
                                "type": "string",
                                "description": "Source code or content to document",
                            },
                        },
                        "required": ["subject", "doc_type"],
                    },
                ),
                Tool(
                    name="explain_concept",
                    description="Explain a concept at a specified level.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "concept": {
                                "type": "string",
                                "description": "Concept to explain",
                            },
                            "level": {
                                "type": "string",
                                "enum": ["beginner", "intermediate", "expert"],
                                "description": "Explanation level",
                            },
                            "context": {
                                "type": "string",
                                "description": "Context for the explanation",
                            },
                        },
                        "required": ["concept"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            try:
                result = await self._execute_tool(name, arguments)
                return [TextContent(type="text", text=json.dumps(result, default=str, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    async def _execute_tool(self, name: str, args: dict[str, Any]) -> Any:
        """Execute a tool."""

        if name == "search_web":
            task_id = await self.db.create_task(
                ministry="research",
                specialist="searcher",
                task_type="web_search",
                description=f"Search: {args['query']}",
                input_context=args,
            )

            return {
                "query": args["query"],
                "task_id": task_id,
                "status": "needs_external_search",
                "message": "Web search requires external API access",
                "prompt_for_llm": self._build_search_prompt(args),
            }

        elif name == "search_codebase":
            return {
                "pattern": args["pattern"],
                "file_types": args.get("file_types", ["*"]),
                "path": args.get("path", "."),
                "status": "needs_execution",
                "message": "Codebase search requires file system access",
            }

        elif name == "analyze_document":
            task_id = await self.db.create_task(
                ministry="research",
                specialist="analyst",
                task_type="document_analysis",
                description="Document analysis",
                input_context=args,
            )

            return {
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_analysis_prompt(args),
            }

        elif name == "compare_options":
            return {
                "options_count": len(args.get("options", [])),
                "criteria": args.get("criteria", []),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_comparison_prompt(args),
            }

        elif name == "synthesize_findings":
            task_id = await self.db.create_task(
                ministry="research",
                specialist="analyst",
                task_type="synthesis",
                description="Synthesize findings",
                input_context=args,
            )

            return {
                "findings_count": len(args.get("findings", [])),
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_synthesis_prompt(args),
            }

        elif name == "write_documentation":
            task_id = await self.db.create_task(
                ministry="research",
                specialist="writer",
                task_type="documentation",
                description=f"Write {args['doc_type']} for {args['subject']}",
                input_context=args,
            )

            return {
                "subject": args["subject"],
                "doc_type": args["doc_type"],
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_documentation_prompt(args),
            }

        elif name == "explain_concept":
            return {
                "concept": args["concept"],
                "level": args.get("level", "intermediate"),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_explanation_prompt(args),
            }

        else:
            raise ValueError(f"Unknown tool: {name}")

    def _build_search_prompt(self, args: dict) -> str:
        """Build prompt for search."""
        return f"""Research query: {args['query']}

Preferred sources: {', '.join(args.get('sources', ['any']))}
Recency: {args.get('recency', 'any')}

Provide:
1. Key findings from authoritative sources
2. Source evaluation (credibility, recency)
3. Summary of findings
4. Areas of uncertainty or conflicting information
"""

    def _build_analysis_prompt(self, args: dict) -> str:
        """Build prompt for document analysis."""
        questions = args.get('questions', [])
        questions_text = chr(10).join(f"- {q}" for q in questions) if questions else "General analysis"

        return f"""Analyze this document:

{args['content']}

Focus: {args.get('focus', 'general')}

Questions to answer:
{questions_text}

Provide:
1. Key points
2. Patterns or themes
3. Answers to specific questions
4. Gaps or missing information
"""

    def _build_comparison_prompt(self, args: dict) -> str:
        """Build prompt for comparison."""
        options_text = "\n".join(
            f"**{o['name']}**: {o.get('description', 'No description')}"
            for o in args.get('options', [])
        )

        return f"""Compare these options:

{options_text}

Criteria:
{chr(10).join(f'- {c}' for c in args.get('criteria', []))}

Context: {args.get('context', 'General comparison')}

Provide:
1. Comparison matrix (option vs criteria)
2. Strengths of each option
3. Weaknesses of each option
4. Recommendation with rationale
"""

    def _build_synthesis_prompt(self, args: dict) -> str:
        """Build prompt for synthesis."""
        findings_text = "\n\n".join(
            f"**{f.get('source', 'Unknown source')}**:\n{f.get('content', '')}"
            for f in args.get('findings', [])
        )

        return f"""Synthesize these findings:

{findings_text}

Question to answer: {args.get('question', 'What are the key insights?')}

Provide:
1. Synthesized answer
2. Points of agreement across sources
3. Points of disagreement
4. Confidence level and reasoning
"""

    def _build_documentation_prompt(self, args: dict) -> str:
        """Build prompt for documentation."""
        return f"""Write {args['doc_type']} documentation for: {args['subject']}

Target audience: {args.get('audience', 'developers')}

Source content:
{args.get('content_source', 'No source content provided')}

Documentation type guidelines:
- api: Endpoints, parameters, responses, examples
- tutorial: Step-by-step instructions, prerequisites, outcomes
- reference: Comprehensive coverage, organized by feature
- guide: Conceptual explanation, best practices
- adr: Context, decision, consequences, alternatives

Write clear, well-structured documentation following the appropriate format.
"""

    def _build_explanation_prompt(self, args: dict) -> str:
        """Build prompt for concept explanation."""
        return f"""Explain: {args['concept']}

Level: {args.get('level', 'intermediate')}
Context: {args.get('context', 'General context')}

Tailor explanation to the level:
- beginner: Simple terms, analogies, no jargon
- intermediate: Technical terms explained, practical examples
- expert: Deep technical details, edge cases, trade-offs

Provide:
1. Definition/overview
2. How it works
3. Examples
4. Common misconceptions (if any)
"""

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

    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        db_path = Path(__file__).parent.parent.parent / config["database"]["path"]
    else:
        db_path = Path(__file__).parent.parent.parent / "data" / "country.db"

    ministry = ResearchMinistry(db_path)
    await ministry.run()


if __name__ == "__main__":
    asyncio.run(main())
