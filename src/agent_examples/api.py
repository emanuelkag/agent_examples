from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .rag.pipeline import answer_query
from .slr.pipeline import run_slr
from .router.router import run_routed_query

app = FastAPI(title="Agent OS Examples")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/rag/query")
def rag_query(req: QueryRequest) -> dict:
    return answer_query(req.query, top_k=req.top_k)


@app.post("/slr/run")
def slr_run(req: QueryRequest) -> dict:
    return run_slr(req.query, max_results=req.top_k)


@app.post("/router")
def router(req: QueryRequest) -> dict:
    return run_routed_query(req.query)
