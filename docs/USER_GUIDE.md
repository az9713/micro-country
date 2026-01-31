# User Guide

Complete guide to using the Micro-Country of Geniuses system.

## Table of Contents

1. [Understanding the System](#understanding-the-system)
2. [Basic Usage](#basic-usage)
3. [The Six Ministries](#the-six-ministries)
4. [Advanced Features](#advanced-features)
5. [Best Practices](#best-practices)
6. [FAQ](#faq)

---

## Understanding the System

### What Is the Micro-Country?

Think of the Micro-Country as a team of AI experts organized like a small government.

> **100% Local Operation**: This system runs entirely on your machine using Ollama for local AI inference. No internet required, no API costs, and your data never leaves your computer.

- **Ministries** are departments with specific responsibilities
- **Specialists** are experts within each ministry
- **The Orchestrator** is the coordinator who routes your requests
- **The Knowledge Server** is the shared memory

### How Requests Work

When you type something:

```
You: "Write a function to sort a list"
         ↓
    Orchestrator analyzes your request
         ↓
    Routes to Code Ministry (sees "write", "function")
         ↓
    Coder Specialist processes it
         ↓
    Uses 7-step Genius Protocol
         ↓
You: Receive structured response
```

### The Genius Protocol

Every specialist thinks in 7 steps:

| Step | What Happens | Why It Matters |
|------|--------------|----------------|
| 1. OBSERVE | Read and understand your request | Prevents misunderstanding |
| 2. THINK | Reason through options | Considers alternatives |
| 3. REFLECT | Check understanding | Catches wrong assumptions |
| 4. CRITIQUE | Find potential problems | Identifies risks |
| 5. REFINE | Improve the approach | Better solutions |
| 6. ACT | Provide the answer | Delivers value |
| 7. VERIFY | Confirm quality | Ensures correctness |

---

## Basic Usage

### Starting the System

1. **Start Ollama** (in one terminal):
   ```bash
   ollama serve
   ```

2. **Start the Orchestrator** (in another terminal):
   ```bash
   cd micro-country
   python orchestrator.py
   ```

3. **Wait for the welcome message**:
   ```
   ============================================================
   Welcome to the Micro-Country of Geniuses
   ============================================================

   Commands:
     /debate <topic>  - Start a debate on a topic
     /review <text>   - Adversarial review of text
     /ministry <name> - Direct request to ministry
     /quit            - Exit
   >
   ```

### Making Requests

Simply type what you need:

```
> Write a Python class for managing a shopping cart
```

The system automatically:
1. Figures out which ministry should handle it
2. Picks the right specialist
3. Returns a structured response

### Using Commands

#### /debate - Start a Discussion

```
> /debate Should we use microservices or a monolith?
```

Multiple specialists discuss and reach a consensus.

#### /review - Get Critical Feedback

```
> /review My API returns all user data including passwords in the response
```

The Auditor becomes a skeptic and finds problems.

#### /ministry - Direct to Specific Ministry

```
> /ministry quality Run security audit on login code
```

Bypasses auto-routing and goes directly to that ministry.

#### /quit - Exit

```
> /quit
```

Cleanly exits the system.

### Understanding Responses

Responses are structured with the 7 steps:

```
[code/architect]    ← Ministry and specialist

### 1. OBSERVE
[What the specialist understood from your request]

### 2. THINK
[Reasoning process and options considered]

### 3. REFLECT
[Self-check on understanding]

### 4. CRITIQUE
[Potential problems identified]

### 5. REFINE
[Improved approach]

### 6. ACT
[The actual answer/code/design]

### 7. VERIFY
[Quality confirmation]
- Rationale explained: Yes
- Trade-offs identified: Yes
- Evidence cited: Yes
```

---

## The Six Ministries

### Ministry of Code

**Purpose**: Software development tasks

**Specialists**:
| Specialist | Best For | Example Request |
|------------|----------|-----------------|
| Architect | System design | "Design architecture for a chat app" |
| Coder | Writing code | "Write a function to parse JSON" |
| Debugger | Finding bugs | "Debug why this loop never exits" |

**Sample Requests**:
```
> Design a REST API for user management
> Write a sorting algorithm in Python
> Debug this code: for i in range(10): if i = 5: break
> Refactor this function to be more readable
> Explain what this code does: lambda x: x**2
```

### Ministry of Research

**Purpose**: Information gathering and analysis

**Specialists**:
| Specialist | Best For | Example Request |
|------------|----------|-----------------|
| Analyst | Data analysis | "Analyze these error patterns" |
| Writer | Documentation | "Write API docs for this endpoint" |
| Searcher | Finding info | "Search for JWT best practices" |

**Sample Requests**:
```
> Search for best practices in API authentication
> Write documentation for my database schema
> Analyze the pros and cons of GraphQL vs REST
> Explain OAuth 2.0 to a beginner
> Compare React and Vue for a dashboard project
```

### Ministry of Quality

**Purpose**: Testing and security

**Specialists**:
| Specialist | Best For | Example Request |
|------------|----------|-----------------|
| Tester | Writing tests | "Write unit tests for this class" |
| Auditor | Security review | "Audit this authentication code" |
| Validator | Verification | "Validate this meets requirements" |

**Sample Requests**:
```
> Write unit tests for a calculator class
> Security audit this login function
> Review this code for quality issues
> Validate that this implementation handles all edge cases
> Design test cases for a file upload feature
```

### Ministry of Operations

**Purpose**: System management

**Specialists**:
| Specialist | Best For | Example Request |
|------------|----------|-----------------|
| File Manager | File operations | "Create a directory structure" |
| Shell Runner | Commands | "Run the test suite" |
| Deployer | Deployment | "Deploy to staging" |

**Sample Requests**:
```
> List files in the project directory
> Create a backup of the config folder
> Check if the database process is running
> Deploy the application to staging
> Show system resource usage
```

### Ministry of Archives

**Purpose**: Knowledge management

**Specialists**:
| Specialist | Best For | Example Request |
|------------|----------|-----------------|
| Memory | Storing/recalling | "Remember this decision" |
| Indexer | Organizing | "Index this knowledge" |

**Sample Requests**:
```
> Remember: We chose PostgreSQL for ACID compliance
> Recall decisions about the database
> Store this lesson: Always validate user input
> Search our knowledge base for authentication
> What did we decide about error handling?
```

### Ministry of Communications

**Purpose**: Messaging and scheduling

**Specialists**:
| Specialist | Best For | Example Request |
|------------|----------|-----------------|
| Messenger | Sending messages | "Notify the team" |
| Scheduler | Scheduling | "Schedule a code review" |

**Sample Requests**:
```
> Schedule a reminder to review the PR tomorrow
> Notify the quality ministry about new code
> Create a task for security audit
> Show my scheduled tasks
> Set a deadline for the feature completion
```

---

## Advanced Features

### The Evidence Court

When specialists disagree, the Evidence Court resolves disputes.

**Evidence Hierarchy** (strongest to weakest):
1. **Empirical** - Data, benchmarks, test results
2. **Precedent** - What worked before
3. **Consensus** - Multiple experts agree
4. **Theoretical** - Logical arguments
5. **Intuition** - Gut feelings

**How It Works**:
1. Specialists present positions with evidence
2. Archives Ministry (as judge) evaluates
3. Strongest evidence wins
4. Decision is recorded as precedent

### Debates

Start a debate to explore decisions:

```
> /debate What's the best approach for handling authentication tokens?
```

**Debate Flow**:
1. **Round 1**: Each participant states their position
2. **Round 2**: Participants critique each other
3. **Round 3**: Refinement based on critiques
4. **Synthesis**: Best ideas combined

### Adversarial Review

Get critical feedback:

```
> /review My new API design stores user preferences in localStorage
```

The Auditor:
- Finds flaws ruthlessly
- Challenges assumptions
- Identifies risks
- Suggests improvements

**Verdicts**:
- **ACCEPT** - Good to go
- **NEEDS_REVISION** - Fix issues first
- **REJECT** - Major problems

### Cross-Ministry Collaboration

Complex requests use multiple ministries:

```
> Create a user registration system with proper security
```

This involves:
1. **Architect** designs the system
2. **Coder** implements it
3. **Auditor** reviews security
4. **Tester** creates test cases
5. **Memory** stores the decisions

### Remembering and Recalling

Store important decisions:
```
> Remember: We use bcrypt for password hashing because it's slow and resistant to brute force
```

Recall later:
```
> Recall what we decided about password hashing
```

---

## Best Practices

### Writing Good Requests

**Be Specific**:
```
Bad:  "Fix the bug"
Good: "Fix the bug where users can't log in after password reset"
```

**Provide Context**:
```
Bad:  "Write a function"
Good: "Write a Python function that validates email addresses using regex"
```

**Mention Constraints**:
```
Bad:  "Design a database"
Good: "Design a PostgreSQL database for a blog with posts, comments, and users"
```

### Getting Better Results

1. **Start simple**, then add complexity
2. **Use the right ministry** for the task
3. **Request debates** for important decisions
4. **Use adversarial review** before committing to designs
5. **Store decisions** for future reference

### When to Use Each Feature

| Situation | What to Use |
|-----------|-------------|
| Need code written | Direct request to Code ministry |
| Choosing between options | /debate |
| Reviewing designs | /review |
| Important decisions | Store in Archives |
| Complex tasks | Let orchestrator route |

---

## FAQ

### General Questions

**Q: Do I need internet access?**
A: No, everything runs locally on your computer.

**Q: Is my data private?**
A: Yes, nothing is sent to external servers. All processing happens locally.

**Q: Can I use a different AI model?**
A: Yes, edit `config.yaml` to change the model name. Any model Ollama supports will work.

**Q: Why are responses slow?**
A: The AI model needs time to think through the 7-step protocol. Smaller models are faster but less capable.

### Technical Questions

**Q: How do I change the model?**
A: Edit `config.yaml`:
```yaml
ollama:
  model: "different-model:tag"
```

**Q: Where is data stored?**
A: In `data/country.db`, a SQLite database.

**Q: Can I see what's stored?**
A: Yes, use any SQLite viewer on `data/country.db`.

**Q: How do I reset everything?**
A: Delete `data/country.db`. It will be recreated on next run.

### Troubleshooting Questions

**Q: The system won't start**
A: Check that Ollama is running (`ollama serve`).

**Q: Responses seem wrong**
A: Try being more specific in your request. Include context and constraints.

**Q: I get "Model not found"**
A: Download the model: `ollama pull mistral:7b`

**Q: How do I stop a long-running request?**
A: Press `Ctrl+C` to interrupt.

### Usage Questions

**Q: Can I have multiple conversations?**
A: Each session is independent. History is stored in the database.

**Q: How do I see past decisions?**
A: Ask the Archives ministry:
```
> Recall all decisions
```

**Q: Can multiple users use it simultaneously?**
A: Currently, no. It's designed for single-user operation.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Submit request |
| Ctrl+C | Cancel current request |
| Ctrl+D | Exit (same as /quit) |
| Up Arrow | Previous request (if supported) |

---

## Tips and Tricks

### Speed Up Responses

1. Use a smaller model (qwen2.5:7b)
2. Keep requests focused
3. Use direct ministry routing for known tasks

### Get More Detailed Answers

1. Ask follow-up questions
2. Request specific formats ("as a list", "with examples")
3. Provide more context

### Build Better Software

1. Start with architecture design
2. Get code written
3. Have it reviewed (security + quality)
4. Generate tests
5. Store decisions in Archives

### Debug Effectively

1. Provide the error message
2. Include the relevant code
3. Explain expected vs actual behavior
4. Let the Debugger work through hypotheses

---

## Next Steps

Now that you understand the system:

1. Work through the [Quick Start Guide](QUICK_START.md) examples
2. Explore each ministry's capabilities
3. Try building a small project with the system
4. Read the [Architecture Guide](ARCHITECTURE.md) to understand how it works

Happy exploring!
