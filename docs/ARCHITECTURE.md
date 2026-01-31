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

**Purpose**: Interface with local LLM

**Key Methods**:

```python
class OllamaBridge:
    async def generate(self, prompt, specialist=None):
        """Generate text response."""
        pass

    async def generate_with_reasoning(self, prompt, specialist):
        """Generate with parsed reasoning trace."""
        pass

    async def chat(self, messages, tools=None):
        """Multi-turn conversation with tool support."""
        pass

    async def debate(self, topic, participants):
        """Run a debate between specialists."""
        pass

    async def adversarial_review(self, output, context):
        """Get critical review of output."""
        pass
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

### Why MCP Protocol?

**Decision**: Use Model Context Protocol
**Rationale**: Standard protocol, future-proof, tool support
**Trade-off**: More complex than direct API calls

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
