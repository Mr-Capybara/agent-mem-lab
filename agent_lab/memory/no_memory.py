"""A memory backend that intentionally stores nothing."""

from __future__ import annotations

from agent_lab.memory.base import MemoryBackend, MemoryEvent, MemoryRecord, MemorySearchResult


class NoMemoryBackend(MemoryBackend):
    """Baseline backend for no long-term memory."""

    name = "no_memory"

    def add(self, event: MemoryEvent) -> MemoryRecord:
        return MemoryRecord.from_event(event)

    def search(
        self,
        query: str,
        *,
        user_id: str,
        project_id: str,
        top_k: int = 5,
    ) -> list[MemorySearchResult]:
        return []

    def reset(
        self,
        *,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        return None

    def export(self) -> list[MemoryRecord]:
        return []
