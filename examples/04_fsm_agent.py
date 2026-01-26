import asyncio
import sys

from agent_examples.agents.fsm import run, run_async

query = "What are the core steps in a compliance-ready RAG pipeline?"
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    print(await run_async(query))


asyncio.run(main())

# Sync variant (uncomment to use)
# print(run(query))

# Streaming variant (final compose step only; uncomment to demo)
# import asyncio
# from agent_examples.llm import build_agent
# from agent_examples.rag.pipeline import answer_query
#
# async def stream_compose() -> None:
#     retrieved = await asyncio.to_thread(answer_query, query)
#     if retrieved.get("answer", "").startswith("Insufficient"):
#         print(retrieved["answer"])
#         return
#     verifier = build_agent(system_prompt="Verify that the answer cites sources.")
#     verification = (await verifier.run(retrieved["answer"])).output
#     composer = build_agent(system_prompt="Compose the final response with citations.")
#     prompt = f"Question: {query}\nDraft: {retrieved['answer']}\nVerification: {verification}"
#     async with composer.run_stream(prompt) as response:
#         async for chunk in response.stream_text(delta=True):
#             print(chunk, end="", flush=True)
#         print()
#         print(await response.get_output())
#
# asyncio.run(stream_compose())
