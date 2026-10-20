# 01 — Product Requirements Document (PRD)
**Version:** 1.0 | **Owner đề xuất:** PACE DigiTech | **Sponsor:** BOD | **Trạng thái:** Draft for review

## 1. Problem statement
Mỗi phòng ban phải tự xây Flow, tự ghép AI prompts, dữ liệu phân tán theo OneDrive cá nhân; khó quản lý API key, chia sẻ tool, theo dõi chi phí và audit. PACE cần self-service AI Tool Catalog có quản trị trung tâm và bảo vệ dữ liệu theo team.

## 2. Objectives & non-goals
**Mục tiêu:** (O1) người dùng tạo Sales Daily Brief từ template trong ≤10 phút sau khi được cấp quyền; (O2) scheduled run có truy vết; (O3) dùng ngân sách Claude API theo team có giới hạn; (O4) mỗi claim nguồn tin có provenance; (O5) báo cáo được duyệt trước khi gửi bên ngoài team.
**Không thuộc MVP:** AI tự viết/chạy code; workflow canvas kiểu n8n; crawler vượt paywall; arbitrary URLs nội bộ; fine-tuning; BYOK tự phục vụ; chatbot đọc toàn bộ tenant; gửi email khách hàng tự động; cross-team sharing dữ liệu mặc định.

## 3. Personas
- **Employee:** tạo tool cá nhân, chọn nguồn, chạy thử, xem brief.
- **Team Admin:** chia sẻ tool, quản lý quota và recipients, duyệt phát hành.
- **IT Platform Admin:** connector, secrets, model, budgets, monitoring, policies.
- **Approver / BOD:** xem báo cáo, xác minh nguồn, phê duyệt hành động.
- **Auditor:** xem run/audit metadata theo quyền, không được xem secret.

## 4. Core user journeys
1. Entra SSO → chọn Personal hoặc Team Workspace → chọn Sales Intelligence template → nhập thị trường, danh sách khách hàng/đối thủ, RSS feeds/Google Alerts mailbox đã được cấp quyền → xem nguồn → chọn 08:30 Asia/Ho_Chi_Minh → preview → lưu Draft → Publish sau approval.
2. Scheduler → collect feeds/authorized mailbox → normalize → dedupe theo canonical URL/hash → select time window (24h; Monday since Friday morning per configurable policy) → classify Customer/Competitor/Market → Claude phân tích có nguồn → validate JSON → render → review → send approved recipients → archive → log usage.
3. Team Admin → tạo quota tháng + per-run → chọn pool ngân sách → cấp quyền use tool (không lộ key) → dashboard chi phí → suspend tool.
4. Người dùng → Weekly Review từ brief đã được duyệt → Action Plan có owner, deadline, evidence → approval trước khi xuất email.

## 5. Functional requirements (MoSCoW)
| ID | Priority | Requirement | Acceptance |
|---|---|---|---|
| FR-01 | Must | Entra SSO và workspace membership | Non-member nhận 403; offboard thu hồi session |
| FR-02 | Must | Tool templates, draft/publish/version | Publish tạo immutable version; rollback được |
| FR-03 | Must | RSS và Google Alerts qua dedicated mailbox được cấp phép | Ingest 20 mẫu; duplicate skip; log lỗi nguồn |
| FR-04 | Must | Scheduled/manual runs | Một scheduled slot không tạo 2 successful runs; timezone rõ |
| FR-05 | Must | Claude Gateway chỉ backend gọi | Browser không thấy API key; deny vượt quota |
| FR-06 | Must | Citation/provenance | 100% claims sự kiện trong brief liên kết source ID + URL |
| FR-07 | Must | Structured report & evidence | 3 nhóm, max 5 tin/nhóm, [Sự kiện]/[Suy luận], thiếu tin ghi rõ |
| FR-08 | Must | HTML preview + Outlook dispatch qua integration được duyệt | Recipient allowlist; trạng thái send + retry |
| FR-09 | Must | Team quota & usage ledger | Reservation/reconciliation; dashboard team |
| FR-10 | Must | Audit & approval | Publish/send/credential operations đều có audit |
| FR-11 | Should | SharePoint library archive | Có URL tài liệu, version, team permissions |
| FR-12 | Should | Weekly Review & Action Plan | Từ approved briefs, không tự tạo nguồn mới |
| FR-13 | Should | Outlook Calendar reminders | Chỉ calendar được người dùng/admin ủy quyền |
| FR-14 | Could | Public template catalog | Share template-only, no private data |

## 6. Sales Intelligence output contract
DailyBrief: date/timezone, 3 key takeaways, reminders today + next 2 days, customer[], competitor[], market[], suggested_actions[], sources[], status, generated_at, reviewed_by. Mỗi item: title, summary_fact, inference, relevance, confidence_label (không ngụ ý xác suất chuẩn), source_ids, source_urls, published_at. Giới hạn 5 item/category; không có tin => 'Không có cập nhật đáng kể'. Tiếng Việt, giữ thuật ngữ chuyên môn. Báo cáo email ngắn tối đa 500 từ; bản archive có thể chi tiết hơn. Weekly Review và Action Plan dùng approved evidence, tách nhận định khỏi quyết định.

## 7. Business rules
- Không quét hộp thư cá nhân rộng; mailbox/label/folder hoặc nguồn có allowlist; consent đúng phạm vi.
- Dedupe per source item canonical URL + content hash, thêm cross-source similarity review; không gộp các URL khác nếu chưa đủ chắc chắn.
- Monday window: 08:00 thứ Sáu → giờ chạy thứ Hai (cấu hình rõ), ngày khác rolling 24h; DST timezone IANA.
- Không tự gửi email khách hàng hoặc ghi CRM trong MVP.
- Source data được coi là untrusted; prompt injection không thể thay đổi tool policy.
- Workspace visibility: personal/private, team membership, organization template only; tool sharing ≠ data sharing ≠ credential sharing.
- Người duyệt có thể reject và yêu cầu regenerate; regenerate tạo report revision, không overwrite approved record.

## 8. NFR / SLO targets (đề xuất, xác nhận trong POC)
- 95% scheduled runs hoàn thành trong cửa sổ 30 phút; >99% platform uptime trong giờ làm việc (pilot); RPO ≤24h, RTO ≤8h.
- 100% secret không nằm trong UI/log; 100% server endpoints tenant/workspace authorized; HTTPS; encrypt at rest; backup encrypted.
- Max 2 concurrent AI calls/team (configurable); p95 UI API ≤1s không gồm job execution; retry backoff + DLQ.
- Dữ liệu giữ 90 ngày cho raw content và 365 ngày cho audit **đề xuất**, phụ thuộc chính sách PACE và pháp lý; PII minimization/redaction.

## 9. Success metrics & gates
- ≥3 team pilot; ≥10 users; ≥30 runs; ≥95% scheduled success; ≥90% claims có URL kiểm chứng (target production 100%); zero unauthorized cross-team read; usage cost ≤ approved budget; Sales chấm ≥4/5 usefulness trên ≥20 briefs.
- BOD quyết định GO/NO-GO sau POC dựa trên KPI, security review, license/cost verified.

## 10. Dependencies / open questions
Team Claude Console credits và billing; Graph delegated/application permission policy; mailbox strategy; whether Power Automate shared service account permitted; SharePoint library taxonomy; expected sources/users/runs; retention; classification; cost ceiling; approved recipients.
