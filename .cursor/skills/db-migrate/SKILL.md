# DB Migrations (Alembic)

Use this skill whenever you need to create, apply, or inspect database migrations.

## Prerequisites

Ensure PostgreSQL is running and `DATABASE_URL` is set in your environment before running any
Alembic command.

## Common operations

### Generate a new migration

Always use `--autogenerate` to derive changes from SQLAlchemy model definitions.
Review the generated file before applying — autogenerate misses some things (e.g. CHECK constraints,
partial indexes, sequences).

```bash
uv run alembic revision --autogenerate -m "<short-description-in-snake-case>"
```

Migration files land in `alembic/versions/`. Open the file and verify the `upgrade()` and
`downgrade()` functions reflect your intent before proceeding.

### Apply pending migrations

```bash
uv run alembic upgrade head
```

### Roll back one migration

```bash
uv run alembic downgrade -1
```

### Check current revision

```bash
uv run alembic current
```

### View full migration history

```bash
uv run alembic history --verbose
```

## Naming convention

Migration message (the `-m` argument) should describe the schema change, not the ticket:

- Good: `add_thesis_column_to_active_holdings`
- Bad: `story-123` or `update`

## Rules

- Never edit an already-applied migration file — create a new one instead
- Always provide a working `downgrade()` — leaving it as `pass` is not acceptable
- If a migration adds a NOT NULL column to an existing table, include a `server_default` or a
  data backfill step in `upgrade()` to avoid locking failures
- Run `alembic current` before generating a new migration to confirm you are on the expected revision
