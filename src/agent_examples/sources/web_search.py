from __future__ import annotations

from ..types import Document


def search_web(query: str, max_results: int = 5, timeout_s: int = 5) -> list[Document]:
    try:
        from ddgs import DDGS
        from ddgs.exceptions import DDGSException, TimeoutException
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Install extras: uv sync --extra sources") from exc

    docs: list[Document] = []
    try:
        with DDGS(timeout=timeout_s) as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                title = item.get("title") or "web"
                snippet = item.get("body") or ""
                url = item.get("href")
                doc_id = f"web:{abs(hash(url or title))}"
                docs.append(
                    Document(
                        doc_id=doc_id,
                        title=title,
                        text=snippet,
                        source="web_search",
                        source_url=url,
                    )
                )
    except (DDGSException, TimeoutException):
        return []
    return docs
