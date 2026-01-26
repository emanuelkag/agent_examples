import asyncio
import sys

from agent_os_examples.agents.multi_agent import run, run_async

query = "Create a short plan and answer for setting up a local agent stack."
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    print(await run_async(query))


asyncio.run(main())

# Sync variant (uncomment to use)
# print(run(query))
