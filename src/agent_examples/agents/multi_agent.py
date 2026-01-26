from __future__ import annotations

from ..llm import build_agent


def run(question: str) -> str:
    planner = build_agent(system_prompt="You are a project manager. Create a short plan.")
    researcher = build_agent(system_prompt="You are a researcher. Provide evidence bullets.")
    writer = build_agent(system_prompt="You are a writer. Produce a concise answer.")

    plan = planner.run_sync(question).output
    evidence = researcher.run_sync(f"Question: {question}\nPlan: {plan}").output
    final = writer.run_sync(f"Question: {question}\nPlan: {plan}\nEvidence: {evidence}").output
    return final


async def run_async(question: str) -> str:
    planner = build_agent(system_prompt="You are a project manager. Create a short plan.")
    researcher = build_agent(system_prompt="You are a researcher. Provide evidence bullets.")
    writer = build_agent(system_prompt="You are a writer. Produce a concise answer.")

    plan = (await planner.run(question)).output
    evidence = (await researcher.run(f"Question: {question}\nPlan: {plan}")).output
    final = (await writer.run(f"Question: {question}\nPlan: {plan}\nEvidence: {evidence}")).output
    return final
