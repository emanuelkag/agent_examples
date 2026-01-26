# Agent OS Examples (PydanticAI)

Local-first agent architecture examples for the Oikos workshop.
Focus: deterministic ingest -> vector + graph -> RAG + SLR -> router patterns.
All runs log to outputs/telemetry.jsonl.

## Requirements
- Docker Desktop (with docker compose)
- Ollama
- Python >= 3.11
- uv (recommended)
- Optional: OPENAI_API_KEY for cloud models

## Quickstart
1) docker compose up -d
2) ollama pull llama3.1:8b
3) ollama pull nomic-embed-text
4) uv sync --extra sources --extra langgraph
5) copy .env.example -> .env
6) uv run python examples/01_single_agent.py
7) uv run uvicorn agent_examples.api:app --reload

## Example scripts
- examples/01_single_agent.py: single agent chat (local Ollama)
- examples/02_tool_use_web.py: tool calling with web/wiki sources
- examples/03_router_rag_slr.py: router chooses direct vs RAG vs SLR
- examples/04_fsm_agent.py: deterministic FSM (intake -> retrieve -> verify -> compose)
- examples/05_multi_agent.py: manager/worker roles
- examples/06_langgraph_flow.py: LangGraph flow (requires langgraph extra)

## Architecture sketch
Sources -> Registry/Adapters -> Normalize/Chunk -> Embeddings -> Qdrant
Graph extraction -> Neo4j
Retriever (vector + graph) -> Self-eval gate -> Composer
SLR endpoint ingests external sources and stores into vector + graph
