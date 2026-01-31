# Developer Guide

Complete technical guide for developers working on the Micro-Country of Geniuses system.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure Deep Dive](#project-structure-deep-dive)
3. [Core Concepts](#core-concepts)
4. [Code Walkthrough](#code-walkthrough)
5. [Common Development Tasks](#common-development-tasks)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Contributing Guidelines](#contributing-guidelines)

---

## Development Environment Setup

### Prerequisites

You'll need:
- Python 3.11+ (we use modern async features)
- Ollama (for AI inference)
- Git (for version control)
- A code editor (VS Code recommended)

### Step-by-Step Setup

#### 1. Clone and Enter the Project

```bash
git clone <repository-url>
cd micro-country
```

#### 2. Create Virtual Environment

A virtual environment isolates project dependencies:

**What is a virtual environment?**
Think of it like a sandbox. Python packages you install go into this sandbox instead of your global Python installation. This prevents conflicts between projects.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# You'll see (venv) in your prompt
```

#### 3. Install Dependencies

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov black flake8
```

#### 4. Set Up Ollama

```bash
# Start Ollama server (keep running)
ollama serve

# In another terminal, download the model
ollama pull mistral:7b
```

#### 5. Initialize Database

```bash
python -c "
import asyncio
from shared.database import Database

async def init():
    db = Database('data/country.db')
    await db.initialize()
    print('Database initialized!')

asyncio.run(init())
"
```

#### 6. Run Tests

```bash
python -m pytest -v
```

All tests should pass. If not, check the [Troubleshooting](#debugging) section.

### VS Code Setup (Recommended)

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

---

## Project Structure Deep Dive

```
micro-country/
├── orchestrator.py           # Main entry point and request routing
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── pytest.ini                # Test configuration
│
├── genius/                   # Core reasoning system
│   ├── __init__.py           # Exports: GeniusProtocol, EvidenceCourt
│   ├── protocol.py           # 7-step reasoning implementation
│   ├── evidence_court.py     # Conflict resolution logic
│   └── prompts/              # System prompts for specialists
│       ├── base_genius.txt   # Base prompt all specialists inherit
│       ├── architect.txt     # Architecture specialist prompt
│       ├── coder.txt         # Coding specialist prompt
│       └── ... (18 total)    # One per specialist
│
├── ministries/               # MCP servers (one per ministry)
│   ├── code/                 # Software development
│   │   ├── __init__.py
│   │   ├── minister.py       # MCP server definition
│   │   └── specialists/      # Specialist helpers
│   │       ├── architect.py
│   │       ├── coder.py
│   │       └── debugger.py
│   ├── research/             # Information & analysis
│   ├── quality/              # Testing & security
│   ├── operations/           # System management
│   ├── archives/             # Knowledge management + Evidence Court
│   └── communications/       # Messaging & scheduling
│
├── shared/                   # Shared infrastructure
│   ├── __init__.py
│   ├── database.py           # SQLite async wrapper
│   ├── schema.sql            # Database schema
│   └── knowledge_server.py   # MCP server for shared state
│
├── bridge/                   # LLM integration
│   ├── __init__.py
│   └── ollama_bridge.py      # Ollama API client
│
├── data/                     # Runtime data
│   └── country.db            # SQLite database (created at runtime)
│
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_genius_protocol.py
│   ├── test_database.py
│   ├── test_ministries.py
│   └── test_orchestrator.py
│
└── docs/                     # Documentation
    ├── QUICK_START.md
    ├── USER_GUIDE.md
    └── ... (this file)
```

### File Purposes

| File | Purpose | When to Modify |
|------|---------|----------------|
| `orchestrator.py` | Routes requests, runs interactive mode | Adding new commands |
| `config.yaml` | All configuration | Changing settings |
| `genius/protocol.py` | 7-step reasoning | Changing reasoning process |
| `genius/evidence_court.py` | Conflict resolution | Changing evidence rules |
| `ministries/*/minister.py` | Ministry MCP servers | Adding tools |
| `shared/database.py` | Database operations | Adding DB methods |
| `shared/schema.sql` | Database structure | Adding tables/columns |
| `bridge/ollama_bridge.py` | LLM communication | Changing LLM behavior |

---

## Core Concepts

### Understanding MCP (Model Context Protocol)

MCP is a protocol for AI systems to communicate. Think of it like HTTP for AI:

```
┌─────────────┐       MCP Request        ┌─────────────┐
│   Client    │ ─────────────────────────│   Server    │
│ (Orchestr.) │                          │  (Ministry) │
│             │ ←────────────────────────│             │
└─────────────┘       MCP Response       └─────────────┘
```

**Key MCP Concepts**:

1. **Tools** - Functions the client can call
   ```python
   Tool(
       name="implement_feature",
       description="Write code for a feature",
       inputSchema={...}
   )
   ```

2. **Resources** - Data the client can read
   ```python
   Resource(
       uri="code://codebase-map",
       name="Codebase Map",
       description="Project structure"
   )
   ```

3. **Handlers** - Server responds to requests
   ```python
   @server.list_tools()
   async def list_tools():
       return [Tool(...), Tool(...)]

   @server.call_tool()
   async def call_tool(name, arguments):
       # Execute the tool
       return result
   ```

### The Genius Protocol

Every specialist uses this 7-step process:

```python
class GeniusProtocol:
    STEPS = ["observe", "think", "reflect", "critique", "refine", "act", "verify"]

    def build_genius_prompt(self, specialist, task_context):
        # Combines base prompt + specialist expertise + task context
        # Returns a prompt that enforces the 7-step reasoning
        pass

    def parse_reasoning_trace(self, response, specialist):
        # Parses LLM response into structured ReasoningTrace
        # Extracts each step's content
        pass

    def assess_quality(self, trace):
        # Calculates quality score (0.0-1.0)
        # Checks for completeness, rationale, evidence
        pass
```

### The Evidence Court

Resolves conflicts between specialists:

```python
class EvidenceType(IntEnum):
    EMPIRICAL = 1    # Data, tests, benchmarks (strongest)
    PRECEDENT = 2    # What worked before
    CONSENSUS = 3    # Multiple experts agree
    THEORETICAL = 4  # Logical arguments
    INTUITION = 5    # Gut feeling (weakest)

class Evidence:
    evidence_type: EvidenceType
    description: str
    source: str
    confidence: float  # 0.0 to 1.0

    def strength_score(self):
        # Combines type ranking with confidence
        type_score = (6 - self.evidence_type) / 5
        return (type_score * 0.6) + (self.confidence * 0.4)
```

### Asynchronous Programming

This project uses Python's async/await:

**Why async?**
- MCP communication is I/O-bound
- LLM requests take time
- Database operations are I/O-bound
- Async allows efficient handling of multiple operations

**Basic patterns**:

```python
# Async function
async def my_function():
    result = await some_io_operation()
    return result

# Running async code
import asyncio
asyncio.run(my_function())

# Async context manager
async with SomeResource() as resource:
    await resource.do_something()

# Multiple concurrent operations
results = await asyncio.gather(
    operation1(),
    operation2(),
    operation3()
)
```

---

## Code Walkthrough

### How a Request Flows

Let's trace what happens when a user types:
```
> Write a function to sort a list
```

#### Step 1: Orchestrator Receives Request

```python
# orchestrator.py

class Orchestrator:
    async def run_interactive(self):
        while True:
            user_input = input("\n> ")  # Gets "Write a function to sort a list"

            request = Request(content=user_input)
            response = await self.process_request(request)
            print(response.content)
```

#### Step 2: Request is Routed

```python
# orchestrator.py

def route_request(self, request):
    content_lower = request.content.lower()

    routing_rules = {
        "code": ["implement", "code", "function", "write", ...],
        "research": ["search", "find", "research", ...],
        # ...
    }

    for ministry, keywords in routing_rules.items():
        if any(kw in content_lower for kw in keywords):
            return ministry  # Returns "code"

    return "code"  # Default
```

#### Step 3: Specialist is Selected

```python
# orchestrator.py

def select_specialist(self, ministry, request):
    # "Write" matches "coder"
    specialist_rules = {
        "coder": ["implement", "code", "function", "write"],
        # ...
    }

    for specialist, keywords in specialist_rules.items():
        if any(kw in request.content.lower() for kw in keywords):
            return specialist  # Returns "coder"
```

#### Step 4: LLM Generates Response

```python
# orchestrator.py

async def process_request(self, request):
    ministry = self.route_request(request)      # "code"
    specialist = self.select_specialist(...)    # "coder"

    async with self.ollama:
        output, trace = await self.ollama.generate_with_reasoning(
            prompt=request.content,
            specialist=specialist,
        )

    return Response(content=output, ministry=ministry, specialist=specialist)
```

#### Step 5: Genius Prompt is Built

```python
# bridge/ollama_bridge.py

async def generate_with_reasoning(self, prompt, specialist, task_id=None):
    response = await self.generate(
        prompt=prompt,
        specialist=specialist,
        include_reasoning_template=True,
    )
    # ...

async def generate(self, prompt, specialist, ...):
    # Build the system prompt
    system = self.genius.build_genius_prompt(
        specialist=specialist,
        task_context=prompt,
        include_reasoning_template=True,
    )
    # Make API call to Ollama
    # ...
```

#### Step 6: Ollama Returns Response

The LLM returns a response structured like:

```
### 1. OBSERVE
The user wants a sorting function...

### 2. THINK
I could use bubble sort, merge sort, or Python's built-in...

### 3. REFLECT
The request doesn't specify algorithm, so I'll use Pythonic approach...

### 4. CRITIQUE
I should handle edge cases like empty list...

### 5. REFINE
I'll add type hints and docstring...

### 6. ACT
def sort_list(items: list) -> list:
    """Sort a list in ascending order."""
    return sorted(items)

### 7. VERIFY
- Rationale explained: Yes (used built-in for simplicity)
- Trade-offs identified: Yes (simplicity vs custom algorithm)
- Evidence cited: Yes (Python best practices)
```

### Ministry Server Structure

Each ministry follows this pattern:

```python
# ministries/code/minister.py

class CodeMinistry:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("code-ministry")
        self._setup_handlers()

    def _setup_handlers(self):
        @self.server.list_resources()
        async def list_resources():
            return [
                Resource(uri="code://codebase-map", ...),
                Resource(uri="code://tech-stack", ...),
            ]

        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(name="implement_feature", ...),
                Tool(name="refactor_code", ...),
            ]

        @self.server.call_tool()
        async def call_tool(name, arguments):
            result = await self._execute_tool(name, arguments)
            return [TextContent(text=json.dumps(result))]

    async def _execute_tool(self, name, args):
        if name == "implement_feature":
            # Implementation logic
            pass
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

#### Step 2: Implement the Tool

In `_execute_tool()`:

```python
elif name == "my_new_tool":
    # Access parameters
    param1 = args["param1"]
    param2 = args.get("param2", 10)

    # Do something
    result = do_something(param1, param2)

    # Return structured response
    return {
        "success": True,
        "result": result,
    }
```

#### Step 3: Add Tests

In `tests/test_ministries.py`:

```python
@pytest.mark.asyncio
async def test_my_new_tool():
    # Setup
    ministry = CodeMinistry(temp_db_path)
    await ministry.db.initialize()

    # Call tool
    result = await ministry._execute_tool(
        "my_new_tool",
        {"param1": "test"}
    )

    # Verify
    assert result["success"] == True
```

### Adding a New Specialist

#### Step 1: Create Specialist Prompt

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

## Example Expert Reasoning

**Request**: "Example request"

**Specialist thinks**:
"First, I'll consider...
Then I'll...
Finally..."
```

#### Step 2: Create Specialist Class

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

    def get_system_prompt(self):
        return self.genius.load_specialist_prompt(self.specialist_name)

    # Add helper methods specific to this specialist


def create_specialist():
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
        results = []
        for row in rows:
            d = dict(row)
            if d.get("data"):
                d["data"] = json.loads(d["data"])
            results.append(d)
        return results
```

#### Step 3: Test the New Methods

```python
@pytest.mark.asyncio
async def test_my_table_operations(temp_db):
    await temp_db.initialize()

    # Create
    record_id = await temp_db.create_my_record(
        name="test",
        data={"key": "value"}
    )
    assert record_id > 0

    # Read
    records = await temp_db.get_my_records()
    assert len(records) > 0
```

---

## Testing

### Running Tests

```bash
# All tests
python -m pytest

# Verbose output
python -m pytest -v

# Specific test file
python -m pytest tests/test_database.py

# Specific test
python -m pytest tests/test_database.py::test_initialize_database

# With coverage
python -m pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Writing Tests

#### Test Structure

```python
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from module_to_test import SomethingToTest


class TestSomething:
    """Tests for Something."""

    def test_basic_functionality(self):
        """Test basic case."""
        thing = SomethingToTest()
        result = thing.do_something("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case."""
        thing = SomethingToTest()
        result = thing.do_something("")
        assert result is None


class TestAsyncOperations:
    """Tests for async operations."""

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async function."""
        result = await some_async_function()
        assert result is not None
```

#### Using Fixtures

```python
@pytest.fixture
def temp_db():
    """Create a temporary database."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = Database(db_path)
    yield db

    # Cleanup
    if db_path.exists():
        db_path.unlink()


@pytest.mark.asyncio
async def test_with_fixture(temp_db):
    await temp_db.initialize()
    # Use temp_db...
```

### Test Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| genius/protocol.py | 90%+ |
| genius/evidence_court.py | 90%+ |
| shared/database.py | 85%+ |
| ministries/*/minister.py | 80%+ |
| orchestrator.py | 75%+ |

---

## Debugging

### Common Issues

#### "Module not found"

**Cause**: Python path not set correctly.

**Fix**: Ensure you're in the project root or add to path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

#### "Ollama connection refused"

**Cause**: Ollama server not running.

**Fix**:
```bash
ollama serve
```

#### Database Locked

**Cause**: Multiple processes accessing the database.

**Fix**: Ensure only one instance is running.

### Debugging Techniques

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

# Run it
asyncio.run(debug_async())
```

#### Checking Database Contents

```python
import asyncio
from shared.database import Database

async def inspect_db():
    db = Database("data/country.db")
    async with db.connection() as conn:
        cursor = await conn.execute("SELECT * FROM decision_log LIMIT 5")
        rows = await cursor.fetchall()
        for row in rows:
            print(dict(row))

asyncio.run(inspect_db())
```

---

## Contributing Guidelines

### Code Style

- Use **black** for formatting
- Use **flake8** for linting
- Use type hints for all function signatures
- Write docstrings for public functions

```bash
# Format code
black .

# Check linting
flake8 .
```

### Commit Messages

Follow conventional commits:

```
type(scope): description

Examples:
feat(code-ministry): add refactoring tool
fix(database): handle null values in JSON fields
docs(readme): update installation instructions
test(genius): add edge case tests for protocol
```

### Pull Request Checklist

- [ ] All tests pass
- [ ] Code is formatted with black
- [ ] No linting errors
- [ ] New code has tests
- [ ] Documentation updated if needed
- [ ] Commit messages follow convention

---

## Quick Reference

### Important Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `Orchestrator` | `orchestrator.py` | Main coordinator |
| `GeniusProtocol` | `genius/protocol.py` | Reasoning implementation |
| `EvidenceCourt` | `genius/evidence_court.py` | Conflict resolution |
| `Database` | `shared/database.py` | SQLite wrapper |
| `OllamaBridge` | `bridge/ollama_bridge.py` | LLM client |
| `KnowledgeServer` | `shared/knowledge_server.py` | Shared state MCP server |

### Key Methods

| Method | Class | Purpose |
|--------|-------|---------|
| `route_request()` | Orchestrator | Determine ministry |
| `select_specialist()` | Orchestrator | Pick specialist |
| `build_genius_prompt()` | GeniusProtocol | Create system prompt |
| `parse_reasoning_trace()` | GeniusProtocol | Parse LLM response |
| `determine_winner()` | EvidenceCourt | Resolve conflicts |
| `generate_with_reasoning()` | OllamaBridge | LLM call with protocol |

### Useful Commands

```bash
# Run the system
python orchestrator.py

# Run tests
python -m pytest -v

# Check code style
black --check .
flake8 .

# Format code
black .

# See test coverage
python -m pytest --cov=. --cov-report=html
```
