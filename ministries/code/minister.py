"""
Ministry of Code - MCP Server

The Code Ministry is responsible for:
- Software architecture and design
- Code implementation
- Debugging and troubleshooting

Tools:
- implement_feature: Write code for a feature
- refactor_code: Improve existing code
- debug_issue: Investigate and fix bugs

Resources:
- codebase_map: Structure of the project
- tech_stack: Technologies in use

Specialists:
- architect: System design and architecture
- coder: Implementation
- debugger: Bug investigation and fixing
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


class CodeMinistry:
    """MCP Server for the Ministry of Code."""

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("code-ministry")

        # Ministry state
        self.current_project = None
        self.codebase_map = {}
        self.tech_stack = {}

        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="code://codebase-map",
                    name="Codebase Map",
                    description="Structure and organization of the codebase",
                    mimeType="application/json",
                ),
                Resource(
                    uri="code://tech-stack",
                    name="Technology Stack",
                    description="Technologies, frameworks, and tools in use",
                    mimeType="application/json",
                ),
                Resource(
                    uri="code://architecture",
                    name="Architecture Overview",
                    description="System architecture and design decisions",
                    mimeType="application/json",
                ),
                Resource(
                    uri="code://conventions",
                    name="Coding Conventions",
                    description="Project coding standards and conventions",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a resource."""
            if uri == "code://codebase-map":
                data = self.codebase_map
            elif uri == "code://tech-stack":
                data = self.tech_stack
            elif uri == "code://architecture":
                # Get architecture decisions from knowledge base
                decisions = await self.db.get_decisions(
                    ministry="code",
                    decision_type="design",
                    limit=20,
                )
                data = {"decisions": decisions}
            elif uri == "code://conventions":
                data = {
                    "language_conventions": {},
                    "naming_conventions": {},
                    "file_organization": {},
                }
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
                # Architect tools
                Tool(
                    name="design_architecture",
                    description="Design system architecture for a feature or component. Produces design documents with trade-off analysis.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "What feature/system to design",
                            },
                            "requirements": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Functional requirements",
                            },
                            "constraints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Non-functional requirements and constraints",
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context about the system",
                            },
                        },
                        "required": ["feature", "requirements"],
                    },
                ),
                Tool(
                    name="review_design",
                    description="Review a design proposal and provide feedback.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "design": {
                                "type": "string",
                                "description": "The design to review",
                            },
                            "criteria": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific criteria to evaluate",
                            },
                        },
                        "required": ["design"],
                    },
                ),
                # Coder tools
                Tool(
                    name="implement_feature",
                    description="Write code to implement a feature based on requirements or design.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "What feature to implement",
                            },
                            "design": {
                                "type": "string",
                                "description": "Design or specification to follow",
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language to use",
                            },
                            "file_path": {
                                "type": "string",
                                "description": "Where to create the file",
                            },
                            "existing_code": {
                                "type": "string",
                                "description": "Existing code to integrate with",
                            },
                        },
                        "required": ["feature"],
                    },
                ),
                Tool(
                    name="refactor_code",
                    description="Improve existing code without changing its behavior.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to refactor",
                            },
                            "goals": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Refactoring goals (readability, performance, etc.)",
                            },
                            "constraints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Things that must not change",
                            },
                        },
                        "required": ["code"],
                    },
                ),
                Tool(
                    name="explain_code",
                    description="Explain what a piece of code does.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to explain",
                            },
                            "level": {
                                "type": "string",
                                "enum": ["beginner", "intermediate", "expert"],
                                "description": "Explanation detail level",
                            },
                        },
                        "required": ["code"],
                    },
                ),
                # Debugger tools
                Tool(
                    name="debug_issue",
                    description="Investigate and diagnose a bug or issue.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Description of the issue",
                            },
                            "error_message": {
                                "type": "string",
                                "description": "Error message if any",
                            },
                            "code": {
                                "type": "string",
                                "description": "Relevant code",
                            },
                            "expected_behavior": {
                                "type": "string",
                                "description": "What should happen",
                            },
                            "actual_behavior": {
                                "type": "string",
                                "description": "What actually happens",
                            },
                            "reproduction_steps": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Steps to reproduce",
                            },
                        },
                        "required": ["description"],
                    },
                ),
                Tool(
                    name="fix_bug",
                    description="Propose a fix for an identified bug.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The buggy code",
                            },
                            "bug_description": {
                                "type": "string",
                                "description": "What the bug is",
                            },
                            "root_cause": {
                                "type": "string",
                                "description": "Identified root cause",
                            },
                        },
                        "required": ["code", "bug_description"],
                    },
                ),
                # Project management
                Tool(
                    name="set_project_context",
                    description="Set the current project context.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_id": {
                                "type": "string",
                                "description": "Project identifier",
                            },
                            "codebase_map": {
                                "type": "object",
                                "description": "Structure of the codebase",
                            },
                            "tech_stack": {
                                "type": "object",
                                "description": "Technologies in use",
                            },
                        },
                        "required": ["project_id"],
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

        if name == "design_architecture":
            # Create design task
            task_id = await self.db.create_task(
                ministry="code",
                specialist="architect",
                task_type="design",
                description=f"Design architecture for: {args['feature']}",
                input_context=args,
            )

            # Build design output (would use LLM in full implementation)
            design = {
                "feature": args["feature"],
                "requirements": args.get("requirements", []),
                "constraints": args.get("constraints", []),
                "design": {
                    "overview": f"Architecture design for {args['feature']}",
                    "components": [],
                    "data_flow": [],
                    "trade_offs": [],
                },
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_architect_prompt(args),
            }

            return design

        elif name == "review_design":
            # Build review output
            review = {
                "design_summary": args["design"][:200] + "...",
                "criteria": args.get("criteria", ["correctness", "scalability", "maintainability"]),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_review_prompt(args),
            }
            return review

        elif name == "implement_feature":
            task_id = await self.db.create_task(
                ministry="code",
                specialist="coder",
                task_type="implementation",
                description=f"Implement: {args['feature']}",
                input_context=args,
            )

            implementation = {
                "feature": args["feature"],
                "language": args.get("language", "python"),
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_coder_prompt(args),
            }
            return implementation

        elif name == "refactor_code":
            refactoring = {
                "original_code": args["code"][:500] + "..." if len(args["code"]) > 500 else args["code"],
                "goals": args.get("goals", ["readability", "maintainability"]),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_refactor_prompt(args),
            }
            return refactoring

        elif name == "explain_code":
            explanation = {
                "code_preview": args["code"][:300] + "...",
                "level": args.get("level", "intermediate"),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_explain_prompt(args),
            }
            return explanation

        elif name == "debug_issue":
            task_id = await self.db.create_task(
                ministry="code",
                specialist="debugger",
                task_type="debugging",
                description=f"Debug: {args['description']}",
                input_context=args,
            )

            debugging = {
                "issue": args["description"],
                "error": args.get("error_message"),
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_debug_prompt(args),
            }
            return debugging

        elif name == "fix_bug":
            fix = {
                "bug": args["bug_description"],
                "root_cause": args.get("root_cause", "Not yet identified"),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_fix_prompt(args),
            }
            return fix

        elif name == "set_project_context":
            self.current_project = args["project_id"]
            if "codebase_map" in args:
                self.codebase_map = args["codebase_map"]
            if "tech_stack" in args:
                self.tech_stack = args["tech_stack"]

            return {
                "success": True,
                "project_id": self.current_project,
                "message": f"Project context set to {args['project_id']}",
            }

        else:
            raise ValueError(f"Unknown tool: {name}")

    def _build_architect_prompt(self, args: dict) -> str:
        """Build prompt for architect specialist."""
        return f"""Design architecture for: {args['feature']}

Requirements:
{chr(10).join(f'- {r}' for r in args.get('requirements', []))}

Constraints:
{chr(10).join(f'- {c}' for c in args.get('constraints', []))}

Context: {args.get('context', 'No additional context provided')}

Please provide:
1. High-level architecture overview
2. Component breakdown
3. Data flow
4. API design (if applicable)
5. Trade-off analysis (at least 2 trade-offs)
6. Recommended approach with rationale
"""

    def _build_review_prompt(self, args: dict) -> str:
        """Build prompt for design review."""
        return f"""Review the following design:

{args['design']}

Evaluate based on:
{chr(10).join(f'- {c}' for c in args.get('criteria', ['correctness', 'scalability', 'maintainability']))}

Provide:
1. Strengths
2. Weaknesses
3. Risks
4. Suggestions for improvement
5. Overall assessment (APPROVE / NEEDS_REVISION / REJECT)
"""

    def _build_coder_prompt(self, args: dict) -> str:
        """Build prompt for coder specialist."""
        return f"""Implement: {args['feature']}

Language: {args.get('language', 'python')}

Design/Specification:
{args.get('design', 'No design provided - use best judgment')}

Existing code to integrate with:
{args.get('existing_code', 'No existing code - start fresh')}

Requirements:
- Write clean, readable code
- Include error handling
- Add comments where logic is complex
- Follow language conventions
"""

    def _build_refactor_prompt(self, args: dict) -> str:
        """Build prompt for refactoring."""
        return f"""Refactor the following code:

```
{args['code']}
```

Goals:
{chr(10).join(f'- {g}' for g in args.get('goals', ['readability']))}

Constraints (must not change):
{chr(10).join(f'- {c}' for c in args.get('constraints', ['external behavior']))}

Provide:
1. Refactored code
2. Explanation of changes
3. Before/after comparison of key improvements
"""

    def _build_explain_prompt(self, args: dict) -> str:
        """Build prompt for code explanation."""
        return f"""Explain this code at {args.get('level', 'intermediate')} level:

```
{args['code']}
```

Include:
1. What the code does (overview)
2. How it works (step by step)
3. Key concepts used
4. Any potential issues or improvements
"""

    def _build_debug_prompt(self, args: dict) -> str:
        """Build prompt for debugger specialist."""
        return f"""Debug this issue:

Description: {args['description']}

Error message: {args.get('error_message', 'No error message')}

Expected behavior: {args.get('expected_behavior', 'Not specified')}

Actual behavior: {args.get('actual_behavior', 'Not specified')}

Reproduction steps:
{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(args.get('reproduction_steps', ['Not provided'])))}

Code:
```
{args.get('code', 'No code provided')}
```

Provide:
1. Analysis of the issue
2. Hypotheses for root cause
3. Diagnostic steps to confirm
4. Recommended fix
"""

    def _build_fix_prompt(self, args: dict) -> str:
        """Build prompt for bug fix."""
        return f"""Fix this bug:

Bug description: {args['bug_description']}

Root cause: {args.get('root_cause', 'Not yet identified')}

Code:
```
{args['code']}
```

Provide:
1. Fixed code
2. Explanation of the fix
3. How to verify the fix works
4. Suggestions to prevent similar bugs
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

    ministry = CodeMinistry(db_path)
    await ministry.run()


if __name__ == "__main__":
    asyncio.run(main())
