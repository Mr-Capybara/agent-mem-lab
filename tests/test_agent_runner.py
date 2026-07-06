import json

from agent_lab.agent_runner import AgentRunner
from agent_lab.memory import MemoryEvent, RawHistoryBackend


def test_agent_runner_uses_memory_and_writes_trace(tmp_path) -> None:
    memory = RawHistoryBackend()
    memory.add(
        MemoryEvent(
            content="The user prefers Chinese summaries.",
            memory_type="user_profile",
            user_id="u1",
            project_id="p1",
        )
    )
    trace_path = tmp_path / "runs.jsonl"
    runner = AgentRunner(memory=memory, trace_path=trace_path)

    result = runner.run(
        "Please create a Chinese summary.",
        user_id="u1",
        project_id="p1",
        session_id="s1",
    )

    assert "offline:" in result.answer
    assert "The user prefers Chinese summaries." in result.trace.memory_context
    assert result.trace.metrics["backend"] == "raw_history"
    assert result.trace.metrics["retrieved_memory_count"] == 1
    assert trace_path.exists()

    payload = json.loads(trace_path.read_text(encoding="utf-8").strip())
    assert payload["task_input"] == "Please create a Chinese summary."
    assert payload["memory_context"] == "The user prefers Chinese summaries."
    assert payload["final_answer"] == result.answer
    assert payload["tool_calls"]
