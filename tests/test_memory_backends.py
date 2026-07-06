from agent_lab.memory import MemoryEvent, NoMemoryBackend, RawHistoryBackend


def test_no_memory_never_returns_results() -> None:
    backend = NoMemoryBackend()
    backend.add(MemoryEvent(content="用户喜欢中文摘要", memory_type="user_profile"))

    results = backend.search(
        "用户喜欢什么语言？",
        user_id="default_user",
        project_id="default_project",
    )

    assert results == []
    assert backend.export() == []


def test_raw_history_returns_matching_scoped_memory() -> None:
    backend = RawHistoryBackend()
    record = backend.add(
        MemoryEvent(
            content="project uses pytest for tests",
            memory_type="project_fact",
            user_id="u1",
            project_id="p1",
        )
    )
    backend.add(
        MemoryEvent(
            content="project uses npm for tests",
            memory_type="project_fact",
            user_id="u2",
            project_id="p1",
        )
    )

    results = backend.search("pytest tests", user_id="u1", project_id="p1")

    assert len(results) == 1
    assert results[0].record.id == record.id
