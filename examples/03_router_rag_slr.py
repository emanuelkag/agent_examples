import asyncio
import sys

from agent_examples.router.router import run_routed_query, run_routed_query_async

query = "Run a systematic review on RAG evaluation methods."
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    result = await run_routed_query_async(query)
    print(result)


asyncio.run(main())

# Sync variant (uncomment to use)
# result = run_routed_query(query)
# print(result)

# Streaming variant (only for direct LLM path; uncomment to demo)
# import asyncio
# from agent_examples.llm import build_agent
#
# async def stream_direct() -> None:
#     agent = build_agent(system_prompt="Answer clearly and concisely.")
#     async with agent.run_stream(query) as response:
#         async for chunk in response.stream_text(delta=True):
#             print(chunk, end="", flush=True)
#         print()
#         print(await response.get_output())
#
# asyncio.run(stream_direct())
