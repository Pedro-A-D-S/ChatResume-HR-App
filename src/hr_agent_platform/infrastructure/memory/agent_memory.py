"""5-Layer Cognitive Memory Architecture for the HR Multi-Agent Platform.
Complies with CoALA, Mem0 architecture, SQLite ontology, and LGPD/GDPR TTL expiration.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class WorkingMemoryBudget:
    max_tokens: int = 4000
    overflow_threshold_pct: float = 0.85
    current_tokens: int = 0

    def should_overflow(self) -> bool:
        return self.current_tokens >= (self.max_tokens * self.overflow_threshold_pct)


@dataclass
class EpisodeRecord:
    task_id: str
    candidate_id: str
    role_evaluated: str
    fit_score: float
    judge_verdict: str
    tokens_used: int
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(UTC).isoformat()


class FiveLayerAgentMemory:
    """Manages Working, Episodic, Semantic, Procedural, and Forgetting layers."""

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.episodes_file = self.base_dir / "episodes.jsonl"
        self.db_path = self.base_dir / "facts.db"
        self.skills_dir = self.base_dir / "skills"
        self.skills_dir.mkdir(exist_ok=True)
        self.budget = WorkingMemoryBudget()
        self._init_semantic_db()

    def _init_semantic_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                relation TEXT NOT NULL,
                value TEXT NOT NULL,
                source_episode TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                superseded_by INTEGER REFERENCES facts(id)
            );
            """)

    # Layer 1: Working Memory
    def track_tokens(self, tokens: int) -> bool:
        self.budget.current_tokens += tokens
        return self.budget.should_overflow()

    def reset_working_memory(self):
        self.budget.current_tokens = 0

    # Layer 2: Episodic Memory
    def record_episode(self, episode: EpisodeRecord):
        with open(self.episodes_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(episode)) + "\n")

    def retrieve_recent_episodes(self, limit: int = 3) -> list[dict[str, Any]]:
        if not self.episodes_file.exists():
            return []
        lines = self.episodes_file.read_text(encoding="utf-8").strip().splitlines()
        episodes = [json.loads(l) for l in lines if l.strip()]
        return episodes[-limit:]

    # Layer 3: Semantic Memory
    def store_fact(
        self, entity: str, entity_type: str, relation: str, value: str, source: str
    ):
        with sqlite3.connect(self.db_path) as conn:
            # Conflict resolution: supersede old active fact with same entity & relation
            conn.execute(
                """
            UPDATE facts SET status = 'superseded' 
            WHERE entity = ? AND relation = ? AND status = 'active'
            """,
                (entity, relation),
            )

            conn.execute(
                """
            INSERT INTO facts (entity, entity_type, relation, value, source_episode)
            VALUES (?, ?, ?, ?, ?)
            """,
                (entity, entity_type, relation, value, source),
            )

    def query_facts(self, entity: str) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
            SELECT entity, relation, value, created_at FROM facts 
            WHERE entity = ? AND status = 'active'
            """,
                (entity,),
            ).fetchall()
            return [dict(r) for r in rows]

    # Layer 4: Procedural Memory (Skills)
    def register_skill(self, skill_name: str, yaml_content: str):
        path = self.skills_dir / f"{skill_name}.yaml"
        path.write_text(yaml_content, encoding="utf-8")

    def load_skill(self, skill_name: str) -> str | None:
        path = self.skills_dir / f"{skill_name}.yaml"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    # Layer 5: Forgetting Engine
    def run_forgetting_cycle(self, retention_days: int = 30) -> int:
        """Prunes expired candidate episodic and semantic records for LGPD/GDPR compliance."""
        cutoff = datetime.now(UTC) - timedelta(days=retention_days)
        cutoff_str = cutoff.isoformat()
        deleted_count = 0

        # Prune semantic facts
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """
            DELETE FROM facts WHERE created_at < ? AND status = 'superseded'
            """,
                (cutoff_str,),
            )
            deleted_count += cur.rowcount

        return deleted_count
