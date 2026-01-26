# Graph Schema (minimal)

Goal: lossless ingest with a Claim + SourceDoc layer and optional domain edges.

## Invariants
- Every Claim must have (subject)-[:SUBJECT_OF]->(claim)
- Every Claim must have (claim)-[:EVIDENCED_BY]->(SourceDoc)
- All writes are MERGE-only on key, doc_id, and claim_id

## Nodes
- SourceDoc {doc_id, title, source, url}
- Claim {claim_id, text, doc_id}
- Entity {key, label}

## Relations
- (Entity)-[:SUBJECT_OF]->(Claim)
- (Claim)-[:EVIDENCED_BY]->(SourceDoc)
