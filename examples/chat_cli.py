from __future__ import annotations

import asyncio

from agent_examples.llm import build_agent
from agent_examples.rag.pipeline import answer_query_stream
from agent_examples.router.router import route_query
from agent_examples.slr.pipeline import run_slr_stream


def _print_help() -> None:
    print(
        "\nCommands:\n"
        "  /slr <question>    Run SLR (ingest + summary)\n"
        "  /rag <question>    Run RAG only (vector + graph)\n"
        "  /route <question>  Use router (direct|rag|slr)\n"
        "  /exit              Quit\n"
    )


async def _stream_direct(query: str) -> str:
    agent = build_agent(system_prompt="Answer clearly and concisely.")
    async with agent.run_stream(query) as response:
        async for chunk in response.stream_text(delta=True):
            print(chunk, end="", flush=True)
        print()
        return await response.get_output()


def _print_chunk(chunk: str) -> None:
    print(chunk, end="", flush=True)


def _print_sources(result: dict) -> None:
    sources = result.get("sources") if isinstance(result, dict) else None
    if not sources:
        return
    print("\nSources:")
    for source in sources:
        print(f"- {source}")


async def _handle_query(query: str, mode: str) -> None:
    if mode == "slr":
        result = await run_slr_stream(query, on_chunk=_print_chunk)
        _print_sources(result)
        return
    if mode == "rag":
        result = await answer_query_stream(query, on_chunk=_print_chunk)
        _print_sources(result)
        return
    if mode == "route":
        route = route_query(query)
        if route == "direct":
            await _stream_direct(query)
        else:
            if route == "slr":
                result = await run_slr_stream(query, on_chunk=_print_chunk)
            else:
                result = await answer_query_stream(query, on_chunk=_print_chunk)
            _print_sources(result)
        return
    await _stream_direct(query)


def main() -> None:
    try:
        import sys

        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("Agent Examples Chat CLI")
    _print_help()
    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return

        if not text:
            continue
        if text in {"/exit", "/quit"}:
            print("Bye.")
            return
        if text == "/help":
            _print_help()
            continue

        if text.startswith("/slr "):
            query = text[5:].strip()
            if not query:
                print("Provide a question after /slr.")
                continue
            asyncio.run(_handle_query(query, "slr"))
            continue

        if text.startswith("/rag "):
            query = text[5:].strip()
            if not query:
                print("Provide a question after /rag.")
                continue
            asyncio.run(_handle_query(query, "rag"))
            continue

        if text.startswith("/route "):
            query = text[7:].strip()
            if not query:
                print("Provide a question after /route.")
                continue
            asyncio.run(_handle_query(query, "route"))
            continue

        asyncio.run(_handle_query(text, "direct"))


if __name__ == "__main__":
    main()
