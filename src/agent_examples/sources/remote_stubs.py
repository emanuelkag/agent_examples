from __future__ import annotations

from ..types import Document


def fetch_confluence(_: str) -> list[Document]:
    raise NotImplementedError("Confluence adapter stub. Provide base_url and token.")


def fetch_ms_graph(_: str) -> list[Document]:
    raise NotImplementedError("MS Graph adapter stub. Provide token.")


def fetch_google_drive(_: str) -> list[Document]:
    raise NotImplementedError("Google Drive adapter stub. Provide token.")
