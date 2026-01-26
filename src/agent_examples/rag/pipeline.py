from __future__ import annotations

from typing import Callable

from ..llm import build_agent
from ..telemetry import log_event
from ..types import RetrievalChunk
from .graph import fetch_graph_context, fetch_graph_context_for_query
from .retriever import retrieve


def _format_sources(chunks: list[RetrievalChunk]) -> list[str]:
    sources = []
    for chunk in chunks:
        label = chunk.source_url or chunk.source or "unknown"
        if label not in sources:
            sources.append(label)
    return sources


def _self_eval(chunks: list[RetrievalChunk]) -> bool:
    return len(chunks) >= 2


def _build_prompt(query: str, top_k: int) -> tuple[str | None, list[str]]:
    chunks = retrieve(query, top_k=top_k)
    sources = _format_sources(chunks)

    if not chunks:
        graph_context, graph_sources = fetch_graph_context_for_query(query)
        if not graph_context:
            return None, []
        context = "\n".join(f"- {g}" for g in graph_context[: top_k])
        prompt = (
            "Answer the question using only the provided context. "
            "Cite sources by name in the answer.\n\n"
            f"Question: {query}\n\nContext:\n{context}\n"
        )
        return prompt, graph_sources

    if not _self_eval(chunks):
        return None, sources

    doc_ids = [c.doc_id for c in chunks if c.doc_id]
    graph_context = fetch_graph_context(doc_ids)

    context_lines = [f"- {c.text}" for c in chunks[: top_k]]
    graph_lines = [f"- {g}" for g in graph_context[:5]]
    context = "\n".join(context_lines + ["", "Graph facts:"] + graph_lines)

    prompt = (
        "Answer the question using only the provided context. "
        "Cite sources by name in the answer.\n\n"
        f"Question: {query}\n\nContext:\n{context}\n"
    )
    return prompt, sources


def answer_query(query: str, top_k: int = 5) -> dict:
    prompt, sources = _build_prompt(query, top_k)
    if not prompt:
        if sources:
            return {"answer": "Insufficient coverage. Add more sources or widen retrieval.", "sources": sources}
        return {"answer": "No sources found in the local corpus.", "sources": []}

    agent = build_agent(system_prompt="You are a precise, source-grounded assistant.")
    result = agent.run_sync(prompt)

    log_event("rag_query", {"query": query, "sources": sources})
    return {"answer": result.output, "sources": sources}


async def answer_query_stream(
    query: str,
    top_k: int = 5,
    on_chunk: Callable[[str], None] | None = None,
) -> dict:
    prompt, sources = _build_prompt(query, top_k)
    if not prompt:
        if sources:
            return {"answer": "Insufficient coverage. Add more sources or widen retrieval.", "sources": sources}
        return {"answer": "No sources found in the local corpus.", "sources": []}

    agent = build_agent(system_prompt="You are a precise, source-grounded assistant.")
    async with agent.run_stream(prompt) as response:
        async for chunk in response.stream_text(delta=True):
            if on_chunk:
                on_chunk(chunk)
        output = await response.get_output()

    log_event("rag_query", {"query": query, "sources": sources})
    return {"answer": output, "sources": sources}
