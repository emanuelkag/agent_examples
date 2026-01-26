from __future__ import annotations

import asyncio

from ..rag.pipeline import answer_query
from ..llm import build_agent


def run(question: str) -> str:
    # FSM: intake -> retrieve -> verify -> compose
    intake = question.strip()
    retrieved = answer_query(intake)
    if retrieved.get("answer", "").startswith("Insufficient"):
        return retrieved["answer"]

    verifier = build_agent(system_prompt="Verify that the answer cites sources.")
    verification = verifier.run_sync(retrieved["answer"]).output

    composer = build_agent(system_prompt="Compose the final response with citations.")
    final = composer.run_sync(
        f"Question: {question}\nDraft: {retrieved['answer']}\nVerification: {verification}"
    ).output
    return final


async def run_async(question: str) -> str:
    intake = question.strip()
    retrieved = await asyncio.to_thread(answer_query, intake)
    if retrieved.get("answer", "").startswith("Insufficient"):
        return retrieved["answer"]

    verifier = build_agent(system_prompt="Verify that the answer cites sources.")
    verification = (await verifier.run(retrieved["answer"])).output

    composer = build_agent(system_prompt="Compose the final response with citations.")
    final = (
        await composer.run(
            f"Question: {question}\nDraft: {retrieved['answer']}\nVerification: {verification}"
        )
    ).output
    return final
