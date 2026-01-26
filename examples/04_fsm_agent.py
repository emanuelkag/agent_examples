import asyncio
import sys

from agent_os_examples.agents.fsm import run, run_async

query = "What are the core steps in a compliance-ready RAG pipeline?"
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    print(await run_async(query))


asyncio.run(main())

# Sync variant (uncomment to use)
# print(run(query))
