from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    doc_id: str
    title: str
    text: str
    source: str
    source_url: str | None = None
    meta: dict[str, Any] | None = None


@dataclass
class RetrievalChunk:
    text: str
    source: str
    source_url: str | None
    score: float
    doc_id: str
