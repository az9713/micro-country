# Concepts Explained

A deep-dive into the foundational concepts used in this project. Each concept is explained from first principles with examples.

---

## Table of Contents

1. [Async/Await Programming](#asyncawait-programming)
2. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
3. [JSON-RPC 2.0](#json-rpc-20)
4. [SQLite and Databases](#sqlite-and-databases)
5. [Large Language Models (LLMs)](#large-language-models-llms)
6. [The Genius Protocol](#the-genius-protocol)
7. [Evidence-Based Decision Making](#evidence-based-decision-making)
8. [Python Dataclasses](#python-dataclasses)
9. [Context Managers](#context-managers)
10. [Type Hints](#type-hints)

---

## Async/Await Programming

### What is Asynchronous Programming?

Imagine you're cooking dinner:

**Synchronous cooking:**
1. Put water on stove (wait 5 minutes until boiling)
2. Add pasta (wait 10 minutes until done)
3. Make sauce (wait 5 minutes)
4. Total: 20 minutes

**Asynchronous cooking:**
1. Put water on stove
2. While waiting, start making sauce
3. When water boils, add pasta
4. Continue sauce while pasta cooks
5. Total: ~12 minutes

Async programming works the same way - instead of waiting for one thing to finish, you can work on other things.

### Why Does This Project Use Async?

This project does a lot of **waiting**:
- Waiting for the AI model to respond (slow!)
- Waiting for database queries
- Waiting for file operations

With sync code, the program would freeze during each wait. With async:

```python
# Sync (blocking) - takes 3 seconds total
user = get_user(1)      # Wait 1 second
posts = get_posts(1)    # Wait 1 second
comments = get_comments(1)  # Wait 1 second

# Async (non-blocking) - takes ~1 second total
user, posts, comments = await asyncio.gather(
    get_user(1),        # All run
    get_posts(1),       # at the
    get_comments(1)     # same time
)
```

### The Three Key Words

**1. `async def` - Defines an async function (coroutine)**

```python
# Regular function
def regular_function():
    return 42

# Async function (coroutine)
async def async_function():
    return 42
```

**2. `await` - Wait for an async operation to complete**

```python
async def get_data():
    # await pauses here until fetch_user() completes
    user = await fetch_user(123)
    return user
```

**3. `asyncio.run()` - Start the async world from sync code**

```python
import asyncio

async def main():
    result = await do_something()
    print(result)

# This is how you run async code from regular Python
asyncio.run(main())
```

### Visual Explanation

```
SYNCHRONOUS:
┌─────────────────────────────────────────────────────────┐
│ Task A ████████████████████                             │
│                           Task B ████████████████████   │
│                                                    Task C ████ │
└─────────────────────────────────────────────────────────┘
Timeline: ─────────────────────────────────────────────────►

ASYNCHRONOUS:
┌─────────────────────────────────────────────────────────┐
│ Task A ██████▒▒▒▒▒▒▒▒▒▒▒▒██████                        │
│         Task B ██████▒▒▒▒▒▒██████                      │
│              Task C ██████████████                      │
└─────────────────────────────────────────────────────────┘
Timeline: ─────────────────────────►

██ = Running
▒▒ = Waiting (other tasks can run)
```

### Common Patterns in This Project

**Pattern 1: Database Query**
```python
async def get_decisions(self, ministry: str = None) -> list[dict]:
    async with self.connection() as db:
        cursor = await db.execute("SELECT * FROM decisions")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
```

**Pattern 2: LLM Call**
```python
async def generate_response(self, prompt: str) -> str:
    response = await self.ollama.generate(
        model=self.model,
        prompt=prompt
    )
    return response["response"]
```

**Pattern 3: Multiple Operations**
```python
async def get_full_context(self):
    constitution, decisions, knowledge = await asyncio.gather(
        self.get_constitution(),
        self.get_recent_decisions(),
        self.get_domain_knowledge()
    )
    return {
        "constitution": constitution,
        "decisions": decisions,
        "knowledge": knowledge
    }
```

---

## Model Context Protocol (MCP)

### What is MCP?

MCP (Model Context Protocol) is a standard way for AI systems to communicate and share capabilities. Think of it like:

- **HTTP** lets browsers talk to web servers
- **SQL** lets apps talk to databases
- **MCP** lets AI systems talk to capability providers

### Why MCP?

Without a standard protocol, every AI system would need custom integration code. MCP provides:

1. **Standard Interface**: Tools and resources have consistent schemas
2. **Discoverability**: Clients can ask servers what they can do
3. **Type Safety**: JSON schemas define expected inputs/outputs
4. **Extensibility**: Easy to add new capabilities

### MCP Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│     MCP HOST        │         │     MCP SERVER      │
│   (Orchestrator)    │         │     (Ministry)      │
│                     │         │                     │
│  ┌───────────────┐  │  JSON   │  ┌───────────────┐  │
│  │ MCP Client    │◄─┼────────►│  │ MCP Server    │  │
│  └───────────────┘  │  -RPC   │  └───────────────┘  │
│                     │         │                     │
└─────────────────────┘         │  ┌───────────────┐  │
                                │  │ Tools         │  │
                                │  │ - implement   │  │
                                │  │ - refactor    │  │
                                │  └───────────────┘  │
                                │                     │
                                │  ┌───────────────┐  │
                                │  │ Resources     │  │
                                │  │ - codebase-map│  │
                                │  │ - tech-stack  │  │
                                │  └───────────────┘  │
                                └─────────────────────┘
```

### MCP Concepts

**Tools**: Actions the server can perform

```python
# Server defines a tool
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="implement_feature",
            description="Write code for a feature",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature": {"type": "string", "description": "What to implement"},
                    "language": {"type": "string", "default": "python"}
                },
                "required": ["feature"]
            }
        )
    ]

# Client calls the tool
result = await server.call_tool("implement_feature", {
    "feature": "user authentication"
})
```

**Resources**: Data the server provides

```python
# Server defines a resource
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="code://codebase-map",
            name="Codebase Map",
            description="Project directory structure",
            mimeType="application/json"
        )
    ]

# Client reads the resource
content = await server.read_resource("code://codebase-map")
```

### MCP in This Project

Each ministry is an MCP server:

```
┌─────────────┐   ┌─────────────────────┐
│             │   │ Code Ministry       │
│             ├──►│ - implement_feature │
│             │   │ - refactor_code     │
│ Orchestrator│   │ - debug_issue       │
│             │   └─────────────────────┘
│             │   ┌─────────────────────┐
│             │   │ Quality Ministry    │
│             ├──►│ - run_tests         │
│             │   │ - security_audit    │
│             │   └─────────────────────┘
└─────────────┘
```

---

## JSON-RPC 2.0

### What is JSON-RPC?

JSON-RPC is a protocol for calling functions remotely using JSON. It's simpler than alternatives like SOAP or gRPC.

### Basic Structure

**Request:**
```json
{
    "jsonrpc": "2.0",
    "method": "implement_feature",
    "params": {
        "feature": "user login",
        "language": "python"
    },
    "id": 1
}
```

**Response (success):**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "code": "def login(username, password): ...",
        "file": "auth.py"
    },
    "id": 1
}
```

**Response (error):**
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32600,
        "message": "Invalid params",
        "data": "feature is required"
    },
    "id": 1
}
```

### Why JSON-RPC for MCP?

1. **Simple**: Easy to implement and debug
2. **Language-agnostic**: Any language can produce/consume JSON
3. **Human-readable**: You can inspect the messages
4. **Well-defined**: Clear specification for errors, notifications, etc.

### Transport: STDIO

MCP uses STDIO (standard input/output) for communication:

```
┌─────────────┐     stdout      ┌─────────────┐
│   Client    │ ───────────────►│   Server    │
│             │◄─────────────── │             │
└─────────────┘     stdin       └─────────────┘
```

Benefits:
- No network setup needed
- Works in any environment
- Simple process management

---

## SQLite and Databases

### What is a Database?

A database is organized storage for data. Think of it as:
- A spreadsheet that can hold millions of rows
- With relationships between tables
- That multiple programs can access safely

### What is SQLite?

SQLite is a **file-based** database:

| Traditional Database | SQLite |
|---------------------|--------|
| Runs as separate process | Just a file |
| Needs installation | Built into Python |
| Network communication | Direct file access |
| Complex configuration | Zero config |

### SQLite in This Project

**Database file**: `data/country.db`

**Schema** (`shared/schema.sql`):
```sql
-- The constitution (core rules)
CREATE TABLE constitution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article TEXT NOT NULL,
    content TEXT NOT NULL,
    rationale TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Decision log (what was decided and why)
CREATE TABLE decision_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT UNIQUE NOT NULL,
    ministry TEXT NOT NULL,
    specialist TEXT,
    decision_type TEXT NOT NULL,
    context TEXT,  -- JSON
    decision TEXT NOT NULL,
    rationale TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- More tables...
```

**Python access** (`shared/database.py`):
```python
class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def initialize(self):
        """Create tables from schema.sql"""
        async with self.connection() as db:
            with open("shared/schema.sql") as f:
                await db.executescript(f.read())

    async def log_decision(self, ministry: str, decision: str, rationale: str) -> str:
        """Store a decision"""
        async with self.connection() as db:
            decision_id = str(uuid.uuid4())
            await db.execute(
                "INSERT INTO decision_log (decision_id, ministry, decision, rationale) VALUES (?, ?, ?, ?)",
                (decision_id, ministry, decision, rationale)
            )
            await db.commit()
            return decision_id
```

### SQL Basics

**Select data:**
```sql
SELECT * FROM decision_log WHERE ministry = 'code';
SELECT decision, rationale FROM decision_log LIMIT 10;
```

**Insert data:**
```sql
INSERT INTO decision_log (ministry, decision, rationale)
VALUES ('code', 'Use microservices', 'Better scalability');
```

**Update data:**
```sql
UPDATE decision_log SET rationale = 'New reason' WHERE id = 1;
```

**Delete data:**
```sql
DELETE FROM decision_log WHERE id = 1;
```

### Why Async SQLite?

Regular SQLite blocks while reading/writing. With `aiosqlite`:
- Other code can run while waiting for database
- Better responsiveness in interactive applications

```python
# Sync (blocks everything)
connection = sqlite3.connect("db.sqlite")
cursor = connection.execute("SELECT ...")

# Async (non-blocking)
async with aiosqlite.connect("db.sqlite") as db:
    cursor = await db.execute("SELECT ...")
```

---

## Large Language Models (LLMs)

### What is an LLM?

A Large Language Model is an AI trained on text to:
- Understand natural language
- Generate human-like text
- Follow instructions
- Reason about problems

Examples: GPT-4, Claude, Llama, Qwen

### How LLMs Work (Simplified)

```
Input: "Write a Python function to sort a list"
         │
         ▼
┌─────────────────────────────────────┐
│           LLM (Neural Network)       │
│                                      │
│  • Trained on billions of text tokens│
│  • Learned patterns of language      │
│  • Learned code patterns             │
│  • Predicts "what comes next"        │
└─────────────────────────────────────┘
         │
         ▼
Output: "def sort_list(items):
            return sorted(items)"
```

### Ollama

Ollama runs LLMs locally on your computer:

```
┌─────────────────┐         ┌─────────────────┐
│ This Application│  HTTP   │  Ollama Server  │
│                 │◄───────►│                 │
│                 │         │  ┌───────────┐  │
└─────────────────┘         │  │ qwen2.5   │  │
                            │  │  model    │  │
                            │  └───────────┘  │
                            └─────────────────┘
```

**Key Commands:**
```bash
# Start the server
ollama serve

# Download a model
ollama pull mistral:7b

# List available models
ollama list

# Chat interactively
ollama run mistral:7b
```

**API Usage (in code):**
```python
import ollama

response = ollama.generate(
    model="mistral:7b",
    prompt="Write a function to calculate factorial"
)
print(response["response"])
```

### Prompts and System Prompts

**Prompt**: What you ask the model

**System Prompt**: Instructions that shape how the model responds

```python
# System prompt (defines behavior)
system = """You are a security expert. Always:
- Consider security implications
- Mention potential vulnerabilities
- Suggest secure alternatives
"""

# User prompt (the actual request)
user = "Review this login function"

# Combined for the API call
response = ollama.chat(
    model="mistral:7b",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]
)
```

### LLM in This Project

The `OllamaBridge` class handles all LLM communication:

```python
class OllamaBridge:
    async def generate(self, prompt: str, specialist: str = None) -> str:
        """Generate text from prompt"""
        system = self.genius.build_genius_prompt(specialist)
        # ... calls Ollama API

    async def generate_with_reasoning(self, prompt: str, specialist: str) -> tuple:
        """Generate with parsed reasoning trace"""
        response = await self.generate(prompt, specialist)
        trace = self.genius.parse_reasoning_trace(response)
        return response, trace
```

---

## The Genius Protocol

### What is the Genius Protocol?

A structured reasoning process that forces the AI to think carefully before answering. Every specialist follows these 7 steps:

```
1. OBSERVE  →  Understand the request
2. THINK    →  Reason through options
3. REFLECT  →  Check assumptions
4. CRITIQUE →  Find problems
5. REFINE   →  Improve approach
6. ACT      →  Produce output
7. VERIFY   →  Confirm quality
```

### Why 7 Steps?

Without structure, AI can:
- Miss important details
- Jump to conclusions
- Make unchecked assumptions
- Produce low-quality output

The 7 steps prevent these issues by forcing:
- **Observation** before action
- **Self-criticism** before output
- **Verification** after completion

### Step Details

**1. OBSERVE**: Read and understand
```
"The user wants a sorting function. They mentioned 'Python' and
'list'. They didn't specify ascending or descending, so I'll
default to ascending."
```

**2. THINK**: Consider options
```
"I could use:
- Built-in sorted() function
- list.sort() method
- Custom implementation (bubble, quick, merge)

Built-in is most Pythonic and efficient."
```

**3. REFLECT**: Check understanding
```
"Am I correct that they want to sort a list in place or return
a new list? The word 'function' suggests returning a new list."
```

**4. CRITIQUE**: Find problems
```
"What if the list contains mixed types? What if it's empty?
What if elements aren't comparable? I should handle these cases."
```

**5. REFINE**: Improve approach
```
"I'll add type hints, a docstring, and handle the empty list case."
```

**6. ACT**: Produce output
```python
def sort_list(items: list) -> list:
    """Sort a list in ascending order.

    Args:
        items: List of comparable elements

    Returns:
        New sorted list
    """
    if not items:
        return []
    return sorted(items)
```

**7. VERIFY**: Confirm quality
```
"✓ Rationale explained: Yes (built-in is most Pythonic)
✓ Trade-offs identified: Yes (new list vs in-place)
✓ Edge cases handled: Yes (empty list)
✓ Type hints included: Yes"
```

### Implementation

```python
class GeniusProtocol:
    STEPS = ["observe", "think", "reflect", "critique", "refine", "act", "verify"]

    def build_genius_prompt(self, specialist: str, task: str) -> str:
        """Build a prompt that enforces the 7-step protocol."""
        return f"""
{self.load_specialist_prompt(specialist)}

You MUST structure your response with these 7 steps:

### 1. OBSERVE
[Carefully read and understand the request]

### 2. THINK
[Reason through possible approaches]

... (all 7 steps)
"""

    def parse_reasoning_trace(self, response: str) -> ReasoningTrace:
        """Parse LLM response into structured trace."""
        # Extract each step's content
        trace = ReasoningTrace()
        for step in self.STEPS:
            trace[step] = self._extract_step(response, step)
        return trace
```

---

## Evidence-Based Decision Making

### The Problem

When multiple experts disagree, how do you decide who's right?

```
Architect: "Use microservices for scalability"
Coder: "Use monolith for simplicity"
```

Both have valid points. Traditional approaches:
- **Voting**: Majority wins (but majority can be wrong)
- **Seniority**: Senior person decides (but may be biased)
- **Random**: Pick one (obviously problematic)

### The Evidence Court Solution

Decisions are based on **quality of evidence**, not opinion:

```
Evidence Hierarchy (strongest to weakest):

1. EMPIRICAL    - Data, tests, benchmarks
                  "Load test shows 10k requests/sec"

2. PRECEDENT    - What worked before
                  "Netflix uses this architecture"

3. CONSENSUS    - Multiple experts agree
                  "Industry best practice"

4. THEORETICAL  - Logical reasoning
                  "This follows SOLID principles"

5. INTUITION    - Gut feeling
                  "I think this is right"
```

### How It Works

```
Step 1: Positions Formalized
┌────────────────────────────────────────────────────────────┐
│ Position A: Use Microservices                               │
│ Arguments: Scalability, team independence                   │
│ Evidence: [EMPIRICAL] Netflix case study (confidence: 0.9) │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ Position B: Use Monolith                                    │
│ Arguments: Simplicity, faster development                   │
│ Evidence: [THEORETICAL] KISS principle (confidence: 0.7)   │
└────────────────────────────────────────────────────────────┘

Step 2: Evidence Evaluated
┌────────────────────────────────────────────────────────────┐
│                    EVIDENCE COURT                           │
│                                                             │
│ Position A Evidence:                                        │
│   Type: EMPIRICAL (rank 1)                                 │
│   Confidence: 0.9                                          │
│   Score: (1.0 × 0.6) + (0.9 × 0.4) = 0.96                 │
│                                                             │
│ Position B Evidence:                                        │
│   Type: THEORETICAL (rank 4)                               │
│   Confidence: 0.7                                          │
│   Score: (0.4 × 0.6) + (0.7 × 0.4) = 0.52                 │
│                                                             │
│ RULING: Position A wins (0.96 > 0.52)                      │
└────────────────────────────────────────────────────────────┘

Step 3: Decision Recorded as Precedent
```

### Implementation

```python
class Evidence:
    evidence_type: EvidenceType  # EMPIRICAL, PRECEDENT, etc.
    description: str
    source: str
    confidence: float  # 0.0 to 1.0

    def strength_score(self) -> float:
        # Type contributes 60%, confidence contributes 40%
        type_score = (6 - self.evidence_type) / 5
        return (type_score * 0.6) + (self.confidence * 0.4)


class EvidenceCourt:
    def determine_winner(self, positions: list[Position]) -> Position:
        """Find the position with strongest evidence."""
        scored = []
        for position in positions:
            total_strength = sum(e.strength_score() for e in position.evidence)
            scored.append((position, total_strength))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]
```

---

## Python Dataclasses

### What are Dataclasses?

Dataclasses are a Python feature for creating classes that mainly hold data. They auto-generate common methods.

### Without Dataclasses

```python
class Person:
    def __init__(self, name: str, age: int, email: str = ""):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age}, email={self.email!r})"

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age and self.email == other.email
```

### With Dataclasses

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str = ""

# Auto-generates __init__, __repr__, __eq__, etc.
```

That's it! Much less code.

### Usage Examples

```python
# Create instance
alice = Person("Alice", 30)
bob = Person("Bob", 25, "bob@example.com")

# Access attributes
print(alice.name)  # "Alice"

# Auto-generated __repr__
print(alice)  # Person(name='Alice', age=30, email='')

# Auto-generated __eq__
alice2 = Person("Alice", 30)
print(alice == alice2)  # True
```

### In This Project

Dataclasses are used for structured data:

```python
@dataclass
class ReasoningTrace:
    specialist: str
    task_id: Optional[str]
    observe: str
    think: str
    reflect: str
    critique: str
    refine: str
    act: str
    verify: str
    quality_score: float = 0.0
    quality_issues: list = field(default_factory=list)

@dataclass
class Evidence:
    evidence_type: EvidenceType
    description: str
    source: str
    confidence: float
    data: Optional[dict] = None

@dataclass
class Position:
    advocate: str
    position: str
    arguments: list[str]
    evidence: list[Evidence]
```

---

## Context Managers

### What are Context Managers?

Context managers handle setup and cleanup automatically. The classic example is file handling:

**Without context manager (error-prone):**
```python
f = open("file.txt")
try:
    content = f.read()
finally:
    f.close()  # Easy to forget!
```

**With context manager (automatic cleanup):**
```python
with open("file.txt") as f:
    content = f.read()
# File automatically closed, even if exception occurs
```

### How They Work

Context managers define:
1. `__enter__`: What to do at the start
2. `__exit__`: What to do at the end (cleanup)

```python
class ManagedResource:
    def __enter__(self):
        print("Acquiring resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")

with ManagedResource() as resource:
    print("Using resource")

# Output:
# Acquiring resource
# Using resource
# Releasing resource
```

### Async Context Managers

For async code, use `async with`:

```python
class AsyncDatabase:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

# Usage
async with AsyncDatabase() as db:
    result = await db.query("SELECT ...")
```

### In This Project

Database connections use async context managers:

```python
class Database:
    @asynccontextmanager
    async def connection(self):
        """Async context manager for database connections."""
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        try:
            yield conn
        finally:
            await conn.close()

# Usage
async with self.connection() as db:
    cursor = await db.execute("SELECT * FROM users")
    rows = await cursor.fetchall()
# Connection automatically closed
```

---

## Type Hints

### What are Type Hints?

Type hints annotate what types functions expect and return. They don't enforce types at runtime but help with:
- Documentation
- IDE autocompletion
- Static analysis (mypy)
- Catching bugs early

### Basic Syntax

```python
# Variable annotation
name: str = "Alice"
age: int = 30
balance: float = 100.50
active: bool = True

# Function annotation
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Optional (can be None)
from typing import Optional
def find_user(user_id: int) -> Optional[dict]:
    # Returns dict or None
    pass

# List of items
def process_names(names: list[str]) -> list[str]:
    return [n.upper() for n in names]

# Dictionary
def count_words(text: str) -> dict[str, int]:
    # Returns word -> count mapping
    pass
```

### Common Type Hints

```python
from typing import Optional, List, Dict, Tuple, Union, Any, Callable

# Optional - can be None
user: Optional[dict] = None

# Union - one of several types
id_or_name: Union[int, str] = 123

# Any - any type (use sparingly)
data: Any = get_something()

# Callable - a function
callback: Callable[[int, str], bool]  # Takes int and str, returns bool

# Generic collections
names: List[str] = ["Alice", "Bob"]  # Older syntax
names: list[str] = ["Alice", "Bob"]  # Python 3.9+ syntax
```

### In This Project

Type hints are used throughout:

```python
async def log_decision(
    self,
    ministry: str,
    specialist: Optional[str],
    decision_type: str,
    context: dict,
    options: list[str],
    decision: str,
    rationale: str,
    evidence: list[dict] = None
) -> str:
    """Log a decision and return its ID."""
    ...

def build_genius_prompt(
    self,
    specialist: str,
    task_context: str,
    include_reasoning_template: bool = True
) -> str:
    """Build a prompt that enforces the Genius Protocol."""
    ...
```

### Benefits

1. **Self-documenting**: Types explain what functions expect
2. **IDE support**: Better autocomplete and error detection
3. **Bug prevention**: Catch type errors before running
4. **Refactoring safety**: Changing types shows what breaks

---

## Summary

These concepts work together in this project:

```
User Request
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                           │
│   Uses: async/await, type hints, context managers           │
└─────────────────────────────────────────────────────────────┘
     │
     │ MCP + JSON-RPC
     ▼
┌─────────────────────────────────────────────────────────────┐
│                        MINISTRIES                            │
│   Uses: MCP, dataclasses, async/await                       │
└─────────────────────────────────────────────────────────────┘
     │
     │ Genius Protocol
     ▼
┌─────────────────────────────────────────────────────────────┐
│                          LLM                                 │
│   Uses: Ollama, prompts, structured reasoning               │
└─────────────────────────────────────────────────────────────┘
     │
     │ Evidence Court
     ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                               │
│   Uses: SQLite, async, context managers                     │
└─────────────────────────────────────────────────────────────┘
```

Now you understand the building blocks of this system!
