#!/usr/bin/env bash
# Verify spec docs and Antigravity customizations are in place.
set -u
root="$(cd "$(dirname "$0")/.." && pwd)"
fail=0
for f in 01_PRD.md 02_SYSTEM_ARCHITECTURE.md 03_DATABASE_SCHEMA.sql 04_API_GATEWAY.md \
         05_UI_UX_SPEC.md 06_MVP_BACKLOG.md 07_DECISIONS_AND_TESTS.md prototype.html; do
  if [ -s "$root/docs/specs/$f" ]; then echo "OK   docs/specs/$f"; else echo "MISS docs/specs/$f"; fail=1; fi
done
for r in "$root"/.agents/rules/*.md; do
  head -1 "$r" | grep -q '^---$' || { echo "BAD  frontmatter: $r"; fail=1; }
  grep -Eq '^trigger: (always_on|model_decision|glob|manual)$' "$r" || { echo "BAD  trigger: $r"; fail=1; }
  size=$(wc -c < "$r"); [ "$size" -le 24000 ] || { echo "BIG  $r ($size bytes)"; fail=1; }
done
for s in "$root"/.agents/skills/*/; do
  [ -f "$s/SKILL.md" ] || { echo "MISS $s/SKILL.md"; fail=1; continue; }
  grep -q '^description: ' "$s/SKILL.md" || { echo "BAD  description: $s"; fail=1; }
done
[ $fail -eq 0 ] && echo "All checks passed." || { echo "Some checks failed."; exit 1; }
