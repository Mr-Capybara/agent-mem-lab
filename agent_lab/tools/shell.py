"""Placeholder for controlled shell execution."""

from __future__ import annotations


class ControlledShell:
    """Shell tool placeholder.

    A real implementation must enforce PROJECT_RULES.md before it can be
    enabled for an agent.
    """

    def run(self, command: str) -> str:
        raise NotImplementedError("Controlled shell is disabled until safety rules are implemented.")
