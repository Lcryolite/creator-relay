"""A local audit trail for a creator's stated preferences and follow-ups."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .relay import CreatorBrief


class CreatorMemory:
    """Persistent state that is visible to the creator, not hidden agent memory."""

    def __init__(self, database: str | Path = ":memory:"):
        self.database = str(database)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS briefs (
                    id INTEGER PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    audience TEXT NOT NULL,
                    channels TEXT NOT NULL,
                    goal TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS follow_ups (
                    id INTEGER PRIMARY KEY,
                    brief_id INTEGER NOT NULL,
                    due_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'queued',
                    FOREIGN KEY (brief_id) REFERENCES briefs(id)
                );
                """
            )

    def remember(self, brief: CreatorBrief) -> dict[str, object]:
        brief.validate()
        created_at = datetime.now(UTC).isoformat()
        due_at = (datetime.now(UTC) + timedelta(days=1)).isoformat()
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO briefs (created_at, source, audience, channels, goal) "
                "VALUES (?, ?, ?, ?, ?)",
                (created_at, brief.source, brief.audience, "|".join(brief.channels), brief.goal),
            )
            brief_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO follow_ups (brief_id, due_at) VALUES (?, ?)",
                (brief_id, due_at),
            )
        return {"brief_id": brief_id, "created_at": created_at, "follow_up_due_at": due_at}

    def timeline(self) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT briefs.id, briefs.created_at, briefs.audience, briefs.channels,
                       briefs.goal, follow_ups.due_at, follow_ups.status
                FROM briefs JOIN follow_ups ON follow_ups.brief_id = briefs.id
                ORDER BY briefs.id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]
