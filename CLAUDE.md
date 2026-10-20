# CLAUDE.md — PACE AI Hub

@AGENTS.md
@docs/HANDOFF.md

## Claude Code specifics
- Project skills live in `.agents/skills/` (written for Antigravity, same SKILL.md format). To use them as Claude Code skills, mirror them: `mkdir -p .claude && ln -s ../.agents/skills .claude/skills` (or copy). Rules in `.agents/rules/*.md` apply here too — read the relevant one before touching `apps/api`, `apps/worker`, `apps/web`, migrations or the gateway.
- Start every session by checking `git status`, the current branch, and the "Việc tiếp theo" section in `docs/HANDOFF.md`.
- Ask before: installing dependencies, schema changes outside a migration, touching auth/gateway/budget/dispatch code, pushing, opening or merging PRs.
- Repo is PUBLIC (ADR-015): check every diff for secrets, internal hostnames/IPs, tenant IDs and real business data before committing.
