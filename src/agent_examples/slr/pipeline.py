from __future__ import annotations

from ..ingest.pipeline import ingest_documents
from ..llm import build_agent
from ..telemetry import log_event
from ..types import Document
from ..sources.arxiv_source import search_arxiv
from ..sources.web_search import search_web
from ..sources.wikipedia_source import fetch_wikipedia_summary


def run_slr(question: str, max_results: int = 5) -> dict:
    docs: list[Document] = []
    docs.extend(search_web(question, max_results=max_results))
    docs.extend(search_arxiv(question, max_results=max_results))
    docs.extend(fetch_wikipedia_summary(question))

    ingest = ingest_documents(docs)

    titles = "\n".join(f"- {d.title}" for d in docs[:10])
    prompt = (
        "You are running a lightweight systematic review. "
        "Summarize the key themes from these sources:\n" + titles
    )
    agent = build_agent(system_prompt="You are a rigorous research synthesizer.")
    result = agent.run_sync(prompt)

    log_event("slr_run", {"question": question, "count": ingest.get("ingested", 0)})
    return {
        "question": question,
        "docs_ingested": ingest.get("ingested", 0),
        "summary": result.output,
    }
