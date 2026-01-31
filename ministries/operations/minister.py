"""
Ministry of Operations - MCP Server

The Operations Ministry is responsible for:
- File system operations
- Command execution
- Deployment and releases

Tools:
- manage_files: File operations (create, read, update, delete)
- run_commands: Execute shell commands
- deploy_service: Deploy applications

Resources:
- system_state: Current system status
- logs: System and application logs

Specialists:
- file_manager: File system operations
- shell_runner: Command execution
- deployer: Deployment management
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


class OperationsMinistry:
    """MCP Server for the Ministry of Operations."""

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("operations-ministry")

        # Ministry state
        self.system_state = {}
        self.command_history = []

        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="ops://system-state",
                    name="System State",
                    description="Current system status and health",
                    mimeType="application/json",
                ),
                Resource(
                    uri="ops://command-history",
                    name="Command History",
                    description="History of executed commands",
                    mimeType="application/json",
                ),
                Resource(
                    uri="ops://deployments",
                    name="Deployment Status",
                    description="Status of deployments",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a resource."""
            if uri == "ops://system-state":
                data = self.system_state
            elif uri == "ops://command-history":
                data = {"commands": self.command_history[-50:]}  # Last 50
            elif uri == "ops://deployments":
                # Get deployment tasks from history
                tasks = await self.db.get_task_history(
                    ministry="operations",
                    limit=20,
                )
                deployment_tasks = [t for t in tasks if t.get("task_type") == "deployment"]
                data = {"deployments": deployment_tasks}
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
                # File manager tools
                Tool(
                    name="read_file",
                    description="Read contents of a file.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to file",
                            },
                            "encoding": {
                                "type": "string",
                                "default": "utf-8",
                            },
                        },
                        "required": ["path"],
                    },
                ),
                Tool(
                    name="write_file",
                    description="Write content to a file.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to file",
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write",
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["write", "append"],
                                "default": "write",
                            },
                        },
                        "required": ["path", "content"],
                    },
                ),
                Tool(
                    name="list_directory",
                    description="List contents of a directory.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Directory path",
                            },
                            "pattern": {
                                "type": "string",
                                "description": "Glob pattern to filter",
                            },
                            "recursive": {
                                "type": "boolean",
                                "default": False,
                            },
                        },
                        "required": ["path"],
                    },
                ),
                Tool(
                    name="manage_files",
                    description="Perform file operations (copy, move, delete).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["copy", "move", "delete", "mkdir"],
                            },
                            "source": {
                                "type": "string",
                                "description": "Source path",
                            },
                            "destination": {
                                "type": "string",
                                "description": "Destination path (for copy/move)",
                            },
                        },
                        "required": ["operation", "source"],
                    },
                ),
                # Shell runner tools
                Tool(
                    name="run_command",
                    description="Execute a shell command.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Command to execute",
                            },
                            "working_dir": {
                                "type": "string",
                                "description": "Working directory",
                            },
                            "timeout": {
                                "type": "integer",
                                "default": 60,
                                "description": "Timeout in seconds",
                            },
                            "env": {
                                "type": "object",
                                "description": "Environment variables",
                            },
                        },
                        "required": ["command"],
                    },
                ),
                Tool(
                    name="check_process",
                    description="Check if a process is running.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Process name or pattern",
                            },
                            "pid": {
                                "type": "integer",
                                "description": "Process ID",
                            },
                        },
                    },
                ),
                # Deployer tools
                Tool(
                    name="deploy",
                    description="Deploy a service or application.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "Service to deploy",
                            },
                            "environment": {
                                "type": "string",
                                "enum": ["development", "staging", "production"],
                            },
                            "version": {
                                "type": "string",
                                "description": "Version to deploy",
                            },
                            "strategy": {
                                "type": "string",
                                "enum": ["rolling", "blue-green", "canary"],
                                "default": "rolling",
                            },
                        },
                        "required": ["service", "environment"],
                    },
                ),
                Tool(
                    name="rollback",
                    description="Rollback a deployment.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "Service to rollback",
                            },
                            "environment": {
                                "type": "string",
                                "description": "Environment",
                            },
                            "version": {
                                "type": "string",
                                "description": "Version to rollback to",
                            },
                        },
                        "required": ["service", "environment"],
                    },
                ),
                Tool(
                    name="check_health",
                    description="Check health of a service.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "Service to check",
                            },
                            "endpoint": {
                                "type": "string",
                                "description": "Health check endpoint",
                            },
                        },
                        "required": ["service"],
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

        if name == "read_file":
            path = Path(args["path"])
            if not path.exists():
                return {"error": f"File not found: {path}"}
            if not path.is_file():
                return {"error": f"Not a file: {path}"}

            try:
                content = path.read_text(encoding=args.get("encoding", "utf-8"))
                return {
                    "path": str(path),
                    "content": content,
                    "size": len(content),
                }
            except Exception as e:
                return {"error": str(e)}

        elif name == "write_file":
            path = Path(args["path"])
            mode = args.get("mode", "write")

            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                if mode == "append":
                    with open(path, "a", encoding="utf-8") as f:
                        f.write(args["content"])
                else:
                    path.write_text(args["content"], encoding="utf-8")

                return {
                    "success": True,
                    "path": str(path),
                    "mode": mode,
                    "bytes_written": len(args["content"]),
                }
            except Exception as e:
                return {"error": str(e)}

        elif name == "list_directory":
            path = Path(args["path"])
            if not path.exists():
                return {"error": f"Directory not found: {path}"}
            if not path.is_dir():
                return {"error": f"Not a directory: {path}"}

            try:
                pattern = args.get("pattern", "*")
                if args.get("recursive"):
                    entries = list(path.rglob(pattern))
                else:
                    entries = list(path.glob(pattern))

                items = []
                for entry in entries[:100]:  # Limit results
                    items.append({
                        "name": entry.name,
                        "path": str(entry),
                        "is_dir": entry.is_dir(),
                        "size": entry.stat().st_size if entry.is_file() else None,
                    })

                return {
                    "path": str(path),
                    "count": len(items),
                    "items": items,
                }
            except Exception as e:
                return {"error": str(e)}

        elif name == "manage_files":
            operation = args["operation"]
            source = Path(args["source"])

            if operation == "mkdir":
                try:
                    source.mkdir(parents=True, exist_ok=True)
                    return {"success": True, "created": str(source)}
                except Exception as e:
                    return {"error": str(e)}

            if not source.exists():
                return {"error": f"Source not found: {source}"}

            if operation == "delete":
                # Safety: don't delete without explicit confirmation
                return {
                    "status": "needs_confirmation",
                    "message": f"Delete operation requires explicit confirmation for: {source}",
                    "target": str(source),
                }

            elif operation in ["copy", "move"]:
                if "destination" not in args:
                    return {"error": "Destination required for copy/move"}
                dest = Path(args["destination"])

                return {
                    "status": "needs_execution",
                    "operation": operation,
                    "source": str(source),
                    "destination": str(dest),
                    "message": "File operations require shell execution",
                }

        elif name == "run_command":
            # Log the command
            self.command_history.append({
                "command": args["command"],
                "working_dir": args.get("working_dir"),
                "status": "logged",
            })

            # Command execution is a sensitive operation
            return {
                "status": "needs_execution",
                "command": args["command"],
                "working_dir": args.get("working_dir", "."),
                "timeout": args.get("timeout", 60),
                "message": "Command execution requires shell access",
            }

        elif name == "check_process":
            return {
                "status": "needs_execution",
                "message": "Process check requires system access",
                "name": args.get("name"),
                "pid": args.get("pid"),
            }

        elif name == "deploy":
            task_id = await self.db.create_task(
                ministry="operations",
                specialist="deployer",
                task_type="deployment",
                description=f"Deploy {args['service']} to {args['environment']}",
                input_context=args,
            )

            return {
                "task_id": task_id,
                "service": args["service"],
                "environment": args["environment"],
                "version": args.get("version", "latest"),
                "strategy": args.get("strategy", "rolling"),
                "status": "needs_execution",
                "checklist": [
                    "Verify pre-deployment checks",
                    "Create deployment snapshot",
                    "Execute deployment",
                    "Run health checks",
                    "Monitor metrics",
                ],
            }

        elif name == "rollback":
            task_id = await self.db.create_task(
                ministry="operations",
                specialist="deployer",
                task_type="rollback",
                description=f"Rollback {args['service']} in {args['environment']}",
                input_context=args,
            )

            return {
                "task_id": task_id,
                "service": args["service"],
                "environment": args["environment"],
                "target_version": args.get("version", "previous"),
                "status": "needs_execution",
            }

        elif name == "check_health":
            return {
                "service": args["service"],
                "endpoint": args.get("endpoint", "/health"),
                "status": "needs_execution",
                "message": "Health check requires HTTP access",
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

    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        db_path = Path(__file__).parent.parent.parent / config["database"]["path"]
    else:
        db_path = Path(__file__).parent.parent.parent / "data" / "country.db"

    ministry = OperationsMinistry(db_path)
    await ministry.run()


if __name__ == "__main__":
    asyncio.run(main())
