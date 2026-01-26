from __future__ import annotations

from neo4j import GraphDatabase

from ..settings import Settings


def fetch_graph_context(doc_ids: list[str], settings: Settings | None = None, limit_per_doc: int = 3) -> list[str]:
    settings = settings or Settings()
    out: list[str] = []
    with GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password.get_secret_value()),
    ) as driver:
        with driver.session() as session:
            for doc_id in doc_ids:
                rows = session.run(
                    "MATCH (c:Claim)-[:EVIDENCED_BY]->(d:SourceDoc {doc_id: $doc_id}) "
                    "RETURN c.text AS text LIMIT $limit",
                    {"doc_id": doc_id, "limit": limit_per_doc},
                )
                for row in rows:
                    out.append(row.get("text"))
    return out


def fetch_graph_context_for_query(
    query: str,
    settings: Settings | None = None,
    limit: int = 5,
) -> tuple[list[str], list[str]]:
    settings = settings or Settings()
    facts: list[str] = []
    sources: list[str] = []
    with GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password.get_secret_value()),
    ) as driver:
        with driver.session() as session:
            rows = session.run(
                "MATCH (c:Claim)-[:EVIDENCED_BY]->(d:SourceDoc) "
                "WHERE toLower(c.text) CONTAINS toLower($query) "
                "RETURN c.text AS text, d.title AS title, d.url AS url "
                "LIMIT $limit",
                {"query": query, "limit": limit},
            )
            for row in rows:
                text = row.get("text")
                if text:
                    facts.append(text)
                label = row.get("title") or row.get("url")
                if label and label not in sources:
                    sources.append(label)
    return facts, sources
