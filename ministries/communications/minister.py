"""
Ministry of Communications - MCP Server

The Communications Ministry is responsible for:
- Messaging and notifications
- Task scheduling
- User notifications

Tools:
- send_message: Send a message
- schedule_task: Schedule a task
- notify_user: Notify the user

Resources:
- inbox: Pending messages
- calendar: Scheduled tasks

Specialists:
- messenger: Message composition and delivery
- scheduler: Task scheduling and tracking
"""

import asyncio
import json
from pathlib import Path
from typing import Any
from datetime import datetime

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


class CommunicationsMinistry:
    """MCP Server for the Ministry of Communications."""

    def __init__(self, db_path: str | Path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("communications-ministry")

        # Ministry state
        self.inbox = []
        self.scheduled_tasks = []
        self.notifications = []

        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="comms://inbox",
                    name="Inbox",
                    description="Pending messages and notifications",
                    mimeType="application/json",
                ),
                Resource(
                    uri="comms://calendar",
                    name="Calendar",
                    description="Scheduled tasks and deadlines",
                    mimeType="application/json",
                ),
                Resource(
                    uri="comms://notifications",
                    name="Notifications",
                    description="System notifications",
                    mimeType="application/json",
                ),
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> ResourceContents:
            """Read a resource."""
            if uri == "comms://inbox":
                data = {"messages": self.inbox}
            elif uri == "comms://calendar":
                data = {"scheduled_tasks": self.scheduled_tasks}
            elif uri == "comms://notifications":
                data = {"notifications": self.notifications[-50:]}
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
                # Messenger tools
                Tool(
                    name="send_message",
                    description="Send a message to a ministry or specialist.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "string",
                                "description": "Recipient (ministry or specialist)",
                            },
                            "subject": {
                                "type": "string",
                                "description": "Message subject",
                            },
                            "body": {
                                "type": "string",
                                "description": "Message body",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["critical", "high", "normal", "low"],
                                "default": "normal",
                            },
                            "action_required": {
                                "type": "boolean",
                                "default": False,
                            },
                        },
                        "required": ["to", "subject", "body"],
                    },
                ),
                Tool(
                    name="broadcast",
                    description="Broadcast a message to all ministries.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "Broadcast subject",
                            },
                            "body": {
                                "type": "string",
                                "description": "Broadcast content",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["critical", "high", "normal", "low"],
                                "default": "normal",
                            },
                        },
                        "required": ["subject", "body"],
                    },
                ),
                Tool(
                    name="notify_user",
                    description="Send a notification to the user.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Notification title",
                            },
                            "message": {
                                "type": "string",
                                "description": "Notification message",
                            },
                            "type": {
                                "type": "string",
                                "enum": ["info", "warning", "error", "success"],
                                "default": "info",
                            },
                        },
                        "required": ["title", "message"],
                    },
                ),
                # Scheduler tools
                Tool(
                    name="schedule_task",
                    description="Schedule a task for future execution.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "Task description",
                            },
                            "ministry": {
                                "type": "string",
                                "description": "Ministry to handle the task",
                            },
                            "due_date": {
                                "type": "string",
                                "description": "When the task is due (ISO format)",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["critical", "high", "normal", "low"],
                                "default": "normal",
                            },
                            "dependencies": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Tasks this depends on",
                            },
                        },
                        "required": ["task", "ministry"],
                    },
                ),
                Tool(
                    name="get_schedule",
                    description="Get scheduled tasks, optionally filtered.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ministry": {
                                "type": "string",
                                "description": "Filter by ministry",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed", "overdue"],
                            },
                            "days_ahead": {
                                "type": "integer",
                                "default": 7,
                                "description": "How many days ahead to show",
                            },
                        },
                    },
                ),
                Tool(
                    name="set_reminder",
                    description="Set a reminder.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Reminder message",
                            },
                            "when": {
                                "type": "string",
                                "description": "When to remind (ISO format)",
                            },
                            "repeat": {
                                "type": "string",
                                "enum": ["none", "daily", "weekly", "monthly"],
                                "default": "none",
                            },
                        },
                        "required": ["message", "when"],
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

        if name == "send_message":
            message = {
                "id": f"msg_{len(self.inbox) + 1}",
                "from": "communications",
                "to": args["to"],
                "subject": args["subject"],
                "body": args["body"],
                "priority": args.get("priority", "normal"),
                "action_required": args.get("action_required", False),
                "sent_at": datetime.now().isoformat(),
                "status": "sent",
            }
            self.inbox.append(message)

            # Log as cross-ministry request
            await self.db.create_cross_ministry_request(
                from_ministry="communications",
                to_ministry=args["to"],
                request_type="message",
                request_content=message,
            )

            return {
                "success": True,
                "message_id": message["id"],
                "status": "sent",
            }

        elif name == "broadcast":
            ministries = ["code", "research", "quality", "operations", "archives"]
            broadcast_id = f"broadcast_{len(self.notifications) + 1}"

            for ministry in ministries:
                message = {
                    "id": f"{broadcast_id}_{ministry}",
                    "from": "communications",
                    "to": ministry,
                    "subject": args["subject"],
                    "body": args["body"],
                    "priority": args.get("priority", "normal"),
                    "is_broadcast": True,
                    "sent_at": datetime.now().isoformat(),
                }
                self.inbox.append(message)

            return {
                "success": True,
                "broadcast_id": broadcast_id,
                "recipients": ministries,
            }

        elif name == "notify_user":
            notification = {
                "id": f"notif_{len(self.notifications) + 1}",
                "title": args["title"],
                "message": args["message"],
                "type": args.get("type", "info"),
                "created_at": datetime.now().isoformat(),
                "read": False,
            }
            self.notifications.append(notification)

            return {
                "success": True,
                "notification_id": notification["id"],
                "delivered": True,
            }

        elif name == "schedule_task":
            task = {
                "id": f"scheduled_{len(self.scheduled_tasks) + 1}",
                "task": args["task"],
                "ministry": args["ministry"],
                "due_date": args.get("due_date"),
                "priority": args.get("priority", "normal"),
                "dependencies": args.get("dependencies", []),
                "status": "pending",
                "created_at": datetime.now().isoformat(),
            }
            self.scheduled_tasks.append(task)

            return {
                "success": True,
                "task_id": task["id"],
                "scheduled": True,
            }

        elif name == "get_schedule":
            tasks = self.scheduled_tasks.copy()

            # Filter by ministry
            if args.get("ministry"):
                tasks = [t for t in tasks if t["ministry"] == args["ministry"]]

            # Filter by status
            if args.get("status"):
                tasks = [t for t in tasks if t["status"] == args["status"]]

            return {
                "count": len(tasks),
                "tasks": tasks,
            }

        elif name == "set_reminder":
            reminder = {
                "id": f"reminder_{len(self.notifications) + 1}",
                "message": args["message"],
                "when": args["when"],
                "repeat": args.get("repeat", "none"),
                "created_at": datetime.now().isoformat(),
                "triggered": False,
            }

            return {
                "success": True,
                "reminder_id": reminder["id"],
                "scheduled_for": args["when"],
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

    ministry = CommunicationsMinistry(db_path)
    await ministry.run()


if __name__ == "__main__":
    asyncio.run(main())
