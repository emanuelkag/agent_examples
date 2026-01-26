from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_examples.llm import build_agent


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    query = "Give a 3-bullet summary of what an AI Act compliance checklist should include."
    agent = build_agent(system_prompt="You are a helpful local assistant.")

    async def run_stream() -> str:
        async with agent.run_stream(query) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)
            print()
            return await response.get_output()

    import asyncio

    output = asyncio.run(run_stream())

    out_path = Path("outputs") / f"streaming_test_run_{datetime.now(timezone.utc):%Y-%m-%d}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path.write_text(
        "\n".join(
            [
                f"# Streaming Test Run ({stamp})",
                "",
                "## Query",
                query,
                "",
                "## Answer",
                output,
                "",
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
