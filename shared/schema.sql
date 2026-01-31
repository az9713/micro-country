-- Micro-Country of Geniuses Database Schema

-- Constitution: Core rules and values that govern the country
CREATE TABLE IF NOT EXISTS constitution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article TEXT NOT NULL,
    content TEXT NOT NULL,
    rationale TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Decision log: Historical decisions with full rationale
CREATE TABLE IF NOT EXISTS decision_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT UNIQUE NOT NULL,
    ministry TEXT NOT NULL,
    specialist TEXT,
    decision_type TEXT NOT NULL,  -- 'design', 'implementation', 'conflict_resolution', etc.
    context TEXT NOT NULL,        -- JSON: what led to this decision
    options_considered TEXT,      -- JSON: alternatives evaluated
    decision TEXT NOT NULL,       -- The actual decision made
    rationale TEXT NOT NULL,      -- Why this decision
    evidence TEXT,                -- JSON: supporting evidence
    outcome TEXT,                 -- JSON: result after implementation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project context: Current state of all projects
CREATE TABLE IF NOT EXISTS project_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',  -- 'active', 'paused', 'completed', 'archived'
    current_phase TEXT,
    goals TEXT,                    -- JSON array of project goals
    constraints TEXT,              -- JSON array of constraints
    tech_stack TEXT,               -- JSON: technologies in use
    file_structure TEXT,           -- JSON: project file tree
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Domain knowledge: Accumulated expertise
CREATE TABLE IF NOT EXISTS domain_knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledge_id TEXT UNIQUE NOT NULL,
    domain TEXT NOT NULL,          -- 'architecture', 'testing', 'security', etc.
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,                   -- Where this knowledge came from
    confidence REAL DEFAULT 0.8,   -- 0.0 to 1.0
    tags TEXT,                     -- JSON array of tags
    related_knowledge TEXT,        -- JSON array of related knowledge_ids
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Task history: What was attempted, what worked
CREATE TABLE IF NOT EXISTS task_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT UNIQUE NOT NULL,
    project_id TEXT,
    ministry TEXT NOT NULL,
    specialist TEXT,
    task_type TEXT NOT NULL,
    description TEXT NOT NULL,
    input_context TEXT,            -- JSON: input to the task
    approach TEXT,                 -- How the task was approached
    output TEXT,                   -- JSON: task output
    status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'failed'
    success BOOLEAN,
    lessons_learned TEXT,          -- What was learned from this task
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project_context(project_id)
);

-- Evidence court cases: Conflict resolution records
CREATE TABLE IF NOT EXISTS evidence_court_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id TEXT UNIQUE NOT NULL,
    topic TEXT NOT NULL,           -- What the conflict is about
    advocates TEXT NOT NULL,       -- JSON: list of positions and their advocates
    evidence_presented TEXT NOT NULL, -- JSON: evidence for each position
    evidence_analysis TEXT,        -- JSON: strength analysis per evidence item
    ruling TEXT NOT NULL,          -- The court's decision
    ruling_rationale TEXT NOT NULL,
    dissenting_opinions TEXT,      -- JSON: any disagreements with ruling
    precedent_set TEXT,            -- What precedent this sets for future
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cross-ministry requests: Track inter-ministry communication
CREATE TABLE IF NOT EXISTS cross_ministry_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT UNIQUE NOT NULL,
    from_ministry TEXT NOT NULL,
    to_ministry TEXT NOT NULL,
    request_type TEXT NOT NULL,
    request_content TEXT NOT NULL,  -- JSON: the actual request
    response_content TEXT,          -- JSON: the response
    status TEXT DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP
);

-- Genius reasoning traces: Track the 7-step reasoning for debugging/learning
CREATE TABLE IF NOT EXISTS genius_reasoning_traces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id TEXT UNIQUE NOT NULL,
    task_id TEXT,
    specialist TEXT NOT NULL,
    step_observe TEXT,
    step_think TEXT,
    step_reflect TEXT,
    step_critique TEXT,
    step_refine TEXT,
    step_act TEXT,
    step_verify TEXT,
    quality_score REAL,            -- Self-assessed quality 0.0-1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task_history(task_id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_decision_log_ministry ON decision_log(ministry);
CREATE INDEX IF NOT EXISTS idx_decision_log_created ON decision_log(created_at);
CREATE INDEX IF NOT EXISTS idx_task_history_project ON task_history(project_id);
CREATE INDEX IF NOT EXISTS idx_task_history_ministry ON task_history(ministry);
CREATE INDEX IF NOT EXISTS idx_task_history_status ON task_history(status);
CREATE INDEX IF NOT EXISTS idx_domain_knowledge_domain ON domain_knowledge(domain);
CREATE INDEX IF NOT EXISTS idx_cross_ministry_from ON cross_ministry_requests(from_ministry);
CREATE INDEX IF NOT EXISTS idx_cross_ministry_to ON cross_ministry_requests(to_ministry);

-- Insert default constitution articles
INSERT OR IGNORE INTO constitution (article, content, rationale) VALUES
('Article 1: Purpose', 'The Micro-Country of Geniuses exists to solve complex problems through collective intelligence, where each specialist contributes deep expertise while respecting the wisdom of the whole.', 'Establishes the fundamental purpose of the system.'),
('Article 2: Reasoning Protocol', 'Every agent must follow the 7-step genius reasoning protocol: OBSERVE, THINK, REFLECT, CRITIQUE, REFINE, ACT, VERIFY. No output without reflection.', 'Ensures consistent high-quality reasoning across all agents.'),
('Article 3: Evidence-Based Decisions', 'When geniuses disagree, evidence decides. Empirical evidence trumps theoretical arguments. Precedent informs but does not dictate.', 'Provides clear conflict resolution mechanism.'),
('Article 4: Knowledge Sharing', 'All significant decisions, learnings, and outcomes must be recorded in the shared knowledge base for the benefit of all.', 'Enables collective learning and prevents repeated mistakes.'),
('Article 5: Quality Threshold', 'No output shall be delivered until it meets the quality threshold: rationale explained, trade-offs identified, evidence cited.', 'Maintains high output quality standards.'),
('Article 6: Adversarial Review', 'Every significant output must be reviewed by a skeptic before acceptance. Challenge assumptions, find flaws, improve quality.', 'Implements checks and balances for better outputs.'),
('Article 7: Humility', 'Geniuses acknowledge uncertainty. When confidence is low, say so. When evidence is weak, seek more. When wrong, learn and adapt.', 'Promotes intellectual honesty and continuous improvement.');
