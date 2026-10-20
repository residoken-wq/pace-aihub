---
name: pace-db-migration
description: Safely create a PostgreSQL schema change for PACE AI Hub with Alembic (new table, column, index, enum, constraint, RLS policy). Use for any change to models or database structure.
---
# Safe migration

1. Compare intent with `docs/specs/03_DATABASE_SCHEMA.sql`; list differences. Deviations from the baseline need an ADR note.
2. Update SQLAlchemy models, then `uv run alembic revision --autogenerate -m "<story-id> <summary>"`. Review the generated file by hand: enums, server defaults, partial/unique indexes, CHECK constraints are often missed by autogenerate.
3. Classify: additive (safe) vs destructive. Destructive → expand/migrate/contract in separate migrations; ask user.
4. Enum changes: `ALTER TYPE ... ADD VALUE` cannot run inside some transactions — use `op.execute` with autocommit block.
5. Large tables: create indexes `CONCURRENTLY` (outside transaction).
6. Test: `alembic upgrade head && alembic downgrade -1 && alembic upgrade head` on the test container; run repository tests.
7. If tenant table: verify `workspace_id` NOT NULL, FK, leading index; consider RLS policy (`USING (workspace_id = current_setting('app.workspace_id')::uuid)`) as defense-in-depth.
8. Note the migration in the PR with rollback instructions.
