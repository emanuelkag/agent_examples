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
from agent_examples.agents.single import run_async as single_run_async
from agent_examples.router.router import run_routed_query_async
from agent_examples.sources.web_search import search_web


async def _with_timeout(coro, timeout_s: float, label: str) -> str:
    try:
        return await asyncio.wait_for(coro, timeout=timeout_s)
    except Exception as exc:
        return f"(error: {label}) {exc}"


async def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path = ROOT / "outputs" / f"all_examples_run_{datetime.now(timezone.utc):%Y-%m-%d}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sections: list[str] = [f"# All Examples Run ({stamp})", ""]

    # 01 Single Agent
    q1 = "Give a 3-bullet summary of what an AI Act compliance checklist should include."
    a1 = await _with_timeout(single_run_async(q1), 20, "single_agent")
    sections += ["## 01 Single Agent", "", "### Query", q1, "", "### Answer", a1, ""]

    # 02 Tool Use (Web)
    q2 = "EU AI Act high-risk obligations"
    results = await asyncio.to_thread(search_web, q2, max_results=3, timeout_s=5)
    lines = [f"- {d.title} ({d.source_url})" for d in results]
    sections += ["## 02 Tool Use (Web Search)", "", "### Query", q2, "", "### Answer", "\n".join(lines) or "(no results)", ""]

    # 03 Router (RAG/SLR)
    q3 = "Run a systematic review on RAG evaluation methods."
    r3 = await _with_timeout(run_routed_query_async(q3), 30, "router_rag_slr")
    sections += ["## 03 Router (RAG/SLR)", "", "### Query", q3, "", "### Answer", str(r3), ""]

    # 04 FSM Agent
    q4 = "What are the core steps in a compliance-ready RAG pipeline?"
    a4 = await _with_timeout(fsm_run_async(q4), 20, "fsm_agent")
    sections += ["## 04 FSM Agent", "", "### Query", q4, "", "### Answer", a4, ""]

    # 05 Multi-Agent
    q5 = "Create a short plan and answer for setting up a local agent stack."
    a5 = await _with_timeout(multi_run_async(q5), 30, "multi_agent")
    sections += ["## 05 Multi-Agent", "", "### Query", q5, "", "### Answer", a5, ""]

    # 06 LangGraph Flow (reuse example script in a subprocess)
    q6 = "Summarize recent work on agent routing."
    try:
        import subprocess

        proc = subprocess.run(
            [sys.executable, "examples/06_langgraph_flow.py"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=30,
        )
        r6 = (proc.stdout or proc.stderr).strip()
    except Exception as exc:
        r6 = f"(langgraph error) {exc}"
    sections += ["## 06 LangGraph Flow", "", "### Query", q6, "", "### Answer", str(r6), ""]

    out_path.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
