---
trigger: glob
globs: apps/web/**
---
# Frontend conventions (Next.js / CMS & end-user UI)

- Next.js App Router, TypeScript `strict`, Server Components by default; `"use client"` only for interactive leaves.
- UI kit: Tailwind + shadcn/ui primitives in `components/ui/`; product components in `components/<domain>/`. Do not install another component library.
- Design tokens only (see `.agents/skills/pace-design-system`): no hard-coded hex, px spacing outside the 8px scale, or ad-hoc fonts.
- Data: typed client generated from `packages/contracts` + TanStack Query. Never call Anthropic or Graph from the browser. No secrets in `NEXT_PUBLIC_*`.
- Forms: react-hook-form + zod; schema mirrors API validation; inline field errors in Vietnamese.
- Every data screen implements 5 states: loading (skeleton), empty (with CTA), error (with retry + request_id), partial/warning, success.
- Status = icon + text + color (never color alone). Times shown local with tz label (e.g. "08:30 (GMT+7)").
- Navigation per spec: Home, My Tools, Team Tools, Templates, Runs & Reports, Knowledge, Usage & Budget, Settings; admin-only: Team Management, Credentials, Policies, Audit — hide AND enforce server-side.
- Accessibility WCAG 2.2 AA: labels, focus visible, keyboard path, contrast ≥ 4.5:1, aria-live for run status.
- UI copy via i18n keys (`messages/vi.json`), Vietnamese default.
- Tests: Vitest + Testing Library for components; Playwright e2e for UAT flows; verify visually with the browser agent at 1440px and 390px.
