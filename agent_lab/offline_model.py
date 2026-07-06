"""Offline model for deterministic local smoke tests."""

from __future__ import annotations

from smolagents.models import (
    ChatMessage,
    ChatMessageToolCall,
    ChatMessageToolCallFunction,
    MessageRole,
    Model,
)


class OfflineFinalAnswerModel(Model):
    """A deterministic model that returns the prompt through final_answer.

    This model is intentionally simple. It exercises the real smolagents
    ToolCallingAgent loop without requiring an external LLM endpoint.
    """

    def generate(self, messages, **kwargs):  # type: ignore[no-untyped-def]
        task_text = _extract_latest_user_text(messages)
        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content="offline final answer",
            tool_calls=[
                ChatMessageToolCall(
                    id="offline-final-answer",
                    type="function",
                    function=ChatMessageToolCallFunction(
                        name="final_answer",
                        arguments={"answer": f"offline: {task_text}"},
                    ),
                )
            ],
        )


def _extract_latest_user_text(messages) -> str:  # type: ignore[no-untyped-def]
    for message in reversed(messages):
        role = _get_value(message, "role")
        if str(role).lower().endswith("user"):
            content = _get_value(message, "content")
            return _content_to_text(content)
    return ""


def _get_value(message, key: str):  # type: ignore[no-untyped-def]
    if isinstance(message, dict):
        return message.get(key)
    return getattr(message, key, None)


def _content_to_text(content) -> str:  # type: ignore[no-untyped-def]
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
                elif "text" in item:
                    parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content or "")
