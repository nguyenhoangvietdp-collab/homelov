# Bản đồ tương tác top-down phân khu Vịnh Xanh (Ocean Park 3)

Ghi nhận ngày 08/10/2026. Đây là bản bóc tách để anh/chị chốt lại, chưa phải thiết kế cuối.

## 1. Yêu cầu theo cách tôi hiểu

Xây một **bản đồ nhìn từ trên xuống (2D, top-down)** của phân khu Vịnh Xanh thuộc Ocean Park 3 (Ocean City), dùng **trong lúc tư vấn bán hàng**. Sale (hoặc khách) chạm vào một lô/dãy/tiện ích trên bản đồ để thấy ngay thông tin kỹ thuật của nó, thay cho việc lật ảnh marketing và bảng hàng Excel.

Tài liệu hiện có (5 ảnh trong thư mục HomeLov, bảng hàng ngày 03/09/2026):

- Ảnh mặt bằng "Quỹ độc quyền phân khu Vịnh Xanh": 5 trục đường Vịnh Xanh 1 đến 5 (lộ giới 13m), Đại lộ Hừng Đông (25m), sông chạy phía Bắc và Đông, công viên có tiện ích đánh số, la bàn và key plan.
- Bảng hàng có 5 căn Vịnh Xanh: VX2-19 (xẻ khe), VX3-52, VX5-124, VX5-126 (song lập), VX3-87 (đơn lập góc), kèm hướng, kích thước, DT đất, DT xây dựng, giá TTS và giá HTLS 18/24/30/36 tháng, ngân hàng, quà tặng.
- Mặt bằng tổng OCP3 cho biết vị trí Vịnh Xanh trong đại đô thị (khối Đông Bắc, giáp sông). Ảnh OCP2 không thuộc phạm vi này.

## 2. Sổ đăng ký các hạng mục (Y1, Y2…)

| # | Hạng mục | Đánh giá | Lý do | Đề xuất |
|---|---|---|---|---|
| Y1 | Bản đồ phân lô Vịnh Xanh vẽ lại dạng vector, chạm vào lô để xem mã căn, loại hình, hướng, kích thước, DT đất, DT xây dựng | Cốt lõi | Đây chính là "hiển thị rõ nét cấu trúc nhìn từ trên xuống" | Làm trước |
| Y2 | Tô màu lô theo trạng thái (đang bán / đã bán / quỹ độc quyền) và giá, lấy từ bảng hàng | Sắc hơn | Giúp khách quyết định chọn căn ngay trên bản đồ, dữ liệu đã có | Gộp vào Y1 |
| Y3 | Lớp thông số quy hoạch (lộ giới đường, chỉ giới xây dựng, mật độ, tầng cao, khoảng lùi) | Tùy | Đúng nghĩa "kỹ thuật", nhưng cần bản vẽ 1/500 của CĐT; ảnh marketing không đủ chính xác | Làm nếu có nguồn chính thức |
| Y4 | Lớp hạ tầng kỹ thuật thật (cấp thoát nước, điện, cao độ nền) | Rộng hơn | Khách mua ít khi quyết định dựa trên đó, dữ liệu khó có | Để giai đoạn sau |
| Y5 | Khoảng cách từ lô đến sông, công viên, trường, Mega Complex; tia hướng/view | Sắc hơn | Trả lời câu hỏi khách hỏi nhiều nhất, tính được từ mặt bằng | Gộp vào Y1 |
| Y6 | Bộ lọc (loại hình, hướng, khoảng giá) và tính dòng tiền HTLS theo kỳ hạn | Tùy | Có ích cho sale, nhưng là công cụ tài chính chứ không phải bản đồ | Bản đơn giản: chỉ hiển thị 4 mức giá đã có |
| Y7 | 3D, bay quanh, mặt bằng từng tầng của căn | Rộng hơn | Tốn công, không cần cho "nhìn từ trên xuống" | Bỏ khỏi phạm vi |

## 3. Sửa lỗi dữ liệu đã phát hiện

- Bảng hàng xếp **VX3-87 (Đơn lập, góc)** dưới tiêu đề nhóm "Biệt thự song lập". Trên bản đồ tôi sẽ để loại hình theo cột "Loại hình" là Đơn lập.
- Ảnh mặt bằng Vịnh Xanh là ảnh render marketing, không có tỉ lệ. Mọi kích thước hiển thị trên bản đồ sẽ lấy từ bảng hàng, không đo từ ảnh.

## 4. Những điểm cần anh/chị chốt

1. **"Cấu trúc kỹ thuật" là gì?** (a) mặt bằng phân lô và thông số lô (gợi ý), (b) thêm thông số quy hoạch 1/500, (c) hạ tầng kỹ thuật thật.
2. **Ai cầm bản đồ?** Sale dùng nội bộ (hiện giá, quỹ, chính sách) hay gửi link cho khách (ẩn bớt thông tin).
3. **Nguồn dữ liệu:** có file mặt bằng 1/500 (CAD hoặc PDF vector) của CĐT không, hay chỉ có ảnh như hiện tại?
4. **Phạm vi lô:** chỉ 5 căn quỹ độc quyền, hay toàn bộ lô Vịnh Xanh (cần danh sách mã căn đầy đủ)?
5. **Cập nhật giá/trạng thái:** sửa tay khi có bảng hàng mới, hay nối với Google Sheet đang dùng?
6. **Nền tảng:** link web mở trên điện thoại/máy tính bảng (gợi ý), hay file trình chiếu.

## 5. Mặc định tôi sẽ theo nếu chưa có trả lời

Link web xem tốt trên điện thoại, bản đồ 2D vẽ lại từ ảnh mặt bằng Vịnh Xanh, gồm Y1 + Y2 + Y5, dữ liệu 5 căn trong bảng hàng 03/09/2026, chế độ nội bộ cho sale.
