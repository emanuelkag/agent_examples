from __future__ import annotations

import hashlib
import uuid
from typing import Iterable

from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from ..embeddings import embed_texts
from ..settings import Settings
from ..telemetry import log_event
from ..types import Document


def chunk_text(text: str, max_chars: int = 800, overlap: int = 100) -> list[str]:
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def _split_sentences(text: str, max_sentences: int = 20) -> list[str]:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    return sentences[:max_sentences]


def _ensure_collection(client: QdrantClient, name: str, vector_size: int) -> None:
    try:
        info = client.get_collection(name)
        existing = getattr(info.config.params.vectors, "size", None)
        if existing and existing != vector_size:
            raise ValueError(f"Qdrant collection size mismatch: {existing} != {vector_size}")
    except Exception:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def _upsert_graph(doc: Document, sentences: Iterable[str], settings: Settings) -> None:
    subject_key = f"doc:{doc.doc_id}"
    with GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password.get_secret_value()),
    ) as driver:
        with driver.session() as session:
            session.run(
                "MERGE (d:SourceDoc {doc_id: $doc_id}) "
                "SET d.title = $title, d.source = $source, d.url = $url",
                {
                    "doc_id": doc.doc_id,
                    "title": doc.title,
                    "source": doc.source,
                    "url": doc.source_url,
                },
            )
            session.run(
                "MERGE (s:Entity {key: $key}) SET s.label = $label",
                {"key": subject_key, "label": doc.title},
            )
            for sent in sentences:
                claim_id = hashlib.sha256(f"{subject_key}:{sent}".encode("utf-8")).hexdigest()
                session.run(
                    "MERGE (c:Claim {claim_id: $claim_id}) "
                    "SET c.text = $text, c.doc_id = $doc_id "
                    "MERGE (s:Entity {key: $subject_key}) "
                    "MERGE (s)-[:SUBJECT_OF]->(c) "
                    "MERGE (c)-[:EVIDENCED_BY]->(d)",
                    {
                        "claim_id": claim_id,
                        "text": sent,
                        "doc_id": doc.doc_id,
                        "subject_key": subject_key,
                    },
                )


def ingest_documents(docs: list[Document], settings: Settings | None = None) -> dict:
    settings = settings or Settings()
    qdrant = QdrantClient(url=settings.qdrant_url)

    ingested = 0
    for doc in docs:
        chunks = chunk_text(doc.text)
        if not chunks:
            continue
        embeddings = embed_texts(chunks, settings=settings)
        _ensure_collection(qdrant, settings.qdrant_collection, len(embeddings[0]))

        points = []
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings, strict=False)):
            payload = {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "source": doc.source,
                "source_url": doc.source_url,
                "chunk_index": idx,
                "text": chunk,
            }
            points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload))

        qdrant.upsert(collection_name=settings.qdrant_collection, points=points)
        _upsert_graph(doc, _split_sentences(doc.text), settings)
        ingested += 1

    log_event("ingest", {"count": ingested})
    return {"ingested": ingested}
