# Cài đặt Antigravity cho PACE AI Hub

Áp dụng cho Antigravity IDE bản hiện hành (10/2026). Lưu ý: **Workflows đã ngừng hoạt động từ 19/10/2026**, nên các lệnh `/...` của dự án được viết thành **Agent Skills**. Không tạo `.agents/workflows/`.

## 1. Cấu trúc kit
```
AGENTS.md                      # rule luôn bật cho toàn repo (bối cảnh, lệnh, nguyên tắc bắt buộc)
.agents/rules/                 # rule theo module (frontmatter trigger: always_on | glob | model_decision | manual)
  10-security.md               # always_on
  20-backend-fastapi.md        # glob apps/api/**, apps/worker/**
  30-frontend-nextjs.md        # glob apps/web/**
  40-database.md               # glob migrations/models/sql
  50-ai-gateway.md             # glob gateway/ai/contracts
  60-quality-gates.md          # model_decision (DoD)
.agents/skills/                # skill dự án (gọi tự động hoặc bằng /tên-skill)
  pace-story-kickoff  pace-story-done  pace-phase-gate
  pace-repo-bootstrap  pace-fastapi-endpoint  pace-db-migration
  pace-claude-gateway  pace-collector-adapter
  pace-design-system  pace-ui-screen  pace-ux-review
  pace-qa-testcases  pace-security-review  pace-deploy-vm
docs/plan/PHASES.md            # kế hoạch phase (agent đọc để biết phạm vi hiện tại)
docs/traceability.md           # Story → FR → files → tests → UAT
docs/adr/0000-template.md
KICKOFF_PROMPTS.md             # prompt mẫu cho từng phase
```

## 2. Các bước cài
1. Tạo repo Git trống `pace-ai-hub`, giải nén kit vào thư mục gốc.
2. Tài liệu 01–07 và `prototype.html` **đã có sẵn trong `docs/specs/`** (chép từ Claude Project "PACE AI Tool HUB" ngày 20/10/2026; 06 và 07 có thêm ghi chú ADR-014/015). Chạy `bash scripts/check-specs.sh` để kiểm tra.
3. Mở thư mục bằng Antigravity. Vào **… → Customizations**:
   - Tab **Rules**: phải thấy `AGENTS.md` và 6 rule trong `.agents/rules/`. Rule thiếu frontmatter hoặc trigger sai sẽ bị **bỏ qua mà không báo lỗi**.
   - Tab **Skills**: phải thấy 14 skill `pace-*`.
4. **Cấu hình an toàn cho agent** (Settings):
   - Terminal auto-execution: **Request Review** (không chọn Always Proceed) cho repo này.
   - Non-workspace file access: **Off**.
   - Browser: chỉ allowlist `localhost`, tài liệu chính thức (nextjs.org, fastapi.tiangolo.com, ui.shadcn.com, docs.anthropic.com, learn.microsoft.com).
   - Review policy: bật duyệt plan/artifact với story chạm auth, gateway, budget hoặc dispatch.
5. **Rule cá nhân (tùy chọn)** ở `~/.gemini/GEMINI.md` của từng dev, ví dụ: "Trả lời tôi bằng tiếng Việt; code, commit viết tiếng Anh; luôn hỏi trước khi cài dependency."
6. **Không đưa secret vào repo.** Mỗi dev dùng `.env.local` (đã gitignore). Key Claude API dùng cho dev là key sandbox do IT cấp, có spend limit thấp trên Anthropic Console.

## 3. Skill bên thứ ba (khuyến nghị, phải audit trước khi dùng)
Đọc toàn bộ file của skill trước khi đặt vào `.agents/skills`, và commit vào repo để cả đội dùng cùng một phiên bản.

| Skill | Dùng cho | Cài đặt | Ghi chú |
|---|---|---|---|
| `vercel-labs/agent-skills` → **react-best-practices** | Hiệu năng React/Next.js (hơn 40 rule) | `npx add-skill vercel-labs/agent-skills --skill react-best-practices`, chọn agent Antigravity | Nên dùng |
| `vercel-labs/agent-skills` → **web-design-guidelines** | Audit UI/UX/a11y (hơn 100 rule) | `npx add-skill vercel-labs/agent-skills --skill web-design-guidelines` | Nên dùng; `pace-ux-review` gộp kết quả của skill này |
| **ui-ux-pro-max** (nextlevelbuilder) | Gợi ý UX, palette, font pairing, chart type | `npm i -g uipro-cli && uipro init --ai antigravity` | Tùy chọn. **Token của PACE luôn được ưu tiên**; chỉ dùng phần UX guideline và gợi ý chart |

Không cài các bộ sưu tập hàng trăm skill (kiểu "awesome-skills"). Metadata của mọi skill chiếm budget ngữ cảnh và dễ làm agent kích hoạt nhầm skill.

## 4. MCP (tùy chọn, bật sau Phase 1)
- GitHub MCP: đọc issue và tạo PR. Dùng fine-grained token, chỉ cấp quyền cho repo `pace-ai-hub`, không có quyền admin.

## 4b. Thiết lập GitHub (ADR-009)
- Repo **tạm thời public** (ADR-015). **Khuyến nghị chuyển private trước 30/10/2026.** Khi còn public, bắt buộc:
  - Không commit `.env*`, hostname/IP nội bộ, tenant ID, dữ liệu khách hàng/đối thủ thật. Những thông tin này để ở `docs/internal/` (đã gitignore).
  - Settings → Actions: bật *Require approval for all outside collaborators*. Không dùng self-hosted runner.
  - Package GHCR đặt private.
  - Thêm `LICENSE` (proprietary).
- Nhánh `main` được bảo vệ: bắt buộc PR, CI xanh, 1 review của người, cấm force-push.
- **Bắt buộc** bật secret scanning + push protection (gói GitHub của PACE có hỗ trợ) và Dependabot alerts. Không ai được bypass push protection khi chưa có phê duyệt của chủ dự án.
- Tạo Environments `dev` và `pilot`; `pilot` yêu cầu reviewer. **Không** lưu Anthropic key hay Entra secret của pilot trong GitHub; các secret này nằm trên VM nội bộ (ADR-010).
- Deploy lên VM nội bộ theo kiểu pull từ GHCR (skill `pace-deploy-vm`). Chỉ dùng self-hosted runner khi IT duyệt.
- PostgreSQL MCP: **chỉ** kết nối DB dev local, user read-only.
- Không cấu hình MCP có quyền vào M365 tenant production.

## 5. Kiểm tra sau khi cài
Mở chat agent và gõ: `Liệt kê rules và skills đang active cho file apps/api/app/main.py, và tóm tắt phase hiện tại.` Agent phải nêu được AGENTS.md, 10-security, 20-backend-fastapi và Phase hiện tại theo PHASES.md.
