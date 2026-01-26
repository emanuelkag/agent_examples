from __future__ import annotations

from ..llm import build_agent


def run(prompt: str) -> str:
    agent = build_agent(system_prompt="You are a helpful local assistant.")
    result = agent.run_sync(prompt)
    return result.output


async def run_async(prompt: str) -> str:
    agent = build_agent(system_prompt="You are a helpful local assistant.")
    result = await agent.run(prompt)
    return result.output
