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
