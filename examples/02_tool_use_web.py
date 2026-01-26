import asyncio
import sys

from agent_examples.sources.web_search import search_web

query = "EU AI Act high-risk obligations"
sys.stdout.reconfigure(encoding="utf-8")

# Async variant (default)
async def main() -> None:
    results = await asyncio.to_thread(search_web, query, max_results=3)
    for doc in results:
        print(f"- {doc.title} ({doc.source_url})")


asyncio.run(main())

# Sync variant (uncomment to use)
# results = search_web(query, max_results=3)
# for doc in results:
#     print(f"- {doc.title} ({doc.source_url})")
