---
name: pace-ux-review
description: Heuristic UX, accessibility and visual-consistency review of a PACE AI Hub screen or flow. Use when the user asks to review/audit UI, before a UI story is marked done, or after usability-test feedback.
---
# UX review

Inspect the running page in the browser (1440px and 390px) and the source. Output a table: `# | Severity (Blocker/Major/Minor) | Location | Issue | Heuristic | Fix`.

## Checklist
1. **Task fit:** primary action obvious; matches spec in `05_UI_UX_SPEC.md`; O1 target — a new user can create a Sales tool in ≤10 minutes (count clicks/fields).
2. **Nielsen heuristics:** status visibility (run status, saving), match real world (Vietnamese business terms), user control (cancel, back, undo draft), consistency (tokens, StatusBadge, button order: secondary left / primary right), error prevention (confirm destructive, validate early), recognition over recall, minimalist design, helpful errors (what + how to fix + request_id).
3. **Trust & governance cues:** cost estimate before run; fact vs inference labels; every fact has a clickable source; approval state visible; "partial" never shown as complete; sharing dialog explains scope.
4. **Accessibility (WCAG 2.2 AA):** labels, focus visible & not obscured, keyboard order, target size ≥24px, contrast, aria-live for async status, no color-only meaning, Vietnamese diacritics render correctly.
5. **Responsive:** no horizontal scroll at 390px; tables collapse to cards; sidebar becomes sheet.
6. **States:** loading/empty/error/partial/success all reachable (use mocks).
7. **Visual:** spacing scale, alignment, type hierarchy, one primary button, icon sizes.
If a third-party `web-design-guidelines` skill is installed, also apply it and merge findings.
