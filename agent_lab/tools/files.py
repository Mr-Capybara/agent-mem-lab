"""Controlled file helpers."""

from __future__ import annotations

from pathlib import Path


class WorkspaceFiles:
    """Read and write files under a configured workspace root."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

    def read_text(self, path: str | Path) -> str:
        target = self._resolve(path)
        return target.read_text(encoding="utf-8")

    def write_text(self, path: str | Path, content: str) -> None:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def _resolve(self, path: str | Path) -> Path:
        target = (self.root / path).resolve()
        if self.root != target and self.root not in target.parents:
            raise ValueError(f"Path escapes workspace root: {path}")
        return target
