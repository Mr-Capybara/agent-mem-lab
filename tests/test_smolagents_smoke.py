from smolagents import ToolCallingAgent, tool
from smolagents.models import ChatMessage, MessageRole, Model


class FakeModel(Model):
    def generate(self, messages, **kwargs):
        return ChatMessage(role=MessageRole.ASSISTANT, content="final answer")


@tool
def add_numbers(left: int, right: int) -> int:
    """Add two integers.

    Args:
        left: First integer.
        right: Second integer.
    """

    return left + right


def test_tool_calling_agent_can_initialize_with_local_fake_model() -> None:
    agent = ToolCallingAgent(tools=[add_numbers], model=FakeModel(model_id="fake"), max_steps=1)

    assert agent.model.model_id == "fake"
    assert "add_numbers" in agent.tools
    assert agent.tools["add_numbers"].forward(2, 3) == 5
