import asyncio
import sys

from agent_examples.agents.multi_agent import run, run_async

query = "Create a short plan and answer for setting up a local agent stack."
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    print(await run_async(query))


asyncio.run(main())

# Sync variant (uncomment to use)
# print(run(query))

# Streaming variant (final writer step only; uncomment to demo)
# import asyncio
# from agent_examples.llm import build_agent
#
# async def stream_writer() -> None:
#     planner = build_agent(system_prompt="You are a project manager. Create a short plan.")
#     researcher = build_agent(system_prompt="You are a researcher. Provide evidence bullets.")
#     writer = build_agent(system_prompt="You are a writer. Produce a concise answer.")
#     plan = (await planner.run(query)).output
#     evidence = (await researcher.run(f"Question: {query}\nPlan: {plan}")).output
#     prompt = f"Question: {query}\nPlan: {plan}\nEvidence: {evidence}"
#     async with writer.run_stream(prompt) as response:
#         async for chunk in response.stream_text(delta=True):
#             print(chunk, end="", flush=True)
#         print()
#         print(await response.get_output())
#
# asyncio.run(stream_writer())
