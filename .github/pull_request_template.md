## Story ID
<!-- Ví dụ: INF-01, AUTH-01, GW-01 -->


## Tóm tắt
<!-- Mô tả ngắn gọn mục đích và bối cảnh thay đổi -->


## Thay đổi chi tiết
<!-- Danh sách các thành phần, file, hoặc logic đã thay đổi -->


## Acceptance Criteria & Tests tương ứng
<!-- Liệt kê AC dạng Given/When/Then và test case kiểm chứng tương ứng -->
- [ ] **AC-1**: Given ... When ... Then ... (Test: `...`)
- [ ] **AC-2**: Given ... When ... Then ... (Test: `...`)


## Bằng chứng kiểm tra (Real Output)
<!-- Dán output THẬT của các lệnh kiểm tra (che thông tin mật/môi trường dev) -->
```text

```


## Checklist An toàn & Bảo mật (ADR-015, ADR-016)
- [ ] Không có secret, private key, token, API key trong diff hoặc commit history
- [ ] Không có hostname, IP nội bộ, URL staging/prod nội bộ trong tracked files
- [ ] Không có Tenant ID, Client ID, email thật, hay dữ liệu khách hàng thật
- [ ] Đã kiểm tra git diff trước khi commit


## Checklist Definition of Done (60-quality-gates.md)
- [ ] Linting & code formatting pass (ruff / eslint)
- [ ] Static type check pass (mypy / tsc)
- [ ] Unit & integration tests pass (0 skipped đối với các test bắt buộc)
- [ ] Build thành công (Docker image / standalone Next.js)
- [ ] Cập nhật tài liệu liên quan (`docs/traceability.md`, ADR, runbooks nếu có)


## Chưa kiểm chứng
<!-- Những gì nằm ngoài phạm vi hoặc chưa thể kiểm tra ở bước này -->
- [ ] Tuân thủ ADR-011: PR này được mở để người phê duyệt duy nhất xem xét và merge, không tự merge.
