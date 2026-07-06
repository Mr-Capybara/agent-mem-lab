"""Trace data structures and JSONL writer."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass
class AgentTrace:
    """One agent/eval run trace."""

    trace_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    user_id: str = "default_user"
    project_id: str = "default_project"
    session_id: str = "default_session"
    task_input: str = ""
    retrieved_memories: list[dict[str, Any]] = field(default_factory=list)
    memory_context: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    final_answer: str = ""
    memory_writes: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


class JsonlTraceWriter:
    """Append traces to a JSONL file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, trace: AgentTrace) -> None:
        payload = asdict(trace)
        payload["timestamp"] = trace.timestamp.isoformat()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
