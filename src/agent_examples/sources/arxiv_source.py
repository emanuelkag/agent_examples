from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

from ..types import Document


def search_arxiv(query: str, max_results: int = 5, timeout_s: float = 8.0) -> list[Document]:
    try:
        import arxiv
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Install extras: uv sync --extra sources") from exc

    def _run() -> list[Document]:
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
        client = arxiv.Client(page_size=max_results, delay_seconds=0.0, num_retries=0)
        docs: list[Document] = []
        for result in client.results(search):
            text = result.summary or ""
            doc_id = f"arxiv:{result.entry_id}"
            docs.append(
                Document(
                    doc_id=doc_id,
                    title=result.title,
                    text=text,
                    source="arxiv",
                    source_url=result.entry_id,
                )
            )
        return docs

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_run)
        try:
            return future.result(timeout=timeout_s)
        except FutureTimeout:
            return []
