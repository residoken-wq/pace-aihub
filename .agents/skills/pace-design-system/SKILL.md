---
name: pace-design-system
description: PACE AI Hub design system — tokens, typography, spacing, status colors and shadcn/ui component conventions. Use when setting up Tailwind/theme, creating or styling any UI component, choosing colors, or reviewing visual consistency.
---
# PACE design system

Source: `docs/specs/05_UI_UX_SPEC.md` (Primary #1E88E5, accent #FB8C00, neutral gray, Roboto/system, 8px spacing, 12px card radius, 1440px desktop / 390px mobile, status icon + text).

## Setup (once, in Phase 1)
1. Tailwind CSS **v4** (CSS-first config, no `tailwind.config.js` theme). Copy `references/tokens.css` into `apps/web/app/globals.css` after `@import "tailwindcss";` — it contains light/dark variables and the `@theme inline` mapping.
2. Run `shadcn init` for Tailwind v4; when it generates its own color variables, replace them with PACE tokens (keep variable names: `--primary`, `--accent`, `--destructive`, `--warning`, `--success`, `--muted`, `--border`, `--ring`, `--radius`).
3. Install shadcn primitives as needed: button, input, textarea, select, checkbox, radio-group, switch, form, label, card, badge, table, tabs, dialog, sheet, dropdown-menu, tooltip, toast/sonner, skeleton, alert, progress, separator, breadcrumb, sidebar, stepper (custom).
4. Fonts: Roboto via `next/font/google` with Vietnamese subset (`subsets: ["latin","vietnamese"]`).

## Rules
- Use semantic tokens (`bg-primary`, `text-muted-foreground`), never raw hex in components.
- Spacing scale 4/8/12/16/24/32/48; cards `rounded-[--radius]` (12px), padding 16–24.
- Type scale: 12 caption · 14 body-sm · 16 body · 20 h3 · 24 h2 · 30 h1; line-height ≥1.5 for Vietnamese diacritics.
- Primary blue for main actions only (one primary button per view). Orange accent for highlights/warnings to draw attention, not for destructive actions (use `destructive`).
- Status badges (`components/domain/StatusBadge.tsx`), each = icon + Vietnamese label + color:
  draft (gray, PencilLine) · published (blue, CheckCircle) · paused (amber, PauseCircle) · archived (gray, Archive) · queued (gray, Clock) · running (blue, Loader spin) · needs_review (amber, AlertTriangle) · partial (amber, AlertTriangle) · failed (red, XCircle) · completed (green, CheckCircle2) · pending_approval (amber, Hourglass) · approved (green, BadgeCheck) · rejected (red, Ban) · sent (green, Send).
- Fact vs inference: `[Sự kiện]` badge solid blue-subtle; `[Suy luận]` badge outlined amber; always show source links next to facts.
- Budget meter: <80% primary, 80–99% warning + text, 100% destructive + "Đã chạm hạn mức".
- Icons: lucide-react only, 16/20px, `aria-hidden` when decorative.
- Dark mode supported via tokens; contrast ≥4.5:1 text, ≥3:1 UI borders/icons.
