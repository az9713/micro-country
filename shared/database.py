"""Database utilities for Micro-Country of Geniuses."""

import aiosqlite
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
from contextlib import asynccontextmanager


class Database:
    """Async SQLite database wrapper for the Micro-Country."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self._connection: Optional[aiosqlite.Connection] = None

    async def initialize(self) -> None:
        """Initialize the database with schema."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        schema_path = Path(__file__).parent / "schema.sql"
        async with aiosqlite.connect(self.db_path) as db:
            with open(schema_path) as f:
                await db.executescript(f.read())
            await db.commit()

    @asynccontextmanager
    async def connection(self):
        """Get a database connection."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            yield db

    # Constitution operations
    async def get_constitution(self) -> list[dict]:
        """Get all constitution articles."""
        async with self.connection() as db:
            cursor = await db.execute(
                "SELECT article, content, rationale FROM constitution ORDER BY id"
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def add_constitution_article(
        self, article: str, content: str, rationale: str = None
    ) -> int:
        """Add a new constitution article."""
        async with self.connection() as db:
            cursor = await db.execute(
                "INSERT INTO constitution (article, content, rationale) VALUES (?, ?, ?)",
                (article, content, rationale),
            )
            await db.commit()
            return cursor.lastrowid

    # Decision log operations
    async def log_decision(
        self,
        ministry: str,
        decision_type: str,
        context: dict,
        decision: str,
        rationale: str,
        specialist: str = None,
        options_considered: list = None,
        evidence: list = None,
    ) -> str:
        """Log a decision with full context."""
        decision_id = f"dec_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO decision_log
                   (decision_id, ministry, specialist, decision_type, context,
                    options_considered, decision, rationale, evidence)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    decision_id,
                    ministry,
                    specialist,
                    decision_type,
                    json.dumps(context),
                    json.dumps(options_considered) if options_considered else None,
                    decision,
                    rationale,
                    json.dumps(evidence) if evidence else None,
                ),
            )
            await db.commit()
        return decision_id

    async def get_decisions(
        self,
        ministry: str = None,
        decision_type: str = None,
        limit: int = 50,
    ) -> list[dict]:
        """Get decisions with optional filtering."""
        query = "SELECT * FROM decision_log WHERE 1=1"
        params = []

        if ministry:
            query += " AND ministry = ?"
            params.append(ministry)
        if decision_type:
            query += " AND decision_type = ?"
            params.append(decision_type)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        async with self.connection() as db:
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                # Parse JSON fields
                for field in ["context", "options_considered", "evidence", "outcome"]:
                    if d.get(field):
                        d[field] = json.loads(d[field])
                results.append(d)
            return results

    # Project context operations
    async def create_project(
        self,
        name: str,
        description: str = None,
        goals: list = None,
        constraints: list = None,
        tech_stack: dict = None,
    ) -> str:
        """Create a new project."""
        project_id = f"proj_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO project_context
                   (project_id, name, description, goals, constraints, tech_stack)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    project_id,
                    name,
                    description,
                    json.dumps(goals) if goals else None,
                    json.dumps(constraints) if constraints else None,
                    json.dumps(tech_stack) if tech_stack else None,
                ),
            )
            await db.commit()
        return project_id

    async def get_project(self, project_id: str) -> Optional[dict]:
        """Get a project by ID."""
        async with self.connection() as db:
            cursor = await db.execute(
                "SELECT * FROM project_context WHERE project_id = ?", (project_id,)
            )
            row = await cursor.fetchone()
            if row:
                d = dict(row)
                for field in ["goals", "constraints", "tech_stack", "file_structure"]:
                    if d.get(field):
                        d[field] = json.loads(d[field])
                return d
        return None

    async def update_project(self, project_id: str, **updates) -> bool:
        """Update a project."""
        if not updates:
            return False

        # Serialize JSON fields
        for field in ["goals", "constraints", "tech_stack", "file_structure"]:
            if field in updates and updates[field] is not None:
                updates[field] = json.dumps(updates[field])

        updates["updated_at"] = datetime.now().isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [project_id]

        async with self.connection() as db:
            cursor = await db.execute(
                f"UPDATE project_context SET {set_clause} WHERE project_id = ?",
                values,
            )
            await db.commit()
            return cursor.rowcount > 0

    # Domain knowledge operations
    async def store_knowledge(
        self,
        domain: str,
        topic: str,
        content: str,
        source: str = None,
        confidence: float = 0.8,
        tags: list = None,
    ) -> str:
        """Store domain knowledge."""
        knowledge_id = f"know_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO domain_knowledge
                   (knowledge_id, domain, topic, content, source, confidence, tags)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    knowledge_id,
                    domain,
                    topic,
                    content,
                    source,
                    confidence,
                    json.dumps(tags) if tags else None,
                ),
            )
            await db.commit()
        return knowledge_id

    async def search_knowledge(
        self,
        domain: str = None,
        query: str = None,
        tags: list = None,
        limit: int = 20,
    ) -> list[dict]:
        """Search domain knowledge."""
        sql = "SELECT * FROM domain_knowledge WHERE 1=1"
        params = []

        if domain:
            sql += " AND domain = ?"
            params.append(domain)
        if query:
            sql += " AND (topic LIKE ? OR content LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%"])

        sql += " ORDER BY confidence DESC, created_at DESC LIMIT ?"
        params.append(limit)

        async with self.connection() as db:
            cursor = await db.execute(sql, params)
            rows = await cursor.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                if d.get("tags"):
                    d["tags"] = json.loads(d["tags"])
                if d.get("related_knowledge"):
                    d["related_knowledge"] = json.loads(d["related_knowledge"])
                results.append(d)
            return results

    # Task history operations
    async def create_task(
        self,
        ministry: str,
        task_type: str,
        description: str,
        specialist: str = None,
        project_id: str = None,
        input_context: dict = None,
    ) -> str:
        """Create a new task."""
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO task_history
                   (task_id, project_id, ministry, specialist, task_type,
                    description, input_context, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')""",
                (
                    task_id,
                    project_id,
                    ministry,
                    specialist,
                    task_type,
                    description,
                    json.dumps(input_context) if input_context else None,
                ),
            )
            await db.commit()
        return task_id

    async def update_task(
        self,
        task_id: str,
        status: str = None,
        approach: str = None,
        output: Any = None,
        success: bool = None,
        lessons_learned: str = None,
        duration_ms: int = None,
    ) -> bool:
        """Update a task."""
        updates = {}
        if status:
            updates["status"] = status
        if approach:
            updates["approach"] = approach
        if output is not None:
            updates["output"] = json.dumps(output)
        if success is not None:
            updates["success"] = success
        if lessons_learned:
            updates["lessons_learned"] = lessons_learned
        if duration_ms:
            updates["duration_ms"] = duration_ms

        if status == "completed":
            updates["completed_at"] = datetime.now().isoformat()

        if not updates:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [task_id]

        async with self.connection() as db:
            cursor = await db.execute(
                f"UPDATE task_history SET {set_clause} WHERE task_id = ?",
                values,
            )
            await db.commit()
            return cursor.rowcount > 0

    async def get_task_history(
        self,
        ministry: str = None,
        project_id: str = None,
        status: str = None,
        limit: int = 50,
    ) -> list[dict]:
        """Get task history with filtering."""
        sql = "SELECT * FROM task_history WHERE 1=1"
        params = []

        if ministry:
            sql += " AND ministry = ?"
            params.append(ministry)
        if project_id:
            sql += " AND project_id = ?"
            params.append(project_id)
        if status:
            sql += " AND status = ?"
            params.append(status)

        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        async with self.connection() as db:
            cursor = await db.execute(sql, params)
            rows = await cursor.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                for field in ["input_context", "output"]:
                    if d.get(field):
                        d[field] = json.loads(d[field])
                results.append(d)
            return results

    # Evidence court operations
    async def record_court_case(
        self,
        topic: str,
        advocates: list[dict],
        evidence_presented: list[dict],
        ruling: str,
        ruling_rationale: str,
        evidence_analysis: dict = None,
        dissenting_opinions: list = None,
        precedent_set: str = None,
    ) -> str:
        """Record an evidence court case."""
        case_id = f"case_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO evidence_court_cases
                   (case_id, topic, advocates, evidence_presented, evidence_analysis,
                    ruling, ruling_rationale, dissenting_opinions, precedent_set)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    case_id,
                    topic,
                    json.dumps(advocates),
                    json.dumps(evidence_presented),
                    json.dumps(evidence_analysis) if evidence_analysis else None,
                    ruling,
                    ruling_rationale,
                    json.dumps(dissenting_opinions) if dissenting_opinions else None,
                    precedent_set,
                ),
            )
            await db.commit()
        return case_id

    async def get_court_precedents(
        self, topic_query: str = None, limit: int = 10
    ) -> list[dict]:
        """Get court precedents, optionally filtered by topic."""
        sql = "SELECT * FROM evidence_court_cases WHERE 1=1"
        params = []

        if topic_query:
            sql += " AND (topic LIKE ? OR precedent_set LIKE ?)"
            params.extend([f"%{topic_query}%", f"%{topic_query}%"])

        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        async with self.connection() as db:
            cursor = await db.execute(sql, params)
            rows = await cursor.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                for field in ["advocates", "evidence_presented", "evidence_analysis", "dissenting_opinions"]:
                    if d.get(field):
                        d[field] = json.loads(d[field])
                results.append(d)
            return results

    # Reasoning trace operations
    async def save_reasoning_trace(
        self,
        specialist: str,
        observe: str,
        think: str,
        reflect: str,
        critique: str,
        refine: str,
        act: str,
        verify: str,
        task_id: str = None,
        quality_score: float = None,
    ) -> str:
        """Save a genius reasoning trace."""
        trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO genius_reasoning_traces
                   (trace_id, task_id, specialist, step_observe, step_think,
                    step_reflect, step_critique, step_refine, step_act, step_verify,
                    quality_score)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    trace_id,
                    task_id,
                    specialist,
                    observe,
                    think,
                    reflect,
                    critique,
                    refine,
                    act,
                    verify,
                    quality_score,
                ),
            )
            await db.commit()
        return trace_id

    # Cross-ministry request operations
    async def create_cross_ministry_request(
        self,
        from_ministry: str,
        to_ministry: str,
        request_type: str,
        request_content: dict,
    ) -> str:
        """Create a cross-ministry request."""
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        async with self.connection() as db:
            await db.execute(
                """INSERT INTO cross_ministry_requests
                   (request_id, from_ministry, to_ministry, request_type, request_content)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    request_id,
                    from_ministry,
                    to_ministry,
                    request_type,
                    json.dumps(request_content),
                ),
            )
            await db.commit()
        return request_id

    async def respond_to_request(
        self, request_id: str, response_content: dict, status: str = "completed"
    ) -> bool:
        """Respond to a cross-ministry request."""
        async with self.connection() as db:
            cursor = await db.execute(
                """UPDATE cross_ministry_requests
                   SET response_content = ?, status = ?, responded_at = ?
                   WHERE request_id = ?""",
                (
                    json.dumps(response_content),
                    status,
                    datetime.now().isoformat(),
                    request_id,
                ),
            )
            await db.commit()
            return cursor.rowcount > 0
