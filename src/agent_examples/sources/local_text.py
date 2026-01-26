from __future__ import annotations

import hashlib
from pathlib import Path

from ..types import Document


def _doc_id_from_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_local_files(paths: list[str]) -> list[Document]:
    docs: list[Document] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for fp in path.rglob("*"):
                if fp.is_file():
                    docs.extend(load_local_files([str(fp)]))
            continue
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        doc_id = _doc_id_from_text(text)
        docs.append(
            Document(
                doc_id=doc_id,
                title=path.name,
                text=text,
                source="local_text",
                source_url=str(path),
            )
        )
    return docs
