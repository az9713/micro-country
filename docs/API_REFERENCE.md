# API Reference

Complete reference for all tools, resources, and interfaces in the Micro-Country system.

## Table of Contents

1. [Ministry of Code](#ministry-of-code)
2. [Ministry of Research](#ministry-of-research)
3. [Ministry of Quality](#ministry-of-quality)
4. [Ministry of Operations](#ministry-of-operations)
5. [Ministry of Archives](#ministry-of-archives)
6. [Ministry of Communications](#ministry-of-communications)
7. [Shared Knowledge Server](#shared-knowledge-server)
8. [Core Classes](#core-classes)

---

## Ministry of Code

**Server Name**: `code-ministry`

### Resources

#### `code://codebase-map`
Structure and organization of the codebase.

**Returns**: JSON object with directory structure

#### `code://tech-stack`
Technologies, frameworks, and tools in use.

**Returns**: JSON object with technology information

#### `code://architecture`
System architecture and design decisions.

**Returns**: JSON object with architecture decisions

#### `code://conventions`
Project coding standards and conventions.

**Returns**: JSON object with coding conventions

### Tools

#### `design_architecture`
Design system architecture for a feature or component.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `feature` | string | Yes | What feature/system to design |
| `requirements` | string[] | Yes | Functional requirements |
| `constraints` | string[] | No | Non-functional requirements |
| `context` | string | No | Additional context |

**Returns**:
```json
{
  "feature": "authentication",
  "design": {
    "overview": "...",
    "components": [...],
    "trade_offs": [...]
  },
  "task_id": "task_abc123"
}
```

#### `implement_feature`
Write code to implement a feature.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `feature` | string | Yes | What to implement |
| `design` | string | No | Design to follow |
| `language` | string | No | Programming language |
| `file_path` | string | No | Where to create file |
| `existing_code` | string | No | Code to integrate with |

#### `refactor_code`
Improve existing code without changing behavior.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | string | Yes | Code to refactor |
| `goals` | string[] | No | Refactoring goals |
| `constraints` | string[] | No | Things to preserve |

#### `explain_code`
Explain what code does.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | string | Yes | Code to explain |
| `level` | string | No | "beginner", "intermediate", "expert" |

#### `debug_issue`
Investigate and diagnose a bug.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `description` | string | Yes | Issue description |
| `error_message` | string | No | Error message |
| `code` | string | No | Relevant code |
| `expected_behavior` | string | No | What should happen |
| `actual_behavior` | string | No | What happens |
| `reproduction_steps` | string[] | No | Steps to reproduce |

#### `fix_bug`
Propose a fix for an identified bug.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | string | Yes | Buggy code |
| `bug_description` | string | Yes | What the bug is |
| `root_cause` | string | No | Identified cause |

---

## Ministry of Research

**Server Name**: `research-ministry`

### Resources

#### `research://cache`
Cached research results.

#### `research://sources`
Index of information sources.

#### `research://findings`
Synthesized research findings.

### Tools

#### `search_web`
Search for information on a topic.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | Search query |
| `sources` | string[] | No | Preferred sources |
| `recency` | string | No | "any", "recent", "last_year" |

#### `search_codebase`
Search codebase for patterns.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pattern` | string | Yes | What to search for |
| `file_types` | string[] | No | File extensions |
| `path` | string | No | Path to search |

#### `analyze_document`
Analyze a document and extract information.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `content` | string | Yes | Document content |
| `focus` | string | No | What to focus on |
| `questions` | string[] | No | Questions to answer |

#### `compare_options`
Compare multiple options or solutions.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `options` | object[] | Yes | Options with name/description |
| `criteria` | string[] | Yes | Comparison criteria |
| `context` | string | No | Context for comparison |

#### `synthesize_findings`
Combine findings from multiple sources.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `findings` | object[] | Yes | Findings with source/content |
| `question` | string | No | Question to answer |

#### `write_documentation`
Write documentation.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subject` | string | Yes | What to document |
| `doc_type` | string | Yes | "api", "tutorial", "reference", "guide", "adr" |
| `audience` | string | No | Target audience |
| `content_source` | string | No | Source content |

#### `explain_concept`
Explain a concept at specified level.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `concept` | string | Yes | Concept to explain |
| `level` | string | No | "beginner", "intermediate", "expert" |
| `context` | string | No | Context for explanation |

---

## Ministry of Quality

**Server Name**: `quality-ministry`

### Resources

#### `quality://test-results`
Latest test execution results.

#### `quality://coverage`
Code coverage data.

#### `quality://security-findings`
Security audit findings.

#### `quality://quality-gates`
Quality gate definitions and status.

### Tools

#### `design_test_cases`
Design test cases for a feature.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `feature` | string | Yes | What to test |
| `code` | string | No | Code to test |
| `requirements` | string[] | No | Requirements to verify |
| `test_type` | string | No | "unit", "integration", "e2e" |

#### `run_tests`
Execute tests and report results.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `test_path` | string | Yes | Path to tests |
| `test_framework` | string | No | pytest, jest, etc. |
| `coverage` | boolean | No | Collect coverage |

#### `security_audit`
Perform security audit on code.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | string | Yes | Code to audit |
| `context` | string | No | What the code does |
| `focus_areas` | string[] | No | Areas to focus on |

#### `review_code`
Code quality and security review.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | string | Yes | Code to review |
| `review_type` | string | No | "security", "quality", "both" |
| `context` | string | No | Context about code |

#### `validate_requirements`
Validate implementation meets requirements.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `requirements` | string[] | Yes | Requirements to validate |
| `implementation` | string | Yes | Implementation to check |
| `evidence` | string[] | No | Evidence of compliance |

#### `check_quality_gates`
Check if quality gates pass.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `test_results` | object | No | Test execution results |
| `coverage` | number | No | Coverage percentage |
| `security_findings` | object[] | No | Security issues |
| `review_approved` | boolean | No | Review status |

---

## Ministry of Operations

**Server Name**: `operations-ministry`

### Resources

#### `ops://system-state`
Current system status and health.

#### `ops://command-history`
History of executed commands.

#### `ops://deployments`
Status of deployments.

### Tools

#### `read_file`
Read contents of a file.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Path to file |
| `encoding` | string | No | File encoding |

#### `write_file`
Write content to a file.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Path to file |
| `content` | string | Yes | Content to write |
| `mode` | string | No | "write" or "append" |

#### `list_directory`
List directory contents.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Directory path |
| `pattern` | string | No | Glob pattern |
| `recursive` | boolean | No | Include subdirectories |

#### `manage_files`
File operations (copy, move, delete).

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | string | Yes | "copy", "move", "delete", "mkdir" |
| `source` | string | Yes | Source path |
| `destination` | string | No | Destination (for copy/move) |

#### `run_command`
Execute a shell command.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `command` | string | Yes | Command to execute |
| `working_dir` | string | No | Working directory |
| `timeout` | integer | No | Timeout in seconds |
| `env` | object | No | Environment variables |

#### `deploy`
Deploy a service.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `service` | string | Yes | Service to deploy |
| `environment` | string | Yes | "development", "staging", "production" |
| `version` | string | No | Version to deploy |
| `strategy` | string | No | "rolling", "blue-green", "canary" |

#### `rollback`
Rollback a deployment.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `service` | string | Yes | Service to rollback |
| `environment` | string | Yes | Environment |
| `version` | string | No | Version to rollback to |

---

## Ministry of Archives

**Server Name**: `archives-ministry`

### Resources

#### `archives://decision-log`
Historical decisions with rationale.

#### `archives://project-history`
Project evolution and milestones.

#### `archives://knowledge-base`
Accumulated domain knowledge.

#### `archives://court-precedents`
Evidence Court rulings.

### Tools

#### `store_decision`
Store a decision with context and rationale.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ministry` | string | Yes | Which ministry decided |
| `decision_type` | string | Yes | Type of decision |
| `context` | object | Yes | What led to decision |
| `decision` | string | Yes | The decision |
| `rationale` | string | Yes | Why this decision |
| `alternatives_considered` | string[] | No | Other options |
| `evidence` | object[] | No | Supporting evidence |

#### `recall_context`
Recall relevant historical context.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topic` | string | Yes | Topic to recall |
| `include_decisions` | boolean | No | Include decisions |
| `include_knowledge` | boolean | No | Include knowledge |
| `include_precedents` | boolean | No | Include court cases |

#### `store_lesson`
Store a lesson learned.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `domain` | string | Yes | Knowledge domain |
| `topic` | string | Yes | Specific topic |
| `lesson` | string | Yes | What was learned |
| `context` | string | No | Where learned |
| `confidence` | number | No | 0.0-1.0 |

#### `adjudicate_conflict`
Evidence Court adjudication.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topic` | string | Yes | Conflict topic |
| `positions` | object[] | Yes | Positions with evidence |

**Position format**:
```json
{
  "advocate": "architect",
  "position": "Use microservices",
  "arguments": ["Scalability", "Independence"],
  "evidence": [
    {
      "type": "EMPIRICAL",
      "description": "Netflix case study",
      "source": "engineering blog",
      "confidence": 0.9
    }
  ]
}
```

---

## Ministry of Communications

**Server Name**: `communications-ministry`

### Resources

#### `comms://inbox`
Pending messages and notifications.

#### `comms://calendar`
Scheduled tasks and deadlines.

#### `comms://notifications`
System notifications.

### Tools

#### `send_message`
Send a message to ministry/specialist.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `to` | string | Yes | Recipient |
| `subject` | string | Yes | Subject |
| `body` | string | Yes | Message body |
| `priority` | string | No | "critical", "high", "normal", "low" |
| `action_required` | boolean | No | Needs action? |

#### `broadcast`
Broadcast to all ministries.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subject` | string | Yes | Subject |
| `body` | string | Yes | Content |
| `priority` | string | No | Priority level |

#### `notify_user`
Send user notification.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Yes | Title |
| `message` | string | Yes | Message |
| `type` | string | No | "info", "warning", "error", "success" |

#### `schedule_task`
Schedule a future task.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task` | string | Yes | Task description |
| `ministry` | string | Yes | Ministry to handle |
| `due_date` | string | No | ISO date string |
| `priority` | string | No | Priority level |
| `dependencies` | string[] | No | Dependent tasks |

---

## Shared Knowledge Server

**Server Name**: `knowledge-server`

### Resources

All resources from all ministries are accessible here.

### Tools

Same tools as Archives Ministry, plus:

#### `create_project`
Create a new project.

#### `get_project`
Get project by ID.

#### `update_project`
Update project.

#### `create_task`
Create a task.

#### `update_task`
Update a task.

---

## Core Classes

### GeniusProtocol

```python
class GeniusProtocol:
    STEPS = ["observe", "think", "reflect", "critique", "refine", "act", "verify"]

    def build_genius_prompt(specialist, task_context, include_reasoning_template=True) -> str
    def parse_reasoning_trace(response, specialist, task_id=None) -> ReasoningTrace
    def assess_quality(trace) -> tuple[float, list[str]]
    def meets_quality_threshold(trace, threshold=0.7) -> bool
```

### ReasoningTrace

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
    quality_score: float
    quality_issues: list[str]

    def is_complete() -> bool
    def to_dict() -> dict
```

### EvidenceCourt

```python
class EvidenceCourt:
    def create_case_prompt(topic, positions) -> str
    def evaluate_positions(positions) -> dict
    def determine_winner(positions) -> tuple[Position, list[Position]]
    def parse_ruling_response(response, topic, positions) -> CourtRuling
```

### Evidence

```python
@dataclass
class Evidence:
    evidence_type: EvidenceType  # EMPIRICAL, PRECEDENT, CONSENSUS, THEORETICAL, INTUITION
    description: str
    source: str
    data: Optional[dict]
    confidence: float  # 0.0-1.0

    def strength_score() -> float
```

### OllamaBridge

```python
class OllamaBridge:
    async def check_connection() -> bool
    async def list_models() -> list[str]
    async def generate(prompt, specialist=None, ...) -> str
    async def generate_with_reasoning(prompt, specialist, task_id=None) -> tuple[str, ReasoningTrace]
    async def chat(messages, tools=None, specialist=None) -> tuple[str, list[dict]]
    async def debate(topic, participants, max_rounds=3) -> dict
    async def adversarial_review(output, output_type, context, reviewer="auditor") -> dict
```

### Database

```python
class Database:
    async def initialize() -> None
    async def get_constitution() -> list[dict]
    async def log_decision(...) -> str
    async def get_decisions(...) -> list[dict]
    async def create_project(...) -> str
    async def get_project(project_id) -> Optional[dict]
    async def store_knowledge(...) -> str
    async def search_knowledge(...) -> list[dict]
    async def create_task(...) -> str
    async def update_task(...) -> bool
    async def record_court_case(...) -> str
    async def get_court_precedents(...) -> list[dict]
```
