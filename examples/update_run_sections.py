from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_examples.agents.fsm import run_async as fsm_run_async
from agent_examples.agents.multi_agent import run_async as multi_run_async


def _replace_section(text: str, header: str, new_block: str) -> str:
    start = text.find(header)
    if start == -1:
        return text + "\n\n" + new_block
    next_header = text.find("\n## ", start + len(header))
    if next_header == -1:
        return text[:start] + new_block
    return text[:start] + new_block + text[next_header:]


async def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    out_path = ROOT / "outputs" / f"all_examples_run_{datetime.now(timezone.utc):%Y-%m-%d}.md"
    if not out_path.exists():
        raise SystemExit(f"missing output file: {out_path}")

    text = out_path.read_text(encoding="utf-8")

    q4 = "What are the core steps in a compliance-ready RAG pipeline?"
    a4 = await fsm_run_async(q4)
    fsm_block = "\n".join(
        [
            "## 04 FSM Agent",
            "",
            "### Query",
            q4,
            "",
            "### Answer",
            a4,
            "",
        ]
    )

    q5 = "Create a short plan and answer for setting up a local agent stack."
    a5 = await multi_run_async(q5)
    multi_block = "\n".join(
        [
            "## 05 Multi-Agent",
            "",
            "### Query",
            q5,
            "",
            "### Answer",
            a5,
            "",
        ]
    )

    text = _replace_section(text, "## 04 FSM Agent", fsm_block)
    text = _replace_section(text, "## 05 Multi-Agent", multi_block)

    out_path.write_text(text, encoding="utf-8")
    print(f"Updated {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
