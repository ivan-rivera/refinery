# Decisions

This section outlines a log of architectural decisions, in the following format:

```md

## ADR-001: Use Postgres over SQLite

**Date:** 2026-04-14
**Status:** Accepted

### Context
Need to support concurrent writes from multiple worker processes.

### Decision
Postgres. SQLite's write locking would be a bottleneck.

### Consequences
- Adds operational complexity (need a running PG instance)
- Enables row-level locking, which we need for the job queue
- Local dev needs Docker or a local PG install

### Alternatives Considered
SQLite (ruled out), MySQL (no strong reason to prefer over PG)

```

## Decision Log
