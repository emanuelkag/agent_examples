# Async Execution Model

## Purpose

This repo uses a split operating model for long-horizon async work:

- **repo file** = source of truth
- **GitHub Issue** = execution projection
- **run artifacts / evidence** = proof

## Packet readiness rule

A packet is not execution-ready unless it defines objective, scope, non-goals, dependencies, acceptance criteria, evidence required, budget envelope, repo targets, and execution policy.

## Special rule for Agent Examples

Packets should preserve explicit evidence, human review, and repo-local canon while this system evolves incrementally.

## Recommended file layout

- `planning/program_registry.v1.yaml`
- `.github/ISSUE_TEMPLATE/work_packet.yml`
- `docs/async_execution_model.md`

## Practical meaning

Clean agent sessions should be able to read `planning/program_registry.v1.yaml`, pick a packet, respect its budget, and continue without hidden context.
