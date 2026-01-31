"""
Tester Specialist - Quality Ministry

Responsible for test design, execution, and coverage analysis.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


@dataclass
class TestCase:
    """A single test case."""

    name: str
    description: str
    test_type: str  # unit, integration, e2e
    setup: list[str] = field(default_factory=list)
    input_data: Any = None
    expected_output: Any = None
    assertions: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


@dataclass
class TestSuite:
    """A collection of test cases."""

    name: str
    description: str
    test_cases: list[TestCase] = field(default_factory=list)
    setup_all: list[str] = field(default_factory=list)
    teardown_all: list[str] = field(default_factory=list)


class TesterSpecialist:
    """
    The Tester Specialist designs and manages tests.

    Capabilities:
    - Design comprehensive test cases
    - Identify edge cases and error conditions
    - Analyze coverage gaps
    - Prioritize test execution
    """

    # Test categories
    TEST_CATEGORIES = {
        "happy_path": "Normal expected operation",
        "edge_cases": "Boundary conditions and limits",
        "error_cases": "Error handling and invalid inputs",
        "security": "Security-related test cases",
        "performance": "Performance and load testing",
    }

    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "tester"

    def get_system_prompt(self) -> str:
        """Get the tester specialist's system prompt."""
        return self.genius.load_specialist_prompt(self.specialist_name)

    def create_test_suite(
        self,
        name: str,
        description: str,
    ) -> TestSuite:
        """Create a new test suite."""
        return TestSuite(name=name, description=description)

    def create_test_case(
        self,
        name: str,
        description: str,
        test_type: str = "unit",
    ) -> TestCase:
        """Create a new test case."""
        return TestCase(
            name=name,
            description=description,
            test_type=test_type,
        )

    def identify_test_categories(self, code: str) -> list[str]:
        """Identify which test categories apply to given code."""
        categories = ["happy_path"]  # Always include happy path

        code_lower = code.lower()

        # Check for patterns that suggest specific categories
        if any(p in code_lower for p in ["if", "else", "try", "except", "catch"]):
            categories.append("error_cases")

        if any(p in code_lower for p in ["max", "min", "limit", "range", "boundary"]):
            categories.append("edge_cases")

        if any(p in code_lower for p in ["password", "auth", "token", "encrypt", "hash"]):
            categories.append("security")

        if any(p in code_lower for p in ["loop", "iterate", "bulk", "batch", "concurrent"]):
            categories.append("performance")

        return categories

    def generate_test_template(
        self,
        language: str,
        test_type: str,
    ) -> str:
        """Generate a test template for a language."""
        templates = {
            "python": {
                "unit": """
import pytest

class Test{ClassName}:
    def setup_method(self):
        # Setup for each test
        pass

    def teardown_method(self):
        # Cleanup after each test
        pass

    def test_{test_name}_happy_path(self):
        # Arrange
        # Act
        # Assert
        pass

    def test_{test_name}_edge_case(self):
        pass

    def test_{test_name}_error_case(self):
        with pytest.raises(ExpectedException):
            pass
""",
                "integration": """
import pytest

@pytest.fixture
def setup_dependencies():
    # Setup external dependencies
    yield
    # Cleanup

class TestIntegration{ClassName}:
    def test_integration_{test_name}(self, setup_dependencies):
        pass
""",
            },
            "javascript": {
                "unit": """
describe('{ClassName}', () => {
    beforeEach(() => {
        // Setup
    });

    afterEach(() => {
        // Cleanup
    });

    test('{test_name} happy path', () => {
        // Arrange
        // Act
        // Assert
    });

    test('{test_name} edge case', () => {
    });

    test('{test_name} error case', () => {
        expect(() => {
        }).toThrow();
    });
});
""",
            },
        }

        return templates.get(language, templates["python"]).get(
            test_type, templates["python"]["unit"]
        )


def create_specialist() -> TesterSpecialist:
    """Factory function to create the specialist."""
    return TesterSpecialist()
