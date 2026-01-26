from __future__ import annotations

from ..llm import build_agent
from ..settings import Settings
from ..slr.pipeline import run_slr
from ..rag.pipeline import answer_query
from ..telemetry import log_event


def _heuristic_route(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["systematic", "slr", "literature", "survey", "meta-analysis", "arxiv", "paper", "research"]):
        return "slr"
    if any(k in q for k in ["internal", "korpus", "knowledge base", "our docs", "company"]):
        return "rag"
    return "direct"


def _llm_route(query: str) -> str:
    agent = build_agent(system_prompt="Classify the query as: direct, rag, or slr.")
    prompt = f"Query: {query}\nAnswer with one token: direct|rag|slr"
    result = agent.run_sync(prompt)
    text = str(result.output).strip().lower()
    if "slr" in text:
        return "slr"
    if "rag" in text:
        return "rag"
    return "direct"


async def _llm_route_async(query: str) -> str:
    agent = build_agent(system_prompt="Classify the query as: direct, rag, or slr.")
    prompt = f"Query: {query}\nAnswer with one token: direct|rag|slr"
    result = await agent.run(prompt)
    text = str(result.output).strip().lower()
    if "slr" in text:
        return "slr"
    if "rag" in text:
        return "rag"
    return "direct"


def route_query(query: str) -> str:
    settings = Settings()
    if settings.router_use_llm:
        return _llm_route(query)
    return _heuristic_route(query)


async def route_query_async(query: str) -> str:
    settings = Settings()
    if settings.router_use_llm:
        return await _llm_route_async(query)
    return _heuristic_route(query)


def run_routed_query(query: str) -> dict:
    route = route_query(query)
    if route == "slr":
        result = run_slr(query)
    elif route == "rag":
        result = answer_query(query)
    else:
        agent = build_agent(system_prompt="Answer clearly and concisely.")
        result = {"answer": agent.run_sync(query).output, "sources": []}

    log_event("router", {"query": query, "route": route})
    result["route"] = route
    return result


async def run_routed_query_async(query: str) -> dict:
    route = await route_query_async(query)
    if route == "slr":
        result = await _run_async_slr(query)
    elif route == "rag":
        result = await _run_async_rag(query)
    else:
        agent = build_agent(system_prompt="Answer clearly and concisely.")
        result = {"answer": (await agent.run(query)).output, "sources": []}

    log_event("router", {"query": query, "route": route})
    result["route"] = route
    return result


async def _run_async_slr(query: str) -> dict:
    from asyncio import to_thread

    return await to_thread(run_slr, query)


async def _run_async_rag(query: str) -> dict:
    from asyncio import to_thread

    return await to_thread(answer_query, query)
