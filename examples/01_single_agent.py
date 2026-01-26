from agent_examples.agents.single import run

print(run("Give a 3-bullet summary of what an AI Act compliance checklist should include."))

# Async streaming variant (uncomment to demo token streaming)
# import asyncio
# from agent_examples.llm import build_agent
#
# async def main() -> None:
#     agent = build_agent(system_prompt="You are a helpful local assistant.")
#     async with agent.run_stream(
#         "Give a 3-bullet summary of what an AI Act compliance checklist should include."
#     ) as response:
#         async for chunk in response.stream_text(delta=True):
#             print(chunk, end="", flush=True)
#         print()
#         full_output = await response.get_output()
#         print(full_output)
#
# asyncio.run(main())
