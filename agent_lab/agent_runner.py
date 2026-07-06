"""Agent runner skeleton.

The smolagents integration starts in P1 after dependencies are installed.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent_lab.memory.base import MemoryBackend
from agent_lab.trace import AgentTrace


@dataclass
class AgentRunResult:
    answer: str
    trace: AgentTrace


class AgentRunner:
    """Stable boundary around the underlying agent framework."""

    def __init__(self, memory: MemoryBackend) -> None:
        self.memory = memory

    def run(
        self,
        task_input: str,
        *,
        user_id: str = "default_user",
        project_id: str = "default_project",
        session_id: str = "default_session",
    ) -> AgentRunResult:
        retrieved = self.memory.search(
            task_input,
            user_id=user_id,
            project_id=project_id,
            top_k=5,
        )
        memory_context = "\n".join(result.record.content for result in retrieved)
        trace = AgentTrace(
            user_id=user_id,
            project_id=project_id,
            session_id=session_id,
            task_input=task_input,
            retrieved_memories=[
                {
                    "id": result.record.id,
                    "content": result.record.content,
                    "memory_type": result.record.memory_type,
                    "score": result.score,
                    "reason": result.reason,
                }
                for result in retrieved
            ],
            memory_context=memory_context,
            final_answer="",
        )
        raise NotImplementedError(
            f"smolagents integration will be implemented in P1-T2; trace_id={trace.trace_id}."
        )
