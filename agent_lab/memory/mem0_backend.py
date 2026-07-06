"""Mem0 backend placeholder.

The concrete integration is intentionally deferred until dependencies are
installed. Keeping the module now makes imports and project structure stable.
"""

from __future__ import annotations

from agent_lab.memory.base import MemoryBackend, MemoryEvent, MemoryRecord, MemorySearchResult


class Mem0Backend(MemoryBackend):
    """Mem0-backed memory implementation."""

    name = "mem0"

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise NotImplementedError("Mem0 integration will be implemented in P2-T4.")

    def add(self, event: MemoryEvent) -> MemoryRecord:
        raise NotImplementedError

    def search(
        self,
        query: str,
        *,
        user_id: str,
        project_id: str,
        top_k: int = 5,
    ) -> list[MemorySearchResult]:
        raise NotImplementedError

    def reset(
        self,
        *,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        raise NotImplementedError

    def export(self) -> list[MemoryRecord]:
        raise NotImplementedError
