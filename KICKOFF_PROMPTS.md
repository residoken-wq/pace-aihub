# Prompt mẫu cho Antigravity theo từng phase

Dùng **Planning mode** cho các prompt dưới đây. Mỗi prompt chỉ làm 1 story, và người duyệt plan trước khi agent code.

## Quy tắc chung: áp dụng cho MỌI prompt bên dưới
Dán khối sau vào cuối mỗi prompt (hoặc nhắc agent "áp dụng mục Hoàn tất trong KICKOFF_PROMPTS.md"). Chủ dự án vẫn duyệt plan ở Planning mode; từ lúc code xong đến lúc mở PR thì agent tự làm.

```
## Hoàn tất (tự làm, không chờ hỏi)
- Sau khi tôi duyệt plan và code xong: commit (conventional commits + story ID), `git push -u origin <nhánh>`,
  rồi MỞ PR vào main bằng `gh pr create` (body theo cấu trúc Tóm tắt / Thay đổi / Kiểm tra / Chưa kiểm chứng).
- Dán OUTPUT THẬT của mọi lệnh kiểm chứng vào mô tả PR (che mọi giá trị trong .env, token, hostname nội bộ).
- Task chỉ kiểm chứng, không có thay đổi code: KHÔNG tạo commit rỗng; dán output bằng `gh pr comment <số PR>`
  (hoặc `gh issue comment` nếu không có PR liên quan).
- Nếu push hoặc `gh` lỗi (chưa đăng nhập, thiếu quyền): DỪNG, in nguyên lỗi, không được báo là đã push hoặc đã mở PR.
- Không tự merge (ADR-011).
```

Điều kiện: máy chạy agent đã đăng nhập `gh` (`gh auth status`) bằng tài khoản có quyền push và mở PR trên repo.

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

### INF-01a: PR-B và PR-C (PR-A đã merge qua residoken-wq/pace-aihub#2)
Prompt bootstrap ở trên đã được thực hiện cho phần api/worker/contracts/compose (PR-A). Phần còn lại của INF-01a chia làm 2 prompt. Chạy PR-B trước để CI ở PR-C bật luôn job web và e2e.

PR-B: khung `apps/web`
```
/pace-repo-bootstrap — INF-01a PR-B: web skeleton (apps/web). Planning mode: chỉ lập plan, chờ tôi duyệt rồi mới code.

## Bối cảnh (đọc trước)
- AGENTS.md, docs/HANDOFF.md, .agents/rules/30-frontend-nextjs.md, .agents/rules/10-security.md,
  .agents/rules/60-quality-gates.md, docs/adr/ADR-013-tech-stack.md (kể cả Phụ lục A),
  docs/runbooks/local-dev.md.
- PR-A (residoken-wq/pace-aihub#2, đã merge) đã dựng: root package.json (pnpm 12.14.0, Node >=24),
  pnpm-workspace.yaml (đã khai báo apps/web), apps/api (/healthz, /readyz), apps/worker,
  packages/contracts, infra/docker-compose.dev.yml (chưa có service web).
- Nhánh: tạo `feat/inf-01a-web-skeleton` từ main mới nhất.

## Phạm vi đã được chủ dự án duyệt (KHÔNG làm thêm)
Trong phạm vi:
1. `apps/web` bằng create-next-app: Next.js 16.x bản patch mới nhất, TypeScript strict, App Router,
   Tailwind CSS v4, ESLint, không dùng `src/`. Package name `@pace/web`.
2. `shadcn init` cho Tailwind v4 (chỉ init, chưa thêm component nào ngoài `button` nếu trang cần).
3. Trang chủ placeholder là Server Component: gọi API server-side qua biến `API_INTERNAL_URL`
   (KHÔNG dùng NEXT_PUBLIC_*), `fetch(`${API_INTERNAL_URL}/healthz`, { cache: "no-store" })`,
   hiển thị trạng thái API (ok / không kết nối được) bằng icon + chữ. Không lỗi trang khi API chết.
4. Chữ hiển thị tiếng Việt đặt trong `apps/web/messages/vi.json` và import trực tiếp;
   CHƯA cài next-intl (thuộc UI-00).
5. Scripts trong apps/web/package.json khớp AGENTS.md: `lint`, `typecheck` (tsc --noEmit),
   `test` (vitest run), `e2e` (playwright test), `dev`, `build`, `start`.
6. Vitest + Testing Library: test render trang placeholder ở 2 trạng thái (API ok / API lỗi), mock fetch.
7. Playwright (pin 1.64.1 theo ADR-013 hoặc bản patch mới nhất của 1.64): 1 smoke test mở trang chủ,
   thấy tiêu đề và trạng thái API "ok" khi chạy với stack compose.
8. `apps/web/Dockerfile`: multi-stage, Node 24 (tag đầy đủ, ví dụ `node:24.x.y-alpine`, tra Docker Hub),
   `output: "standalone"`, chạy user non-root, build từ repo root
   (`docker build -f apps/web/Dockerfile .`), dùng corepack để có pnpm 12.14.0.
9. Thêm service `web` vào infra/docker-compose.dev.yml: build Dockerfile trên, env
   `API_INTERNAL_URL=http://api:8000`, port `127.0.0.1:3000:3000`, depends_on api healthy, healthcheck.
10. Cập nhật: README.md (bỏ chữ "đang dựng"), docs/runbooks/local-dev.md (lệnh web),
    ADR-013 Phụ lục A (thêm dòng phiên bản web), docs/traceability.md (INF-01 → PR-B).

Ngoài phạm vi (KHÔNG làm, dù skill pace-repo-bootstrap có nhắc tới):
- Design tokens / tokens.css, font Roboto, AppShell, sidebar, i18n next-intl, TanStack Query,
  StatusBadge → thuộc UI-00.
- Đăng nhập / OIDC / cookie → AUTH-01.
- CI workflows, Dependabot, pre-commit, CODEOWNERS → PR-C.
- Không sửa code trong apps/api, apps/worker, packages/contracts.

## Quy tắc bắt buộc
- Phiên bản: tra registry tại thời điểm làm (`npm view <pkg> version`, Docker Hub). KHÔNG ghi theo
  trí nhớ. Pin exact version (không dùng ^ hay ~). Liệt kê bảng phiên bản trong plan để tôi duyệt
  TRƯỚC khi cài. Nếu TypeScript 7.x không tương thích với Next 16 / ESLint / Vitest thì dùng 5.x
  mới nhất và ghi lý do vào ADR-013 Phụ lục A (giống trường hợp packages/contracts).
- Hỏi tôi trước khi cài bất kỳ dependency nào ngoài danh sách đã duyệt.
- Repo đang PUBLIC (ADR-015): không ghi hostname/IP nội bộ, tenant ID, email thật, dữ liệu thật.
  Không tạo file .env có giá trị; chỉ thêm tên biến mới (API_INTERNAL_URL) vào .env.example nếu cần.
- Không đưa secret hay PII vào prompt, fixture, log (ADR-012).
- Code, identifier, commit bằng tiếng Anh; commit theo conventional commits có story ID,
  ví dụ `feat(web): next.js 16 skeleton with api health status [INF-01a]`.
- Không tự merge PR (ADR-011).

## Plan cần trả về (trước khi code)
1. Bảng phiên bản tra từ registry (next, react, react-dom, tailwindcss, @tailwindcss/postcss,
   typescript, eslint, eslint-config-next, vitest, @testing-library/react, jsdom,
   @playwright/test, shadcn CLI, node image tag).
2. Danh sách file sẽ tạo/sửa.
3. Acceptance criteria Given/When/Then, tối thiểu:
   - Given stack compose chạy, when mở http://localhost:3000, then thấy trang placeholder và
     trạng thái API "ok".
   - Given API dừng, when mở trang, then trang vẫn render và hiện "không kết nối được API",
     không lộ URL nội bộ hay stack trace.
   - Given build production, when kiểm tra bundle client, then không có chuỗi API_INTERNAL_URL
     hay biến môi trường server nào.
   - Given repo vừa clone, when chạy `pnpm -C apps/web lint && pnpm -C apps/web typecheck &&
     pnpm -C apps/web test`, then tất cả pass.
4. Danh sách test và cách chạy.
5. Rủi ro/giới hạn (ví dụ máy không có Docker thì e2e chưa chạy được).

## Định nghĩa xong (DoD)
- Đã CHẠY THẬT trong phiên này và dán output: lint, typecheck, vitest, `pnpm -C apps/web build`,
  `docker compose -f infra/docker-compose.dev.yml --env-file .env up -d --build` (mọi service healthy),
  Playwright smoke pass, screenshot trang ở 1440px và 390px.
- Kiểm tra AC bundle: `grep -r "API_INTERNAL_URL\|api:8000" apps/web/.next/static` không có kết quả.
- Mở PR vào main, mô tả theo cấu trúc: Tóm tắt / Thay đổi / Kiểm tra (output thật) / Chưa kiểm chứng.
  Không được ghi "tests pass" nếu chưa chạy.
```

PR-C: CI/CD và quy trình repo
```
/pace-repo-bootstrap — INF-01a PR-C: CI/CD + quy trình repo. Planning mode: chỉ lập plan, chờ tôi duyệt rồi mới code.

## Bối cảnh (đọc trước)
- AGENTS.md, docs/HANDOFF.md, .agents/skills/pace-repo-bootstrap/SKILL.md (mục 8, 9),
  .agents/rules/10-security.md, .agents/rules/60-quality-gates.md,
  docs/adr/ADR-009-015-decisions.md (ADR-009, ADR-015), docs/adr/ADR-013-tech-stack.md (§6 + Phụ lục A),
  docs/runbooks/local-dev.md.
- Đã có từ PR-A (residoken-wq/pace-aihub#2):
  - apps/api: uv, Python 3.12. Kiểm tra: `uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run pytest -q`.
    Test marker `integration` dùng testcontainers (postgres:17.11-alpine, valkey/valkey:9.1.2-alpine),
    tự skip khi không có Docker → trên runner GitHub (có Docker) chúng PHẢI chạy, không được skip.
    tests/test_migrations.py đã kiểm tra alembic up → down → up.
  - apps/worker: cùng bộ lệnh như api; phụ thuộc ../api qua path dependency.
  - packages/contracts: `pnpm contracts:gen` sinh openapi.yaml + src/api.d.ts từ FastAPI.
  - infra/docker-compose.dev.yml: cần file .env có POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB.
  - Dockerfile: apps/api/Dockerfile, apps/worker/Dockerfile (build từ repo root).
  - Root: package.json (packageManager pnpm@12.14.0), .nvmrc = 24, uv 0.13.3.
- apps/web (PR-B) có thể CHƯA merge. Các job/bước liên quan web phải tự bỏ qua khi
  `apps/web/package.json` không tồn tại (dùng `hashFiles(...) != ''`), và tự bật khi PR-B vào main.
- Nhánh: tạo `ci/inf-01a-pipelines` từ main mới nhất.

## Phạm vi đã được chủ dự án duyệt
1. `.github/workflows/ci.yml` — trigger `pull_request` và `push` lên main. Job:
   - `api`: setup-uv (pin 0.13.3), Python 3.12, `uv sync --frozen`, ruff format --check, ruff check,
     mypy, pytest (gồm cả integration — kiểm tra trong log là 0 skipped).
   - `worker`: tương tự api.
   - `migrations`: chạy riêng `alembic upgrade head` → `downgrade base` → `upgrade head` với
     `services: postgres` image `postgres:17.11-alpine` (mật khẩu sinh ngẫu nhiên trong job,
     không phải secret của repo).
   - `contracts`: `pnpm contracts:gen` rồi `git diff --exit-code packages/contracts` (chặn quên regen).
   - `web` (chỉ khi có apps/web): lint, typecheck, test.
   - `security`: gitleaks quét toàn lịch sử (`fetch-depth: 0`), `pnpm audit --prod`, `pip-audit` cho
     api và worker (xuất requirements bằng `uv export --frozen --no-dev`).
     gitleaks: dùng binary CLI tải từ GitHub Releases, pin version + kiểm tra SHA256 checksum.
     KHÔNG dùng gitleaks-action (yêu cầu license khi repo chuyển vào GitHub organization — HANDOFF mục 6.2).
   - `e2e` (chỉ khi có apps/web): tạo .env tạm trong job (giá trị ngẫu nhiên bằng `openssl rand -hex 16`),
     `docker compose -f infra/docker-compose.dev.yml --env-file .env up -d --build --wait`,
     chạy Playwright, upload playwright-report làm artifact, luôn `docker compose down -v` ở cuối.
2. `.github/workflows/build.yml` — trigger push lên main và tag `v*`:
   - Build image api, worker (và web nếu có), quét Trivy, FAIL khi có lỗ hổng HIGH/CRITICAL đã có bản vá.
   - Push lên GHCR `ghcr.io/residoken-wq/pace-aihub-<service>`, tag `sha-<7 ký tự>` (+ semver khi là tag).
   - Attest provenance bằng `actions/attest-build-provenance`.
   - Chỉ job push có `packages: write`, `id-token: write`, `attestations: write`.
3. Bảo mật cho MỌI workflow:
   - `permissions:` mặc định `contents: read` ở cấp workflow; mở thêm quyền ở cấp job khi thật cần.
   - Pin mọi action (kể cả actions/*) theo commit SHA đầy đủ, kèm comment version (`# v4.2.2`).
   - Chỉ dùng `pull_request`, KHÔNG `pull_request_target`. Không self-hosted runner (ADR-015).
   - Không dùng secret của repo trong ci.yml. build.yml chỉ dùng `GITHUB_TOKEN`.
   - Không nội suy `${{ github.event.* }}` vào lệnh `run:` (chống script injection); nếu cần thì qua `env:`.
   - `concurrency` hủy run cũ cùng ref; `timeout-minutes` cho mọi job; cache uv và pnpm.
   - KHÔNG dùng `paths:` ở cấp workflow (các check sẽ trở thành required, path filter làm check treo).
4. `.github/dependabot.yml`: ecosystem npm (/, /packages/contracts, /apps/web), uv (/apps/api, /apps/worker),
   github-actions (/), docker (/apps/api, /apps/worker, /apps/web).
   Lịch weekly, thứ Hai 08:00, timezone Asia/Ho_Chi_Minh (ADR-013 §6). Gom patch+minor theo nhóm,
   major mở PR riêng. Giới hạn số PR mở mỗi ecosystem.
5. `.github/CODEOWNERS`: `* @residoken-wq` (tạm thời — chủ dự án quyết định 20/10/2026).
   Thêm dòng riêng (vẫn @residoken-wq) cho các đường dẫn nhạy cảm để sau này dễ tách người duyệt:
   `.github/`, `infra/`, `apps/api/app/gateway/`, `apps/api/migrations/`, `docs/adr/`.
6. `.github/pull_request_template.md`: Story ID, Tóm tắt, AC (Given/When/Then) → test tương ứng,
   Bằng chứng kiểm tra (output thật), checklist ADR-015 (không secret, không hostname/IP nội bộ,
   không tenant ID, không dữ liệu thật), checklist DoD theo 60-quality-gates.md, Chưa kiểm chứng.
7. `.pre-commit-config.yaml`: ruff + ruff-format (repo astral-sh/ruff-pre-commit, rev khớp ruff 0.17.1),
   mypy cho api và worker qua hook local `uv run mypy`, gitleaks (pin version),
   eslint cho apps/web qua hook local (chỉ khi có web). Chạy bằng `uvx pre-commit`.
   Prettier: CHƯA có trong repo → chỉ thêm nếu PR-B đã đưa vào; nếu chưa, ghi vào "đề xuất", không tự cài.
8. Cập nhật docs/runbooks/local-dev.md (mục pre-commit + cách đọc kết quả CI),
   docs/traceability.md (INF-01 → PR-C), ADR-013 Phụ lục A (thêm version gitleaks, trivy, các action chính).

Ngoài phạm vi (KHÔNG làm):
- Deploy lên VM, compose.prod.yml, TLS → INF-01c (skill pace-deploy-vm).
- Thay đổi code ứng dụng trong apps/*, trừ khi CI lộ ra lỗi thật — khi đó DỪNG và báo tôi, không tự sửa rộng.
- Đổi settings GitHub (branch protection, secret scanning, visibility package) — agent không làm,
  chỉ liệt kê cho chủ dự án (mục "Việc chủ dự án cần làm" bên dưới).

## Quy tắc bắt buộc
- Version: tra thật tại thời điểm làm (GitHub Releases cho actions/gitleaks/trivy, PyPI, npm),
  không ghi theo trí nhớ. Liệt kê bảng action + commit SHA + version trong plan để tôi duyệt.
- Hỏi tôi trước khi thêm bất kỳ tool/dependency nào ngoài danh sách trên.
- Repo PUBLIC (ADR-015): không ghi hostname/IP nội bộ, tenant ID, email thật vào workflow hay docs.
- KHÔNG push secret giả lên repo để "thử" gitleaks. Chứng minh gitleaks bắt được secret bằng cách
  chạy local trên một thư mục tạm ngoài repo, rồi xoá.
- Code, commit tiếng Anh, conventional commits + story ID, ví dụ
  `ci: add ci and build workflows with ghcr push [INF-01a]`. Không tự merge (ADR-011).

## Plan cần trả về (trước khi code)
1. Bảng action/tool: tên, version, commit SHA, nguồn tra cứu.
2. Danh sách file tạo/sửa.
3. Sơ đồ job của ci.yml và build.yml (job nào chạy khi nào, quyền gì).
4. Acceptance criteria Given/When/Then, tối thiểu:
   - Given PR từ nhánh trong repo, when CI chạy, then api/worker/migrations/contracts/security xanh,
     integration test thực sự chạy (0 skipped).
   - Given commit có chuỗi giống secret, when gitleaks chạy, then job security fail
     (chứng minh local, không push).
   - Given PR mở từ fork, when workflow chạy, then không đọc được secret nào và không có quyền
     ghi package (chứng minh bằng khối `permissions` và trigger).
   - Given merge vào main, when build.yml chạy, then image qua Trivy, được push lên GHCR với tag
     `sha-<short>` và có provenance attestation.
   - Given ai đó sửa route API mà quên `pnpm contracts:gen`, when CI chạy, then job contracts fail.
5. Rủi ro và giới hạn.

## Định nghĩa xong (DoD)
- `actionlint` sạch cho mọi workflow (tải binary có checksum; chạy local).
- Push nhánh, mở PR vào main: link run CI xanh (dán link + tóm tắt từng job), gitleaks local
  bắt được secret giả (dán output, đã redact).
- Không ghi "pass" nếu chưa thấy run thật.
- Mô tả PR có mục "Việc chủ dự án cần làm sau khi merge":
  1. Branch protection cho main: bắt buộc PR, 1 review, các check bắt buộc (liệt kê đúng tên job), cấm force-push.
  2. Bật secret scanning + push protection (ADR-009, ADR-015).
  3. Settings → Actions: "Require approval for all outside collaborators" cho workflow từ fork;
     default workflow permissions = read.
  4. Sau lần build.yml đầu tiên: kiểm tra package GHCR và đặt private (ADR-015 điều kiện 4).
  5. Khi chuyển repo vào GitHub organization của PACE: cập nhật tên image GHCR và CODEOWNERS.
```

### Các story Phase 1 khác
INF-01c: walking skeleton lên VM (chỉ chạy sau khi PR-B và PR-C đã merge; checklist: `docs/plan/INF-01_STEPS.md`)
```
/pace-deploy-vm — INF-01c: walking skeleton lên VM nội bộ. Planning mode: chỉ lập plan, chờ tôi duyệt rồi mới code.

## Điều kiện trước (kiểm tra đầu tiên, nếu thiếu thì DỪNG và báo tôi)
- PR-B (apps/web + apps/web/Dockerfile) và PR-C (.github/workflows/ci.yml + build.yml đẩy image lên GHCR) đã merge vào main.
- Trên GHCR đã có image api, worker, web với tag `sha-<7 ký tự>` từ ít nhất một lần build.yml chạy trên main.
- Nhánh: tạo `feat/inf-01c-walking-skeleton` từ main mới nhất.

## Bối cảnh (đọc trước)
- AGENTS.md, CLAUDE.md, docs/HANDOFF.md, docs/plan/INF-01_STEPS.md (Bước 0: quyết định đã chốt),
  .agents/skills/pace-deploy-vm/SKILL.md, .agents/rules/10-security.md, .agents/rules/60-quality-gates.md.
- docs/adr/ADR-009-015-decisions.md (ADR-009 phương án A pull-based, ADR-010 VM nội bộ, ADR-015),
  docs/adr/ADR-016-repo-visibility-until-pilot.md (repo PUBLIC đến Pilot — điều kiện bổ sung cho INF-01c),
  docs/adr/ADR-013-tech-stack.md (Phụ lục A: postgres:17.11-alpine, valkey/valkey:9.1.2-alpine, ...).
- infra/docker-compose.dev.yml, apps/api (/healthz, /readyz kiểm tra Postgres + Valkey),
  apps/worker (task `worker.tasks.ping`, queue reconcile), docs/runbooks/local-dev.md.

## Quyết định đã chốt (docs/plan/INF-01_STEPS.md, Bước 0, 22/10/2026) — làm đúng, không đổi
- Token GHCR trên VM: PAT chỉ quyền đọc package (tài khoản `residoken-wq`), xoay 90 ngày, đặt ở
  `/etc/pace-ai-hub/ghcr.token`. Tra docs GitHub hiện hành để ghi đúng loại token và quyền tối thiểu.
- VM lấy code deploy: `git clone` qua HTTPS không xác thực (repo đang public). Runbook PHẢI có mục
  "Trước khi repo chuyển private: đổi sang deploy key chỉ đọc" (ADR-016, checklist chuyển repo).
- TLS: chứng chỉ do IT cấp, mount vào proxy. Proxy: **Nginx** (không dùng ACME).
- PostgreSQL chạy chung VM với app (service `postgres` trong compose.prod).
- Deploy chạy tay bằng `deploy.sh <tag>`; không dùng systemd timer tự kéo.
- IT đã bàn giao VM; giá trị thật nằm ở docs/internal/ hoặc trên VM, agent không cần và không được ghi vào repo.

## Phạm vi đã được chủ dự án duyệt
1. `infra/compose.prod.yml`:
   - Services: `proxy` (Nginx, ưu tiên image chạy non-root, pin tag đầy đủ), `web`, `api`, `worker`,
     `migrate` (one-off `alembic upgrade head`), `postgres:17.11-alpine`,
     `valkey/valkey:9.1.2-alpine` (AOF `appendfsync everysec`).
   - Image app pin theo DIGEST (`ghcr.io/...@sha256:...`) đọc từ file `release.env`, không dùng `latest`.
   - Chỉ proxy publish cổng 443 (và 80 → redirect 443). postgres/valkey/api/worker/web chỉ ở network nội bộ.
   - Mọi service: healthcheck, `restart: unless-stopped`, giới hạn CPU/RAM, log driver json-file có max-size/max-file,
     user không phải root, `read_only: true` + tmpfs khi image cho phép, `no-new-privileges`.
   - Không có `beat`, `mailpit`, backup (ngoài phạm vi).
2. Nginx (`infra/nginx/`): chứng chỉ mount từ `/etc/pace-ai-hub/tls/`; TLS 1.2+; HSTS; ẩn version (`server_tokens off`).
   Route: `/api/`, `/healthz`, `/readyz` → api:8000; còn lại → web:3000. Truyền `X-Request-ID`, `X-Forwarded-*`.
   Access log KHÔNG ghi header Authorization/Cookie hay query string nhạy cảm.
3. Cấu hình trên VM (KHÔNG commit): `/etc/pace-ai-hub/` gồm `app.env`, `db.env`, `release.env`, `tls/`,
   `ghcr.token`. Quyền `root:pace 0640`, riêng `ghcr.token` 0600. Trong repo chỉ có `infra/prod.env.example`
   liệt kê TÊN biến; domain dùng placeholder `pilot.example.invalid` (ADR-016).
4. `deploy/deploy.sh <tag>` (bash, `set -euo pipefail`):
   docker login ghcr.io bằng `--password-stdin` từ `/etc/pace-ai-hub/ghcr.token` → resolve digest cho tag →
   ghi `release.env` → `docker compose pull` → chạy `migrate` → `up -d` → chờ `https://$PACE_DOMAIN/readyz`
   (timeout cấu hình được) → smoke: `/healthz` 200, `/readyz` = ready, trang web 200, worker trả `pong` →
   ghi một dòng vào `/var/lib/pace-ai-hub/releases.log` (thời gian UTC, tag, digest, người chạy).
   Lỗi ở bất kỳ bước nào: exit ≠ 0, KHÔNG ghi releases.log là thành công, in lệnh rollback.
5. `deploy/rollback.sh <tag-trước>`: deploy lại image cũ; KHÔNG chạy alembic downgrade (chỉ in hướng dẫn,
   downgrade DB phải có người xác nhận).
6. `deploy/check-egress.sh`: gọi được `api.anthropic.com`, `login.microsoftonline.com`, `graph.microsoft.com`,
   `ghcr.io`; một host ngoài allowlist (ví dụ `example.com`) phải BỊ CHẶN. In bảng kết quả, exit ≠ 0 nếu sai.
7. `deploy/check-image-secrets.sh`: `docker history --no-trunc` + trivy secret scan trên 3 image; fail nếu thấy secret.
8. CI: thêm job `deploy-smoke` vào `.github/workflows/ci.yml` (khớp quy tắc bảo mật đã có trong PR-C:
   action pin SHA, `permissions: contents: read`, không secret, có timeout):
   build image local → tạo chứng chỉ self-signed → env giả (mật khẩu `openssl rand -hex 16`) →
   `docker compose -f infra/compose.prod.yml up -d --wait` → chạy đúng các smoke test của deploy.sh
   (cho phép `--insecure` CHỈ trong job này vì chứng chỉ self-signed) → `down -v`.
   Thêm `shellcheck` cho mọi file trong `deploy/` và `nginx -t` cho cấu hình proxy.
9. Runbook: `docs/runbooks/deploy-vm.md` (cài lần đầu: user `pace`, Docker, thư mục /etc/pace-ai-hub,
   `git clone` qua HTTPS, tạo mật khẩu DB bằng `openssl rand`, đặt PAT GHCR; deploy; rollback; xoay PAT;
   đổi sang deploy key trước khi repo private; đọc log; xử lý /readyz 503) và `docs/runbooks/vm-egress.md`.
   Giá trị thật (domain, IP, đường dẫn) chỉ ghi ở `docs/internal/` (gitignored) hoặc trên VM.
10. Cập nhật docs/traceability.md (INF-01 → INF-01c), ADR-013 Phụ lục A (version Nginx và các tool mới),
    docs/plan/INF-01_STEPS.md (đánh dấu Bước 5 khi PR mở).

Ngoài phạm vi (KHÔNG làm): backup/restore + systemd timer (INF-01b, Phase 4); beat (RUN-01); Entra/redirect URI
(AUTH-01); Wazuh/giám sát (INF-01b); self-hosted runner hay deploy tự động từ GitHub vào mạng nội bộ
(ADR-015/016); sửa code trong apps/* (nếu cần, DỪNG và báo tôi).

## Quy tắc bắt buộc
- Version: tra registry/Docker Hub/GitHub Releases tại thời điểm làm (Nginx, shellcheck, trivy, actions),
  KHÔNG ghi theo trí nhớ. Liệt kê bảng version + digest/SHA trong plan.
- Hỏi tôi trước khi thêm dependency/tool ngoài danh sách trên.
- KHÔNG chạy bất kỳ lệnh nào trên VM thật. Agent chỉ viết script + runbook; người giữ vai DevOps-Sec chạy trên VM
  và gửi output lại.
- Repo PUBLIC (ADR-016): không ghi domain, hostname, IP, tenant ID, đường dẫn backup, token thật vào bất kỳ file
  tracked nào, kể cả mô tả PR và commit message. Chỉ dùng placeholder `*.example.invalid`.
- Không tắt kiểm tra TLS ngoài job `deploy-smoke` (10-security.md).
- Code, commit tiếng Anh, conventional commits + story ID, ví dụ
  `feat(infra): prod compose, pull-based deploy and rollback scripts [INF-01c]`. Không tự merge (ADR-011).

## Plan cần trả về (trước khi code)
1. Kết quả kiểm tra điều kiện trước (PR-B, PR-C, image trên GHCR).
2. Bảng version/digest của image và tool.
3. Danh sách file tạo/sửa.
4. Sơ đồ mạng compose.prod (service nào ở network nào, cổng nào publish).
5. Acceptance criteria Given/When/Then, tối thiểu:
   - Given VM cài theo runbook và có tag trên GHCR, when chạy `deploy.sh <tag>`, then mọi service healthy,
     `/healthz` 200, `/readyz` ready qua HTTPS, web hiển thị, releases.log có dòng mới.
   - Given migration hoặc /readyz lỗi, when deploy.sh chạy, then exit ≠ 0, in lệnh rollback, không ghi thành công.
   - Given bản trước đang chạy, when `rollback.sh <tag-trước>`, then app về image cũ, DB không bị downgrade.
   - Given một máy khác trong mạng nội bộ, when quét cổng VM, then chỉ 80/443 mở.
   - Given egress đã cấu hình, when `check-egress.sh`, then allowlist gọi được, host khác bị chặn.
   - Given PR đổi infra/ hoặc deploy/, when CI chạy, then `deploy-smoke`, shellcheck và `nginx -t` xanh.
   - Given diff của PR, when review, then không có giá trị hạ tầng thật; gitleaks xanh.
6. Câu hỏi còn lại cho chủ dự án/IT (nếu có).
7. Rủi ro và giới hạn.

## Định nghĩa xong (DoD)
- Đã chạy thật và dán output: shellcheck, `nginx -t`, `docker compose -f infra/compose.prod.yml config`,
  link run CI có `deploy-smoke` xanh.
- Mô tả PR có mục "Checklist chạy trên VM" cho DevOps-Sec: cài lần đầu → `check-egress.sh` → `deploy.sh <tag>` →
  quét cổng → `rollback.sh` → `deploy.sh` lại; mỗi bước ghi rõ output mong đợi để đối chiếu AC
  (khớp docs/plan/INF-01_STEPS.md, Bước 6).
- Chưa có output thật từ VM thì ghi rõ AC 1–5 "chưa kiểm chứng trên VM", không ghi "done".
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
