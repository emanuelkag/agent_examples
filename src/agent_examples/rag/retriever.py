from __future__ import annotations

from qdrant_client import QdrantClient

from ..embeddings import embed_texts
from ..settings import Settings
from ..types import RetrievalChunk


def retrieve(query: str, top_k: int = 5, settings: Settings | None = None) -> list[RetrievalChunk]:
    settings = settings or Settings()
    qdrant = QdrantClient(url=settings.qdrant_url, check_compatibility=False)

    try:
        qdrant.get_collection(settings.qdrant_collection)
    except Exception:
        return []

    vector = embed_texts([query], settings=settings)[0]
    try:
        response = qdrant.query_points(
            collection_name=settings.qdrant_collection,
            query=vector,
            limit=top_k,
        )
    except Exception:
        return []
    hits = response.points
    results: list[RetrievalChunk] = []
    for hit in hits:
        payload = hit.payload or {}
        results.append(
            RetrievalChunk(
                text=payload.get("text", ""),
                source=payload.get("source", ""),
                source_url=payload.get("source_url"),
                score=float(hit.score),
                doc_id=payload.get("doc_id", ""),
            )
        )
    return results
