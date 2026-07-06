"""Simple in-memory baseline that searches raw stored history."""

from __future__ import annotations

import re
from collections import Counter

from agent_lab.memory.base import MemoryBackend, MemoryEvent, MemoryRecord, MemorySearchResult


class RawHistoryBackend(MemoryBackend):
    """A transparent lexical baseline for memory experiments."""

    name = "raw_history"

    def __init__(self, max_items: int = 1000) -> None:
        self.max_items = max_items
        self._records: list[MemoryRecord] = []

    def add(self, event: MemoryEvent) -> MemoryRecord:
        record = MemoryRecord.from_event(event)
        self._records.append(record)
        if len(self._records) > self.max_items:
            self._records = self._records[-self.max_items :]
        return record

    def search(
        self,
        query: str,
        *,
        user_id: str,
        project_id: str,
        top_k: int = 5,
    ) -> list[MemorySearchResult]:
        query_terms = _term_counts(query)
        if not query_terms:
            return []

        results: list[MemorySearchResult] = []
        for record in self._records:
            if record.user_id != user_id or record.project_id != project_id:
                continue
            score = _overlap_score(query_terms, _term_counts(record.content))
            if score > 0:
                results.append(
                    MemorySearchResult(
                        record=record,
                        score=score,
                        reason="lexical_overlap",
                    )
                )

        results.sort(key=lambda item: (item.score or 0, item.record.timestamp), reverse=True)
        return results[:top_k]

    def reset(
        self,
        *,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        if user_id is None and project_id is None:
            self._records = []
            return

        self._records = [
            record
            for record in self._records
            if not _matches_scope(record, user_id=user_id, project_id=project_id)
        ]

    def export(self) -> list[MemoryRecord]:
        return list(self._records)


def _term_counts(text: str) -> Counter[str]:
    terms = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
    return Counter(terms)


def _overlap_score(left: Counter[str], right: Counter[str]) -> float:
    overlap = sum(min(count, right[term]) for term, count in left.items())
    return float(overlap)


def _matches_scope(
    record: MemoryRecord,
    *,
    user_id: str | None,
    project_id: str | None,
) -> bool:
    if user_id is not None and record.user_id != user_id:
        return False
    if project_id is not None and record.project_id != project_id:
        return False
    return True
