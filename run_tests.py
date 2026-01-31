#!/usr/bin/env python3
"""Run all tests for the Micro-Country of Geniuses."""

import sys
import subprocess
from pathlib import Path


def main():
    """Run the test suite."""
    project_dir = Path(__file__).parent

    # Ensure we're in the project directory
    print(f"Running tests from: {project_dir}")
    print("=" * 60)

    # Run pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short"],
        cwd=project_dir,
    )

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
