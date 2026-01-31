"""Tests for Ministry MCP servers."""

import pytest
import asyncio
import json
from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database import Database


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    yield db_path
    if db_path.exists():
        db_path.unlink()


class TestArchivesMinistry:
    """Tests for Archives Ministry."""

    @pytest.mark.asyncio
    async def test_ministry_import(self):
        """Test ministry can be imported."""
        from ministries.archives.minister import ArchivesMinistry
        assert ArchivesMinistry is not None

    @pytest.mark.asyncio
    async def test_ministry_creation(self, temp_db_path):
        """Test ministry can be created."""
        from ministries.archives.minister import ArchivesMinistry

        ministry = ArchivesMinistry(temp_db_path)
        assert ministry is not None
        assert ministry.server is not None


class TestCodeMinistry:
    """Tests for Code Ministry."""

    @pytest.mark.asyncio
    async def test_ministry_import(self):
        """Test ministry can be imported."""
        from ministries.code.minister import CodeMinistry
        assert CodeMinistry is not None

    @pytest.mark.asyncio
    async def test_ministry_creation(self, temp_db_path):
        """Test ministry can be created."""
        from ministries.code.minister import CodeMinistry

        ministry = CodeMinistry(temp_db_path)
        assert ministry is not None
        assert ministry.genius is not None


class TestQualityMinistry:
    """Tests for Quality Ministry."""

    @pytest.mark.asyncio
    async def test_ministry_import(self):
        """Test ministry can be imported."""
        from ministries.quality.minister import QualityMinistry
        assert QualityMinistry is not None

    @pytest.mark.asyncio
    async def test_ministry_creation(self, temp_db_path):
        """Test ministry can be created."""
        from ministries.quality.minister import QualityMinistry

        ministry = QualityMinistry(temp_db_path)
        assert ministry is not None


class TestResearchMinistry:
    """Tests for Research Ministry."""

    @pytest.mark.asyncio
    async def test_ministry_import(self):
        """Test ministry can be imported."""
        from ministries.research.minister import ResearchMinistry
        assert ResearchMinistry is not None

    @pytest.mark.asyncio
    async def test_ministry_creation(self, temp_db_path):
        """Test ministry can be created."""
        from ministries.research.minister import ResearchMinistry

        ministry = ResearchMinistry(temp_db_path)
        assert ministry is not None


class TestOperationsMinistry:
    """Tests for Operations Ministry."""

    @pytest.mark.asyncio
    async def test_ministry_import(self):
        """Test ministry can be imported."""
        from ministries.operations.minister import OperationsMinistry
        assert OperationsMinistry is not None

    @pytest.mark.asyncio
    async def test_ministry_creation(self, temp_db_path):
        """Test ministry can be created."""
        from ministries.operations.minister import OperationsMinistry

        ministry = OperationsMinistry(temp_db_path)
        assert ministry is not None


class TestCommunicationsMinistry:
    """Tests for Communications Ministry."""

    @pytest.mark.asyncio
    async def test_ministry_import(self):
        """Test ministry can be imported."""
        from ministries.communications.minister import CommunicationsMinistry
        assert CommunicationsMinistry is not None

    @pytest.mark.asyncio
    async def test_ministry_creation(self, temp_db_path):
        """Test ministry can be created."""
        from ministries.communications.minister import CommunicationsMinistry

        ministry = CommunicationsMinistry(temp_db_path)
        assert ministry is not None


class TestSpecialists:
    """Tests for specialists."""

    def test_architect_specialist(self):
        """Test architect specialist."""
        from ministries.code.specialists.architect import ArchitectSpecialist, create_specialist

        specialist = create_specialist()
        assert specialist is not None
        assert specialist.specialist_name == "architect"

    def test_coder_specialist(self):
        """Test coder specialist."""
        from ministries.code.specialists.coder import CoderSpecialist, create_specialist

        specialist = create_specialist()
        assert specialist is not None
        assert "python" in specialist.LANGUAGES

    def test_debugger_specialist(self):
        """Test debugger specialist."""
        from ministries.code.specialists.debugger import DebuggerSpecialist, create_specialist

        specialist = create_specialist()
        assert specialist is not None
        assert "TypeError" in specialist.ERROR_PATTERNS

    def test_tester_specialist(self):
        """Test tester specialist."""
        from ministries.quality.specialists.tester import TesterSpecialist, create_specialist

        specialist = create_specialist()
        assert specialist is not None
        assert "happy_path" in specialist.TEST_CATEGORIES

    def test_auditor_specialist(self):
        """Test auditor specialist."""
        from ministries.quality.specialists.auditor import AuditorSpecialist, create_specialist

        specialist = create_specialist()
        assert specialist is not None
        assert "A01" in specialist.OWASP_TOP_10

    def test_memory_specialist(self):
        """Test memory specialist."""
        from ministries.archives.specialists.memory import MemorySpecialist, create_specialist

        specialist = create_specialist()
        assert specialist is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
