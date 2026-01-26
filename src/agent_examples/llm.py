from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from .model_registry import get_chat_model_spec
from .settings import Settings


def build_agent(system_prompt: str | None = None) -> Agent:
    settings = Settings()
    spec = get_chat_model_spec(settings)

    if spec.provider == "openai":
        base_url = spec.base_url or settings.openai_base_url
        api_key = spec.api_key or (settings.openai_api_key.get_secret_value() if settings.openai_api_key else None)
    else:
        base_url = spec.base_url or settings.ollama_base_url
        api_key = spec.api_key or "ollama"

    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    model = OpenAIChatModel(spec.model, provider=provider)
    model_settings = {"timeout": settings.model_timeout_s} if settings.model_timeout_s else None
    return (
        Agent(model, system_prompt=system_prompt, model_settings=model_settings)
        if system_prompt
        else Agent(model, model_settings=model_settings)
    )
