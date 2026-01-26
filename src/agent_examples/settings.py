from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: SecretStr | None = Field(default=None)
    openai_base_url: str = "https://api.openai.com/v1"
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_api_base: str = "http://localhost:11434"

    chat_model: str = "llama3.1:8b"
    embed_model: str = "nomic-embed-text"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "agent_os_docs"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: SecretStr = SecretStr("neo4jpass")

    postgres_dsn: str = "postgresql://agentos:agentos@localhost:5432/agentos"

    telemetry_path: str = "outputs/telemetry.jsonl"
    model_registry_path: str = "configs/model_registry.yaml"
    source_registry_path: str = "configs/source_registry.yaml"

    router_use_llm: bool = True
    model_timeout_s: float | None = 60.0
