import asyncio
import sys
from typing import TypedDict

try:
    from langgraph.graph import StateGraph
except Exception as exc:
    raise SystemExit("Install extras: uv sync --extra langgraph") from exc

from agent_os_examples.router.router import run_routed_query


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
