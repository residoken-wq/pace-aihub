# PACE AI Hub — Solution Blueprint v1.0
**Ngày:** 20/10/2026 · **Trạng thái:** Đề xuất để phê duyệt thiết kế; chưa triển khai · **Use case chuẩn:** Sales Intelligence

## Bộ bàn giao
1. [01_PRD.md](01_PRD.md) — PRD, persona, user stories, acceptance criteria, business rules.
2. [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md) — architecture, sequence, integrations, threat model, operations.
3. [03_DATABASE_SCHEMA.sql](03_DATABASE_SCHEMA.sql) — PostgreSQL DDL, khóa, index, RBAC, quotas, audit.
4. [04_API_GATEWAY.md](04_API_GATEWAY.md) — API contract, credits, metering, reservations, security.
5. [05_UI_UX_SPEC.md](05_UI_UX_SPEC.md) — IA, screens, flows, states, accessibility.
6. [06_MVP_BACKLOG.md](06_MVP_BACKLOG.md) — epics, priorities, estimates, DoD, rollout.
7. [07_DECISIONS_AND_TESTS.md](07_DECISIONS_AND_TESTS.md) — ADR, assumptions, POC gates, test plan.
8. [prototype.html](prototype.html) — clickable browser prototype, illustrative data only.

## Nguồn & giới hạn
- Nguồn nghiệp vụ: `BỘ PROMPT CẤU HÌNH MẪU.docx` (Sales); `PACE_AI_Hub_BOD_Proposal.md` (đề xuất trước đó); `PACE_PowerAutomate_Daily_Briefing_User_Guide.md` (Flow đã thử nghiệm).
- Tài liệu Sales yêu cầu: Google Alerts/email, Outlook Calendar, khung thời gian 24h (thứ Hai tính từ thứ Sáu), 3 nhóm Customer/Competitor/Market, tối đa 5 tin/nhóm, nguồn gốc và nhãn [Sự kiện]/[Suy luận], Daily/Weekly/Action Plan, không bịa nguồn, người dùng phê duyệt.
- Quyết định thiết kế **mới**: Claude API Gateway, team workspace, PostgreSQL, SharePoint library, RBAC, quotas, structured JSON, approval workflow.
- **Chưa xác nhận:** số seat Claude Team, credit entitlement, API price, Microsoft Graph permissions, tenant DLP, premium connector licensing, infrastructure sizing. Không đưa con số marketing/credits chưa xác minh vào ngân sách.
- POC phải xác nhận: Claude Team subscription **không đồng nghĩa** được dùng Claude API miễn phí; chỉ sử dụng credit khi được xác nhận trên Anthropic Console/billing.

## Khuyến nghị phê duyệt
GO có điều kiện cho discovery + POC; chỉ GO MVP sau khi qua security/license/data gates. Không phát hành production dựa trên prototype này.
