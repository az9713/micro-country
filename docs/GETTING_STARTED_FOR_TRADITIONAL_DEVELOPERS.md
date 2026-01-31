# Getting Started Guide for Traditional Developers

A comprehensive guide for developers with C, C++, or Java experience who are new to Python and full-stack/web development.

---

## Table of Contents

1. [Introduction: What's Different?](#introduction-whats-different)
2. [Python Fundamentals for C/C++/Java Developers](#python-fundamentals)
3. [Understanding Async Programming](#understanding-async-programming)
4. [Web and API Concepts](#web-and-api-concepts)
5. [Understanding This Project](#understanding-this-project)
6. [Hands-On: Your First Code Change](#hands-on-your-first-code-change)
7. [Common Pitfalls and How to Avoid Them](#common-pitfalls)
8. [Reference: Python vs C/C++/Java Syntax](#reference-syntax-comparison)

---

## Introduction: What's Different?

If you're coming from C, C++, or Java, Python will feel very different. Here's a quick orientation:

### Key Differences at a Glance

| Aspect | C/C++/Java | Python |
|--------|------------|--------|
| **Compilation** | Compiled to binary/bytecode | Interpreted at runtime |
| **Types** | Static typing required | Dynamic typing (optional hints) |
| **Memory** | Manual (C/C++) or GC (Java) | Automatic garbage collection |
| **Braces** | `{ }` for blocks | Indentation defines blocks |
| **Semicolons** | Required `;` | Not required |
| **Main function** | `main()` or `public static void main` | `if __name__ == "__main__":` |
| **Build system** | Make, CMake, Maven, Gradle | pip, requirements.txt |
| **Package manager** | apt, brew, Maven | pip |

### The Good News

- **Faster development**: No compile step, no header files
- **Less boilerplate**: Python is more concise
- **Great for prototyping**: Quick iteration
- **Excellent libraries**: Everything you need is a `pip install` away

### The Adjustment Period

- **No type safety by default**: Bugs may surface at runtime
- **Whitespace matters**: Indentation is part of syntax
- **Different debugging**: No stepping through compiled code
- **Performance**: Python is slower than C/C++/Java (but often doesn't matter)

---

## Python Fundamentals

### Your First Python Program

**C:**
```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

**Java:**
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Python:**
```python
print("Hello, World!")
```

That's it. No includes, no class wrapper, no main function needed for simple scripts.

### Variables and Types

**C/Java (static typing):**
```c
int count = 5;
char* name = "Alice";
double price = 19.99;
```

**Python (dynamic typing):**
```python
count = 5           # int inferred
name = "Alice"      # str inferred
price = 19.99       # float inferred

# You can change types (but shouldn't usually)
count = "five"      # Now it's a string!
```

**Python with Type Hints (recommended in this project):**
```python
count: int = 5
name: str = "Alice"
price: float = 19.99

def greet(person: str) -> str:
    return f"Hello, {person}!"
```

Type hints don't enforce types at runtime but help with:
- Documentation
- IDE autocompletion
- Static analysis tools (mypy)

### Functions

**C:**
```c
int add(int a, int b) {
    return a + b;
}
```

**Java:**
```java
public int add(int a, int b) {
    return a + b;
}
```

**Python:**
```python
def add(a, b):
    return a + b

# With type hints (preferred in this project)
def add(a: int, b: int) -> int:
    return a + b
```

### Default Arguments (Python feature)

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

greet("Alice")              # "Hello, Alice!"
greet("Bob", "Hi")          # "Hi, Bob!"
greet(greeting="Hey", name="Carol")  # Named arguments
```

### Classes

**Java:**
```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return this.name;
    }
}
```

**Python:**
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def get_name(self) -> str:
        return self.name
```

Note: `self` is explicit in Python (like `this` but always passed).

### Dataclasses (Modern Python)

This project uses dataclasses heavily - they're like Java records or C++ structs with auto-generated methods:

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str = ""  # Default value

# Auto-generates __init__, __repr__, __eq__, etc.
alice = Person("Alice", 30)
print(alice)  # Person(name='Alice', age=30, email='')
```

### Collections

**Lists (like ArrayList):**
```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)           # Add to end
first = numbers[0]          # Access by index
numbers.pop()               # Remove last
length = len(numbers)       # Get length
```

**Dictionaries (like HashMap):**
```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC"
}
name = person["name"]           # Access
person["email"] = "a@b.com"     # Add/update
age = person.get("age", 0)      # Get with default
```

**List Comprehensions (Python specialty):**
```python
# Instead of this (Java-style):
squares = []
for i in range(10):
    squares.append(i * i)

# Python way:
squares = [i * i for i in range(10)]

# With filter:
even_squares = [i * i for i in range(10) if i % 2 == 0]
```

### Error Handling

**Java:**
```java
try {
    int result = riskyOperation();
} catch (IOException e) {
    System.out.println("Error: " + e.getMessage());
} finally {
    cleanup();
}
```

**Python:**
```python
try:
    result = risky_operation()
except IOError as e:
    print(f"Error: {e}")
finally:
    cleanup()
```

### File I/O

**C:**
```c
FILE *f = fopen("file.txt", "r");
// ... read file
fclose(f);
```

**Python (with context manager):**
```python
with open("file.txt", "r") as f:
    content = f.read()
# File automatically closed when leaving 'with' block
```

### Imports and Modules

**Java:**
```java
import java.util.ArrayList;
import com.mycompany.utils.*;
```

**Python:**
```python
# Import entire module
import os

# Import specific items
from pathlib import Path

# Import with alias
import numpy as np

# Import from local file
from mymodule import MyClass
from .relative_module import something  # Relative import
```

### Running Python Code

**Compile and run (C):**
```bash
gcc program.c -o program
./program
```

**Compile and run (Java):**
```bash
javac Program.java
java Program
```

**Run (Python):**
```bash
python program.py
# or
python3 program.py
```

No compilation step. Python interprets the code directly.

---

## Understanding Async Programming

### Why Async?

In C/C++/Java, you typically handle concurrency with threads:

```java
// Java threads
Thread t = new Thread(() -> {
    // long-running task
});
t.start();
```

Python has threads too, but for I/O-bound operations (network calls, database queries, file operations), **async/await** is often better because:

1. **More efficient**: No thread overhead
2. **Simpler code**: Looks synchronous but runs concurrently
3. **Better for I/O**: Perfect for waiting on external resources

### The Problem Async Solves

**Synchronous code (blocking):**
```python
def fetch_all_users():
    user1 = fetch_user(1)      # Wait 1 second
    user2 = fetch_user(2)      # Wait 1 second
    user3 = fetch_user(3)      # Wait 1 second
    return [user1, user2, user3]
# Total: 3 seconds
```

**Async code (non-blocking):**
```python
async def fetch_all_users():
    user1, user2, user3 = await asyncio.gather(
        fetch_user(1),         # Start all three
        fetch_user(2),         # at the same time
        fetch_user(3),
    )
    return [user1, user2, user3]
# Total: ~1 second (parallel)
```

### Async Syntax

```python
import asyncio

# 1. Define an async function with 'async def'
async def fetch_data(url: str) -> dict:
    # 2. Use 'await' before calling other async functions
    response = await make_request(url)
    return response

# 3. Run async code with asyncio.run()
result = asyncio.run(fetch_data("https://api.example.com"))
```

### Key Concepts

**Coroutine**: A function defined with `async def`. It doesn't run immediately - it returns a coroutine object.

```python
async def my_func():
    return 42

# This doesn't run the function!
coro = my_func()  # Returns a coroutine object

# This runs it:
result = asyncio.run(my_func())  # Returns 42
```

**Await**: Pauses the coroutine until the awaited operation completes.

```python
async def example():
    print("Before")
    await asyncio.sleep(1)  # Pause 1 second (non-blocking!)
    print("After")
```

**Important**: You can only use `await` inside an `async def` function!

### Async Context Managers

Similar to `with` statements, but async:

```python
# Sync context manager
with open("file.txt") as f:
    content = f.read()

# Async context manager
async with aiohttp.ClientSession() as session:
    response = await session.get(url)
```

This project uses async context managers for database connections:

```python
async with self.connection() as db:
    cursor = await db.execute(query)
    rows = await cursor.fetchall()
```

### Common Async Patterns in This Project

**Pattern 1: Simple async method**
```python
async def get_user(self, user_id: str) -> dict:
    async with self.connection() as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
```

**Pattern 2: Gathering multiple operations**
```python
async def get_all_data(self):
    users, posts, comments = await asyncio.gather(
        self.get_users(),
        self.get_posts(),
        self.get_comments(),
    )
    return {"users": users, "posts": posts, "comments": comments}
```

**Pattern 3: Async generator (yielding results)**
```python
async def fetch_pages(self, urls: list[str]):
    for url in urls:
        page = await fetch_page(url)
        yield page  # Caller receives results as they come
```

### When to Use Async

**Use async for:**
- Database queries
- HTTP/API requests
- File I/O (with async libraries)
- Waiting on external services

**Don't use async for:**
- CPU-intensive calculations
- Simple, quick operations
- Code that doesn't wait on anything

---

## Web and API Concepts

### What is an API?

In C/C++, you might think of an API as a header file defining function signatures. In web development:

**API (Application Programming Interface)**: A way for programs to communicate over the network, typically using HTTP.

```
Client                    Server
  │                         │
  │  HTTP Request           │
  │  GET /users/123         │
  ├────────────────────────►│
  │                         │
  │  HTTP Response          │
  │  {"id": 123, "name":..} │
  │◄────────────────────────┤
```

### HTTP Methods

| Method | Purpose | SQL Equivalent |
|--------|---------|----------------|
| GET | Retrieve data | SELECT |
| POST | Create new data | INSERT |
| PUT | Update/replace data | UPDATE |
| PATCH | Partial update | UPDATE (partial) |
| DELETE | Remove data | DELETE |

### JSON (JavaScript Object Notation)

The standard data format for APIs. It's like a text representation of a dictionary:

```json
{
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "active": true,
    "roles": ["admin", "user"],
    "profile": {
        "avatar": "https://..."
    }
}
```

**Python to JSON:**
```python
import json

data = {"name": "Alice", "age": 30}
json_string = json.dumps(data)  # '{"name": "Alice", "age": 30}'

parsed = json.loads(json_string)  # Back to dict
```

### What is MCP (Model Context Protocol)?

MCP is a protocol for AI agents to communicate. Think of it like:

- **HTTP** is for web browsers talking to web servers
- **MCP** is for AI systems talking to AI capability servers

In this project:
- **Orchestrator** = MCP Host (client)
- **Ministries** = MCP Servers (provide tools)

**MCP Communication:**
```
┌─────────────┐     JSON-RPC      ┌─────────────┐
│ Orchestrator│ ◄───────────────► │  Ministry   │
│ (MCP Host)  │                   │ (MCP Server)│
└─────────────┘                   └─────────────┘
```

**Tools** are functions the server provides:
```python
# Server defines a tool
Tool(
    name="implement_feature",
    description="Write code for a feature",
    inputSchema={...}
)

# Host calls the tool
result = await server.call_tool("implement_feature", {"feature": "login"})
```

**Resources** are data the server provides:
```python
# Server defines a resource
Resource(
    uri="code://codebase-map",
    name="Codebase Map",
    description="Project structure"
)

# Host reads the resource
content = await server.read_resource("code://codebase-map")
```

### What is Ollama?

Ollama runs AI models locally on your computer:

```
┌─────────────┐     HTTP API      ┌─────────────┐
│ This Project│ ◄───────────────► │   Ollama    │
│             │                   │   Server    │
└─────────────┘                   └──────┬──────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │  AI Model   │
                                  │ (qwen2.5)   │
                                  └─────────────┘
```

**Commands:**
```bash
# Start the server
ollama serve

# Download a model
ollama pull mistral:7b

# List models
ollama list

# Interactive chat (testing)
ollama run mistral:7b
```

### What is SQLite?

SQLite is a file-based database. Unlike MySQL/PostgreSQL which run as separate servers:

| Traditional DB | SQLite |
|----------------|--------|
| Separate server process | Just a file |
| Network communication | Direct file access |
| Complex setup | Zero setup |
| `mysql://host:port/db` | Just `database.db` |

**In this project:**
- Database file: `data/country.db`
- Schema: `shared/schema.sql`
- Python access: `shared/database.py`

```python
# Connecting to SQLite
from shared.database import Database

db = Database("data/country.db")
await db.initialize()

# Querying (like JDBC but async)
async with db.connection() as conn:
    cursor = await conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
```

---

## Understanding This Project

### The Big Picture

This project creates a "micro-country" of AI experts:

```
┌─────────────────────────────────────────────────────────────┐
│                    MICRO-COUNTRY                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    ORCHESTRATOR                        │   │
│  │  • Receives your requests                             │   │
│  │  • Routes to the right ministry                       │   │
│  │  • Coordinates specialists                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│       ┌────────┬───────────┼───────────┬─────────┐          │
│       │        │           │           │         │          │
│       ▼        ▼           ▼           ▼         ▼          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │
│  │ CODE   │ │RESEARCH│ │QUALITY │ │  OPS   │ │ARCHIVES│    │
│  │Ministry│ │Ministry│ │Ministry│ │Ministry│ │Ministry│    │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              SHARED KNOWLEDGE SERVER                   │   │
│  │            (SQLite Database + MCP Server)              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### How a Request Flows

When you type: "Write a function to sort a list"

```
1. You type request
         │
         ▼
2. Orchestrator receives it
         │
         ▼
3. route_request() analyzes keywords
   "write" + "function" → Code Ministry
         │
         ▼
4. select_specialist() picks expert
   "write" → Coder (not Architect or Debugger)
         │
         ▼
5. OllamaBridge.generate_with_reasoning()
   - Builds prompt with Genius Protocol
   - Sends to Ollama
   - Parses response
         │
         ▼
6. Coder follows 7-step Genius Protocol:
   OBSERVE → THINK → REFLECT → CRITIQUE → REFINE → ACT → VERIFY
         │
         ▼
7. Response returned to you
```

### Key Components Explained

**1. Orchestrator (`orchestrator.py`)**

The "main" of the application. Think of it as:
- The receptionist who directs your calls
- The traffic controller routing requests

```python
class Orchestrator:
    def route_request(self, request: Request) -> str:
        """Determine which ministry handles this."""
        # Keywords like "code", "function" → Code Ministry
        # Keywords like "test", "security" → Quality Ministry
        pass

    def select_specialist(self, ministry: str, request: Request) -> str:
        """Pick the right expert within a ministry."""
        pass

    async def process_request(self, request: Request) -> Response:
        """Main processing logic."""
        pass
```

**2. Genius Protocol (`genius/protocol.py`)**

Forces every AI response through structured reasoning:

```
Step 1: OBSERVE - "What am I being asked?"
Step 2: THINK   - "What are my options?"
Step 3: REFLECT - "Am I understanding correctly?"
Step 4: CRITIQUE - "What could go wrong?"
Step 5: REFINE  - "How can I improve my approach?"
Step 6: ACT     - "Here's my answer."
Step 7: VERIFY  - "Did I answer correctly?"
```

This prevents the AI from giving shallow or incorrect responses.

**3. Evidence Court (`genius/evidence_court.py`)**

When experts disagree, evidence decides:

```
Architect: "Use microservices"
  Evidence: Netflix case study (EMPIRICAL)

Coder: "Use monolith"
  Evidence: KISS principle (THEORETICAL)

Evidence Court: EMPIRICAL > THEORETICAL
  Winner: Architect
```

**4. Ministries (`ministries/*/`)**

Each ministry is an MCP server with specialists:

```
ministries/code/
├── minister.py          # The MCP server
└── specialists/
    ├── architect.py     # System design
    ├── coder.py         # Implementation
    └── debugger.py      # Bug fixing
```

**5. Database (`shared/database.py`)**

Async SQLite wrapper for persistent storage:

```python
class Database:
    async def initialize(self):
        """Create tables from schema.sql"""

    async def log_decision(self, ministry, decision, rationale):
        """Store a decision"""

    async def get_decisions(self, ministry=None, limit=50):
        """Retrieve decisions"""
```

**6. Ollama Bridge (`bridge/ollama_bridge.py`)**

Connects to the local AI model:

```python
class OllamaBridge:
    async def generate(self, prompt: str, specialist: str) -> str:
        """Send prompt to AI, get response"""

    async def generate_with_reasoning(self, prompt, specialist):
        """Generate with parsed Genius Protocol steps"""
```

### File Organization Mental Model

```
micro-country/
│
├── orchestrator.py          # Main entry point
│                            # Like main.c or Main.java
│
├── genius/                  # Core algorithms
│   ├── protocol.py          # Reasoning logic
│   └── evidence_court.py    # Conflict resolution
│                            # Like core/*.c or core/*.java
│
├── ministries/              # Feature modules
│   ├── code/                # Software development features
│   ├── research/            # Research features
│   └── ...                  # Like features/ or modules/
│
├── shared/                  # Shared utilities
│   ├── database.py          # Database access
│   └── schema.sql           # Database structure
│                            # Like utils/ or common/
│
├── bridge/                  # External integrations
│   └── ollama_bridge.py     # LLM integration
│                            # Like drivers/ or adapters/
│
└── tests/                   # Test suite
    └── test_*.py            # Like test/ or tests/
```

---

## Hands-On: Your First Code Change

Let's make a real change to understand the codebase.

### Exercise 1: Add a Simple Command

**Goal**: Add a `/hello` command that responds with a greeting.

**Step 1: Find where commands are handled**

Open `orchestrator.py` and find the `run_interactive` method.

**Step 2: Add the command**

Find where other commands like `/debate` and `/review` are handled, and add:

```python
# Inside run_interactive method, with other command handling
if user_input.startswith("/hello"):
    name = user_input[len("/hello"):].strip() or "World"
    print(f"\n[orchestrator]\nHello, {name}! Welcome to the Micro-Country of Geniuses!")
    continue
```

**Step 3: Test it**

```bash
python orchestrator.py
> /hello Alice
# Should see: Hello, Alice! Welcome to the Micro-Country of Geniuses!
```

### Exercise 2: Add a Database Method

**Goal**: Add a method to count decisions by ministry.

**Step 1: Open `shared/database.py`**

**Step 2: Add the method**

```python
async def count_decisions_by_ministry(self) -> dict[str, int]:
    """Count decisions grouped by ministry."""
    async with self.connection() as db:
        cursor = await db.execute("""
            SELECT ministry, COUNT(*) as count
            FROM decision_log
            GROUP BY ministry
        """)
        rows = await cursor.fetchall()
        return {row["ministry"]: row["count"] for row in rows}
```

**Step 3: Test it**

Create a test file `test_my_changes.py`:

```python
import asyncio
from shared.database import Database

async def test_count():
    db = Database("data/country.db")
    await db.initialize()
    counts = await db.count_decisions_by_ministry()
    print(f"Decision counts: {counts}")

asyncio.run(test_count())
```

Run it:
```bash
python test_my_changes.py
```

### Exercise 3: Add a New Tool to a Ministry

**Goal**: Add a `get_line_count` tool to the Operations ministry.

**Step 1: Open `ministries/operations/minister.py`**

**Step 2: Add the tool definition in `list_tools()`:**

```python
Tool(
    name="get_line_count",
    description="Count lines in a file",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file",
            },
        },
        "required": ["path"],
    },
),
```

**Step 3: Add the implementation in `_execute_tool()`:**

```python
elif name == "get_line_count":
    file_path = Path(args["path"])
    if not file_path.exists():
        return {"success": False, "error": "File not found"}

    with open(file_path, "r") as f:
        line_count = sum(1 for _ in f)

    return {"success": True, "line_count": line_count, "path": str(file_path)}
```

**Step 4: Test it (conceptually)**

You would test this through the MCP interface or by calling the method directly.

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Forgetting `await`

**Wrong:**
```python
async def get_user(self):
    user = self.fetch_from_db()  # Missing await!
    return user  # Returns a coroutine, not the result
```

**Right:**
```python
async def get_user(self):
    user = await self.fetch_from_db()
    return user
```

**Symptom**: You get a coroutine object instead of actual data.

### Pitfall 2: Indentation Errors

**Wrong:**
```python
def my_function():
    print("Hello")
     print("World")  # Extra space - SyntaxError!
```

**Right:**
```python
def my_function():
    print("Hello")
    print("World")  # Same indentation
```

**Tip**: Use 4 spaces per level. Configure your editor to show whitespace.

### Pitfall 3: Mutable Default Arguments

**Wrong:**
```python
def add_item(item, items=[]):  # Don't do this!
    items.append(item)
    return items

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] - Unexpected!
```

**Right:**
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Pitfall 4: Not Using `async with` for Connections

**Wrong:**
```python
async def query(self):
    db = await self.get_connection()
    result = await db.execute("SELECT ...")
    # Connection never closed!
    return result
```

**Right:**
```python
async def query(self):
    async with self.connection() as db:
        result = await db.execute("SELECT ...")
        return await result.fetchall()
    # Connection automatically closed
```

### Pitfall 5: Forgetting `self`

**Wrong:**
```python
class MyClass:
    def my_method():  # Missing self!
        return "hello"

obj = MyClass()
obj.my_method()  # TypeError!
```

**Right:**
```python
class MyClass:
    def my_method(self):
        return "hello"
```

### Pitfall 6: String Formatting

**C-style (works but not Pythonic):**
```python
name = "Alice"
age = 30
print("Name: %s, Age: %d" % (name, age))
```

**Python f-string (preferred):**
```python
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age}")
```

### Pitfall 7: Path Handling

**Wrong (Windows-specific):**
```python
path = "data\\country.db"  # Won't work on Linux/Mac
```

**Right (cross-platform):**
```python
from pathlib import Path
path = Path("data") / "country.db"
```

---

## Reference: Python vs C/C++/Java Syntax

### Variables

| C/C++/Java | Python |
|------------|--------|
| `int x = 5;` | `x = 5` or `x: int = 5` |
| `const int X = 5;` | `X = 5` (convention: UPPERCASE) |
| `String s = "hello";` | `s = "hello"` |
| `int[] arr = {1,2,3};` | `arr = [1, 2, 3]` |

### Control Flow

**If/Else:**

| C/Java | Python |
|--------|--------|
| `if (x > 5) { ... }` | `if x > 5:` |
| `else if (x < 0) { ... }` | `elif x < 0:` |
| `else { ... }` | `else:` |

**Loops:**

| C/Java | Python |
|--------|--------|
| `for (int i=0; i<10; i++)` | `for i in range(10):` |
| `while (condition) { ... }` | `while condition:` |
| `for (String s : list)` | `for s in list:` |

### Functions

| C/Java | Python |
|--------|--------|
| `int add(int a, int b) { return a+b; }` | `def add(a, b): return a + b` |
| `void print(String s) { ... }` | `def print_it(s): ...` |

### Classes

| Java | Python |
|------|--------|
| `public class Foo { ... }` | `class Foo:` |
| `public Foo() { ... }` | `def __init__(self):` |
| `private int x;` | `self._x = ...` (convention) |
| `this.x = 5;` | `self.x = 5` |

### Null/None

| C/C++/Java | Python |
|------------|--------|
| `null` / `NULL` / `nullptr` | `None` |
| `if (x == null)` | `if x is None:` |
| `if (x != null)` | `if x is not None:` |

### Boolean

| C/C++/Java | Python |
|------------|--------|
| `true` / `false` | `True` / `False` |
| `&&` | `and` |
| `||` | `or` |
| `!` | `not` |

### Common Operations

| Operation | C/Java | Python |
|-----------|--------|--------|
| Print | `printf()` / `System.out.println()` | `print()` |
| String length | `strlen()` / `s.length()` | `len(s)` |
| Array length | `sizeof(arr)/sizeof(arr[0])` / `arr.length` | `len(arr)` |
| Type check | `instanceof` | `isinstance(obj, Type)` |
| String concat | `strcat()` / `+` | `+` or f-strings |

### Exception Handling

| Java | Python |
|------|--------|
| `try { ... }` | `try:` |
| `catch (Exception e) { ... }` | `except Exception as e:` |
| `finally { ... }` | `finally:` |
| `throw new Exception()` | `raise Exception()` |

---

## Next Steps

Now that you understand the basics:

1. **Run the system**: `python orchestrator.py`
2. **Explore the code**: Start with `orchestrator.py`
3. **Try the exercises** in this guide
4. **Read the other docs**:
   - [QUICK_START.md](QUICK_START.md) - Hands-on examples
   - [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Technical details
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design

### Recommended Learning Path

1. **Week 1**: Run the system, try all Quick Start examples
2. **Week 2**: Read orchestrator.py, understand request flow
3. **Week 3**: Read genius/protocol.py, understand Genius Protocol
4. **Week 4**: Modify a ministry, add a simple tool
5. **Week 5**: Add a new specialist
6. **Week 6**: Work on a real enhancement

Good luck, and welcome to Python development!
