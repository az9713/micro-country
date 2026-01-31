# Architecture Guide

Deep dive into the system architecture of the Micro-Country of Geniuses.

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [The Genius Protocol](#the-genius-protocol)
5. [The Evidence Court](#the-evidence-court)
6. [Database Design](#database-design)
7. [Design Decisions](#design-decisions)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                    (Interactive CLI Mode)                           │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                      CENTRAL ORCHESTRATOR                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │  │
│  │   │ Ollama Bridge│  │   Request    │  │   Context    │       │  │
│  │   │ (LLM Client) │  │   Router     │  │  Aggregator  │       │  │
│  │   └──────────────┘  └──────────────┘  └──────────────┘       │  │
│  │                                                               │  │
│  │   ┌──────────────┐  ┌──────────────┐                         │  │
│  │   │   Genius     │  │   Evidence   │                         │  │
│  │   │  Protocol    │  │    Court     │                         │  │
│  │   └──────────────┘  └──────────────┘                         │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                           MCP Host                                  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
     ┌───────────┬───────────────┼───────────────┬───────────────┐
     │           │               │               │               │
┌────▼────┐ ┌────▼────┐ ┌───────▼───────┐ ┌────▼────┐ ┌────▼────┐
│  CODE   │ │RESEARCH │ │    QUALITY    │ │   OPS   │ │ARCHIVES │
│Ministry │ │Ministry │ │   Ministry    │ │Ministry │ │Ministry │
├─────────┤ ├─────────┤ ├───────────────┤ ├─────────┤ ├─────────┤
│architect│ │ analyst │ │    tester     │ │file_mgr │ │ memory  │
│ coder   │ │ writer  │ │   auditor     │ │shell_run│ │ indexer │
│debugger │ │searcher │ │  validator    │ │deployer │ │(+ Judge)│
└─────────┘ └─────────┘ └───────────────┘ └─────────┘ └─────────┘
     │           │               │               │               │
     └───────────┴───────────────┼───────────────┴───────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   SHARED KNOWLEDGE      │
                    │       SERVER            │
                    │  (SQLite Database)      │
                    │                         │
                    │  • Constitution         │
                    │  • Decision Log         │
                    │  • Domain Knowledge     │
                    │  • Task History         │
                    │  • Court Precedents     │
                    └─────────────────────────┘
```

### Design Philosophy

The system is designed around these principles:

1. **Separation of Concerns**: Each ministry has a specific responsibility
2. **Single Source of Truth**: All shared data in one database
3. **Local-First**: Everything runs on your machine
4. **Evidence-Based**: Decisions backed by evidence, not opinion
5. **Transparent Reasoning**: Every answer shows its thought process

---

## Component Architecture

### 1. Central Orchestrator

**Location**: `orchestrator.py`

**Responsibilities**:
- Receive user requests
- Route to appropriate ministry
- Select specialist within ministry
- Coordinate multi-ministry tasks
- Manage debates and conflict resolution

**Key Classes**:

```python
@dataclass
class Request:
    content: str              # User's request text
    ministry: Optional[str]   # Override ministry routing
    specialist: Optional[str] # Override specialist selection
    context: dict             # Additional context

@dataclass
class Response:
    content: str              # The response text
    ministry: str             # Which ministry handled it
    specialist: Optional[str] # Which specialist processed it
    reasoning_trace: Optional[dict]  # The 7-step reasoning
    tool_calls: list[dict]    # Any tools that were called
```

**Routing Logic**:

```
User Request
     │
     ▼
┌─────────────┐   explicit ministry?   ┌──────────────┐
│ Check if    │────── Yes ─────────────│ Use that     │
│ ministry    │                        │ ministry     │
│ specified   │                        └──────────────┘
└──────┬──────┘
       │ No
       ▼
┌─────────────┐
│  Keyword    │
│  Matching   │
└──────┬──────┘
       │
       ▼
┌───────────────────────────────────────────────┐
│ "implement" "code" "function" → Code Ministry │
│ "search" "research" "analyze" → Research      │
│ "test" "security" "audit"     → Quality       │
│ "deploy" "file" "run"         → Operations    │
│ "remember" "recall" "decision"→ Archives      │
│ "schedule" "notify" "message" → Communications│
│ (default)                     → Code Ministry │
└───────────────────────────────────────────────┘
```

### 2. Genius Protocol

**Location**: `genius/protocol.py`

**Purpose**: Enforce structured reasoning for all specialists

**The 7 Steps**:

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1.OBSERVE│ → │ 2. THINK │ → │3.REFLECT │ → │4.CRITIQUE│
│          │   │          │   │          │   │          │
│ Understand   │ Reason     │ Check      │ Find       │
│ the request  │ through    │ assumption │ problems   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                 │
     ┌───────────────────────────────────────────┘
     │
     ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ 5.REFINE │ → │  6. ACT  │ → │ 7.VERIFY │
│          │   │          │   │          │
│ Improve    │ Execute    │ Confirm    │
│ approach   │ and output │ quality    │
└──────────┘   └──────────┘   └──────────┘
```

**Quality Threshold**:
- Rationale explained?
- Trade-offs identified?
- Evidence cited?

### 3. Ministry Servers

Each ministry is a standalone MCP server:

**Structure**:
```
ministry/
├── __init__.py           # Exports
├── minister.py           # MCP server
└── specialists/
    ├── __init__.py
    ├── specialist1.py
    └── specialist2.py
```

**Minister Pattern**:
```python
class SomeMinistry:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.genius = GeniusProtocol()
        self.server = Server("ministry-name")
        self._setup_handlers()

    def _setup_handlers(self):
        @self.server.list_resources()
        async def list_resources():
            # Return available resources
            pass

        @self.server.list_tools()
        async def list_tools():
            # Return available tools
            pass

        @self.server.call_tool()
        async def call_tool(name, arguments):
            # Execute tool
            pass
```

### 4. Shared Knowledge Server

**Location**: `shared/knowledge_server.py`

**Purpose**: Central repository for all shared state

**Resources Exposed**:
| URI | Content |
|-----|---------|
| `knowledge://constitution` | Core rules |
| `knowledge://decisions` | Decision history |
| `knowledge://projects` | Project state |
| `knowledge://domain` | Accumulated knowledge |
| `knowledge://tasks` | Task history |
| `knowledge://court-cases` | Precedents |

**Tools Provided**:
- `log_decision` - Record a decision
- `search_decisions` - Query past decisions
- `store_knowledge` - Save domain knowledge
- `search_knowledge` - Query knowledge base
- `record_court_case` - Log Evidence Court case

### 5. Ollama Bridge

**Location**: `bridge/ollama_bridge.py`

**Purpose**: Interface with local LLM via Ollama's HTTP API

---

## How Ollama Works in This Application

### What is Ollama?

Ollama is a local LLM inference server that:
1. Downloads and manages AI models on your machine
2. Loads models into GPU/CPU memory
3. Exposes a REST API for generating text
4. Handles all the complex ML inference internally

```
┌─────────────────────────────────────────────────────────────────────┐
│                         YOUR COMPUTER                               │
│                                                                     │
│  ┌─────────────────────┐          ┌─────────────────────────────┐  │
│  │   micro-country     │   HTTP   │         OLLAMA              │  │
│  │   (Python app)      │ ◄──────► │        SERVER               │  │
│  │                     │  :11434  │                             │  │
│  │  • Orchestrator     │          │  • Model Manager            │  │
│  │  • Ollama Bridge    │          │  • Inference Engine         │  │
│  │  • Genius Protocol  │          │  • GPU/CPU Scheduler        │  │
│  └─────────────────────┘          └──────────────┬──────────────┘  │
│                                                  │                  │
│                                   ┌──────────────▼──────────────┐  │
│                                   │      AI MODEL (e.g.         │  │
│                                   │       mistral:7b)           │  │
│                                   │                             │  │
│                                   │  Loaded in GPU VRAM         │  │
│                                   │  or System RAM              │  │
│                                   └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Communication Flow Overview

```
┌──────────────┐                ┌──────────────┐              ┌──────────────┐
│     USER     │                │ ORCHESTRATOR │              │    OLLAMA    │
│              │                │              │              │    SERVER    │
└──────┬───────┘                └──────┬───────┘              └──────┬───────┘
       │                               │                             │
       │  1. "Write hello world"       │                             │
       │──────────────────────────────►│                             │
       │                               │                             │
       │                               │  2. Build prompt with       │
       │                               │     Genius Protocol         │
       │                               │     + specialist context    │
       │                               │                             │
       │                               │  3. HTTP POST /api/generate │
       │                               │─────────────────────────────►
       │                               │     {                       │
       │                               │       "model": "mistral:7b",│
       │                               │       "prompt": "...",      │
       │                               │       "stream": false       │
       │                               │     }                       │
       │                               │                             │
       │                               │              4. Model loads │
       │                               │                 (if needed) │
       │                               │                             │
       │                               │              5. Generate    │
       │                               │                 tokens      │
       │                               │                             │
       │                               │  6. HTTP Response           │
       │                               │◄─────────────────────────────
       │                               │     {                       │
       │                               │       "response": "...",    │
       │                               │       "done": true          │
       │                               │     }                       │
       │                               │                             │
       │                               │  7. Parse response,         │
       │                               │     extract reasoning       │
       │                               │                             │
       │  8. Display result            │                             │
       │◄──────────────────────────────│                             │
       │                               │                             │
```

### The Ollama Bridge Class

```python
class OllamaBridge:
    """
    Async HTTP client for Ollama API.
    Handles all LLM communication for the application.
    """

    def __init__(self, config: OllamaConfig, genius: GeniusProtocol):
        self.config = config      # host, model, timeout
        self.genius = genius      # For building prompts
        self._client = None       # httpx.AsyncClient

    # Context manager for connection lifecycle
    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self

    async def __aexit__(self, ...):
        await self._client.aclose()
```

### API Endpoints Used

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OLLAMA REST API (localhost:11434)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  GET  /api/tags                                                     │
│       └─► List available models                                     │
│           Used by: check_connection(), list_models()                │
│                                                                     │
│  POST /api/generate                                                 │
│       └─► Generate text from prompt                                 │
│           Used by: generate(), debate(), adversarial_review()       │
│           Body: { "model": "...", "prompt": "...", "stream": false }│
│                                                                     │
│  POST /api/chat                                                     │
│       └─► Multi-turn conversation with tool support                 │
│           Used by: chat()                                           │
│           Body: { "model": "...", "messages": [...], "tools": [...]}│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Simple Generate Flow

```
                    generate(prompt, specialist="coder")
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                    PROMPT CONSTRUCTION                            │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ SYSTEM PROMPT (from genius/prompts/base_genius.txt)         │ │
│  │ "You are a genius specialist. Follow the 7-step protocol..."│ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              +                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ SPECIALIST PROMPT (from genius/prompts/coder.txt)           │ │
│  │ "You are the Coder genius. Your expertise includes..."      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              +                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ USER REQUEST                                                 │ │
│  │ "Write hello world in Python"                                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              +                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ REASONING TEMPLATE                                           │ │
│  │ "Structure your response with: 1.OBSERVE 2.THINK..."        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              =                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ FINAL PROMPT (sent to Ollama)                                │ │
│  │ ~500-1000 tokens                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                    HTTP REQUEST TO OLLAMA                         │
│                                                                   │
│  POST http://localhost:11434/api/generate                         │
│  Content-Type: application/json                                   │
│                                                                   │
│  {                                                                │
│    "model": "mistral:7b",                                         │
│    "prompt": "[full constructed prompt]",                         │
│    "stream": false,                                               │
│    "options": {                                                   │
│      "temperature": 0.7,                                          │
│      "num_ctx": 8192                                              │
│    }                                                              │
│  }                                                                │
└───────────────────────────────────────────────────────────────────┘
                                    │
                            (model processes)
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                    HTTP RESPONSE FROM OLLAMA                      │
│                                                                   │
│  {                                                                │
│    "model": "mistral:7b",                                         │
│    "response": "### 1. OBSERVE\nThe user wants...\n\n### 2...",  │
│    "done": true,                                                  │
│    "total_duration": 5234000000,                                  │
│    "eval_count": 250,                                             │
│    "eval_duration": 4500000000                                    │
│  }                                                                │
└───────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                         Return response text
```

### Debate Flow (Multiple Ollama Calls)

```
                    debate(topic, participants=["architect", "coder"])
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                    ROUND 1: INITIAL POSITIONS                     │
│                                                                   │
│   ┌─────────────────┐         ┌─────────────────┐                │
│   │ Call 1: architect│         │ Call 2: coder   │                │
│   │ "State position │         │ "State position │                │
│   │  on topic..."   │         │  on topic..."   │                │
│   └────────┬────────┘         └────────┬────────┘                │
│            │                           │                          │
│            ▼                           ▼                          │
│   ┌─────────────────┐         ┌─────────────────┐                │
│   │ POST /api/generate        │ POST /api/generate               │
│   │ specialist=architect      │ specialist=coder                 │
│   └────────┬────────┘         └────────┬────────┘                │
│            │                           │                          │
│            ▼                           ▼                          │
│   ┌─────────────────┐         ┌─────────────────┐                │
│   │ Position 1      │         │ Position 2      │                │
│   │ (with 7 steps)  │         │ (with 7 steps)  │                │
│   └────────┬────────┘         └────────┬────────┘                │
│            │                           │                          │
│            └───────────┬───────────────┘                          │
│                        ▼                                          │
│              Collect all positions                                │
└───────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────┐
│                    SYNTHESIS                                      │
│                                                                   │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │ Call 3: architect (as synthesizer)                       │    │
│   │ "Given these positions, synthesize key agreements,       │    │
│   │  disagreements, and recommendation..."                   │    │
│   └────────────────────────┬────────────────────────────────┘    │
│                            │                                      │
│                            ▼                                      │
│                  POST /api/generate                               │
│                            │                                      │
│                            ▼                                      │
│                  Synthesis response                               │
└───────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    Return { positions, synthesis }

Total Ollama calls: 3 (2 participants + 1 synthesis)
With 3 participants and 3 rounds: 3×3 + 1 = 10 calls
```

### Model Loading and Memory

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MODEL LIFECYCLE IN OLLAMA                        │
└─────────────────────────────────────────────────────────────────────┘

    First Request                    Subsequent Requests
    ─────────────                    ────────────────────
         │                                   │
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│ Model on disk   │                 │ Model in memory │
│ (~4GB file)     │                 │ (already loaded)│
└────────┬────────┘                 └────────┬────────┘
         │                                   │
         │ Load into                         │ Immediate
         │ GPU VRAM                          │
         │ (5-15 sec)                        │
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│ Generate tokens │                 │ Generate tokens │
│ (~15-30 tok/sec)│                 │ (~15-30 tok/sec)│
└────────┬────────┘                 └────────┬────────┘
         │                                   │
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│ Model stays in  │                 │ Model stays in  │
│ memory for      │                 │ memory          │
│ ~5 minutes      │                 │                 │
└─────────────────┘                 └─────────────────┘

Note: If model is larger than GPU VRAM, it runs on CPU
      which is 3-5x slower (~4-5 tokens/sec)
```

### Error Handling

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ERROR SCENARIOS                                  │
└─────────────────────────────────────────────────────────────────────┘

  Scenario                  Error                    Solution
  ────────────────────────────────────────────────────────────────────
  Ollama not running        ConnectionRefused        ollama serve
  Model not downloaded      Model not found          ollama pull model
  Request too long          ReadTimeout              Increase timeout
  GPU out of memory         CUDA OOM                 Use smaller model
  Invalid model name        Model not found          Check ollama list

┌─────────────────────────────────────────────────────────────────────┐
│                    TIMEOUT CONFIGURATION                            │
│                                                                     │
│  config.yaml:                                                       │
│    ollama:                                                          │
│      timeout: 300  # seconds                                        │
│                                                                     │
│  This affects httpx.AsyncClient timeout for all Ollama calls        │
│  Increase if seeing ReadTimeout errors on slow hardware             │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Methods Summary

```python
class OllamaBridge:
    async def check_connection(self) -> bool:
        """GET /api/tags - verify Ollama is running"""

    async def list_models(self) -> list[str]:
        """GET /api/tags - list available models"""

    async def generate(self, prompt, specialist=None) -> str:
        """POST /api/generate - single text generation"""

    async def generate_with_reasoning(self, prompt, specialist) -> tuple:
        """generate() + parse 7-step reasoning trace"""

    async def chat(self, messages, tools=None) -> dict:
        """POST /api/chat - multi-turn with tool support"""

    async def debate(self, topic, participants, max_rounds=1) -> dict:
        """Multiple generate() calls for debate workflow"""

    async def adversarial_review(self, output, context) -> dict:
        """Single generate() call for critical review"""
```

---

## Data Flow

### Simple Request Flow

```
1. User types: "Write a sorting function"
           │
           ▼
2. Orchestrator.route_request()
   - Matches "write" "function" → Code Ministry
           │
           ▼
3. Orchestrator.select_specialist()
   - Matches "write" → Coder
           │
           ▼
4. OllamaBridge.generate_with_reasoning()
   - Builds genius prompt for "coder"
   - Calls Ollama API
   - Parses response into ReasoningTrace
           │
           ▼
5. Response returned to user
   - Shows [code/coder]
   - Shows 7-step reasoning
   - Shows final code
```

### Debate Flow

```
1. User types: "/debate SQL vs NoSQL"
           │
           ▼
2. Orchestrator.coordinate_debate()
           │
           ▼
3. Round 1: Initial Positions
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │  Architect  │ │   Coder     │ │   Tester    │
   │  Position   │ │  Position   │ │  Position   │
   └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
4. Round 2: Critiques
   Each specialist critiques others
                           │
                           ▼
5. Round 3: Refinements
   Specialists refine based on critiques
                           │
                           ▼
6. Synthesis
   Architect synthesizes final recommendation
                           │
                           ▼
7. Return combined result
```

### Evidence Court Flow

```
1. Conflict Detected
   Architect: "Use microservices"
   Coder: "Use monolith"
           │
           ▼
2. Positions Formalized
   ┌────────────────────────┐  ┌────────────────────────┐
   │ Position: Microservices│  │ Position: Monolith     │
   │ Arguments:             │  │ Arguments:             │
   │ - Scalability          │  │ - Simplicity           │
   │ - Independence         │  │ - Faster development   │
   │ Evidence:              │  │ Evidence:              │
   │ - [EMPIRICAL] Netflix  │  │ - [THEORETICAL] KISS   │
   │   case study           │  │   principle            │
   └────────────────────────┘  └────────────────────────┘
           │                           │
           └─────────────┬─────────────┘
                         ▼
3. Evidence Evaluation
   ┌──────────────────────────────────────┐
   │         EVIDENCE COURT               │
   │                                      │
   │  Judge: Archives Ministry            │
   │                                      │
   │  Evidence Hierarchy:                 │
   │  EMPIRICAL > PRECEDENT > CONSENSUS > │
   │  THEORETICAL > INTUITION             │
   │                                      │
   │  Netflix case (EMPIRICAL) beats      │
   │  KISS principle (THEORETICAL)        │
   └──────────────────────────────────────┘
                         │
                         ▼
4. Ruling
   "Microservices wins based on empirical evidence"
                         │
                         ▼
5. Precedent Recorded
   Stored in decision_log for future reference
```

---

## The Genius Protocol

### Prompt Structure

```
┌─────────────────────────────────────────────────────────┐
│                    SYSTEM PROMPT                        │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         BASE GENIUS PROMPT                      │   │
│  │  - Core identity                                │   │
│  │  - 7-step protocol definition                   │   │
│  │  - Quality threshold rules                      │   │
│  │  - Evidence standards                           │   │
│  └─────────────────────────────────────────────────┘   │
│                         +                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │      SPECIALIST EXPERTISE PROMPT                │   │
│  │  - Domain-specific knowledge                    │   │
│  │  - Responsibilities                             │   │
│  │  - Example reasoning                            │   │
│  └─────────────────────────────────────────────────┘   │
│                         +                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           TASK CONTEXT                          │   │
│  │  - The user's actual request                    │   │
│  └─────────────────────────────────────────────────┘   │
│                         +                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │       REASONING TEMPLATE                        │   │
│  │  "You MUST structure your response with..."     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Quality Scoring

```python
def assess_quality(trace):
    score = 1.0
    issues = []

    # Completeness check (-0.1 per missing step)
    for step in STEPS:
        if not getattr(trace, step):
            score -= 0.1
            issues.append(f"Missing {step}")

    # Depth check (-0.05 for brief steps)
    for step in STEPS:
        if len(getattr(trace, step)) < 20:
            score -= 0.05
            issues.append(f"{step} too brief")

    # Quality markers in VERIFY (-0.05 each if missing)
    if "rationale" not in trace.verify.lower():
        score -= 0.05
    if "trade-off" not in trace.verify.lower():
        score -= 0.05
    if "evidence" not in trace.verify.lower():
        score -= 0.05

    return max(0.0, score), issues
```

---

## The Evidence Court

### Evidence Hierarchy

```
    Strength
       │
    1.0├── EMPIRICAL (Data, Tests, Benchmarks)
       │   "Load test shows 10k req/sec"
       │
    0.8├── PRECEDENT (What Worked Before)
       │   "Twitter uses this for scale"
       │
    0.6├── CONSENSUS (Experts Agree)
       │   "Industry standard approach"
       │
    0.4├── THEORETICAL (Logical Argument)
       │   "This should work because..."
       │
    0.2├── INTUITION (Gut Feeling)
       │   "I think this is right"
       │
    0.0┴───────────────────────────────────
```

### Strength Calculation

```python
def strength_score(evidence):
    # Type contributes 60%
    type_score = (6 - evidence.evidence_type) / 5
    # Confidence contributes 40%
    return (type_score * 0.6) + (evidence.confidence * 0.4)

# Example:
# EMPIRICAL (1) with 0.9 confidence:
# type_score = (6-1)/5 = 1.0
# strength = (1.0 * 0.6) + (0.9 * 0.4) = 0.96

# THEORETICAL (4) with 0.7 confidence:
# type_score = (6-4)/5 = 0.4
# strength = (0.4 * 0.6) + (0.7 * 0.4) = 0.52
```

---

## Database Design

### Entity-Relationship Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  constitution   │     │  decision_log   │     │ project_context │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id              │     │ id              │     │ id              │
│ article         │     │ decision_id     │     │ project_id      │
│ content         │     │ ministry        │     │ name            │
│ rationale       │     │ specialist      │     │ description     │
│ created_at      │     │ decision_type   │     │ status          │
│ updated_at      │     │ context (JSON)  │     │ goals (JSON)    │
└─────────────────┘     │ options (JSON)  │     │ tech_stack(JSON)│
                        │ decision        │     └────────┬────────┘
                        │ rationale       │              │
                        │ evidence (JSON) │              │
                        └────────┬────────┘              │
                                 │                       │
                                 │ references            │
                                 ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│domain_knowledge │     │  task_history   │     │evidence_court_  │
├─────────────────┤     ├─────────────────┤     │    cases        │
│ id              │     │ id              │     ├─────────────────┤
│ knowledge_id    │     │ task_id         │     │ id              │
│ domain          │     │ project_id ─────┼─────│ case_id         │
│ topic           │     │ ministry        │     │ topic           │
│ content         │     │ specialist      │     │ advocates(JSON) │
│ source          │     │ task_type       │     │ evidence (JSON) │
│ confidence      │     │ description     │     │ ruling          │
│ tags (JSON)     │     │ status          │     │ rationale       │
└─────────────────┘     │ success         │     │ precedent_set   │
                        │ lessons_learned │     └─────────────────┘
                        └─────────────────┘
```

### Table Purposes

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `constitution` | Core rules | article, content |
| `decision_log` | Historical decisions | ministry, decision, rationale |
| `project_context` | Project state | name, status, tech_stack |
| `domain_knowledge` | Learned knowledge | domain, topic, content |
| `task_history` | Task tracking | ministry, status, success |
| `evidence_court_cases` | Conflict records | ruling, precedent_set |
| `genius_reasoning_traces` | Reasoning audit | 7 step fields |
| `cross_ministry_requests` | Ministry comms | from/to ministry |

---

## Design Decisions

### Why Local-Only?

**Decision**: All processing happens locally
**Rationale**: Privacy, no API costs, works offline
**Trade-off**: Requires capable hardware

### Why Single Model?

**Decision**: One model for all specialists
**Rationale**: Simplicity, consistent behavior
**Trade-off**: Can't optimize per specialist

### Why MCP Protocol for Ministries?

**Decision**: Implement each ministry as an MCP (Model Context Protocol) server

**What is MCP?**

MCP is a standard protocol (developed by Anthropic) for communication between AI applications and external tools/resources. It uses JSON-RPC 2.0 over STDIO.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE PATTERN                         │
│                                                                     │
│   ┌─────────────────┐         JSON-RPC 2.0        ┌──────────────┐ │
│   │   MCP HOST      │◄────────────────────────────►│  MCP SERVER  │ │
│   │  (Orchestrator) │           STDIO             │  (Ministry)  │ │
│   │                 │                             │              │ │
│   │ • Sends requests│                             │ • Exposes    │ │
│   │ • Calls tools   │                             │   tools      │ │
│   │ • Reads resources                             │ • Provides   │ │
│   │                 │                             │   resources  │ │
│   └─────────────────┘                             └──────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Why Not Just Use Direct Function Calls?**

Alternative approaches we could have used:

```
OPTION A: Direct Function Calls (What we could have done)
─────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────┐
│                         orchestrator.py                              │
│                                                                     │
│  from ministries.code import architect, coder, debugger             │
│  from ministries.research import analyst, writer                    │
│                                                                     │
│  result = architect.design(request)  # Direct call                  │
│  result = coder.implement(spec)      # Direct call                  │
└─────────────────────────────────────────────────────────────────────┘

  Pros: Simple, fast, easy to debug
  Cons: Tightly coupled, hard to extend, no standard interface


OPTION B: MCP Servers (What we chose)
─────────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────┐
│     Orchestrator          Code Ministry           Research Ministry │
│    (MCP Host)             (MCP Server)            (MCP Server)      │
│         │                      │                       │            │
│         │  list_tools()        │                       │            │
│         │─────────────────────►│                       │            │
│         │  [architect_design,  │                       │            │
│         │   coder_implement]   │                       │            │
│         │◄─────────────────────│                       │            │
│         │                      │                       │            │
│         │  call_tool(          │                       │            │
│         │    "architect_design"│                       │            │
│         │    {spec: "..."})    │                       │            │
│         │─────────────────────►│                       │            │
│         │  {result: "..."}     │                       │            │
│         │◄─────────────────────│                       │            │
└─────────────────────────────────────────────────────────────────────┘

  Pros: Decoupled, standard interface, extensible, future-proof
  Cons: More complex, slight overhead
```

**Benefits of MCP for This Application**

1. **Modularity and Isolation**
```
┌─────────────────────────────────────────────────────────────────────┐
│  Each ministry is a separate process with its own:                  │
│  • Memory space (no leaks between ministries)                       │
│  • Error handling (one crash doesn't kill others)                   │
│  • Dependencies (can use different libraries)                       │
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │   Code   │   │ Research │   │ Quality  │   │   Ops    │        │
│  │ Ministry │   │ Ministry │   │ Ministry │   │ Ministry │        │
│  │          │   │          │   │          │   │          │        │
│  │ Process 1│   │ Process 2│   │ Process 3│   │ Process 4│        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│       │              │              │              │               │
│       └──────────────┴──────────────┴──────────────┘               │
│                              │                                      │
│                    ┌─────────▼─────────┐                           │
│                    │   Orchestrator    │                           │
│                    │   (MCP Host)      │                           │
│                    └───────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
```

2. **Standard Tool/Resource Interface**
```
Every MCP server exposes the same interface:

┌─────────────────────────────────────────────────────────────────────┐
│                    MCP SERVER INTERFACE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  TOOLS (actions the server can perform)                             │
│  ──────────────────────────────────────                             │
│  list_tools() → [                                                   │
│    { name: "architect_design",                                      │
│      description: "Design system architecture",                     │
│      inputSchema: { type: "object", properties: {...} }             │
│    },                                                               │
│    { name: "coder_implement", ... },                                │
│    { name: "debugger_fix", ... }                                    │
│  ]                                                                  │
│                                                                     │
│  call_tool(name, arguments) → result                                │
│                                                                     │
│  RESOURCES (data the server provides)                               │
│  ─────────────────────────────────────                              │
│  list_resources() → [                                               │
│    { uri: "ministry://code/specialists", ... },                     │
│    { uri: "ministry://code/recent-tasks", ... }                     │
│  ]                                                                  │
│                                                                     │
│  read_resource(uri) → content                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

3. **Future Extensibility**
```
Adding a new ministry is plug-and-play:

BEFORE:                              AFTER:
─────────────────────────────────────────────────────────────────────
┌──────────┐  ┌──────────┐          ┌──────────┐  ┌──────────┐
│   Code   │  │ Research │          │   Code   │  │ Research │
└────┬─────┘  └────┬─────┘          └────┬─────┘  └────┬─────┘
     └──────┬──────┘                     │             │
            │                            │  ┌──────────┴──────────┐
     ┌──────▼──────┐                     │  │                     │
     │ Orchestrator│               ┌─────▼──▼──┐  ┌──────────────┐
     └─────────────┘               │Orchestrator│  │  NEW: Legal  │
                                   └────────────┘  │   Ministry   │
                                         ▲         └──────────────┘
                                         │                │
                                         └────────────────┘

No code changes to orchestrator needed - just:
1. Create ministries/legal/minister.py
2. Add to config.yaml
3. Restart
```

4. **Alignment with AI Ecosystem**
```
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP ECOSYSTEM COMPATIBILITY                      │
│                                                                     │
│  MCP is supported by:                                               │
│  • Claude Desktop                                                   │
│  • Claude Code (this tool!)                                         │
│  • Other AI assistants adopting the standard                        │
│                                                                     │
│  This means ministries could potentially be:                        │
│  • Used by other MCP-compatible AI systems                          │
│  • Extended with third-party MCP servers                            │
│  • Integrated into larger AI workflows                              │
└─────────────────────────────────────────────────────────────────────┘
```

**Current Implementation Status**

```
┌─────────────────────────────────────────────────────────────────────┐
│  NOTE: In the current implementation, ministries are defined as     │
│  MCP servers but the orchestrator uses a simplified direct          │
│  approach for the initial version:                                  │
│                                                                     │
│  CURRENT:                                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Orchestrator                                                 │   │
│  │   │                                                          │   │
│  │   ├─► Ollama Bridge (for LLM calls)                          │   │
│  │   │     └─► Uses specialist prompts from genius/prompts/     │   │
│  │   │                                                          │   │
│  │   └─► Ministry definitions (for routing/display)             │   │
│  │         └─► config.yaml lists ministries and specialists     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  FUTURE (full MCP implementation):                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Orchestrator (MCP Host)                                      │   │
│  │   │                                                          │   │
│  │   ├─► Code Ministry (MCP Server process)                     │   │
│  │   │     ├─► architect tool                                   │   │
│  │   │     ├─► coder tool                                       │   │
│  │   │     └─► debugger tool                                    │   │
│  │   │                                                          │   │
│  │   ├─► Research Ministry (MCP Server process)                 │   │
│  │   │     └─► ...                                              │   │
│  │   │                                                          │   │
│  │   └─► Knowledge Server (MCP Server process)                  │   │
│  │         └─► Shared database access                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  The MCP server code exists in ministries/*/minister.py but        │
│  full inter-process communication is planned for future versions.  │
└─────────────────────────────────────────────────────────────────────┘
```

**Trade-offs Acknowledged**

| Benefit | Trade-off |
|---------|-----------|
| Modularity | More complex than direct calls |
| Standard interface | Learning curve for contributors |
| Process isolation | IPC overhead |
| Future extensibility | Over-engineering for simple use cases |
| Ecosystem alignment | Dependency on MCP SDK |

**Summary**: MCP was chosen to create a clean, extensible architecture that aligns with the emerging AI tool ecosystem, even though a simpler direct-call approach would work for the current scope. This is a deliberate investment in future flexibility.

### Why SQLite?

**Decision**: SQLite for all storage
**Rationale**: Zero config, portable, sufficient for local use
**Trade-off**: No concurrent write scaling

### Why 7-Step Protocol?

**Decision**: Enforce structured reasoning
**Rationale**: Better quality, transparent thinking, self-correction
**Trade-off**: Longer responses, more tokens

### Why Evidence Hierarchy?

**Decision**: Rank evidence types
**Rationale**: Objective conflict resolution, better decisions
**Trade-off**: May override valid intuition

---

## Extension Points

### Adding a New Ministry

1. Create directory `ministries/new_ministry/`
2. Implement `minister.py` with MCP server
3. Add specialists to `specialists/`
4. Create prompts in `genius/prompts/`
5. Register in `config.yaml`
6. Add routing rules in `orchestrator.py`

### Adding New Evidence Types

1. Add to `EvidenceType` enum
2. Update evidence hierarchy
3. Update strength calculation
4. Document in Architecture guide

### Custom Reasoning Protocol

1. Subclass `GeniusProtocol`
2. Override `STEPS` and `STEP_PROMPTS`
3. Update `parse_reasoning_trace()`
4. Update `assess_quality()`

---

## Performance Considerations

### Bottlenecks

1. **LLM Inference**: ~5-30 seconds per request
2. **Database I/O**: Minimal (<10ms)
3. **Prompt Building**: Minimal (<1ms)

### Optimizations Applied

- Async I/O throughout
- Connection pooling for database
- Prompt caching in `GeniusProtocol`
- Lazy loading of prompts

### Future Optimizations

- Streaming responses
- Model caching
- Parallel specialist execution
- Response caching for similar queries
