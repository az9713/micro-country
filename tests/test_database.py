"""Tests for the database module."""

import pytest
import asyncio
from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = Database(db_path)
    yield db

    # Cleanup
    if db_path.exists():
        db_path.unlink()


@pytest.mark.asyncio
async def test_initialize_database(temp_db):
    """Test database initialization."""
    await temp_db.initialize()

    # Check that tables were created by reading constitution
    articles = await temp_db.get_constitution()
    assert len(articles) > 0
    assert any("Purpose" in a["article"] for a in articles)


@pytest.mark.asyncio
async def test_log_decision(temp_db):
    """Test logging a decision."""
    await temp_db.initialize()

    decision_id = await temp_db.log_decision(
        ministry="code",
        decision_type="design",
        context={"feature": "authentication"},
        decision="Use JWT tokens",
        rationale="Stateless and scalable",
        options_considered=["sessions", "JWT", "OAuth"],
    )

    assert decision_id.startswith("dec_")

    # Retrieve decisions
    decisions = await temp_db.get_decisions(ministry="code")
    assert len(decisions) > 0
    assert decisions[0]["decision"] == "Use JWT tokens"


@pytest.mark.asyncio
async def test_project_operations(temp_db):
    """Test project CRUD operations."""
    await temp_db.initialize()

    # Create project
    project_id = await temp_db.create_project(
        name="Test Project",
        description="A test project",
        goals=["Goal 1", "Goal 2"],
        tech_stack={"language": "python"},
    )

    assert project_id.startswith("proj_")

    # Get project
    project = await temp_db.get_project(project_id)
    assert project is not None
    assert project["name"] == "Test Project"
    assert "Goal 1" in project["goals"]

    # Update project
    success = await temp_db.update_project(
        project_id,
        status="completed",
        current_phase="done",
    )
    assert success

    # Verify update
    project = await temp_db.get_project(project_id)
    assert project["status"] == "completed"


@pytest.mark.asyncio
async def test_knowledge_operations(temp_db):
    """Test knowledge storage and search."""
    await temp_db.initialize()

    # Store knowledge
    knowledge_id = await temp_db.store_knowledge(
        domain="architecture",
        topic="API Design",
        content="RESTful APIs should use proper HTTP methods",
        source="best practices",
        confidence=0.9,
        tags=["rest", "api", "design"],
    )

    assert knowledge_id.startswith("know_")

    # Search by domain
    results = await temp_db.search_knowledge(domain="architecture")
    assert len(results) > 0

    # Search by query
    results = await temp_db.search_knowledge(query="RESTful")
    assert len(results) > 0
    assert "RESTful" in results[0]["content"]


@pytest.mark.asyncio
async def test_task_operations(temp_db):
    """Test task creation and updates."""
    await temp_db.initialize()

    # Create task
    task_id = await temp_db.create_task(
        ministry="code",
        task_type="implementation",
        description="Implement user authentication",
        specialist="coder",
    )

    assert task_id.startswith("task_")

    # Update task
    success = await temp_db.update_task(
        task_id,
        status="in_progress",
        approach="Using JWT with refresh tokens",
    )
    assert success

    # Complete task
    success = await temp_db.update_task(
        task_id,
        status="completed",
        success=True,
        lessons_learned="JWT works well for stateless auth",
    )
    assert success

    # Get task history
    history = await temp_db.get_task_history(ministry="code")
    assert len(history) > 0
    assert history[0]["status"] == "completed"


@pytest.mark.asyncio
async def test_court_case_recording(temp_db):
    """Test Evidence Court case recording."""
    await temp_db.initialize()

    case_id = await temp_db.record_court_case(
        topic="Database choice",
        advocates=[
            {"advocate": "architect", "position": "Use PostgreSQL"},
            {"advocate": "coder", "position": "Use MongoDB"},
        ],
        evidence_presented=[
            {"advocate": "architect", "evidence": [{"type": "EMPIRICAL", "description": "ACID compliance"}]},
            {"advocate": "coder", "evidence": [{"type": "THEORETICAL", "description": "Flexibility"}]},
        ],
        ruling="Use PostgreSQL",
        ruling_rationale="ACID compliance is essential for this use case",
        precedent_set="Relational data should use relational databases",
    )

    assert case_id.startswith("case_")

    # Search precedents
    precedents = await temp_db.get_court_precedents(topic_query="Database")
    assert len(precedents) > 0
    assert "PostgreSQL" in precedents[0]["ruling"]


@pytest.mark.asyncio
async def test_reasoning_trace_storage(temp_db):
    """Test storing reasoning traces."""
    await temp_db.initialize()

    trace_id = await temp_db.save_reasoning_trace(
        specialist="architect",
        observe="The system needs authentication",
        think="JWT vs sessions vs OAuth",
        reflect="Am I considering all options?",
        critique="Sessions might have scaling issues",
        refine="JWT with refresh tokens",
        act="Designed JWT-based auth system",
        verify="Design meets requirements",
        quality_score=0.85,
    )

    assert trace_id.startswith("trace_")


@pytest.mark.asyncio
async def test_cross_ministry_requests(temp_db):
    """Test cross-ministry request handling."""
    await temp_db.initialize()

    # Create request
    request_id = await temp_db.create_cross_ministry_request(
        from_ministry="code",
        to_ministry="quality",
        request_type="test_request",
        request_content={"feature": "auth", "tests_needed": ["unit", "integration"]},
    )

    assert request_id.startswith("req_")

    # Respond to request
    success = await temp_db.respond_to_request(
        request_id,
        response_content={"tests_created": 5, "coverage": 80},
        status="completed",
    )
    assert success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
