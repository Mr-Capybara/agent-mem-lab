"""Shared memory backend contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

MemoryType = Literal[
    "user_profile",
    "project_fact",
    "task_state",
    "episodic_trace",
    "failure_lesson",
    "preference_update",
]


@dataclass
class MemoryEvent:
    """Candidate memory item produced by an interaction."""

    content: str
    memory_type: MemoryType
    user_id: str = "default_user"
    project_id: str = "default_project"
    session_id: str = "default_session"
    source: str = "agent"
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryRecord:
    """Persisted memory item."""

    id: str
    content: str
    memory_type: MemoryType
    user_id: str
    project_id: str
    session_id: str
    source: str
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_event(cls, event: MemoryEvent) -> MemoryRecord:
        return cls(
            id=str(uuid4()),
            content=event.content,
            memory_type=event.memory_type,
            user_id=event.user_id,
            project_id=event.project_id,
            session_id=event.session_id,
            source=event.source,
            timestamp=event.timestamp,
            metadata=dict(event.metadata),
        )


@dataclass
class MemorySearchResult:
    """Result returned by a backend search."""

    record: MemoryRecord
    score: float | None = None
    reason: str | None = None


class MemoryBackend(ABC):
    """Stable interface all memory backends must implement."""

    name: str

    @abstractmethod
    def add(self, event: MemoryEvent) -> MemoryRecord:
        """Persist a memory event and return the stored record."""

    @abstractmethod
    def search(
        self,
        query: str,
        *,
        user_id: str,
        project_id: str,
        top_k: int = 5,
    ) -> list[MemorySearchResult]:
        """Return memories relevant to a query."""

    @abstractmethod
    def reset(
        self,
        *,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        """Clear memories, optionally scoped to user/project."""

    @abstractmethod
    def export(self) -> list[MemoryRecord]:
        """Export backend state for trace/debugging."""
