"""
Ministry of Quality - MCP Server

The Quality Ministry is responsible for:
- Testing (unit, integration, e2e)
- Security auditing
- Code review
- Validation and verification

Tools:
- run_tests: Execute test suites
- security_audit: Perform security review
- review_code: Code quality review

Resources:
- test_results: Latest test outcomes
- coverage_metrics: Code coverage data

Specialists:
- tester: Test design and execution
- auditor: Security analysis
- validator: Verification and validation
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


class QualityMinistry:
    """MCP Server for the Ministry of Quality."""

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("quality-ministry")

        # Ministry state
        self.test_results = {}
        self.coverage_metrics = {}
        self.security_findings = []

        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="quality://test-results",
                    name="Test Results",
                    description="Latest test execution results",
                    mimeType="application/json",
                ),
                Resource(
                    uri="quality://coverage",
                    name="Coverage Metrics",
                    description="Code coverage data",
                    mimeType="application/json",
                ),
                Resource(
                    uri="quality://security-findings",
                    name="Security Findings",
                    description="Security audit findings",
                    mimeType="application/json",
                ),
                Resource(
                    uri="quality://quality-gates",
                    name="Quality Gates",
                    description="Quality gate definitions and status",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a resource."""
            if uri == "quality://test-results":
                data = self.test_results
            elif uri == "quality://coverage":
                data = self.coverage_metrics
            elif uri == "quality://security-findings":
                data = self.security_findings
            elif uri == "quality://quality-gates":
                data = {
                    "gates": [
                        {"name": "tests_pass", "required": True},
                        {"name": "coverage_minimum", "threshold": 80},
                        {"name": "no_critical_security", "required": True},
                        {"name": "code_review_approved", "required": True},
                    ],
                    "status": "not_evaluated",
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
                # Tester tools
                Tool(
                    name="design_test_cases",
                    description="Design test cases for a feature or component.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "What feature to test",
                            },
                            "code": {
                                "type": "string",
                                "description": "The code to test",
                            },
                            "requirements": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Requirements to verify",
                            },
                            "test_type": {
                                "type": "string",
                                "enum": ["unit", "integration", "e2e"],
                                "description": "Type of tests to design",
                            },
                        },
                        "required": ["feature"],
                    },
                ),
                Tool(
                    name="run_tests",
                    description="Execute tests and report results.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_path": {
                                "type": "string",
                                "description": "Path to test files",
                            },
                            "test_framework": {
                                "type": "string",
                                "description": "Test framework (pytest, jest, etc.)",
                            },
                            "coverage": {
                                "type": "boolean",
                                "default": True,
                                "description": "Collect coverage data",
                            },
                        },
                        "required": ["test_path"],
                    },
                ),
                Tool(
                    name="analyze_coverage",
                    description="Analyze code coverage and identify gaps.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "coverage_data": {
                                "type": "object",
                                "description": "Coverage data to analyze",
                            },
                            "threshold": {
                                "type": "number",
                                "default": 80,
                                "description": "Minimum coverage threshold",
                            },
                        },
                    },
                ),
                # Auditor tools
                Tool(
                    name="security_audit",
                    description="Perform a security audit on code.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Code to audit",
                            },
                            "context": {
                                "type": "string",
                                "description": "Context about what the code does",
                            },
                            "focus_areas": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific areas to focus on",
                            },
                        },
                        "required": ["code"],
                    },
                ),
                Tool(
                    name="check_vulnerabilities",
                    description="Check for known vulnerabilities in dependencies.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dependencies": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "version": {"type": "string"},
                                    },
                                },
                                "description": "List of dependencies to check",
                            },
                        },
                        "required": ["dependencies"],
                    },
                ),
                Tool(
                    name="review_code",
                    description="Perform a code review focusing on quality and security.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Code to review",
                            },
                            "review_type": {
                                "type": "string",
                                "enum": ["security", "quality", "both"],
                                "default": "both",
                            },
                            "context": {
                                "type": "string",
                                "description": "Context about the code",
                            },
                        },
                        "required": ["code"],
                    },
                ),
                # Validator tools
                Tool(
                    name="validate_requirements",
                    description="Validate that implementation meets requirements.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "requirements": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Requirements to validate",
                            },
                            "implementation": {
                                "type": "string",
                                "description": "Implementation to validate against",
                            },
                            "evidence": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Evidence of implementation",
                            },
                        },
                        "required": ["requirements", "implementation"],
                    },
                ),
                Tool(
                    name="check_quality_gates",
                    description="Check if quality gates are passed.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_results": {"type": "object"},
                            "coverage": {"type": "number"},
                            "security_findings": {"type": "array"},
                            "review_approved": {"type": "boolean"},
                        },
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

        if name == "design_test_cases":
            task_id = await self.db.create_task(
                ministry="quality",
                specialist="tester",
                task_type="test_design",
                description=f"Design tests for: {args['feature']}",
                input_context=args,
            )

            return {
                "feature": args["feature"],
                "test_type": args.get("test_type", "unit"),
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_test_design_prompt(args),
            }

        elif name == "run_tests":
            # In real implementation, would execute tests
            return {
                "test_path": args["test_path"],
                "framework": args.get("test_framework", "pytest"),
                "status": "needs_execution",
                "message": "Test execution requires shell access",
            }

        elif name == "analyze_coverage":
            threshold = args.get("threshold", 80)
            coverage_data = args.get("coverage_data", {})

            analysis = {
                "threshold": threshold,
                "overall_coverage": coverage_data.get("total", 0),
                "meets_threshold": coverage_data.get("total", 0) >= threshold,
                "gaps": [],
                "recommendations": [],
            }

            if not analysis["meets_threshold"]:
                analysis["recommendations"].append(
                    f"Coverage is below {threshold}%. Add tests for uncovered code."
                )

            return analysis

        elif name == "security_audit":
            task_id = await self.db.create_task(
                ministry="quality",
                specialist="auditor",
                task_type="security_audit",
                description="Security audit",
                input_context=args,
            )

            return {
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_security_audit_prompt(args),
            }

        elif name == "check_vulnerabilities":
            # In real implementation, would check vulnerability databases
            return {
                "dependencies_checked": len(args.get("dependencies", [])),
                "vulnerabilities_found": [],
                "status": "needs_external_check",
                "message": "Vulnerability check requires external database access",
            }

        elif name == "review_code":
            task_id = await self.db.create_task(
                ministry="quality",
                specialist="auditor",
                task_type="code_review",
                description="Code review",
                input_context=args,
            )

            return {
                "review_type": args.get("review_type", "both"),
                "task_id": task_id,
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_review_prompt(args),
            }

        elif name == "validate_requirements":
            return {
                "requirements_count": len(args.get("requirements", [])),
                "status": "needs_llm_generation",
                "prompt_for_llm": self._build_validation_prompt(args),
            }

        elif name == "check_quality_gates":
            gates = {
                "tests_pass": args.get("test_results", {}).get("all_passed", False),
                "coverage_minimum": args.get("coverage", 0) >= 80,
                "no_critical_security": len([
                    f for f in args.get("security_findings", [])
                    if f.get("severity") == "critical"
                ]) == 0,
                "review_approved": args.get("review_approved", False),
            }

            all_passed = all(gates.values())

            return {
                "gates": gates,
                "all_passed": all_passed,
                "blocking_gates": [g for g, passed in gates.items() if not passed],
            }

        else:
            raise ValueError(f"Unknown tool: {name}")

    def _build_test_design_prompt(self, args: dict) -> str:
        """Build prompt for test design."""
        return f"""Design test cases for: {args['feature']}

Test type: {args.get('test_type', 'unit')}

Code to test:
```
{args.get('code', 'No code provided')}
```

Requirements to verify:
{chr(10).join(f'- {r}' for r in args.get('requirements', ['No specific requirements']))}

Design test cases covering:
1. Happy path (normal operation)
2. Edge cases
3. Error cases
4. Security considerations (if applicable)

For each test case, provide:
- Name
- Description
- Setup/preconditions
- Input
- Expected output
- Assertions
"""

    def _build_security_audit_prompt(self, args: dict) -> str:
        """Build prompt for security audit."""
        return f"""Perform security audit on:

```
{args['code']}
```

Context: {args.get('context', 'No context provided')}

Focus areas: {', '.join(args.get('focus_areas', ['general security']))}

Check for:
1. OWASP Top 10 vulnerabilities
2. Input validation issues
3. Authentication/authorization flaws
4. Data exposure risks
5. Injection vulnerabilities
6. Cryptography issues

For each finding:
- Severity: Critical/High/Medium/Low
- Description
- Location in code
- Remediation recommendation
"""

    def _build_review_prompt(self, args: dict) -> str:
        """Build prompt for code review."""
        return f"""Review this code for {args.get('review_type', 'quality and security')}:

```
{args['code']}
```

Context: {args.get('context', 'No context provided')}

Evaluate:
1. Code quality (readability, maintainability)
2. Error handling
3. Security issues
4. Performance concerns
5. Best practices adherence

Provide:
- Issues found (with severity)
- Positive aspects
- Suggestions for improvement
- Overall verdict (APPROVE / NEEDS_REVISION / REJECT)
"""

    def _build_validation_prompt(self, args: dict) -> str:
        """Build prompt for requirement validation."""
        requirements = args.get('requirements', [])
        return f"""Validate implementation against requirements:

Requirements:
{chr(10).join(f'{i+1}. {r}' for i, r in enumerate(requirements))}

Implementation:
{args['implementation']}

Evidence:
{chr(10).join(f'- {e}' for e in args.get('evidence', ['No evidence provided']))}

For each requirement:
- Status: MET / PARTIALLY_MET / NOT_MET
- Evidence of compliance
- Gaps (if any)
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

    ministry = QualityMinistry(db_path)
    await ministry.run()


if __name__ == "__main__":
    asyncio.run(main())
