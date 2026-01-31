"""
Scheduler Specialist - Communications Ministry

Responsible for task scheduling and coordination.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class ScheduledTask:
    """A scheduled task."""

    task_id: str
    description: str
    ministry: str
    due_date: Optional[datetime] = None
    priority: str = "normal"
    dependencies: list[str] = field(default_factory=list)
    status: str = "pending"


class SchedulerSpecialist:
    """
    The Scheduler Specialist manages task scheduling.

    Capabilities:
    - Schedule tasks with dependencies
    - Track deadlines
    - Prioritize work
    - Identify scheduling conflicts
    """

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "scheduler"

    def get_system_prompt(self) -> str:
        """Get the scheduler specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_task(
        self,
        task_id: str,
        description: str,
        ministry: str,
        due_date: datetime = None,
        priority: str = "normal",
    ) -> ScheduledTask:
        """Create a scheduled task."""
        return ScheduledTask(
            task_id=task_id,
            description=description,
            ministry=ministry,
            due_date=due_date,
            priority=priority,
        )

    def check_dependencies(
        self,
        task: ScheduledTask,
        all_tasks: list[ScheduledTask],
    ) -> tuple[bool, list[str]]:
        """Check if task dependencies are met."""
        if not task.dependencies:
            return True, []

        blocking = []
        for dep_id in task.dependencies:
            dep_task = next((t for t in all_tasks if t.task_id == dep_id), None)
            if dep_task and dep_task.status != "completed":
                blocking.append(dep_id)

        return len(blocking) == 0, blocking

    def prioritize_tasks(
        self,
        tasks: list[ScheduledTask],
    ) -> list[ScheduledTask]:
        """Prioritize tasks by due date and priority."""
        priority_order = {"critical": 0, "high": 1, "normal": 2, "low": 3}

        def sort_key(t):
            p = priority_order.get(t.priority, 2)
            d = t.due_date or datetime.max
            return (p, d)

        return sorted(tasks, key=sort_key)


def create_specialist() -> SchedulerSpecialist:
    """Factory function to create the specialist."""
    return SchedulerSpecialist()
