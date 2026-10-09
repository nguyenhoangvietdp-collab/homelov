# HomeLov

Tài liệu bán hàng tương tác cho các dự án bất động sản.

## vinh-xanh/

Sơ đồ tương tác phân khu Vịnh Xanh, Ocean Park 3. Mở `vinh-xanh/ban-do-vinh-xanh.html` trong trình duyệt. Chạm vào một lô để xem mã căn, diện tích, mẫu nhà và chính sách bán hàng.

| Thư mục | Nội dung |
|---|---|
| `ban-do-vinh-xanh.html` | Bản đồ đã dựng, một file tự chứa (ảnh nền, dữ liệu, mặt bằng mẫu nhà nhúng sẵn) |
| `build/` | `v3.py` ghép `template2.html` + `lots.json` + `base.jpg` + `pdf/fp_*.jpg` thành file HTML |
| `floorplan/` | Dựng lại mặt bằng 7 mẫu nhà từ PDF vector của CĐT thành SVG/DXF (`extract.py`), trang xem cho kỹ sư (`build_viewer.py` ra `viewer.html`). `data/` là đầu vào của `build/v3.py` |
| `pipeline/` | Các bước dựng khung lô từ tổng mặt bằng CĐT, `data/` là kết quả trung gian |
| `source/` | Tổng mặt bằng phân khu Vịnh Xanh của chủ đầu tư (8000 px) |
| `qa/` | Script Playwright kiểm tra chạm lô trên máy tính và điện thoại |
| `docs/` | Yêu cầu ban đầu và ghi chú rà soát lỗi |

### Dựng lại bản đồ

```bash
cd vinh-xanh/build && python3 v3.py        # ra ban-do-vinh-xanh.html
```

### Dựng lại mặt bằng mẫu nhà

```bash
cd vinh-xanh/floorplan
PYTHONUTF8=1 python extract.py <thư mục chứa các PDF HL-*.pdf> [--dxf]   # cần pymupdf, numpy, opencv-python-headless (và ezdxf nếu --dxf)
PYTHONUTF8=1 python build_viewer.py                                      # ra viewer.html
```

`extract.py` hiệu chỉnh tỉ lệ bằng ranh đất và đối chiếu diện tích từng tầng với bảng của CĐT; kết quả kiểm tra nằm ở `report.json`. Sau đó dựng lại bản đồ như bên dưới.

### Dựng lại khung lô từ tổng mặt bằng

Chạy trong một thư mục làm việc có `new_full.jpg` (bản sao của `source/mat-bang-phan-khu-vinh-xanh.jpg`) và các file trong `pipeline/data/`:

1. `ocrfull.py`: đọc vị trí mã căn trên toàn ảnh, ra `ocrfull.json` (cần `rapidocr_onnxruntime`).
2. `ws.py`: tách vùng màu của bốn loại nhà.
3. `grid.py`: cắt từng dãy thành lô theo vạch chia; bề ngang lô theo diện tích in trên mặt bằng chia cho chiều sâu dãy, chừa khe xẻ; ra `grid_lots.json`.
4. `ocrarea_all.py`: đọc diện tích in tại mỗi mã căn, ra `area_all.json`.
5. `merge.py`: chuyển khung về toạ độ bản đồ (`old2new.npy`) và gắn dữ liệu cũ theo mã căn, ra `lots.json`. Chép file này vào `build/`.

Kết quả hiện tại: 747 lô, khớp số căn CĐT công bố (song lập 278, nhà vườn 169, đơn lập 115, shophouse 185).

### Nguồn số liệu

Mã căn, diện tích, lộ giới và tiện ích theo tổng mặt bằng của chủ đầu tư (Đại lộ Bốn Mùa 25 m, Hừng Đông 25 m). Khoảng giá và mật độ xây dựng theo vinhomesland.vn, mang tính tham khảo. Chính sách bán hàng theo văn bản của chủ đầu tư.
