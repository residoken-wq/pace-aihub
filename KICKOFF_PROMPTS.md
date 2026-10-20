# Prompt mẫu cho Antigravity theo từng phase

Dùng **Planning mode** cho các prompt dưới đây. Mỗi prompt chỉ làm 1 story, và người duyệt plan trước khi agent code.

## Phase 0 — Kiểm tra môi trường
```
Đọc AGENTS.md, docs/plan/PHASES.md và toàn bộ docs/specs/. Không viết code.
Hãy: (1) tóm tắt sản phẩm trong 10 dòng; (2) liệt kê mâu thuẫn hoặc khoảng trống giữa các spec;
(3) đề xuất ADR-013 tech stack với phiên bản ổn định hiện hành (Next.js, FastAPI, Python, Postgres,
Redis, Celery, shadcn, Tailwind), ghi vào docs/adr/ADR-013-tech-stack.md ở trạng thái Proposed.
Tuân thủ các quyết định đã chốt trong docs/adr/ADR-009-015-decisions.md.
```
```
Spike (không commit vào main): viết script apps/api/spikes/measure_brief.py gọi Claude API
bằng key trong .env.local, với 20 mẫu nguồn trong tests/fixtures/sources/. Đo input/output tokens
mỗi brief và ước tính chi phí theo bảng giá mà tôi sẽ nhập tay. Không hard-code giá.
```

## Phase 1 — Foundation
```
/pace-repo-bootstrap  — Repo đang trống. Lập plan scaffold monorepo theo AGENTS.md.
CI dùng GitHub Actions (ADR-009): ci.yml + build.yml đẩy image lên GHCR.
```
```
/pace-deploy-vm — INF-01c walking skeleton: compose.prod tối thiểu (proxy TLS + web + api /healthz),
deploy.sh pull từ GHCR. VM nội bộ đã bàn giao; hỏi tôi trước mọi lệnh chạy trên VM.
```
```
/pace-story-kickoff DB-01
```
```
/pace-story-kickoff AUTH-01 — Entra tenant dev: dùng biến môi trường ENTRA_TENANT_ID,
ENTRA_CLIENT_ID, ENTRA_CLIENT_SECRET (tôi tự điền). Bắt buộc có test IDOR cross-workspace.
```
```
/pace-design-system rồi /pace-ui-screen — Dựng AppShell + sidebar theo 05_UI_UX_SPEC
(menu admin chỉ hiện với role admin), workspace switcher, các trang rỗng với empty state.
Kiểm tra bằng browser ở 1440px và 390px.
```

## Phase 2 — Vertical Slice 1
```
/pace-story-kickoff TOOL-01
/pace-story-kickoff COL-01
/pace-story-kickoff GW-01
/pace-story-kickoff AI-01   — dùng schema .agents/skills/pace-claude-gateway/references/daily_brief.schema.json
/pace-story-kickoff UI-01   — Wizard 5 bước đúng field ở 05_UI_UX_SPEC; mục tiêu UAT-01 ≤10 phút
/pace-story-kickoff RUN-01  — chỉ phần manual run (RUN-01a)
/pace-story-kickoff RPT-01  — chỉ phần preview (RPT-01a)
```
Cuối phase: `/pace-phase-gate 2`

## Phase 3 — Governance & Automation
```
/pace-story-kickoff GW-02  — bắt buộc test 20 request đồng thời với $1 còn lại
/pace-story-kickoff RUN-01 — phần scheduler (RUN-01b), Monday lookback, unique slot
/pace-story-kickoff COL-02
/pace-story-kickoff RPT-01 — approve/reject/revision (RPT-01b)
/pace-story-kickoff OUT-01 — dev dùng mailpit; production qua Graph scope đã duyệt
/pace-story-kickoff OBS-01
/pace-story-kickoff CMS-01 — Admin console: Team Management, Credentials (vault ref), Policies, Audit, Budget dashboard
```
Cuối phase: `/pace-security-review` toàn phase, sau đó `/pace-phase-gate 3`

## Phase 4 — Hardening
```
/pace-qa-testcases — lập test plan toàn bộ test matrix ở 07, ghi vào docs/qa/phase-4.md, đánh dấu case
đã/chưa tự động hoá, rồi tự động hoá các case P0 còn thiếu.
```
```
/pace-deploy-vm — chuẩn bị compose.prod, deploy/rollback/backup scripts cho VM nội bộ (pull-based từ GHCR).
Không chạy lệnh nào trên VM thật khi chưa hỏi tôi.
```
```
Viết docs/runbooks/: deploy, rollback, backup/restore (kèm lệnh test restore), rotate key, revoke user,
xử lý budget 100%, xử lý DLQ. Mỗi runbook có mục "Kiểm tra sau khi làm".
```
Cuối phase: `/pace-phase-gate 4`

## Prompt sửa lỗi (dùng mọi lúc)
```
Bug: <mô tả + bước tái hiện + log/request_id>. Trước khi sửa: viết test tái hiện lỗi và cho thấy test fail,
sau đó mới sửa. Nêu nguyên nhân gốc và kiểm tra lỗi tương tự ở module khác.
```
