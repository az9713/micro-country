# Quick Start Guide

Welcome! This guide will get you up and running with 10 hands-on examples in about 30 minutes. Each example builds on the previous one, so work through them in order.

## Before You Begin

Make sure you have:
1. Completed the [Installation Guide](INSTALLATION.md)
2. Ollama running (`ollama serve` in a terminal)
3. A model downloaded (choose based on your GPU - see [Ollama Commands Reference](#ollama-commands-reference) below)

## Starting the System

Open a terminal and run:

```bash
cd micro-country
python orchestrator.py
```

You should see:
```
Starting Micro-Country Orchestrator...
[OK] Connected to Ollama at http://localhost:11434
[OK] Model mistral:7b available
Knowledge server ready for connection at ...
Ministry code ready for connection at ...
Ministry research ready for connection at ...
Ministry quality ready for connection at ...
Ministry operations ready for connection at ...
Ministry archives ready for connection at ...
Ministry communications ready for connection at ...

Orchestrator ready!

============================================================
Welcome to the Micro-Country of Geniuses
============================================================

Commands:
  /debate <topic>  - Start a debate on a topic
  /review <text>   - Adversarial review of text
  /ministry <name> - Direct request to ministry
  /quit            - Exit

Or just type your request.

>
```

Now you're ready for the examples!

---

## Example 1: Your First Request

**Goal**: Understand how the system routes requests to specialists.

**What to type**:
```
> Explain what a REST API is
```

**What happens**:
1. The Orchestrator sees "explain" and routes to the **Research Ministry**
2. The **Writer specialist** is selected (explains concepts)
3. The specialist follows the 7-step Genius Protocol
4. You get a clear explanation

**What you'll see**:
```
[research/writer]

### 1. OBSERVE
The user wants to understand REST APIs...

### 2. THINK
REST stands for Representational State Transfer...

[... continues through all 7 steps ...]

### 6. ACT
A REST API is a way for computer programs to talk to each other...
```

**What you learned**: The system automatically picks the right specialist for your request.

---

## Example 2: Getting Code Written

**Goal**: Have the system write working code for you.

**What to type**:
```
> Write a Python function that checks if a string is a valid email address
```

**What happens**:
1. Orchestrator routes to **Code Ministry** (sees "write", "function")
2. The **Coder specialist** handles it
3. You get working code with explanation

**Expected output**:
```python
import re

def is_valid_email(email: str) -> bool:
    """
    Check if a string is a valid email address.

    Args:
        email: The string to validate

    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

**What you learned**: The Code Ministry writes real, usable code.

---

## Example 3: Designing Architecture

**Goal**: Get architectural advice for a software project.

**What to type**:
```
> Design the architecture for a simple blog application with posts and comments
```

**What happens**:
1. Routes to **Code Ministry**
2. The **Architect specialist** handles design requests
3. You get a structured design with components and trade-offs

**Expected output structure**:
- Overview of the architecture
- Component breakdown (Frontend, Backend, Database)
- Data models (Post, Comment, User)
- API endpoints
- Trade-offs considered
- Recommendation with rationale

**What you learned**: The Architect thinks through designs systematically, not just throwing out ideas.

---

## Example 4: Debugging Help

**Goal**: Get help finding and fixing bugs.

**What to type**:
```
> Debug this code - it should return the sum but returns None:
def add_numbers(a, b):
    result = a + b
```

**What happens**:
1. Routes to **Code Ministry**
2. The **Debugger specialist** analyzes the code
3. You get diagnosis and fix

**Expected insight**:
```
Root cause: The function calculates `result` but never returns it.

Fix:
def add_numbers(a, b):
    result = a + b
    return result  # Add this line

Or more simply:
def add_numbers(a, b):
    return a + b
```

**What you learned**: The Debugger finds root causes, not just symptoms.

---

## Example 5: Getting Tests Written

**Goal**: Have the Quality Ministry create tests for your code.

**What to type**:
```
> Write unit tests for a function that calculates the factorial of a number
```

**What happens**:
1. Routes to **Quality Ministry** (sees "test")
2. The **Tester specialist** creates comprehensive tests
3. You get tests for happy path, edge cases, and errors

**Expected output**:
```python
import pytest

def test_factorial_of_zero():
    assert factorial(0) == 1

def test_factorial_of_one():
    assert factorial(1) == 1

def test_factorial_of_five():
    assert factorial(5) == 120

def test_factorial_negative_raises_error():
    with pytest.raises(ValueError):
        factorial(-1)

def test_factorial_non_integer_raises_error():
    with pytest.raises(TypeError):
        factorial(3.5)
```

**What you learned**: The Tester thinks about edge cases you might miss.

---

## Example 6: Security Review

**Goal**: Get a security audit of code.

**What to type**:
```
> Security audit this login code:
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result
```

**What happens**:
1. Routes to **Quality Ministry** (sees "security audit")
2. The **Auditor specialist** reviews for vulnerabilities
3. You get findings with severity and fixes

**Expected findings**:
```
CRITICAL: SQL Injection Vulnerability
- Location: Line 2, query construction
- Problem: User input directly in SQL string
- Fix: Use parameterized queries

HIGH: Plain Text Password
- Location: Password handling
- Problem: Password compared in plain text
- Fix: Hash passwords with bcrypt/argon2

Recommended secure version:
def login(username, password):
    query = "SELECT password_hash FROM users WHERE username = ?"
    result = db.execute(query, (username,))
    if result and verify_password(password, result.password_hash):
        return create_session(result.user_id)
    return None
```

**What you learned**: The Auditor catches security issues that could be exploited.

---

## Example 7: Starting a Debate

**Goal**: Have specialists debate a topic with different perspectives.

**What to type**:
```
/debate money is the scorecard
```

**What happens**:
1. Two specialists (architect, coder) participate by default
2. Each presents their position following the 7-step Genius Protocol
3. Progress is shown as each participant responds
4. A synthesis combines the key insights

**Real example session**:
```
> /debate money is the scorecard

Starting debate on: money is the scorecard
Participants: architect, coder
(Progress will be shown as each participant responds)

[Round 1/1] Gathering initial positions...
  [1/3] architect is thinking...
  [1/3] architect done.
  [2/3] coder is thinking...
  [2/3] coder done.

[Synthesis] Creating final summary...
  [3/3] Synthesizing all positions...
  [3/3] Synthesis complete!

==================================================
DEBATE POSITIONS
==================================================

--- architect (Round 1) ---
### 1. OBSERVE
The topic at hand is "money is the scorecard", which suggests a perspective
that financial success or wealth is the primary measure of achievement...

### 2. THINK
When considering the statement "money is the scorecard," it's crucial to
recognize its implications and potential consequences...

### 3. REFLECT
Upon reflection, it's essential to acknowledge that financial success is
indeed a valuable outcome. However, it should not be the sole measure...

### 4. CRITIQUE
Criticizing this perspective, one can argue that an overemphasis on financial
success may lead to unethical practices, increased income inequality...

### 5. REFINE
Refining this perspective, we should strive to create a balanced approach
that prioritizes financial success while also considering ethics...

### 6. ACT
In practice, this could manifest through setting financial goals alongside
non-financial objectives, adopting ethical business practices...

### 7. VERIFY
- Rationale explained: Yes
- Trade-offs identified: Yes
- Evidence cited: No (philosophical topic)

--- coder (Round 1) ---
[Similar 7-step reasoning from the coder's perspective...]

==================================================
SYNTHESIS
==================================================
### Agreement
Both participants agree that money alone should not be the sole measure
of success. A balanced approach is needed.

### Disagreements
Minor differences in emphasis on specific non-financial factors.

### Recommendation
Create architectures that support financial success but also encourage
innovation, ethical decision-making, and social responsibility.
```

**What you learned**: Debates surface trade-offs and lead to better decisions through structured reasoning.

---

## Example 8: Adversarial Review

**Goal**: Have your work critically reviewed.

**What to type**:
```
/review This API design uses a single endpoint /api/data that accepts all parameters as query strings and returns all data types in one response
```

**What happens**:
1. The **Auditor** becomes a skeptic
2. Ruthlessly finds problems
3. Provides specific improvements

**Expected output**:
```
Verdict: REJECT

Issues found:
- Violates REST principles (not resource-based)
- No separation of concerns
- Will be hard to cache
- Query strings have length limits
- Response size will be unpredictable

Recommended changes:
- Split into resource-specific endpoints (/api/users, /api/posts)
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Implement pagination for collections
- Return only requested data types
```

**What you learned**: Adversarial review finds flaws before they become problems.

---

## Example 9: Remembering Decisions

**Goal**: Store a decision for future reference.

**What to type**:
```
> Remember this decision: We chose PostgreSQL for the user database because it provides ACID compliance and we need strong consistency for financial transactions
```

**What happens**:
1. Routes to **Archives Ministry** (sees "remember")
2. The **Memory specialist** stores it with context
3. Can be recalled later

**To recall later**:
```
> Recall decisions about the database
```

**What you learned**: The Archives Ministry creates institutional memory.

---

## Example 10: Multi-Step Task

**Goal**: Combine multiple specialists for a complex request.

**What to type**:
```
> I need to add a password reset feature to our app. Design it, show me the code, and explain how to test it.
```

**What happens**:
1. **Architect** designs the feature (email flow, token generation)
2. **Coder** implements the code
3. **Tester** provides test cases
4. Everything is coordinated automatically

**Expected output sections**:
1. **Architecture**: Email flow diagram, security considerations
2. **Implementation**: Token generation, email sending, reset endpoint
3. **Testing**: Unit tests, integration tests, security tests

**What you learned**: Complex tasks use multiple specialists working together.

---

## Bonus Examples

### Ask for Documentation
```
> Write API documentation for a user registration endpoint
```

### Get Research
```
> Search for best practices for handling authentication tokens
```

### Schedule a Task
```
> Schedule a reminder to review the security audit findings tomorrow
```

### Compare Options
```
> Compare React vs Vue vs Angular for a small dashboard project
```

---

## Summary of Commands

| Command | What It Does | Example |
|---------|--------------|---------|
| (plain text) | Route to appropriate ministry | `Write a sorting function` |
| `/debate <topic>` | Start a multi-specialist debate | `/debate SQL vs NoSQL` |
| `/review <text>` | Adversarial review | `/review My API design uses...` |
| `/ministry <name> <text>` | Direct to specific ministry | `/ministry quality Test this code` |
| `/quit` | Exit the system | `/quit` |

---

## What's Next?

Now that you've completed the quick start:

1. **Read the [User Guide](USER_GUIDE.md)** for all features
2. **Explore the ministries** - each has unique tools
3. **Try the Evidence Court** - when specialists disagree
4. **Build something real** - use it for an actual project

---

## Troubleshooting Quick Start Issues

### "Could not connect to Ollama"
```bash
# Make sure Ollama is running
ollama serve
```

### "Model not found"
```bash
# Download the model (choose one based on your GPU)
ollama pull mistral:7b    # For 4GB GPU (recommended)
ollama pull llama3.2      # For limited hardware
```

### Responses are slow
- The first request takes longer (model loading)
- Subsequent requests are faster
- Consider a smaller model for faster responses

### "No output" or empty responses
- Check Ollama is running
- Check the model is downloaded
- Try a simpler request first

---

## Ollama Commands Reference

These are the essential Ollama commands you'll need:

### Starting Ollama

```bash
# Start the Ollama server (required before running orchestrator)
ollama serve
```

### Managing Models

```bash
# List all downloaded models
ollama list

# Download a model (choose based on your GPU VRAM)
ollama pull mistral:7b        # 4GB VRAM - recommended for most users
ollama pull llama3.2          # 2GB - fastest, for limited hardware
ollama pull qwen2.5:7b        # 6GB VRAM
ollama pull deepseek-r1:7b    # 6GB VRAM - good for reasoning

# Delete a model to free disk space
ollama rm model-name:tag

# Example: Delete a large model you no longer need
ollama rm gpt-oss:20b
```

### Testing Models

```bash
# Quick test that a model works
ollama run mistral:7b "Say hello"

# Test with verbose output to see performance stats
ollama run mistral:7b "What is 2+2?" --verbose

# Look for "eval rate" in output - should be 15+ tokens/sec with GPU
# If under 5 tokens/sec, model is running on CPU (too large for GPU)
```

### Checking System Status

```bash
# Check Ollama version
ollama --version

# See what models are currently loaded in memory
ollama ps

# Check GPU usage (NVIDIA only)
nvidia-smi
```

### Model Size vs GPU VRAM Guide

| GPU VRAM | Recommended Model | Download Command |
|----------|-------------------|------------------|
| 4 GB | mistral:7b | `ollama pull mistral:7b` |
| 6-8 GB | qwen2.5:7b | `ollama pull qwen2.5:7b` |
| 12+ GB | qwen2.5:14b | `ollama pull qwen2.5:14b` |
| No GPU | llama3.2 | `ollama pull llama3.2` |

**Important**: If a model is larger than your GPU's VRAM, it will run mostly on CPU and be very slow (4-5 tokens/sec instead of 15-30 tokens/sec).

### Configuration

The model used by the orchestrator is set in `config.yaml`:

```yaml
ollama:
  host: "http://localhost:11434"
  model: "mistral:7b"  # Change this to use a different model
  timeout: 300  # seconds
```

---

Congratulations! You've completed the Quick Start Guide. You now understand:
- How requests are routed to specialists
- How to get code, designs, and reviews
- How to use debates for decisions
- How to store and recall knowledge
- How to manage Ollama models

Ready for more? Continue to the [User Guide](USER_GUIDE.md)!
