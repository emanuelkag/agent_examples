from __future__ import annotations

from typing import Iterable
import httpx

from .model_registry import get_embed_model_spec
from .settings import Settings


def embed_texts(texts: list[str], settings: Settings | None = None) -> list[list[float]]:
    settings = settings or Settings()
    spec = get_embed_model_spec(settings)

    if spec.provider == "ollama_embed":
        return _ollama_embed(texts, settings, spec.model, spec.base_url)

    return _openai_embed(texts, settings, spec.model, spec.base_url, spec.api_key)


def _ollama_embed(texts: Iterable[str], settings: Settings, model: str, base_url: str | None) -> list[list[float]]:
    api_base = base_url or settings.ollama_api_base
    url = api_base.rstrip("/") + "/api/embeddings"
    out: list[list[float]] = []
    with httpx.Client(timeout=30) as client:
        for text in texts:
            payload = {"model": model, "prompt": text}
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            out.append(data["embedding"])
    return out


def _openai_embed(
    texts: list[str],
    settings: Settings,
    model: str,
    base_url: str | None,
    api_key: str | None,
) -> list[list[float]]:
    url = (base_url or settings.openai_base_url).rstrip("/") + "/embeddings"
    key = api_key or (settings.openai_api_key.get_secret_value() if settings.openai_api_key else None)
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    payload = {"model": model, "input": texts}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return [item["embedding"] for item in data.get("data", [])]
