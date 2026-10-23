# INF-01 (Phase 1): checklist từng bước

> Chủ dự án duyệt ngày 22/10/2026. Đánh dấu `[x]` khi xong và ghi link PR hoặc bằng chứng bên cạnh.
> Repo đang PUBLIC (ADR-016): không ghi domain, hostname, IP, tenant ID, token thật vào file này. Giá trị thật để ở `docs/internal/` (gitignored) hoặc trên VM.
> Prompt Antigravity của từng bước: `KICKOFF_PROMPTS.md`, mục Phase 1.

Đã xong trước khi có checklist này: INF-01a PR-A (residoken-wq/pace-aihub#2), prompt PR-B/PR-C (#3), LICENSE (#4), ADR-016 (#5).

## Bước 0: Quyết định và bàn giao (Chủ dự án, IT)
Đã chốt ngày 22/10/2026:

| # | Quyết định | Lựa chọn |
|---|---|---|
| 0.1 | Token để VM kéo image từ GHCR (package private) | PAT chỉ quyền đọc package, tạo từ tài khoản `residoken-wq`, xoay 90 ngày. Thay bằng token của organization khi chuyển repo (ADR-016) |
| 0.2 | VM lấy code deploy | `git clone` qua HTTPS không xác thực, chỉ chạy được khi repo còn public. **Phải đổi sang deploy key chỉ đọc trước khi repo chuyển private** (ADR-016, checklist chuyển repo) |
| 0.3 | TLS và reverse proxy | IT cấp chứng chỉ, proxy dùng **Nginx** (không dùng ACME) |
| 0.4 | PostgreSQL | Chạy chung VM với app. Đổi sang VM riêng chỉ cần đổi `PACE_DATABASE_URL` |
| 0.5 | Kiểu deploy | DevOps-Sec chạy tay `deploy.sh <tag>` (chưa dùng systemd timer) |
| 0.6 | IT bàn giao VM | Đã bàn giao đủ: VM, domain nội bộ, chứng chỉ TLS, egress allowlist, tài khoản deploy, nơi lưu backup |

- [ ] Giá trị thật của bàn giao IT đã ghi vào `docs/internal/` (không commit).

## Bước 1: PR-B, dựng khung `apps/web` (FE/UI + Antigravity)
- [ ] Chạy prompt "PR-B" (Planning mode).
- [ ] Duyệt plan, kiểm tra:
  - có bảng phiên bản tra từ registry;
  - không làm phần của UI-00 (tokens, AppShell, next-intl) và AUTH-01;
  - có AC Given/When/Then.
- [ ] PR có output thật: lint, typecheck, vitest, build, compose, Playwright; screenshot 1440px và 390px.
- [x] Merge vào `main`. PR: #7 (residoken-wq/pace-aihub#7)

## Bước 2: PR-C, CI/CD (Fullstack/DevOps-Sec + Antigravity)
- [x] Chỉ chạy prompt "PR-C" **sau khi PR-B đã merge** (PR #7 đã merge ngày 22/10/2026).
- [x] Duyệt plan, kiểm tra:
  - có bảng action kèm commit SHA;
  - không dùng `pull_request_target`, không dùng `paths:` ở cấp workflow;
  - gitleaks dùng bản CLI, không dùng action.
- [ ] PR có:
  - link một lần chạy CI xanh;
  - test tích hợp chạy thật, log ghi **0 skipped**;
  - output gitleaks chạy local bắt được secret giả.
- [ ] Merge vào `main`. PR: ____

## Bước 3: Cài đặt GitHub sau khi merge PR-C (Chủ dự án)
- [ ] Branch protection cho `main`: bắt buộc PR, 1 review, đúng tên các check bắt buộc, cấm force-push.
- [ ] Bật secret scanning và push protection.
- [ ] Actions: yêu cầu duyệt workflow từ fork; quyền mặc định của workflow là read.
- [ ] Sau lần chạy `build.yml` đầu tiên: đặt 3 package GHCR (api, worker, web) sang **private**.
- [ ] Tạo PAT chỉ đọc package (quyết định 0.1); ghi ngày hết hạn ở `docs/internal/`.
- [ ] Ghi lại tag `sha-xxxxxxx` đầu tiên trên GHCR: ____

## Bước 4: Chuẩn bị VM (Fullstack/DevOps-Sec + IT; làm song song với Bước 5)
- [ ] Tạo user `pace` không phải root; cài Docker.
- [ ] Tạo `/etc/pace-ai-hub/`, quyền `root:pace 0640`.
- [ ] Đặt chứng chỉ TLS vào `/etc/pace-ai-hub/tls/`.
- [ ] Firewall egress theo allowlist của ADR-010.
- [ ] `git clone` repo qua HTTPS (quyết định 0.2).
- [ ] Đặt PAT vào `/etc/pace-ai-hub/ghcr.token` (quyền 0600).
- Runbook chi tiết của bước này có trong PR INF-01c (`docs/runbooks/deploy-vm.md`).

## Bước 5: INF-01c, walking skeleton (Fullstack/DevOps-Sec + Antigravity)
- [ ] Chạy prompt "INF-01c". Agent phải xác nhận đủ 3 điều kiện trước: có `apps/web`, có `ci.yml` và `build.yml`, có image trên GHCR.
- [ ] Duyệt plan, kiểm tra plan dùng đúng các quyết định ở Bước 0.
- [ ] PR có:
  - job `deploy-smoke` và shellcheck xanh;
  - không có domain, IP, token thật trong diff;
  - có mục "Checklist chạy trên VM".
- [ ] Merge vào `main`. PR: ____

## Bước 6: Chạy thật trên VM (Fullstack/DevOps-Sec; Claude hoặc QA đối chiếu)
- [ ] `check-egress.sh`: host trong allowlist gọi được, host ngoài bị chặn (AC-5).
- [ ] `deploy.sh <tag>`: mọi service healthy, `/healthz` và `/readyz` qua HTTPS ổn, web hiển thị (AC-1).
- [ ] Quét cổng VM từ một máy khác trong mạng: chỉ 80 và 443 mở (AC-4).
- [ ] `rollback.sh <tag-trước>` rồi `deploy.sh` lại: app về bản cũ, DB giữ nguyên (AC-3).
- [ ] Gửi output (đã che giá trị nội bộ) để đối chiếu AC 1–5.

## Bước 7: Đóng phần INF-01 của Phase 1 (BA-PO/QA)
- [ ] Cập nhật `docs/traceability.md`: INF-01a và INF-01c xong; TLS hardening, backup và giám sát còn lại cho INF-01b (Phase 4).
- [ ] Chạy `/pace-story-done` cho INF-01 (một phần).
- [ ] Chuyển sang DB-01, AUTH-01, UI-00. AUTH-01 cần chốt thời hạn session trước (HANDOFF mục 6.7).
