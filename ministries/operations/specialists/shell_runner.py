"""
Shell Runner Specialist - Operations Ministry

Responsible for safe command execution.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


class ShellRunnerSpecialist:
    """
    The Shell Runner Specialist executes commands safely.

    Capabilities:
    - Execute shell commands
    - Manage processes
    - Handle environment variables
    - Capture output safely
    """

    # Commands that require extra caution
    DANGEROUS_COMMANDS = [
        "rm -rf", "del /f", "format",
        "mkfs", "dd", "chmod 777",
        "> /dev/sda", ":(){ :|:& };:",
    ]

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "shell_runner"

    def get_system_prompt(self) -> str:
        """Get the shell runner specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def is_safe_command(self, command: str) -> tuple[bool, str]:
        """Check if a command is safe to execute."""
        command_lower = command.lower()

        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous.lower() in command_lower:
                return False, f"Command contains dangerous pattern: {dangerous}"

        return True, "Command appears safe"

    def format_command(
        self,
        command: str,
        working_dir: str = None,
        env: dict = None,
    ) -> dict:
        """Format a command for execution."""
        return {
            "command": command,
            "working_dir": working_dir or ".",
            "env": env or {},
        }


def create_specialist() -> ShellRunnerSpecialist:
    """Factory function to create the specialist."""
    return ShellRunnerSpecialist()
