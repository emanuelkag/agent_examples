import asyncio
import sys

from agent_os_examples.router.router import run_routed_query, run_routed_query_async

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
