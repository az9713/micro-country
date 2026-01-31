# CLAUDE.md - Comprehensive Guide for Claude Code

This file provides complete context for Claude Code when working on the Micro-Country of Geniuses project. It serves as the definitive reference for understanding the codebase, making changes, and extending functionality.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Overview](#architecture-overview)
4. [Directory Structure](#directory-structure)
5. [Key Files Reference](#key-files-reference)
6. [Code Conventions](#code-conventions)
7. [Common Development Tasks](#common-development-tasks)
8. [Testing](#testing)
9. [Debugging](#debugging)
10. [Configuration](#configuration)
11. [Dependencies](#dependencies)
12. [Known Limitations](#known-limitations)
13. [Future Improvements](#future-improvements)

---

## Project Overview

**Micro-Country of Geniuses** is a local multi-agent AI system that simulates a self-governing country of specialized AI experts working together to solve complex problems.

### Core Concepts

1. **Multi-Agent System**: Multiple AI "specialists" with different expertise areas
2. **Ministry Structure**: Specialists organized into 6 ministries (departments)
3. **Genius Protocol**: 7-step structured reasoning process for all specialists
4. **Evidence Court**: Conflict resolution mechanism based on evidence hierarchy
5. **Knowledge Server**: Shared database for institutional memory

### How It Works

```
User Request
     │
     ▼
┌─────────────────┐
│   Orchestrator  │ ← Routes requests, manages specialists
└────────┬────────┘
         │
    ┌────┴────┬────────────┬────────────┬────────────┬────────────┐
    ▼         ▼            ▼            ▼            ▼            ▼
┌───────┐ ┌────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌───────────┐
│ Code  │ │Research│ │ Quality │ │Operations│ │Archives │ │   Comms   │
│Ministry│ │Ministry│ │Ministry │ │ Ministry │ │Ministry │ │ Ministry  │
└───┬───┘ └────┬───┘ └────┬────┘ └────┬─────┘ └────┬────┘ └─────┬─────┘
    │          │          │           │            │            │
    └──────────┴──────────┴───────────┴────────────┴────────────┘
                                      │
                                      ▼
                          ┌───────────────────┐
                          │ SQLite Database   │
                          │ (Shared Knowledge)│
                          └───────────────────┘
```

---

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Primary language |
| Ollama | Latest | Local LLM inference engine |
| MCP SDK | ≥1.0.0 | Model Context Protocol for agent communication |
| SQLite | Built-in | Local database for persistence |
| aiosqlite | ≥0.19.0 | Async SQLite wrapper |

### Key Libraries

| Library | Purpose | Used In |
|---------|---------|---------|
| `mcp` | MCP server/client implementation | All ministries |
| `ollama` | Ollama API client | `bridge/ollama_bridge.py` |
| `aiosqlite` | Async database operations | `shared/database.py` |
| `pyyaml` | Configuration parsing | `orchestrator.py` |
| `httpx` | Async HTTP requests | `bridge/ollama_bridge.py` |
| `pytest` | Testing framework | `tests/` |
| `pytest-asyncio` | Async test support | `tests/` |

### Communication Protocol

- **Transport**: STDIO (Standard Input/Output)
- **Format**: JSON-RPC 2.0
- **Pattern**: Request-Response

---

## Architecture Overview

### Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Request Router  │  │ Ollama Bridge   │  │ Context Manager │ │
│  │ (route_request) │  │ (LLM calls)     │  │ (aggregation)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ Genius Protocol │  │ Evidence Court  │                      │
│  │ (7-step reason) │  │ (conflict res.) │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ MINISTRY      │    │ MINISTRY      │    │ MINISTRY      │
│ (MCP Server)  │    │ (MCP Server)  │    │ (MCP Server)  │
│               │    │               │    │               │
│ • Tools       │    │ • Tools       │    │ • Tools       │
│ • Resources   │    │ • Resources   │    │ • Resources   │
│ • Specialists │    │ • Specialists │    │ • Specialists │
└───────────────┘    └───────────────┘    └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │ KNOWLEDGE SERVER  │
                    │ (SQLite + MCP)    │
                    └───────────────────┘
```

### The Six Ministries

| Ministry | Server Name | Specialists | Responsibilities |
|----------|-------------|-------------|------------------|
| Code | `code-ministry` | Architect, Coder, Debugger | Software development |
| Research | `research-ministry` | Analyst, Writer, Searcher | Information gathering |
| Quality | `quality-ministry` | Tester, Auditor, Validator | Testing & security |
| Operations | `operations-ministry` | File Manager, Shell Runner, Deployer | System management |
| Archives | `archives-ministry` | Memory, Indexer | Knowledge management |
| Communications | `communications-ministry` | Messenger, Scheduler | Coordination |

### The Genius Protocol (7 Steps)

Every specialist processes requests through these steps:

1. **OBSERVE** - Understand the request, identify context
2. **THINK** - Reason through options, consider approaches
3. **REFLECT** - Check assumptions, validate understanding
4. **CRITIQUE** - Find flaws in own reasoning (devil's advocate)
5. **REFINE** - Improve approach based on critique
6. **ACT** - Execute and produce output
7. **VERIFY** - Confirm output meets quality threshold

### Evidence Court Hierarchy

When specialists disagree, evidence determines the winner:

| Rank | Type | Description | Example |
|------|------|-------------|---------|
| 1 | EMPIRICAL | Data, tests, benchmarks | "Load test shows 10k req/sec" |
| 2 | PRECEDENT | What worked before | "Netflix uses this pattern" |
| 3 | CONSENSUS | Multiple experts agree | "Industry best practice" |
| 4 | THEORETICAL | Logical arguments | "This follows SOLID principles" |
| 5 | INTUITION | Gut feeling | "I think this is right" |

---

## Directory Structure

```
micro-country/
│
├── orchestrator.py              # MAIN ENTRY POINT - Central coordinator
├── config.yaml                  # Configuration file
├── requirements.txt             # Python dependencies
├── run_tests.py                 # Test runner script
├── CLAUDE.md                    # This file
├── README.md                    # Project overview
│
├── genius/                      # Core reasoning system
│   ├── __init__.py              # Exports: GeniusProtocol, EvidenceCourt
│   ├── protocol.py              # 7-step reasoning implementation
│   ├── evidence_court.py        # Conflict resolution logic
│   └── prompts/                 # System prompts (18 files)
│       ├── base_genius.txt      # Base prompt inherited by all
│       ├── architect.txt        # Architecture specialist
│       ├── coder.txt            # Coding specialist
│       ├── debugger.txt         # Debugging specialist
│       ├── analyst.txt          # Analysis specialist
│       ├── writer.txt           # Documentation specialist
│       ├── searcher.txt         # Research specialist
│       ├── tester.txt           # Testing specialist
│       ├── auditor.txt          # Security specialist
│       ├── validator.txt        # Validation specialist
│       ├── file_manager.txt     # File operations specialist
│       ├── shell_runner.txt     # Shell command specialist
│       ├── deployer.txt         # Deployment specialist
│       ├── memory.txt           # Knowledge storage specialist
│       ├── indexer.txt          # Indexing specialist
│       ├── messenger.txt        # Messaging specialist
│       └── scheduler.txt        # Scheduling specialist
│
├── ministries/                  # MCP servers (one per ministry)
│   ├── code/                    # Ministry of Code
│   │   ├── __init__.py
│   │   ├── minister.py          # MCP server definition
│   │   └── specialists/
│   │       ├── __init__.py
│   │       ├── architect.py
│   │       ├── coder.py
│   │       └── debugger.py
│   │
│   ├── research/                # Ministry of Research
│   │   ├── __init__.py
│   │   ├── minister.py
│   │   └── specialists/
│   │       ├── __init__.py
│   │       ├── analyst.py
│   │       ├── writer.py
│   │       └── searcher.py
│   │
│   ├── quality/                 # Ministry of Quality
│   │   ├── __init__.py
│   │   ├── minister.py
│   │   └── specialists/
│   │       ├── __init__.py
│   │       ├── tester.py
│   │       ├── auditor.py
│   │       └── validator.py
│   │
│   ├── operations/              # Ministry of Operations
│   │   ├── __init__.py
│   │   ├── minister.py
│   │   └── specialists/
│   │       ├── __init__.py
│   │       ├── file_manager.py
│   │       ├── shell_runner.py
│   │       └── deployer.py
│   │
│   ├── archives/                # Ministry of Archives
│   │   ├── __init__.py
│   │   ├── minister.py
│   │   └── specialists/
│   │       ├── __init__.py
│   │       ├── memory.py
│   │       └── indexer.py
│   │
│   └── communications/          # Ministry of Communications
│       ├── __init__.py
│       ├── minister.py
│       └── specialists/
│           ├── __init__.py
│           ├── messenger.py
│           └── scheduler.py
│
├── shared/                      # Shared infrastructure
│   ├── __init__.py
│   ├── database.py              # Async SQLite wrapper (Database class)
│   ├── schema.sql               # Database schema (8 tables)
│   └── knowledge_server.py      # MCP server for shared state
│
├── bridge/                      # LLM integration layer
│   ├── __init__.py
│   └── ollama_bridge.py         # Ollama API client (OllamaBridge class)
│
├── data/                        # Runtime data
│   └── country.db               # SQLite database (created at runtime)
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_orchestrator.py     # Orchestrator tests
│   ├── test_genius_protocol.py  # Protocol tests
│   ├── test_ministries.py       # Ministry tests
│   └── test_database.py         # Database tests
│
└── docs/                        # Documentation
    ├── QUICK_START.md           # 10 hands-on examples
    ├── USER_GUIDE.md            # Complete user manual
    ├── DEVELOPER_GUIDE.md       # Development guide
    ├── INSTALLATION.md          # Setup instructions
    ├── ARCHITECTURE.md          # Technical architecture
    ├── API_REFERENCE.md         # Tool/resource documentation
    ├── TROUBLESHOOTING.md       # Problem solving
    └── GLOSSARY.md              # Term definitions
```

---

## Key Files Reference

### Entry Point

| File | Purpose | When to Modify |
|------|---------|----------------|
| `orchestrator.py` | Main program, CLI, request routing | Adding commands, changing routing |

### Core Logic

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `genius/protocol.py` | 7-step reasoning | `GeniusProtocol`, `ReasoningTrace`, `DebateProtocol` |
| `genius/evidence_court.py` | Conflict resolution | `EvidenceCourt`, `Evidence`, `Position`, `CourtRuling` |
| `bridge/ollama_bridge.py` | LLM integration | `OllamaBridge` |
| `shared/database.py` | Database operations | `Database` |
| `shared/knowledge_server.py` | Shared state MCP server | `KnowledgeServer` |

### Configuration

| File | Purpose |
|------|---------|
| `config.yaml` | All runtime configuration |
| `shared/schema.sql` | Database table definitions |
| `requirements.txt` | Python dependencies |

### Ministry Servers

Each ministry follows this pattern:

| File | Purpose |
|------|---------|
| `ministries/<name>/minister.py` | MCP server with tools and resources |
| `ministries/<name>/specialists/*.py` | Specialist helper classes |

---

## Code Conventions

### Python Style

```python
# Type hints for all function signatures
def process_request(self, request: Request) -> Response:
    pass

# Async/await for I/O operations
async def query_database(self, query: str) -> list[dict]:
    async with self.connection() as db:
        cursor = await db.execute(query)
        return await cursor.fetchall()

# Dataclasses for structured data
@dataclass
class Evidence:
    evidence_type: EvidenceType
    description: str
    confidence: float

# Explicit return types
def calculate_score(self) -> float:
    return (self.type_score * 0.6) + (self.confidence * 0.4)
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `GeniusProtocol`, `EvidenceCourt` |
| Functions | snake_case | `process_request`, `build_prompt` |
| Constants | UPPER_SNAKE_CASE | `STEPS`, `EVIDENCE_TYPES` |
| Private methods | _prefix | `_execute_tool`, `_parse_response` |
| Files | snake_case | `evidence_court.py`, `ollama_bridge.py` |

### File Organization

- **One class per file** for major components
- **< 500 lines** per file (split if larger)
- **Specialists** go in `specialists/` subdirectory
- **Prompts** go in `genius/prompts/`

### Error Handling

```python
# Return structured errors from tools
async def _execute_tool(self, name: str, args: dict) -> dict:
    try:
        result = await self._do_work(args)
        return {"success": True, "result": result}
    except ValueError as e:
        return {"success": False, "error": str(e), "error_type": "validation"}
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        return {"success": False, "error": str(e), "error_type": "internal"}
```

### Import Order

```python
# 1. Standard library
import asyncio
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# 2. Third-party libraries
import yaml
from mcp import Server, Tool, Resource

# 3. Local imports
from genius import GeniusProtocol
from shared.database import Database
```

---

## Common Development Tasks

### Adding a New Tool to a Ministry

#### Step 1: Define the Tool Schema

In `ministries/<ministry>/minister.py`, add to `list_tools()`:

```python
Tool(
    name="my_new_tool",
    description="What this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of param1",
            },
            "param2": {
                "type": "integer",
                "default": 10,
            },
        },
        "required": ["param1"],
    },
),
```

#### Step 2: Implement the Handler

In `_execute_tool()`:

```python
elif name == "my_new_tool":
    param1 = args["param1"]
    param2 = args.get("param2", 10)

    # Implementation logic
    result = await self._do_something(param1, param2)

    return {
        "success": True,
        "result": result,
    }
```

#### Step 3: Add Tests

In `tests/test_ministries.py`:

```python
@pytest.mark.asyncio
async def test_my_new_tool(temp_db):
    ministry = SomeMinistry(temp_db)
    await ministry.db.initialize()

    result = await ministry._execute_tool(
        "my_new_tool",
        {"param1": "test"}
    )

    assert result["success"] == True
```

### Adding a New Specialist

#### Step 1: Create the Prompt

Create `genius/prompts/my_specialist.txt`:

```
# My Specialist Genius - Ministry of X

You are the My Specialist genius, responsible for [purpose].

## Your Expertise

- Skill 1
- Skill 2
- Skill 3

## Your Responsibilities

1. Task 1
2. Task 2
3. Task 3

## Example Expert Reasoning

**Request**: "Example request"

**Specialist thinks**:
"First, I'll consider...
Then I'll analyze...
Finally, I'll..."
```

#### Step 2: Create the Specialist Class

Create `ministries/<ministry>/specialists/my_specialist.py`:

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from genius import GeniusProtocol


class MySpecialist:
    def __init__(self):
        self.genius = GeniusProtocol()
        self.specialist_name = "my_specialist"

    def get_system_prompt(self) -> str:
        return self.genius.load_specialist_prompt(self.specialist_name)

    async def process(self, request: str) -> dict:
        # Specialist-specific logic
        pass


def create_specialist() -> MySpecialist:
    return MySpecialist()
```

#### Step 3: Register in Ministry

Update `ministries/<ministry>/specialists/__init__.py`:

```python
from .my_specialist import MySpecialist

__all__ = [..., "MySpecialist"]
```

#### Step 4: Add to Config

Update `config.yaml`:

```yaml
ministries:
  my_ministry:
    specialists:
      - existing_specialist
      - my_specialist  # Add here
```

### Adding a Database Table

#### Step 1: Update Schema

In `shared/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS my_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    data TEXT,  -- JSON field
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_my_table_name ON my_table(name);
```

#### Step 2: Add Database Methods

In `shared/database.py`:

```python
async def create_my_record(self, name: str, data: dict = None) -> int:
    """Create a new record in my_table."""
    async with self.connection() as db:
        cursor = await db.execute(
            "INSERT INTO my_table (name, data) VALUES (?, ?)",
            (name, json.dumps(data) if data else None),
        )
        await db.commit()
        return cursor.lastrowid

async def get_my_records(self, limit: int = 50) -> list[dict]:
    """Get records from my_table."""
    async with self.connection() as db:
        cursor = await db.execute(
            "SELECT * FROM my_table ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
```

#### Step 3: Test

```python
@pytest.mark.asyncio
async def test_my_table_operations(temp_db):
    await temp_db.initialize()

    record_id = await temp_db.create_my_record("test", {"key": "value"})
    assert record_id > 0

    records = await temp_db.get_my_records()
    assert len(records) > 0
```

### Adding a New Command

In `orchestrator.py`, in the `run_interactive()` method:

```python
# Add to command handling
if user_input.startswith("/mycommand"):
    args = user_input[len("/mycommand"):].strip()
    result = await self.handle_my_command(args)
    print(result)
    continue

# Add the handler method
async def handle_my_command(self, args: str) -> str:
    """Handle the /mycommand command."""
    # Implementation
    return f"Result: {args}"
```

---

## Testing

### Running Tests

```bash
# All tests
python -m pytest -v

# Specific test file
python -m pytest tests/test_genius_protocol.py -v

# Specific test
python -m pytest tests/test_database.py::test_initialize -v

# With coverage
python -m pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Test Structure

```python
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from module_to_test import ClassToTest


class TestClassName:
    """Tests for ClassName."""

    def test_basic_functionality(self):
        """Test the basic case."""
        obj = ClassToTest()
        result = obj.method("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case handling."""
        obj = ClassToTest()
        result = obj.method("")
        assert result is None


class TestAsyncOperations:
    """Tests for async operations."""

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async function."""
        result = await some_async_function()
        assert result is not None
```

### Test Fixtures

```python
# In tests/conftest.py
import pytest
import tempfile
from pathlib import Path
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
```

### Coverage Goals

| Component | Target |
|-----------|--------|
| genius/protocol.py | 90%+ |
| genius/evidence_court.py | 90%+ |
| shared/database.py | 85%+ |
| ministries/*/minister.py | 80%+ |
| orchestrator.py | 75%+ |

---

## Debugging

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Path not set | Add `sys.path.insert(0, ...)` |
| `Connection refused` | Ollama not running | Start `ollama serve` |
| `Model not found` | Model not downloaded | Run `ollama pull qwen2.5:14b` |
| `Database locked` | Multiple instances | Close other instances |
| `Timeout` | Request too complex | Simplify or increase timeout |

### Debug Techniques

#### Print Debugging

```python
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: type = {type(variable)}")
```

#### Using the Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or in Python 3.7+
breakpoint()
```

#### Async Debugging

```python
import asyncio

async def debug_async():
    result = await some_operation()
    print(f"Result: {result}")
    return result

asyncio.run(debug_async())
```

#### Check Ollama Connection

```python
async with OllamaBridge() as bridge:
    connected = await bridge.check_connection()
    models = await bridge.list_models()
    print(f"Connected: {connected}, Models: {models}")
```

#### Inspect Database

```python
import asyncio
from shared.database import Database

async def inspect():
    db = Database("data/country.db")
    async with db.connection() as conn:
        cursor = await conn.execute("SELECT * FROM decision_log LIMIT 5")
        for row in await cursor.fetchall():
            print(dict(row))

asyncio.run(inspect())
```

---

## Configuration

### config.yaml Structure

```yaml
# Ollama Integration
ollama:
  host: "http://localhost:11434"
  model: "qwen2.5:14b"
  timeout: 120  # seconds

# Database
database:
  path: "data/country.db"

# Ministries
ministries:
  code:
    path: "ministries/code"
    specialists:
      - architect
      - coder
      - debugger
  # ... other ministries

# Genius Protocol
genius:
  prompts_dir: "genius/prompts"
  reasoning_steps:
    - OBSERVE
    - THINK
    - REFLECT
    - CRITIQUE
    - REFINE
    - ACT
    - VERIFY

# Evidence Court
evidence_court:
  evidence_ranking:
    empirical: 1
    precedent: 2
    consensus: 3
    theoretical: 4
    intuition: 5

# Logging
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Environment Variables

No `.env` file is required. All configuration is in `config.yaml`.

---

## Dependencies

### Runtime Dependencies

```
mcp>=1.0.0          # MCP SDK
ollama>=0.3.0       # Ollama client
aiosqlite>=0.19.0   # Async SQLite
pyyaml>=6.0.0       # YAML parsing
httpx>=0.25.0       # Async HTTP
```

### Development Dependencies

```
pytest>=8.0.0       # Testing framework
pytest-asyncio>=0.23.0  # Async test support
pytest-cov>=4.0.0   # Coverage reporting
black>=24.0.0       # Code formatting
flake8>=7.0.0       # Linting
```

### Installing

```bash
# Runtime only
pip install -r requirements.txt

# With development tools
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov black flake8
```

---

## Known Limitations

1. **Single-machine only** - No distributed operation
2. **One model for all tasks** - No model specialization per specialist
3. **No persistent MCP connections** - Reconnects per request
4. **No streaming responses** - Full response returned at once
5. **Single user** - No concurrent user support
6. **No web UI** - CLI only

---

## Future Improvements

- [ ] Add persistent MCP connections
- [ ] Support multiple models per specialist
- [ ] Add web UI interface
- [ ] Add conversation memory/history
- [ ] Add plugin system for custom ministries
- [ ] Add streaming response support
- [ ] Add multi-user support
- [ ] Add distributed operation

---

## Quick Reference

### Key Classes

| Class | File | Purpose |
|-------|------|---------|
| `Orchestrator` | `orchestrator.py` | Main coordinator |
| `GeniusProtocol` | `genius/protocol.py` | 7-step reasoning |
| `ReasoningTrace` | `genius/protocol.py` | Reasoning record |
| `EvidenceCourt` | `genius/evidence_court.py` | Conflict resolution |
| `Evidence` | `genius/evidence_court.py` | Evidence data |
| `Database` | `shared/database.py` | SQLite operations |
| `OllamaBridge` | `bridge/ollama_bridge.py` | LLM client |

### Key Methods

| Method | Class | Purpose |
|--------|-------|---------|
| `route_request()` | Orchestrator | Determine ministry |
| `select_specialist()` | Orchestrator | Pick specialist |
| `build_genius_prompt()` | GeniusProtocol | Create system prompt |
| `parse_reasoning_trace()` | GeniusProtocol | Parse LLM response |
| `determine_winner()` | EvidenceCourt | Resolve conflicts |
| `generate_with_reasoning()` | OllamaBridge | LLM with protocol |

### Useful Commands

```bash
# Run the system
python orchestrator.py

# Run tests
python -m pytest -v

# Format code
black .

# Check linting
flake8 .

# See coverage
python -m pytest --cov=. --cov-report=html
```

---

## Contact and Support

For issues with the codebase:
1. Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review error messages carefully
3. Check Ollama is running and model is available
4. Verify Python version is 3.11+
