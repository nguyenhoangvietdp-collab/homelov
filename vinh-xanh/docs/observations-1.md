# Rà soát hiển thị & tương tác — đợt 1 (08/10/2026)

Cách kiểm tra: Playwright với thao tác thật (click chuột trên desktop 1400×900; chạm thật với hasTouch + isMobile trên điện thoại 390×844), so thông tin thẻ hiện ra với dữ liệu của lô được chạm.

## Quan sát
| # | Loại | Lỗi | Nguyên nhân gốc | Mức độ | Đã sửa |
|---|---|---|---|---|---|
| OBS-1 | Dữ liệu ↔ code | Chạm lô hiện thông tin lô bên cạnh (shophouse hiện "đơn lập", VX3-52 hiện như lô thường); lô đầu tiên không chạm được | `select()` tra `LOTS[id-1]` nhưng lots.json dựng lại từ keyplan đánh id từ 0; `if(state.sel)` coi id 0 là "chưa chọn" | Chặn | Tra theo `Map` id→lô, so `!= null` |
| OBS-2 | Bố cục điện thoại | Trên điện thoại thật trang bị rộng 533px thay vì 390px: trình duyệt thu nhỏ trang, thanh thông tin ở đáy nằm ngoài màn hình, không bấm được | Cột lưới `1fr` co theo hàng chip lọc không xuống dòng (min-content) | Chặn | `minmax(0,1fr)` cho cột/hàng lưới, `min-width:0` cho hàng chip |
| OBS-3 | Tương tác | Kéo bản đồ có thể trôi mất hẳn khỏi màn hình | Không giới hạn khung nhìn | Giảm chất lượng | Giới hạn tâm khung nhìn trong vùng phân khu |
| OBS-4 | Hiển thị | Khung giá phóng to theo bản đồ và che lô khi xem gần; không có đường nối từ khung tới lô (VX5-124/126 nằm xa lô) | Khung giá vẽ theo tọa độ bản đồ | Giảm chất lượng | Ẩn khung khi phóng gần; thêm đường dẫn; điện thoại dùng nhãn mã căn gọn cạnh lô |
| OBS-5 | Hiển thị | Lọc loại hình nhưng khung giá của loại đã ẩn vẫn hiện | Bộ lọc chỉ làm mờ ô lô | Thẩm mỹ | Ẩn khung/dot/đường dẫn theo bộ lọc |
| OBS-6 | Ảnh nền | Vùng dưới các khung giá cũ nhòe cầu vồng, lộ ra khi khung ẩn | Inpaint vùng lớn | Thẩm mỹ | Góc dưới trái vẽ lại theo keyplan; vùng sông nối dải theo hướng sông + vân lấy từ bờ sông sạch |
| OBS-7 | Tương tác | Chụm 2 ngón không kéo theo ngón tay; nhấc 1 ngón thì không kéo tiếp được; ô tìm kiếm giữ bàn phím sau khi tìm; đóng mặt bằng không trả focus | Thiếu xử lý | Thẩm mỹ | Đã sửa |

## Kết quả sau sửa
5/5 lô thử (đơn lập DL1-02, shophouse SH1, cặp ghép VX1-81/83, VX3-52, đơn lập góc DL1-06) chạm đúng trên cả máy tính và điện thoại; không lỗi JS.

## Bài học (knowledge)
- know-001: Kiểm thử bằng gọi hàm (`select(id)`) che mất lỗi ánh xạ id. Luôn kiểm thử bằng thao tác thật và so dữ liệu thẻ với lô được chạm.
- know-002: Mô phỏng điện thoại phải bật `isMobile` + `hasTouch`; viewport thường không lộ lỗi trang rộng hơn màn hình.
- know-003: Sau mỗi lần dựng lại dữ liệu lô, kiểm tra quy ước id (0 hay 1) với code giao diện.
