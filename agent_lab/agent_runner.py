"""Stable runner boundary around smolagents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from smolagents import Tool, ToolCallingAgent
from smolagents.models import Model

from agent_lab.memory.base import MemoryBackend
from agent_lab.offline_model import OfflineFinalAnswerModel
from agent_lab.smol_tools import CalculatorTool
from agent_lab.trace import AgentTrace, JsonlTraceWriter


@dataclass
class AgentRunResult:
    answer: str
    trace: AgentTrace


class AgentRunner:
    """Run one task through smolagents with project memory and tracing."""

    def __init__(
        self,
        memory: MemoryBackend,
        *,
        model: Model | None = None,
        tools: list[Tool] | None = None,
        trace_path: str | Path | None = None,
        max_steps: int = 2,
    ) -> None:
        self.memory = memory
        self.model = model or OfflineFinalAnswerModel(model_id="offline-final-answer")
        self.tools = tools or [CalculatorTool()]
        self.trace_writer = JsonlTraceWriter(trace_path) if trace_path else None
        self.max_steps = max_steps

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
        agent_task = _compose_agent_task(task_input, memory_context)

        agent = ToolCallingAgent(
            tools=self.tools,
            model=self.model,
            max_steps=self.max_steps,
        )
        answer = str(agent.run(agent_task))

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
            tool_calls=_extract_tool_calls(agent),
            final_answer=answer,
            metrics={
                "backend": self.memory.name,
                "retrieved_memory_count": len(retrieved),
            },
        )
        if self.trace_writer:
            self.trace_writer.write(trace)
        return AgentRunResult(answer=answer, trace=trace)


def _compose_agent_task(task_input: str, memory_context: str) -> str:
    if not memory_context:
        return task_input
    return (
        "Use these relevant long-term memories when helpful. "
        "If they are irrelevant, ignore them.\n\n"
        f"<memory_context>\n{memory_context}\n</memory_context>\n\n"
        f"Task:\n{task_input}"
    )


def _extract_tool_calls(agent: ToolCallingAgent) -> list[dict[str, object]]:
    calls: list[dict[str, object]] = []
    for step in getattr(agent.memory, "steps", []):
        observations = getattr(step, "observations", None)
        if observations:
            calls.append({"observations": observations})
        model_output_message = getattr(step, "model_output_message", None)
        for call in getattr(model_output_message, "tool_calls", []) or []:
            function = getattr(call, "function", None)
            calls.append(
                {
                    "id": getattr(call, "id", None),
                    "type": getattr(call, "type", None),
                    "name": getattr(function, "name", None),
                    "arguments": getattr(function, "arguments", None),
                }
            )
    return calls
