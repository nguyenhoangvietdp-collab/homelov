"""Dựng lại mặt bằng mẫu nhà từ PDF vector của chủ đầu tư.

Chạy:  PYTHONUTF8=1 python extract.py <thư mục chứa PDF> [--dxf]
Cần:   pymupdf, numpy, opencv-python-headless, ezdxf (chỉ khi --dxf)

Ra:
  data/<mã mẫu>.json   dữ liệu từng tầng (SVG rút gọn, nhãn, phòng + diện tích, hệ số tỉ lệ). Đây là đầu vào cho build/v3.py.
  out/<mã mẫu>_<tầng>.dxf  (chỉ khi --dxf; đơn vị mét, bị gitignore)
  report.json          kết quả kiểm tra (hiệu chỉnh tỉ lệ, đối chiếu diện tích, phòng nào bị loại và vì sao)
"""
import json, os, re, sys, math, glob
import numpy as np, cv2, pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
# mã mẫu -> (file PDF, kích thước đất rộng x dài (m))
SHEETS = {
    'DL1-02':  ('HL-DL1-02.pdf', (12, 20)),
    'DL1-06':  ('HL-DL1-06 (ĐL góc view sông).pdf', (13, 20)),
    'SL2-01':  ('HL-SL2-01.pdf', (7, 18)),
    'SL2-01G': ('Đập thông_HL-SL2-01 (VX1-81,VX1-83).pdf', (14, 18)),
    'SL2-02':  ('HL-SL2-02 (SL 144m2).pdf', (8, 18)),
    'LK1':     ('HL-LK1-5X18-01.pdf', (5, 18)),
    'SH1':     ('HL-SH1-5.5x20-01.pdf', (5.5, 20)),
}
FLOOR_NAMES = {'1': 'Tầng 1', '2': 'Tầng 2', '3': 'Tầng 3', '4': 'Tầng 4', 'TUM': 'Tầng tum'}
GROUP_LABEL = {'WALL': 'Tường', 'CONC': 'Cột, bê tông', 'DOOR': 'Cửa, ô thoáng', 'FURN': 'Nội thất', 'PATT': 'Hatch, ký hiệu',
               'FINE': 'Chi tiết mảnh', 'STRS': 'Thang, lan can', 'DIMS': 'Kích thước', 'FNSH': 'Hoàn thiện, vân sàn',
               'HIDD': 'Nét khuất', 'OTHER': 'Khác'}
MAP_GROUPS = ['WALL', 'CONC', 'DOOR', 'FURN', 'PATT', 'FINE', 'STRS', 'OTHER']   # bản nhúng vào bản đồ
ROOM_NAMES = {'P. NGỦ': 'Phòng ngủ', 'P.NGỦ': 'Phòng ngủ', 'P.KHÁCH': 'Phòng khách', 'P. KHÁCH': 'Phòng khách', 'BẾP & ĂN': 'Bếp và ăn',
              'P. SHC': 'Phòng sinh hoạt chung', 'P.SHC': 'Phòng sinh hoạt chung', 'P. ĐA NĂNG': 'Phòng đa năng', 'SÂN KT': 'Sân kỹ thuật',
              'WC': 'WC', 'P. THỜ': 'Phòng thờ', 'P.THỜ': 'Phòng thờ', 'P. LÀM VIỆC': 'Phòng làm việc'}
ROOM_RE = re.compile(r'^(P\.|PHÒNG|DỊCH VỤ|BẾP|SÂN|KHO|SẢNH|GARA|LOGIA|BAN CÔNG|KINH DOANH|CỬA HÀNG|SHOP|THANG|TUM|TERRACE|VƯỜN|HIÊN|PHƠI|GIẾNG|SINH HOẠT|ĐA NĂNG|TẬP|THỜ|LÀM VIỆC|ĂN)', re.I)
WC = chr(0x57) + chr(0x43)


def is_room(t):
    return bool(ROOM_RE.match(t)) or t == WC
PX = 4.0        # điểm ảnh trên mỗi pt khi dò phòng


def disp(t):
    """Tên phòng in trên bản vẽ (viết tắt, in hoa) -> tên đọc được."""
    if t in ROOM_NAMES: return ROOM_NAMES[t]
    u = re.sub(r'^P\.\s*', 'PHÒNG ', t.strip())
    return WC if u == WC else u.lower().capitalize().replace(' wc', ' ' + WC)


def group(layer):
    t = (layer or '').split('$')[-1].upper()
    for key, g in (('FNSH', 'FNSH'), ('HIDD', 'HIDD'), ('DIMS', 'DIMS'), ('STRS', 'STRS'), ('RAIL', 'STRS'), ('DOOR', 'DOOR'), ('LITE', 'DOOR'),
                   ('WALL', 'WALL'), ('CONC', 'CONC'), ('COLUMN', 'CONC'), ('FURN', 'FURN'), ('PATT', 'PATT'), ('HATCH', 'PATT'), ('FINE', 'FINE')):
        if key in t: return g
    return 'OTHER'


def hexc(c):
    return '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in c[:3])


def fmt(v):
    s = '%.1f' % v
    return s[:-2] if s.endswith('.0') else s


def pathd(items):
    out = []; cur = None
    def mv(a):
        nonlocal cur
        if cur is None or abs(cur.x - a.x) > .05 or abs(cur.y - a.y) > .05: out.append('M%s %s' % (fmt(a.x), fmt(a.y)))
    for it in items:
        k = it[0]
        if k == 'l': mv(it[1]); out.append('L%s %s' % (fmt(it[2].x), fmt(it[2].y))); cur = it[2]
        elif k == 'c':
            mv(it[1]); out.append('C%s %s %s %s %s %s' % tuple(fmt(v) for v in (it[2].x, it[2].y, it[3].x, it[3].y, it[4].x, it[4].y))); cur = it[4]
        elif k == 're':
            r = it[1]; out.append('M%s %sh%sv%sh%sz' % (fmt(r.x0), fmt(r.y0), fmt(r.width), fmt(r.height), fmt(-r.width))); cur = None
        elif k == 'qu':
            q = it[1]; out.append('M%s %sL%s %sL%s %sL%s %sz' % tuple(fmt(v) for v in (q.ul.x, q.ul.y, q.ur.x, q.ur.y, q.lr.x, q.lr.y, q.ll.x, q.ll.y))); cur = None
    return ''.join(out)


def polylines(items, steps=8):
    res = []; cur = []
    for it in items:
        k = it[0]
        if k == 'l':
            a, b = (it[1].x, it[1].y), (it[2].x, it[2].y)
            if cur and math.hypot(cur[-1][0] - a[0], cur[-1][1] - a[1]) < .05: cur.append(b)
            else:
                if len(cur) > 1: res.append(cur)
                cur = [a, b]
        elif k == 'c':
            p = it[1:5]
            if len(cur) > 1: res.append(cur)
            cur = []
            for i in range(steps + 1):
                t = i / steps; u = 1 - t
                cur.append((u**3*p[0].x + 3*u*u*t*p[1].x + 3*u*t*t*p[2].x + t**3*p[3].x, u**3*p[0].y + 3*u*u*t*p[1].y + 3*u*t*t*p[2].y + t**3*p[3].y))
        elif k in ('re', 'qu'):
            if len(cur) > 1: res.append(cur)
            cur = []
            if k == 're': r = it[1]; res.append([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)])
            else: q = it[1]; res.append([(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y), (q.ul.x, q.ul.y)])
    if len(cur) > 1: res.append(cur)
    return res


def text_lines(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ''.join(s['text'] for s in ln['spans']).strip()
            if t: out.append((pymupdf.Rect(ln['bbox']), t, ln['spans'][0]['size']))
    return out


def find_floors(lines):
    """Tìm các tiêu đề 'MẶT BẰNG TẦNG n' -> {khóa tầng: rect tiêu đề}."""
    ft = {}
    for r, t, _ in lines:
        m = re.match(r'MẶT BẰNG TẦNG\s+(TUM|\d)', t)
        if m: ft[m.group(1)] = r
    return ft


def floor_regions(ft, kp_x=None):
    """Chia trang thành vùng cho từng tầng: theo hàng (trên/dưới) và cột (cắt giữa hai tiêu đề kề nhau)."""
    ys = sorted({round(r.y0) for r in ft.values()})
    rows = [[k for k, r in ft.items() if abs(r.y0 - y) < 6] for y in ys]
    regs = {}
    top = 150
    for i, row in enumerate(rows):
        row.sort(key=lambda k: ft[k].x0)
        y1 = min(ft[k].y0 for k in row) - 1
        cs = [(ft[k].x0 + ft[k].x1) / 2 for k in row]
        for j, k in enumerate(row):
            x0 = 40 if j == 0 else (cs[j - 1] + cs[j]) / 2
            x1 = 935 if j == len(row) - 1 else (cs[j] + cs[j + 1]) / 2
            x1 = min(x1, 935)
            if kp_x and top > 400: x1 = min(x1, kp_x)   # hàng dưới: bỏ khung keyplan bên phải
            regs[k] = pymupdf.Rect(x0, top, x1, y1)
        top = max(ft[k].y1 for k in row) + 1   # hàng dưới bắt đầu ngay dưới tiêu đề hàng trên
    return regs


def parse_areas(lines):
    """Bảng THÔNG SỐ (m²): 'TỔNG DIỆN TÍCH SÀN' và từng tầng."""
    res = {}
    for r, t, _ in lines:
        m = re.fullmatch(r'TẦNG\s+(TUM|\d)', t)
        if m and r.x0 > 900:
            for r2, t2, _ in lines:
                if r2.x0 > 1050 and abs((r2.y0 + r2.y1) / 2 - (r.y0 + r.y1) / 2) < 5 and re.fullmatch(r'\d+[.,]?\d*', t2):
                    res[m.group(1)] = float(t2.replace(',', '.'))
        if t.startswith('TỔNG DIỆN TÍCH'):
            for r2, t2, _ in lines:
                if r2.x0 > 1050 and abs((r2.y0 + r2.y1) / 2 - (r.y0 + r.y1) / 2) < 5 and re.fullmatch(r'\d+[.,]?\d*', t2): res['total'] = float(t2.replace(',', '.'))
    return res


def door_boxes(rows, k):
    """Gom các nét của cùng một cửa (cánh + cung quét) thành hộp bao; hộp dùng để bịt ô cửa khi dò phòng."""
    rs = [pymupdf.Rect(dr['rect']) + (-1.5, -1.5, 1.5, 1.5) for g, dr in rows if g == 'DOOR']
    boxes = []
    for r in rs:
        r = pymupdf.Rect(r); merged = True
        while merged:
            merged = False
            for b in boxes:
                if r.intersects(b): r |= b; boxes.remove(b); merged = True; break
        boxes.append(r)
    return [b for b in boxes if max(b.width, b.height) <= 2.4 * k]


def struct_mask(rows, W, H, ox, oy, k):
    """Ảnh nhị phân của các nét ngăn phòng: tường, cột, thang/lan can, hộp cửa."""
    m = np.zeros((H, W), np.uint8)
    for g, dr in rows:
        if g not in ('WALL', 'CONC', 'STRS', 'DOOR'): continue
        for pl in polylines(dr['items']):
            pts = np.array([[(x - ox) * PX, (y - oy) * PX] for x, y in pl], np.int32)
            cv2.polylines(m, [pts], False, 255, 2)
            if g != 'DOOR' and dr.get('fill') and len(pts) > 2: cv2.fillPoly(m, [pts], 255)
    for b in door_boxes(rows, k):
        cv2.rectangle(m, (int((b.x0 - ox) * PX), int((b.y0 - oy) * PX)), (int((b.x1 - ox) * PX), int((b.y1 - oy) * PX)), 255, -1)
    return m


def seal_envelope(m, k):
    """Bịt các ô cửa sổ/ô thoáng ở tường ngoài: đóng hình thái học cỡ lớn để lấy đường bao công trình, rồi vẽ đường bao đó vào ảnh."""
    ks = int(3.0 * k * PX) | 1
    big = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ks, ks)))
    n, lab = cv2.connectedComponents((big == 0).astype(np.uint8), connectivity=4)
    bl = np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])); bl = bl[bl != 0]
    outside = np.isin(lab, bl)
    inside = (~outside).astype(np.uint8) * 255
    ring = cv2.morphologyEx(inside, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8))
    return cv2.bitwise_or(m, ring)


def detect_rooms(rows, labels, box, k, floor_area):
    """Dò phòng bằng cách loang từ vị trí nhãn. Trả về (danh sách phòng, danh sách phòng bị loại kèm lý do)."""
    ox, oy = box.x0, box.y0
    W, H = int(box.width * PX) + 2, int(box.height * PX) + 2
    m = struct_mask(rows, W, H, ox, oy, k)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = seal_envelope(m, k)
    free = (m == 0).astype(np.uint8)
    n, lab = cv2.connectedComponents(free, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])))
    groups = {}
    skipped = []
    for lb in labels:
        x, y = int((lb['x'] - ox) * PX), int((lb['y'] - oy) * PX)
        if not (0 <= x < W and 0 <= y < H): continue
        # nhãn thường đè lên nét nội thất, không đè lên tường; nếu rơi vào nét thì dò quanh vài px
        c = 0
        for dx, dy in [(0, 0)] + [(a, b) for a in (-6, 0, 6) for b in (-6, 0, 6)]:
            xx, yy = min(max(x + dx, 0), W - 1), min(max(y + dy, 0), H - 1)
            if lab[yy, xx] != 0 and free[yy, xx]: c = lab[yy, xx]; break
        if c == 0: skipped.append((lb['t'], 'nhãn nằm trên nét tường')); continue
        groups.setdefault(int(c), []).append(lb)
    rooms = []
    for c, lbs in groups.items():
        reg = (lab == c).astype(np.uint8)
        area_px = int(reg.sum()); area = area_px / (PX * PX) / (k * k)
        names = [x['t'] for x in lbs]
        if c in border: skipped.append((' + '.join(names), 'vùng loang chạm mép khung (hở tường ngoài)')); continue
        if area > .35 * floor_area: skipped.append((' + '.join(names), 'vùng quá lớn so với diện tích tầng (nghi thông sang phòng khác)')); continue
        if area < 1.0: skipped.append((' + '.join(names), 'vùng quá nhỏ')); continue
        cnts, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(cnts, key=cv2.contourArea)
        sol = cv2.contourArea(cnt) / max(cv2.contourArea(cv2.convexHull(cnt)), 1)
        if sol < .9: skipped.append((' + '.join(names), 'hình dạng không gọn (độ đặc %.2f), nghi lẫn cầu thang hoặc phòng kề' % sol)); continue
        cnt = cv2.approxPolyDP(cnt, 1.5, True)
        poly = [[round(p[0][0] / PX + ox, 1), round(p[0][1] / PX + oy, 1)] for p in cnt]
        rooms.append({'names': names, 'area': round(area, 1), 'poly': poly, 'combined': len(lbs) > 1,
                      'lx': round(sum(l['x'] for l in lbs) / len(lbs), 1), 'ly': round(sum(l['y'] for l in lbs) / len(lbs), 1)})
    return rooms, skipped


def process(key, pdf_path, land, want_dxf, dxf_dir):
    d = pymupdf.open(pdf_path); page = d[0]
    lines = text_lines(page)
    ft = find_floors(lines)
    kps = [r.x0 for r, t, _ in lines if t in ('MẪU ĐỐI XỨNG', 'VỊ TRÍ CÔNG TRÌNH', 'MẪU GỐC')]
    regs = floor_regions(ft, min(kps) - 32 if kps else None); areas = parse_areas(lines)
    drs = page.get_drawings()
    rep = {'floors': {}, 'issues': []}
    # --- hiệu chỉnh tỉ lệ từ ranh đất (nét khuất A-HIDD) của tầng 1 so với kích thước đất đã biết
    R1 = regs['1']
    hid = pymupdf.Rect(1e9, 1e9, -1e9, -1e9)
    for dr in drs:
        if group(dr.get('layer')) == 'HIDD' and R1.contains(dr['rect'].tl) and R1.contains(dr['rect'].br): hid |= dr['rect']
    kw, kh = hid.width / land[0], hid.height / land[1]
    rep['calibration'] = {'lot_bbox_pt': [round(v, 1) for v in hid], 'k_from_width': round(kw, 3), 'k_from_length': round(kh, 3),
                          'diff_pct': round(abs(kw - kh) / kh * 100, 2)}
    # đối chiếu độc lập thứ hai: chữ kích thước in trên bản vẽ phải chứa đúng chiều đất
    txt = {t.replace('m', '').replace(',', '.') for _, t, _ in lines if re.fullmatch(r'\d+,\d+m', t)}
    for v in land:
        if ('%.1f' % v) not in txt: rep['issues'].append('không thấy chữ kích thước %.1fm trên bản vẽ' % v)
    ok_cal = abs(kw - kh) / kh < .02
    if not ok_cal: rep['issues'].append('hệ số tỉ lệ từ chiều rộng và chiều dài lệch %.1f%% (>2%%)' % rep['calibration']['diff_pct'])
    k = (kw + kh) / 2
    rep['calibration']['k_pt_per_m'] = round(k, 3)
    out = {'code': key, 'k': round(k, 3), 'calibrated': ok_cal, 'land': list(land), 'total': areas.get('total'), 'floors': {}, 'order': []}
    # chia drawing theo tầng bằng tâm
    skip_layers = ('KHUNGTEN', 'NET-PHAN')
    assign = {fk: [] for fk in regs}
    for dr in drs:
        r = dr['rect']
        if r.width > 500 or r.height > 500: continue
        ly = (dr.get('layer') or '').upper()
        if any(s in ly.replace('Ư', 'U') or s in ly for s in skip_layers): continue
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        for fk, R in regs.items():
            if R.x0 <= cx < R.x1 and R.y0 <= cy < R.y1: assign[fk].append((group(dr.get('layer')), dr)); break
    for fk in sorted(regs, key=lambda x: 9 if x == 'TUM' else int(x)):
        rows = assign[fk]
        if not rows: rep['issues'].append('tầng %s không có nét vẽ' % fk); continue
        box = pymupdf.Rect(1e9, 1e9, -1e9, -1e9)
        for g, dr in rows:
            if g in ('FNSH', 'HIDD'): continue
            box |= dr['rect']
        box = pymupdf.Rect(box.x0 - 4, box.y0 - 4, box.x1 + 4, box.y1 + 4)
        # nhãn trong vùng
        R = regs[fk]; cand = []
        for r, t, sz in lines:
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if not (R.x0 <= cx < R.x1 and R.y0 <= cy < R.y1): continue
            if re.fullmatch(r'\d+[,.]\d+m?', t) or t.startswith('MẶT BẰNG') or t == 'RANH ĐẤT': continue
            t = t.replace('С', 'C')   # một số nhãn WC dùng chữ С (Cyrillic)
            cand.append({'t': t, 'x': cx, 'y': cy, 'sz': sz, 'y0': r.y0, 'y1': r.y1})
        # nhãn nhiều dòng (vd 'P. ĐA' + 'NĂNG') gộp lại trước khi lọc tên phòng
        cand.sort(key=lambda c: (round(c['x'] / 8), c['y']))
        merged = []
        for c in cand:
            m = None if is_room(c['t']) else next((q for q in merged if is_room(q['t']) and abs(q['x'] - c['x']) < 8 and 0 <= c['y0'] - q['y1'] < q['sz'] * .8 and abs(q['sz'] - c['sz']) < .5), None)
            if m: m['t'] += ' ' + c['t']; m['y1'] = c['y1']; m['y'] = (m['y0'] + m['y1']) / 2
            else: merged.append(dict(c))
        labels = [{'t': c['t'], 'n': disp(c['t']), 'x': round(c['x'], 1), 'y': round(c['y'], 1), 'sz': round(c['sz'], 1)} for c in merged if is_room(c['t'])]
        area_tbl = areas.get(fk)
        rooms, skipped = detect_rooms(rows, labels, box, k, area_tbl or 100)
        # SVG bản đồ: gộp theo nhóm layer, rồi theo kiểu nét/tô
        parts = []
        counts = {}
        for g in GROUP_LABEL:
            lst = [dr for gg, dr in rows if gg == g]
            if not lst: continue
            counts[g] = len(lst)
            if g not in MAP_GROUPS: continue
            bucket = {}
            for dr in lst:
                st = hexc(dr['color']) if dr.get('color') else None
                fl = hexc(dr['fill']) if dr.get('fill') else None
                w = max(round(dr.get('width') or 0, 1), .1) if st else 0
                bucket.setdefault((st, fl, w), []).append(pathd(dr['items']))
            gs = ['<path d="%s" fill="%s" stroke="%s"%s/>' % (''.join(ds), fl or 'none', st or 'none', ' stroke-width="%s"' % fmt(w) if st else '') for (st, fl, w), ds in bucket.items()]
            parts.append('<g class="L-%s">%s</g>' % (g, ''.join(gs)))
        svg = ''.join(parts)
        out['floors'][fk] = {'name': FLOOR_NAMES[fk], 'area_m2': area_tbl, 'box': [round(v, 1) for v in (box.x0, box.y0, box.width, box.height)],
                             'svg': svg, 'labels': labels, 'rooms': rooms, 'counts': counts}
        out['order'].append(fk)
        rep['floors'][fk] = {'area_table': area_tbl, 'labels': [l['t'] for l in labels], 'rooms_ok': [(' + '.join(r['names']), r['area']) for r in rooms],
                             'rooms_skipped': skipped, 'rooms_sum': round(sum(r['area'] for r in rooms), 1), 'svg_kb': len(svg) // 1024}
        if want_dxf:
            import ezdxf
            doc = ezdxf.new('R2010'); doc.header['$INSUNITS'] = 6; msp = doc.modelspace()
            for g, dr in rows:
                ln = 'A-' + g
                if ln not in doc.layers: doc.layers.add(ln)
                for pl in polylines(dr['items']): msp.add_lwpolyline([((x - box.x0) / k, -(y - box.y0) / k) for x, y in pl], dxfattribs={'layer': ln})
            if 'TEXT' not in doc.layers: doc.layers.add('TEXT')
            for lb in labels: msp.add_text(lb['t'], height=.25, dxfattribs={'layer': 'TEXT', 'insert': ((lb['x'] - box.x0) / k, -(lb['y'] - box.y0) / k)})
            os.makedirs(dxf_dir, exist_ok=True); doc.saveas(os.path.join(dxf_dir, '%s_%s.dxf' % (key, 'T' + fk if fk != 'TUM' else 'TUM')))
    # đối chiếu diện tích bảng
    s = sum(v for kk, v in areas.items() if kk != 'total')
    if areas.get('total') and abs(s - areas['total']) > .6: rep['issues'].append('tổng các tầng %.1f khác tổng in %.1f' % (s, areas['total']))
    if len(out['order']) != 5: rep['issues'].append('chỉ tìm được %d tầng' % len(out['order']))
    return out, rep


_cache = {}
def text_lines_cache(lines): return lines


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args: sys.exit(__doc__)
    pdf_dir = args[0]; want_dxf = '--dxf' in sys.argv
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    report = {}
    for key, (fn, land) in SHEETS.items():
        out, rep = process(key, os.path.join(pdf_dir, fn), land, want_dxf, os.path.join(HERE, 'out'))
        json.dump(out, open(os.path.join(HERE, 'data', key + '.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
        report[key] = rep
        print(key, 'k=%s' % rep['calibration']['k_pt_per_m'], 'lệch %s%%' % rep['calibration']['diff_pct'], rep['issues'])
        for fk, f in rep['floors'].items():
            print('  Tầng %s bảng %s | phòng %d tổng %s | bỏ %d | svg %d KB' % (fk, f['area_table'], len(f['rooms_ok']), f['rooms_sum'], len(f['rooms_skipped']), f['svg_kb']))
    json.dump(report, open(os.path.join(HERE, 'report.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
