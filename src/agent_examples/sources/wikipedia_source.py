from __future__ import annotations

from ..types import Document


def fetch_wikipedia_summary(topic: str, lang: str = "en") -> list[Document]:
    try:
        import wikipedia
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Install extras: uv sync --extra sources") from exc

    wikipedia.set_lang(lang)
    try:
        summary = wikipedia.summary(topic, sentences=5)
        page = wikipedia.page(topic)
    except Exception:
        return []
    doc_id = f"wikipedia:{page.pageid}"
    return [
        Document(
            doc_id=doc_id,
            title=page.title,
            text=summary,
            source="wikipedia",
            source_url=page.url,
        )
    ]
