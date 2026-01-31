# Glossary

This glossary defines terms used in the Micro-Country of Geniuses system. Terms are organized alphabetically with cross-references to related concepts.

---

## A

### Adversarial Review
A review process where a specialist (usually the Auditor) acts as a skeptic to find flaws in work produced by another specialist. The reviewer actively looks for problems rather than confirming the work is correct.

**Related**: [Auditor](#auditor), [Debate Protocol](#debate-protocol)

### Analyst
A specialist in the Ministry of Research who examines data, finds patterns, and draws conclusions from information. The analyst processes complex information and extracts insights.

**Related**: [Ministry of Research](#ministry-of-research), [Specialist](#specialist)

### API (Application Programming Interface)
A set of rules that allow different software programs to communicate with each other. In this system, MCP servers expose APIs (tools and resources) that the orchestrator calls.

**Example**: The `implement_feature` tool is part of the Code Ministry's API.

**Related**: [MCP](#mcp-model-context-protocol), [Tool](#tool)

### Architect
A specialist in the Ministry of Code who designs system structures before implementation. The architect decides how components should fit together, which patterns to use, and how data should flow.

**Related**: [Ministry of Code](#ministry-of-code), [Design](#design)

### Archives
See [Ministry of Archives](#ministry-of-archives).

### Async/Await
A Python programming pattern for writing code that can wait for slow operations (like network requests or database queries) without blocking other work. This system uses async/await extensively.

**Example**:
```python
async def get_data():
    result = await database.query("SELECT * FROM users")
    return result
```

### Auditor
A specialist in the Ministry of Quality who reviews code and designs for security vulnerabilities, quality issues, and potential problems. The auditor is deliberately skeptical.

**Related**: [Ministry of Quality](#ministry-of-quality), [Adversarial Review](#adversarial-review)

---

## B

### Bridge
A software component that connects two different systems. The **Ollama Bridge** connects the Micro-Country system to the Ollama LLM server.

**Related**: [Ollama](#ollama), [OllamaBridge](#ollamabridge)

---

## C

### Coder
A specialist in the Ministry of Code who writes actual code implementations. Unlike the Architect who designs, the Coder produces working code.

**Related**: [Ministry of Code](#ministry-of-code), [Architect](#architect)

### Collective Intelligence
The ability of multiple agents working together to produce results better than any single agent could. In this system, collective intelligence emerges from debates, adversarial reviews, and synthesis.

**Related**: [Debate Protocol](#debate-protocol), [Emergent Synthesis](#emergent-synthesis)

### Config (Configuration)
Settings that control how the system behaves. Stored in `config.yaml`. Includes things like which AI model to use, where the database is located, and timeout values.

**Related**: [YAML](#yaml)

### Constitution
The core rules and values that govern how the system behaves. Stored in the database and consulted before making decisions. Think of it as the "laws" of the micro-country.

**Related**: [Knowledge Server](#knowledge-server), [Database](#database)

### Context
Information that helps specialists understand a situation. There are several types:
- **Temporal context**: What happened before
- **Social context**: Who else is involved
- **Task context**: What we're trying to accomplish
- **Domain context**: Relevant background knowledge

### Court
See [Evidence Court](#evidence-court).

### Critique
Step 4 of the Genius Protocol where a specialist identifies potential problems with their approach. Self-criticism before producing output.

**Related**: [Genius Protocol](#genius-protocol)

---

## D

### Database
A structured way to store data permanently. This system uses SQLite, a simple database stored as a single file. The database keeps decisions, knowledge, and task history.

**Location**: `data/country.db`

**Related**: [SQLite](#sqlite)

### Dataclass
A Python feature for creating classes that mainly hold data. Used throughout this system for structured data like `ReasoningTrace` and `Evidence`.

**Example**:
```python
@dataclass
class Evidence:
    evidence_type: EvidenceType
    description: str
    confidence: float
```

### Debate Protocol
A structured discussion between specialists to reach consensus on important decisions. Multiple specialists present their views, critique each other, and synthesize the best ideas.

**Flow**: Position → Critique → Refine → Synthesize

**Related**: [Collective Intelligence](#collective-intelligence), [Evidence Court](#evidence-court)

### Debugger
A specialist in the Ministry of Code who finds and fixes problems in code. The debugger analyzes error messages, traces code execution, and identifies root causes.

**Related**: [Ministry of Code](#ministry-of-code)

### Decision Log
A record of decisions made by the system, including the rationale and context. Stored in the database for future reference.

**Related**: [Ministry of Archives](#ministry-of-archives), [Knowledge Server](#knowledge-server)

### Deployer
A specialist in the Ministry of Operations who handles deploying software to different environments (development, staging, production).

**Related**: [Ministry of Operations](#ministry-of-operations)

### Design
A plan for how something should be built. Architectural designs describe system structure, API designs describe interfaces, and data designs describe how information is organized.

---

## E

### Emergent Synthesis
When multiple perspectives combine to create insight that none could produce alone. For example, combining Research findings + Code implementation details + Quality testing results into a better understanding.

**Related**: [Collective Intelligence](#collective-intelligence)

### Empirical Evidence
Evidence based on observation or experiment. The strongest type of evidence in the Evidence Court. Includes benchmarks, test results, and measured data.

**Related**: [Evidence Court](#evidence-court), [Evidence Hierarchy](#evidence-hierarchy)

### Evidence
Supporting information for a position or decision. In the Evidence Court, evidence is classified by type and strength.

**Types**: Empirical, Precedent, Consensus, Theoretical, Intuition

### Evidence Court
A mechanism for resolving disagreements between specialists. When geniuses disagree, they present evidence for their positions, and the court (Ministry of Archives) rules based on evidence strength.

**Related**: [Evidence Hierarchy](#evidence-hierarchy), [Ministry of Archives](#ministry-of-archives)

### Evidence Hierarchy
The ranking of evidence types from strongest to weakest:
1. **Empirical** - Data, tests, measurements (strongest)
2. **Precedent** - What worked before
3. **Consensus** - Multiple experts agree
4. **Theoretical** - Logical arguments
5. **Intuition** - Gut feelings (weakest)

---

## F

### File Manager
A specialist in the Ministry of Operations who handles file operations: reading, writing, copying, moving, and deleting files.

**Related**: [Ministry of Operations](#ministry-of-operations)

---

## G

### Genius
An AI specialist with exceptional reasoning ability, implemented through the Genius Protocol. Each genius has deep domain expertise and follows structured reasoning.

**Related**: [Genius Protocol](#genius-protocol), [Specialist](#specialist)

### Genius Protocol
A 7-step reasoning process that every specialist follows:
1. **OBSERVE** - Understand the request
2. **THINK** - Reason through options
3. **REFLECT** - Check understanding
4. **CRITIQUE** - Find problems
5. **REFINE** - Improve approach
6. **ACT** - Produce output
7. **VERIFY** - Check quality

**Related**: [ReasoningTrace](#reasoningtrace)

### Glob Pattern
A pattern for matching file names. Uses wildcards like `*` (any characters) and `**` (any directories).

**Example**: `*.py` matches all Python files, `tests/**/*.py` matches all Python files in tests directory and subdirectories.

---

## H

### Handler
A function that processes a specific type of request. In MCP, handlers process tool calls, resource reads, and other operations.

### Host
In MCP architecture, the program that connects to and manages MCP servers. The orchestrator is the MCP host in this system.

**Related**: [MCP](#mcp-model-context-protocol), [Orchestrator](#orchestrator)

---

## I

### Indexer
A specialist in the Ministry of Archives who organizes and categorizes knowledge for efficient retrieval.

**Related**: [Ministry of Archives](#ministry-of-archives)

### Inference
The process of running an AI model to generate output from input. When you ask a question, the model performs inference to produce an answer.

**Related**: [LLM](#llm-large-language-model), [Ollama](#ollama)

### Intuition Evidence
The weakest form of evidence in the Evidence Court - gut feelings or hunches without supporting data or reasoning.

**Related**: [Evidence Hierarchy](#evidence-hierarchy)

---

## J

### JSON (JavaScript Object Notation)
A text format for structured data. Used throughout this system for communication, configuration, and storage.

**Example**:
```json
{
  "name": "architect",
  "ministry": "code",
  "active": true
}
```

### JSON-RPC
A protocol for remote procedure calls using JSON. MCP uses JSON-RPC 2.0 for communication between servers and hosts.

**Related**: [MCP](#mcp-model-context-protocol), [STDIO](#stdio)

---

## K

### Knowledge Base
Accumulated information stored in the database. Includes domain knowledge, lessons learned, and project context.

**Related**: [Knowledge Server](#knowledge-server), [Database](#database)

### Knowledge Server
The MCP server that provides access to shared information stored in SQLite. All ministries can read from and write to the knowledge server.

**File**: `shared/knowledge_server.py`

**Related**: [Database](#database), [Resource](#resource)

---

## L

### LLM (Large Language Model)
An AI model trained on large amounts of text that can understand and generate human-like text. This system uses Ollama to run LLMs locally.

**Related**: [Ollama](#ollama), [Model](#model)

### Local
Running on your own computer rather than on a remote server. This entire system runs locally - no data is sent to external services.

---

## M

### MCP (Model Context Protocol)
A protocol developed by Anthropic for AI agents to communicate and share capabilities. Each ministry is an MCP server exposing tools and resources.

**Components**: Servers, Hosts, Tools, Resources

**Related**: [Tool](#tool), [Resource](#resource), [Server](#server)

### Memory
A specialist in the Ministry of Archives who stores and recalls decisions, lessons, and context from the knowledge base.

**Related**: [Ministry of Archives](#ministry-of-archives)

### Messenger
A specialist in the Ministry of Communications who handles sending messages between ministries and to users.

**Related**: [Ministry of Communications](#ministry-of-communications)

### Ministry
A department of specialists with related responsibilities. There are six ministries:
- [Code](#ministry-of-code)
- [Research](#ministry-of-research)
- [Quality](#ministry-of-quality)
- [Operations](#ministry-of-operations)
- [Archives](#ministry-of-archives)
- [Communications](#ministry-of-communications)

### Ministry of Archives
Department responsible for knowledge management. Stores decisions, recalls context, manages the knowledge base, and serves as judge in the Evidence Court.

**Specialists**: Memory, Indexer

### Ministry of Code
Department responsible for software development. Designs architecture, writes code, and debugs issues.

**Specialists**: Architect, Coder, Debugger

### Ministry of Communications
Department responsible for messaging and scheduling. Sends messages between ministries and notifies users.

**Specialists**: Messenger, Scheduler

### Ministry of Operations
Department responsible for system management. Manages files, runs commands, and handles deployments.

**Specialists**: File Manager, Shell Runner, Deployer

### Ministry of Quality
Department responsible for testing and security. Writes tests, performs security audits, and validates implementations.

**Specialists**: Tester, Auditor, Validator

### Ministry of Research
Department responsible for information gathering. Searches for information, analyzes documents, and writes documentation.

**Specialists**: Analyst, Writer, Searcher

### Model
In AI context, the trained neural network that processes inputs and generates outputs. This system uses models through Ollama (e.g., `qwen2.5:14b`).

**Related**: [LLM](#llm-large-language-model), [Ollama](#ollama)

---

## O

### Observe
Step 1 of the Genius Protocol where a specialist reads and understands the request before taking action.

**Related**: [Genius Protocol](#genius-protocol)

### Ollama
A program that runs AI models locally on your computer. It provides an API that the Micro-Country system uses for inference.

**Website**: ollama.ai

**Related**: [LLM](#llm-large-language-model), [OllamaBridge](#ollamabridge)

### OllamaBridge
The Python class that connects to Ollama and handles LLM inference. Manages prompts, injects the Genius Protocol, and processes responses.

**File**: `bridge/ollama_bridge.py`

### Orchestrator
The central coordinator of the Micro-Country system. Routes user requests to appropriate ministries, manages debates, and aggregates responses.

**File**: `orchestrator.py`

**Related**: [Ministry](#ministry), [Routing](#routing)

---

## P

### PATH
An environment variable that tells your operating system where to find programs. If Python or Ollama isn't in PATH, your terminal won't recognize them.

### Precedent
A type of evidence based on what worked before. "We did X in a similar situation and it worked." Second strongest evidence type.

**Related**: [Evidence Hierarchy](#evidence-hierarchy), [Evidence Court](#evidence-court)

### Prompt
Text sent to an LLM to instruct it what to do. Each specialist has a system prompt that defines their expertise and reasoning style.

**Location**: `genius/prompts/`

### Protocol
A set of rules for communication or behavior. This system uses multiple protocols:
- **Genius Protocol** - How specialists reason
- **MCP** - How servers communicate
- **Debate Protocol** - How specialists discuss

---

## Q

### Quality Gate
A checkpoint that must pass before proceeding. For example, code must pass tests (a quality gate) before deployment.

**Related**: [Ministry of Quality](#ministry-of-quality)

---

## R

### ReasoningTrace
A record of a specialist's reasoning through the 7 steps of the Genius Protocol. Stored in the database for debugging and analysis.

**Related**: [Genius Protocol](#genius-protocol)

### Refine
Step 5 of the Genius Protocol where a specialist improves their approach based on self-critique.

**Related**: [Genius Protocol](#genius-protocol)

### Reflect
Step 3 of the Genius Protocol where a specialist checks their understanding before proceeding.

**Related**: [Genius Protocol](#genius-protocol)

### Resource
In MCP, a piece of data that can be read. Resources are identified by URIs like `code://codebase-map`. Unlike tools, resources are read-only.

**Related**: [MCP](#mcp-model-context-protocol), [Tool](#tool)

### Routing
The process of deciding which ministry or specialist should handle a request. The orchestrator analyzes requests and routes them appropriately.

**Example**: "Write a function" → Ministry of Code → Coder

**Related**: [Orchestrator](#orchestrator)

---

## S

### Scheduler
A specialist in the Ministry of Communications who schedules tasks for future execution and manages deadlines.

**Related**: [Ministry of Communications](#ministry-of-communications)

### Schema
The structure of a database - what tables exist, what columns they have, and how they relate. Defined in `shared/schema.sql`.

**Related**: [Database](#database), [SQLite](#sqlite)

### Searcher
A specialist in the Ministry of Research who finds information from various sources.

**Related**: [Ministry of Research](#ministry-of-research)

### Server
In MCP, a program that provides tools and resources. Each ministry is an MCP server.

**Related**: [MCP](#mcp-model-context-protocol), [Ministry](#ministry)

### Shell Runner
A specialist in the Ministry of Operations who executes command-line commands.

**Related**: [Ministry of Operations](#ministry-of-operations)

### Specialist
An expert within a ministry, implemented as an MCP server with specific tools. Each specialist follows the Genius Protocol for their domain.

**Examples**: Architect, Coder, Tester, Auditor

**Related**: [Genius Protocol](#genius-protocol), [Ministry](#ministry)

### SQLite
A simple, file-based database system. The entire database is stored in a single file (`data/country.db`). Used for its simplicity and portability.

**Related**: [Database](#database)

### STDIO (Standard Input/Output)
A communication method where programs send/receive data through standard input and output streams. MCP uses STDIO for server communication.

**Related**: [MCP](#mcp-model-context-protocol), [JSON-RPC](#json-rpc)

### Synthesis
Combining multiple pieces of information into a coherent whole. In debates, synthesis combines the best ideas from all participants.

**Related**: [Debate Protocol](#debate-protocol), [Emergent Synthesis](#emergent-synthesis)

---

## T

### Task
A unit of work to be completed. Tasks are tracked in the database with status (pending, in_progress, completed) and can have dependencies.

### Tester
A specialist in the Ministry of Quality who designs and runs tests to verify code works correctly.

**Related**: [Ministry of Quality](#ministry-of-quality)

### Think
Step 2 of the Genius Protocol where a specialist reasons through options and approaches.

**Related**: [Genius Protocol](#genius-protocol)

### Tool
In MCP, an action that can be performed. Tools have inputs (parameters) and outputs (results). Unlike resources, tools perform actions.

**Examples**: `implement_feature`, `run_tests`, `security_audit`

**Related**: [MCP](#mcp-model-context-protocol), [Resource](#resource)

### Transport
The method used to send messages between programs. This system uses STDIO transport for all MCP communication.

**Related**: [STDIO](#stdio), [MCP](#mcp-model-context-protocol)

---

## U

### URI (Uniform Resource Identifier)
A string that identifies a resource. In MCP, resources have URIs like `code://codebase-map` or `quality://test-results`.

**Related**: [Resource](#resource)

---

## V

### Validator
A specialist in the Ministry of Quality who verifies that implementations meet requirements.

**Related**: [Ministry of Quality](#ministry-of-quality)

### Verify
Step 7 of the Genius Protocol where a specialist checks that their output is correct and complete.

**Related**: [Genius Protocol](#genius-protocol)

### Virtual Environment (venv)
An isolated Python environment that keeps this project's packages separate from other Python projects. Recommended for all Python development.

**Commands**:
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

---

## W

### Writer
A specialist in the Ministry of Research who creates documentation and written content.

**Related**: [Ministry of Research](#ministry-of-research)

---

## Y

### YAML (YAML Ain't Markup Language)
A human-readable data format used for configuration. The system's configuration is stored in `config.yaml`.

**Example**:
```yaml
ollama:
  host: "http://localhost:11434"
  model: "qwen2.5:14b"
```

---

## Quick Reference

### The 7 Steps
1. OBSERVE → 2. THINK → 3. REFLECT → 4. CRITIQUE → 5. REFINE → 6. ACT → 7. VERIFY

### The 6 Ministries
Code • Research • Quality • Operations • Archives • Communications

### The 5 Evidence Types
Empirical > Precedent > Consensus > Theoretical > Intuition

### Key Files
| File | Purpose |
|------|---------|
| `orchestrator.py` | Main program |
| `config.yaml` | Settings |
| `data/country.db` | Database |
| `genius/protocol.py` | Reasoning logic |

---

## See Also

- [User Guide](USER_GUIDE.md) - How to use the system
- [Developer Guide](DEVELOPER_GUIDE.md) - How to develop for the system
- [Architecture](ARCHITECTURE.md) - How the system is designed
- [API Reference](API_REFERENCE.md) - Detailed API documentation
