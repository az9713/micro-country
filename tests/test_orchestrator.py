"""Tests for the Central Orchestrator."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator import Orchestrator, Request, Response


class TestOrchestrator:
    """Tests for the Central Orchestrator."""

    def test_orchestrator_creation(self):
        """Test orchestrator can be created."""
        orchestrator = Orchestrator()
        assert orchestrator is not None
        assert orchestrator.genius is not None
        assert orchestrator.court is not None

    def test_route_request_code(self):
        """Test request routing to code ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Implement a user authentication feature")
        ministry = orchestrator.route_request(request)
        assert ministry == "code"

        request = Request(content="Debug this function that's failing")
        ministry = orchestrator.route_request(request)
        assert ministry == "code"

    def test_route_request_research(self):
        """Test request routing to research ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Search for best practices for API design")
        ministry = orchestrator.route_request(request)
        assert ministry == "research"

        request = Request(content="Write documentation for the auth module")
        ministry = orchestrator.route_request(request)
        assert ministry == "research"

    def test_route_request_quality(self):
        """Test request routing to quality ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Run tests for the user module")
        ministry = orchestrator.route_request(request)
        assert ministry == "quality"

        request = Request(content="Perform security audit on the API")
        ministry = orchestrator.route_request(request)
        assert ministry == "quality"

    def test_route_request_operations(self):
        """Test request routing to operations ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Deploy the application to staging")
        ministry = orchestrator.route_request(request)
        assert ministry == "operations"

        request = Request(content="Run the build script")
        ministry = orchestrator.route_request(request)
        assert ministry == "operations"

    def test_route_request_archives(self):
        """Test request routing to archives ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Remember this decision about auth")
        ministry = orchestrator.route_request(request)
        assert ministry == "archives"

        request = Request(content="Recall the history of design decisions")
        ministry = orchestrator.route_request(request)
        assert ministry == "archives"

    def test_route_request_communications(self):
        """Test request routing to communications ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Schedule a reminder for the review")
        ministry = orchestrator.route_request(request)
        assert ministry == "communications"

        request = Request(content="Notify the team about the update")
        ministry = orchestrator.route_request(request)
        assert ministry == "communications"

    def test_route_explicit_ministry(self):
        """Test explicit ministry routing."""
        orchestrator = Orchestrator()

        request = Request(content="Do something", ministry="quality")
        ministry = orchestrator.route_request(request)
        assert ministry == "quality"

    def test_select_specialist_code(self):
        """Test specialist selection in code ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Design the architecture for auth")
        specialist = orchestrator.select_specialist("code", request)
        assert specialist == "architect"

        request = Request(content="Implement the login function")
        specialist = orchestrator.select_specialist("code", request)
        assert specialist == "coder"

        request = Request(content="Debug the failing test")
        specialist = orchestrator.select_specialist("code", request)
        assert specialist == "debugger"

    def test_select_specialist_quality(self):
        """Test specialist selection in quality ministry."""
        orchestrator = Orchestrator()

        request = Request(content="Write unit tests for auth")
        specialist = orchestrator.select_specialist("quality", request)
        assert specialist == "tester"

        request = Request(content="Security audit the API")
        specialist = orchestrator.select_specialist("quality", request)
        assert specialist == "auditor"


class TestRequest:
    """Tests for Request dataclass."""

    def test_request_creation(self):
        """Test request creation."""
        request = Request(content="Do something")
        assert request.content == "Do something"
        assert request.ministry is None
        assert request.specialist is None

    def test_request_with_ministry(self):
        """Test request with ministry specified."""
        request = Request(content="Do something", ministry="code", specialist="coder")
        assert request.ministry == "code"
        assert request.specialist == "coder"


class TestResponse:
    """Tests for Response dataclass."""

    def test_response_creation(self):
        """Test response creation."""
        response = Response(
            content="Here is the result",
            ministry="code",
            specialist="architect",
        )
        assert response.content == "Here is the result"
        assert response.ministry == "code"
        assert response.specialist == "architect"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
