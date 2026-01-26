from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os
import yaml

from .settings import Settings


@dataclass
class ModelSpec:
    name: str
    provider: str
    model: str
    base_url: str | None = None
    api_key: str | None = None


def _resolve_env(key: str | None) -> str | None:
    if not key:
        return None
    return os.getenv(key)


def load_registry(settings: Settings) -> dict[str, Any]:
    path = Path(settings.model_registry_path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def get_model_spec(settings: Settings, *, name: str | None, kind: str) -> ModelSpec:
    data = load_registry(settings)
    default_key = data.get("default_chat") if kind == "chat" else data.get("default_embed")
    model_name = name or default_key
    models = data.get("models") or {}
    entry = models.get(model_name, {})

    base_url = _resolve_env(entry.get("base_url_env")) or entry.get("base_url")
    api_key = _resolve_env(entry.get("api_key_env")) or entry.get("api_key")
    model = entry.get("model") or (settings.chat_model if kind == "chat" else settings.embed_model)
    provider = entry.get("provider", "openai_compat")

    return ModelSpec(
        name=model_name or "default",
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=api_key,
    )


def get_chat_model_spec(settings: Settings, name: str | None = None) -> ModelSpec:
    return get_model_spec(settings, name=name, kind="chat")


def get_embed_model_spec(settings: Settings, name: str | None = None) -> ModelSpec:
    return get_model_spec(settings, name=name, kind="embed")
