"""
File Manager Specialist - Operations Ministry

Responsible for safe, reliable file system operations.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


class FileManagerSpecialist:
    """
    The File Manager Specialist handles file system operations safely.

    Capabilities:
    - File CRUD operations
    - Directory management
    - Path manipulation
    - Safe deletion with confirmation
    """

    # Dangerous paths that should never be modified
    PROTECTED_PATHS = [
        "/", "/bin", "/sbin", "/usr", "/etc", "/var",
        "C:\\Windows", "C:\\Program Files",
    ]

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "file_manager"

    def get_system_prompt(self) -> str:
        """Get the file manager specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def is_safe_path(self, path: str | Path) -> tuple[bool, str]:
        """Check if a path is safe to modify."""
        path = Path(path).resolve()

        for protected in self.PROTECTED_PATHS:
            if str(path).startswith(protected):
                return False, f"Path is protected: {protected}"

        return True, "Path is safe"

    def normalize_path(self, path: str | Path) -> Path:
        """Normalize a path for cross-platform compatibility."""
        return Path(path).resolve()


def create_specialist() -> FileManagerSpecialist:
    """Factory function to create the specialist."""
    return FileManagerSpecialist()
