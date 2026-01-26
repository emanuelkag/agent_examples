from __future__ import annotations

from ..router.router import run_routed_query


def run(question: str) -> dict:
    return run_routed_query(question)
