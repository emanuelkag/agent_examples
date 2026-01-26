import asyncio
import sys
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    from langgraph.graph import StateGraph
except Exception as exc:
    raise SystemExit("Install extras: uv sync --extra langgraph") from exc

from agent_examples.router.router import run_routed_query


class State(TypedDict):
    query: str
    result: dict


def router_node(state: State) -> State:
    return {"query": state["query"], "result": run_routed_query(state["query"])}


graph = StateGraph(State)
graph.add_node("router", router_node)
graph.set_entry_point("router")
graph.set_finish_point("router")
app = graph.compile()

query = "Summarize recent work on agent routing."
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    result = await asyncio.to_thread(app.invoke, {"query": query})
    print(result)


asyncio.run(main())

# Sync variant (uncomment to use)
# print(app.invoke({"query": query}))

# Streaming variant (direct LLM path only; uncomment to demo)
# import asyncio
# from agent_examples.llm import build_agent
#
# async def stream_direct() -> None:
#     agent = build_agent(system_prompt="Answer clearly and concisely.")
#     async with agent.run_stream(query) as response:
#         async for chunk in response.stream_text(delta=True):
#             print(chunk, end="", flush=True)
#         print()
#         print(await response.get_output())
#
# asyncio.run(stream_direct())
