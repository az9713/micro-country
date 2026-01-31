# Step-by-Step Tutorial

A hands-on tutorial with 15 progressive exercises. Work through these in order - each builds on the previous ones.

---

## Before You Start

### Prerequisites Checklist

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Ollama installed (`ollama --version`)
- [ ] Project dependencies installed (`pip install -r requirements.txt`)
- [ ] Ollama running (`ollama serve` in a separate terminal)
- [ ] Model downloaded (`ollama pull mistral:7b`)

### Starting the System

```bash
cd micro-country
python orchestrator.py
```

You should see:
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

---

## Part 1: Basic Usage (Exercises 1-5)

### Exercise 1: Your First Request

**Goal**: Understand how requests are processed.

**What to do**:
```
> Explain what a REST API is in simple terms
```

**What to observe**:
1. The response shows `[research/writer]` - indicating which ministry and specialist handled it
2. The response is structured with the 7-step Genius Protocol:
   - OBSERVE
   - THINK
   - REFLECT
   - CRITIQUE
   - REFINE
   - ACT
   - VERIFY

**Key Learning**: The system automatically routes your request to the appropriate specialist based on keywords ("explain" → Research Ministry → Writer).

**Try These Variations**:
```
> What is a database?
> Explain the difference between HTTP and HTTPS
> Define object-oriented programming
```

---

### Exercise 2: Getting Code Written

**Goal**: Have the Code Ministry write actual code.

**What to do**:
```
> Write a Python function that checks if a number is prime
```

**What to observe**:
1. Routes to `[code/coder]`
2. The OBSERVE step shows understanding of the requirement
3. The THINK step considers different approaches
4. The ACT step contains the actual code
5. The VERIFY step confirms quality

**Expected Output** (in ACT step):
```python
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
```

**Try These Variations**:
```
> Write a function to reverse a string
> Write a class for a simple calculator
> Write a function to find the nth Fibonacci number
```

---

### Exercise 3: Designing Architecture

**Goal**: Get system design advice from the Architect.

**What to do**:
```
> Design the architecture for a simple todo list application with tasks and due dates
```

**What to observe**:
1. Routes to `[code/architect]`
2. The response includes:
   - System overview
   - Component breakdown
   - Data model design
   - API endpoints (if relevant)
   - Trade-offs considered

**Key Learning**: The Architect thinks about structure, not just code. Use the Architect for:
- New project designs
- Feature architecture
- System refactoring decisions

**Try These Variations**:
```
> Design a URL shortener service
> Design a chat application architecture
> Design a file upload system
```

---

### Exercise 4: Debugging Help

**Goal**: Use the Debugger to find and fix bugs.

**What to do**:
```
> Debug this code - it should calculate the average but returns wrong values:

def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers) + 1
```

**What to observe**:
1. Routes to `[code/debugger]`
2. The OBSERVE step identifies what the code is supposed to do
3. The THINK step analyzes the code logic
4. The CRITIQUE step identifies the bug (the `+ 1` at the end)
5. The ACT step provides the fix

**Expected Insight**:
```
Bug: The function adds 1 to the final result, which shouldn't be there.

Fix:
def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)  # Remove the + 1
```

**Try These Variations**:
```
> Debug this: def multiply(a, b): return a + b
> Debug this: for i in range(10): if i = 5: print(i)
> Why does this return None: def add(a, b): result = a + b
```

---

### Exercise 5: Getting Tests Written

**Goal**: Have the Quality Ministry write tests for code.

**What to do**:
```
> Write comprehensive unit tests for a function that validates email addresses
```

**What to observe**:
1. Routes to `[quality/tester]`
2. The response includes:
   - Happy path tests (valid emails)
   - Edge case tests (empty string, special characters)
   - Error case tests (invalid formats)
   - Boundary tests

**Expected Output**:
```python
import pytest

def test_valid_simple_email():
    assert is_valid_email("user@example.com") == True

def test_valid_email_with_subdomain():
    assert is_valid_email("user@mail.example.com") == True

def test_invalid_empty_string():
    assert is_valid_email("") == False

def test_invalid_no_at_symbol():
    assert is_valid_email("userexample.com") == False

def test_invalid_no_domain():
    assert is_valid_email("user@") == False

def test_invalid_spaces():
    assert is_valid_email("user @example.com") == False
```

**Try These Variations**:
```
> Write tests for a password strength checker
> Write tests for a date parser function
> Write integration tests for a user registration API
```

---

## Part 2: Advanced Features (Exercises 6-10)

### Exercise 6: Security Auditing

**Goal**: Have code reviewed for security vulnerabilities.

**What to do**:
```
> Security audit this login function:

def login(username, password, db):
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    result = db.execute(query)
    if result:
        return create_session(result[0])
    return None
```

**What to observe**:
1. Routes to `[quality/auditor]`
2. Identifies vulnerabilities with severity levels:
   - CRITICAL: SQL injection
   - HIGH: Plain text password comparison
   - MEDIUM: No rate limiting mentioned
3. Provides remediation steps
4. Shows secure alternative code

**Expected Findings**:
```
CRITICAL: SQL Injection Vulnerability
- Location: query construction
- Problem: User input directly concatenated into SQL
- Fix: Use parameterized queries

HIGH: Plain Text Password
- Location: Password comparison
- Problem: Passwords should be hashed
- Fix: Use bcrypt or argon2

Secure Version:
def login(username: str, password: str, db) -> Optional[Session]:
    query = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.execute(query, (username,))
    if result and verify_password(password, result[0]['password_hash']):
        return create_session(result[0]['id'])
    return None
```

**Try These Variations**:
```
> Audit this file upload handler
> Review this API key storage approach
> Check this session management code for vulnerabilities
```

---

### Exercise 7: Starting a Debate

**Goal**: Have multiple specialists debate a technical decision.

**What to do**:
```
/debate Should we use a relational database (SQL) or a document database (NoSQL) for a social media application?
```

**What to observe**:
1. Multiple specialists participate (architect, coder, tester)
2. **Round 1**: Each states their initial position
3. **Round 2**: Each critiques the others
4. **Round 3**: Positions are refined
5. **Synthesis**: Best ideas are combined into a recommendation

**Typical Debate Flow**:
```
--- Round 1: Initial Positions ---

Architect: "I recommend a hybrid approach. Use SQL for user data
and relationships (ACID compliance), NoSQL for posts and media
(flexibility, scale)."

Coder: "From an implementation standpoint, starting with SQL makes
sense. It's simpler to maintain and most developers know it."

Tester: "For testing, SQL is easier. Clear schema, predictable
queries, better transaction testing."

--- Round 2: Critiques ---

Architect critiques Coder: "Starting simple is good, but we should
plan for scale from the beginning."

Coder critiques Architect: "Hybrid adds complexity. Do we really
need NoSQL initially?"

--- Synthesis ---

The strongest position: Start with PostgreSQL for all data. It
handles JSON documents well (jsonb type) and provides SQL when
needed. Migrate to hybrid only if performance requires it.

Evidence supporting this:
- EMPIRICAL: PostgreSQL benchmarks show good JSON performance
- PRECEDENT: Instagram started with PostgreSQL
- THEORETICAL: YAGNI principle - don't add complexity prematurely
```

**Try These Variations**:
```
/debate Microservices vs monolith for a startup
/debate REST vs GraphQL for a mobile app backend
/debate TypeScript vs JavaScript for a new frontend project
```

---

### Exercise 8: Adversarial Review

**Goal**: Get critical feedback that finds flaws.

**What to do**:
```
/review My API design has a single endpoint /api/data that accepts any parameters and returns all data types based on query strings
```

**What to observe**:
1. The Auditor becomes a skeptic
2. Ruthlessly identifies problems
3. Provides specific, actionable improvements
4. Gives a verdict: ACCEPT, NEEDS_REVISION, or REJECT

**Expected Output**:
```
VERDICT: REJECT

CRITICAL ISSUES:

1. Violates REST Principles
   - Single endpoint for all resources is anti-pattern
   - Resources should have their own endpoints (/users, /posts, etc.)

2. Poor Cacheability
   - Query string variations make caching ineffective
   - Same endpoint, different data = cache misses

3. Security Concerns
   - No clear access control per resource type
   - Difficult to audit who accessed what

4. Scalability Issues
   - Single endpoint = single point of failure
   - Cannot scale specific resources independently

5. Client Complexity
   - Clients must know all possible parameters
   - No discoverability

RECOMMENDED APPROACH:

Instead of:
  GET /api/data?type=user&id=123

Use:
  GET /api/users/123        (get user)
  GET /api/posts?userId=123 (get user's posts)
  GET /api/comments?postId=456 (get post's comments)

Each resource gets its own endpoint with proper:
- HTTP methods (GET, POST, PUT, DELETE)
- Pagination
- Filtering
- Caching headers
```

**Try These Variations**:
```
/review My password reset sends the new password via email
/review My API uses sequential integer IDs for all resources
/review My frontend stores the JWT token in localStorage
```

---

### Exercise 9: Storing Knowledge

**Goal**: Use the Archives Ministry to remember decisions.

**What to do**:
```
> Remember this decision: We chose PostgreSQL over MongoDB for the user database because we need ACID transactions for financial operations and strong data consistency
```

**What to observe**:
1. Routes to `[archives/memory]`
2. Confirms the decision is stored
3. Adds context about when and why

**Then recall it later**:
```
> Recall decisions about the database
```

**Expected Output**:
```
Found 1 relevant decision:

[2024-01-30] Database Selection
Ministry: archives
Decision: Use PostgreSQL for user database
Rationale: Need ACID transactions for financial operations
           and strong data consistency
Related: MongoDB was considered but rejected due to
         eventual consistency model
```

**Try These Variations**:
```
> Remember: We use bcrypt for password hashing with cost factor 12
> Remember: API versioning will use URL path (/v1/, /v2/)
> Recall all decisions about security
```

---

### Exercise 10: Comparing Options

**Goal**: Get a structured comparison of alternatives.

**What to do**:
```
> Compare React, Vue, and Angular for building a dashboard with many interactive charts
```

**What to observe**:
1. Routes to `[research/analyst]`
2. Creates a structured comparison with:
   - Criteria identified (performance, learning curve, ecosystem, etc.)
   - Each option evaluated against each criterion
   - Pros and cons listed
   - Final recommendation with rationale

**Expected Structure**:
```
COMPARISON: React vs Vue vs Angular for Dashboard

CRITERIA:
1. Learning Curve
2. Performance with Many Components
3. Chart Library Ecosystem
4. Bundle Size
5. TypeScript Support
6. Community & Support

EVALUATION:

React:
+ Large ecosystem of chart libraries (Recharts, Victory, Nivo)
+ Excellent performance with virtual DOM
+ Strong TypeScript support
- Steeper learning curve
- Need to choose many libraries yourself

Vue:
+ Gentle learning curve
+ Good performance
+ Growing ecosystem (Vue-ChartJS, Apache ECharts)
+ Progressive adoption possible
- Smaller community than React

Angular:
+ Complete framework, less decision fatigue
+ Built-in TypeScript
+ ngx-charts well-integrated
- Largest bundle size
- Steepest learning curve
- May be overkill for dashboard-only app

RECOMMENDATION:

For a dashboard with many charts, React is the strongest choice:
- Best chart library ecosystem
- Proven performance at scale
- Easy to find developers

If team is new to frontend, Vue is a close second due to
gentler learning curve.
```

**Try These Variations**:
```
> Compare AWS, GCP, and Azure for a startup
> Compare Docker and Kubernetes for a small team
> Compare pytest and unittest for Python testing
```

---

## Part 3: Multi-Step Tasks (Exercises 11-15)

### Exercise 11: Complete Feature Development

**Goal**: Go through the full cycle of designing, implementing, testing, and reviewing a feature.

**Step 1: Design**
```
> Design a password reset feature for a web application
```

**Step 2: Implement**
```
> Implement the password reset feature you just designed
```

**Step 3: Test**
```
> Write tests for the password reset implementation
```

**Step 4: Security Review**
```
> Security audit the password reset feature
```

**What to observe**:
- Each step builds on the previous
- Different specialists handle different aspects
- The final review may find issues to address

---

### Exercise 12: Debugging Session

**Goal**: Work through a multi-step debugging process.

**Step 1: Describe the Problem**
```
> I have a Python web scraper that works fine for small sites but hangs on large sites. It uses requests library to fetch pages and BeautifulSoup to parse them. Help me debug this.
```

**Step 2: Hypothesize**
```
> What are the most likely causes of the hanging?
```

**Step 3: Investigate**
```
> How would I add logging to identify which specific operation is slow?
```

**Step 4: Fix**
```
> Based on the hypothesis that it's memory issues with BeautifulSoup, how should I fix it?
```

**What to learn**: Real debugging is iterative. The Debugger helps you:
1. Form hypotheses
2. Design investigations
3. Interpret findings
4. Implement fixes

---

### Exercise 13: Documentation Sprint

**Goal**: Create comprehensive documentation for a feature.

**Step 1: API Documentation**
```
> Write API documentation for a user authentication endpoint with login, logout, and refresh token operations
```

**Step 2: User Guide**
```
> Write a user guide section explaining how to use the authentication system
```

**Step 3: Developer Guide**
```
> Write developer documentation explaining how the authentication system is implemented and how to extend it
```

**What to observe**:
- Different documentation types have different audiences
- API docs focus on "what" and "how to call"
- User guides focus on "how to use"
- Developer guides focus on "how it works"

---

### Exercise 14: Code Review Workflow

**Goal**: Simulate a code review with multiple reviewers.

**Step 1: Submit Code for Review**
```
> Review this code for quality, security, and performance:

class UserService:
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_user(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]

        query = f"SELECT * FROM users WHERE id = {user_id}"
        result = self.db.execute(query)
        user = result.fetchone()
        self.cache[user_id] = user
        return user

    def update_user(self, user_id, data):
        for key, value in data.items():
            query = f"UPDATE users SET {key} = '{value}' WHERE id = {user_id}"
            self.db.execute(query)
        self.db.commit()
        return True
```

**Step 2: Get Security Review**
```
/review The above UserService class
```

**Step 3: Get Performance Review**
```
> What are the performance issues with the UserService class?
```

**Step 4: Get Improved Version**
```
> Rewrite the UserService class addressing all the security and performance issues found
```

---

### Exercise 15: Architecture Decision Record (ADR)

**Goal**: Create a formal decision record with debate and evidence.

**Step 1: Initiate Debate**
```
/debate For our e-commerce platform, should we use a microservices architecture or a modular monolith?
```

**Step 2: Document the Decision**
```
> Create an Architecture Decision Record (ADR) for the database decision, including context, options considered, decision, and consequences
```

**Step 3: Store in Archives**
```
> Remember this ADR: [paste the key decision]
```

**What to learn**: ADRs are a best practice for documenting:
- **Context**: Why we needed to decide
- **Options**: What we considered
- **Decision**: What we chose
- **Consequences**: What this means for the project

---

## Tips for Success

### Getting Better Responses

1. **Be Specific**: "Write a login function" → "Write a login function using JWT tokens with 15-minute expiration"

2. **Provide Context**: "Fix this bug" → "Fix this bug in our Flask API. The `/users` endpoint returns 500 when the database is empty"

3. **Mention Constraints**: "Design an API" → "Design an API for mobile clients with slow connections"

### Using the Right Specialist

| Task | Ministry | Specialist |
|------|----------|------------|
| Design a system | Code | Architect |
| Write code | Code | Coder |
| Fix a bug | Code | Debugger |
| Research topic | Research | Analyst |
| Write docs | Research | Writer |
| Find information | Research | Searcher |
| Write tests | Quality | Tester |
| Security review | Quality | Auditor |
| Validate requirements | Quality | Validator |
| File operations | Operations | File Manager |
| Run commands | Operations | Shell Runner |
| Deploy | Operations | Deployer |
| Store decisions | Archives | Memory |
| Organize knowledge | Archives | Indexer |
| Send notifications | Communications | Messenger |
| Schedule tasks | Communications | Scheduler |

### Troubleshooting

**Slow responses?**
- First response is slower (model loading)
- Use a smaller model for faster responses
- Simplify complex requests

**Wrong specialist?**
- Use `/ministry <name>` to direct to specific ministry
- Be more explicit about what you need

**Response cut off?**
- Request was too complex
- Break into smaller parts
- Ask follow-up questions

---

## What's Next?

After completing these exercises:

1. **Build Something Real**: Use the system for an actual project
2. **Read the Developer Guide**: Understand how to extend the system
3. **Add Custom Tools**: Create tools specific to your needs
4. **Contribute**: Improve the system for others

---

## Quick Reference Card

### Commands

| Command | Description |
|---------|-------------|
| `<text>` | Send request to appropriate ministry |
| `/debate <topic>` | Multi-specialist debate |
| `/review <text>` | Adversarial review |
| `/ministry <name> <text>` | Direct to specific ministry |
| `/quit` | Exit the system |

### Ministry Names

`code` • `research` • `quality` • `operations` • `archives` • `communications`

### The 7 Steps

`OBSERVE` → `THINK` → `REFLECT` → `CRITIQUE` → `REFINE` → `ACT` → `VERIFY`

### Evidence Hierarchy

`EMPIRICAL` > `PRECEDENT` > `CONSENSUS` > `THEORETICAL` > `INTUITION`

---

Congratulations on completing the tutorial! You now have practical experience with all major features of the Micro-Country of Geniuses system.
