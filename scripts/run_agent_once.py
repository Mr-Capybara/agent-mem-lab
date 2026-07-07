"""Run one AgentRunner task from the command line."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

from agent_lab.agent_runner import AgentRunner  # noqa: E402
from agent_lab.memory import NoMemoryBackend  # noqa: E402
from agent_lab.model_factory import create_model_from_env  # noqa: E402


def main() -> None:
    load_dotenv()
    os.environ.setdefault("MEM0_DIR", ".local/mem0")

    parser = argparse.ArgumentParser(description="Run one agent task.")
    parser.add_argument("task", nargs="?", default="请用一句话介绍太阳系。")
    parser.add_argument(
        "--provider",
        default=os.environ.get("AGENT_MODEL_PROVIDER", "offline"),
        choices=["offline", "wq_openai_compatible", "openai_compatible"],
    )
    parser.add_argument("--trace", default="traces/manual_run.jsonl")
    args = parser.parse_args()

    model = create_model_from_env(args.provider)
    runner = AgentRunner(
        memory=NoMemoryBackend(),
        model=model,
        trace_path=Path(args.trace),
        max_steps=4,
    )
    result = runner.run(args.task, session_id="manual")
    print(result.answer)
    print(f"trace_id={result.trace.trace_id}")


if __name__ == "__main__":
    main()
