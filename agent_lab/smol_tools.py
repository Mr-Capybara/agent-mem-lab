"""smolagents tool adapters used by AgentRunner."""

from __future__ import annotations

from smolagents import Tool

from agent_lab.tools.calculator import calculate


class CalculatorTool(Tool):
    name = "calculate"
    description = "Evaluate a basic arithmetic expression and return a numeric result."
    inputs = {
        "expression": {
            "type": "string",
            "description": "Arithmetic expression using numbers and +, -, *, /, ** operators.",
        }
    }
    output_type = "number"

    def forward(self, expression: str) -> float:
        return calculate(expression)
