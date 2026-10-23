"""Dựng bản vẽ mặt bằng đen trắng kiểu CAD cho từng tầng, từ vector mẫu liền kề LK1 (floorplan/data/LK1.json).
Chạy: python3 build_cad.py  ->  VX2-87_T1.svg ... VX2-87_TUM.svg và VX2-87_mat-bang.pdf (cần Playwright + Chromium cho PDF)."""
import json, re, os, html
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(H, '..', 'floorplan', 'data', 'LK1.json'), encoding='utf8'))
CODE = 'VX2-87'
BUILD, LK1_TOTAL = 339.1, 358.9          # DT xây dựng theo bảng hàng; tổng mẫu LK1
SC = 75                                  # tỉ lệ in 1:75
K = D['k']                               # pt trên mét của bản vẽ gốc
MM = 1000 / SC / K                       # mm trên pt bản vẽ ở tỉ lệ 1:75
NAMES = {'1': 'TẦNG 1', '2': 'TẦNG 2', '3': 'TẦNG 3', '4': 'TẦNG 4', 'TUM': 'TẦNG TUM'}
fmt = lambda v: f'{v:,.1f}'.replace('.', ',')

def bw(svg):
    svg = re.sub(r'(fill|stroke)="#(?:aeaeae|adadad)"', lambda m: 'fill="none"' if m.group(1) == 'fill' else 'stroke="#000000"', svg)
    return re.sub(r'(fill|stroke)="#e6e6e8"', r'\1="none"', svg)

floors = D['order']
tot = sum(D['floors'][k]['area_m2'] for k in floors)
scaled = {k: round(D['floors'][k]['area_m2'] * BUILD / tot, 1) for k in floors}
scaled[floors[-1]] = round(BUILD - sum(scaled[k] for k in floors[:-1]), 1)

def sheet(k):
    f = D['floors'][k]; x, y, w, h = f['box']
    W, Hh = 420, 297
    px, py = 22, 20                                    # lề khung
    pw, ph = w * MM, h * MM
    ox = 30 + (150 - pw) / 2 if pw < 150 else 30
    oy = py + 8 + (215 - ph) / 2
    labels = ''.join(f'<text x="{l["x"]:.1f}" y="{l["y"]:.1f}" text-anchor="middle" font-size="4.2" class="lb">{html.escape(l["n"].upper())}</text>' for l in f['labels'])
    plan = (f'<g transform="translate({ox - x * MM:.2f} {oy - y * MM:.2f}) scale({MM:.5f})">{bw(f["svg"])}{labels}</g>')
    sb = 50 * 1000 / SC if False else 0
    bar = ''.join(f'<rect x="{235 + i * 10 / 1}" y="262" width="10" height="2" fill="{"#000" if i % 2 == 0 else "#fff"}" stroke="#000" stroke-width=".25"/>' for i in range(0, 1))
    m = 1000 / SC                                       # 1 m = 13,33 mm
    scalebar = ''.join(f'<rect x="{205 + i * m:.2f}" y="258" width="{m:.2f}" height="2.2" fill="{"#000" if i % 2 == 0 else "#fff"}" stroke="#000" stroke-width=".25"/>' for i in range(3))
    scalebar += ''.join(f'<text x="{205 + i * m:.2f}" y="256.5" font-size="3" text-anchor="middle">{i}</text>' for i in range(4)) + f'<text x="{205 + 3 * m + 3:.2f}" y="260" font-size="3">m</text>'
    rows = ''.join(f'<text x="205" y="{111 + i * 5.2:.1f}" font-size="3.4">{html.escape(l["n"])}</text>' for i, l in enumerate(f['labels']))
    info = [('CÔNG TRÌNH', 'Phân khu Vịnh Xanh, Ocean City'), ('CĂN', f'{CODE} · liền kề xẻ khe'), ('KÍCH THƯỚC ĐẤT', '7 × 18 m · 126 m²'),
            ('MẪU ÁP DỤNG', f'LK1 ({D["land"][0]} × {D["land"][1]} m)'), ('BẢN VẼ', f'MẶT BẰNG {NAMES[k]}'),
            ('DIỆN TÍCH SÀN MẪU', f'{fmt(f["area_m2"])} m²'), (f'QUY ĐỔI THEO {fmt(BUILD)} m²', f'{fmt(scaled[k])} m²'), ('TỈ LỆ', f'1:{SC}')]
    ib = ''.join(f'<text x="205" y="{32 + i * 9:.1f}" font-size="2.6" fill="#555">{html.escape(a)}</text><text x="205" y="{36.2 + i * 9:.1f}" font-size="4" font-weight="700">{html.escape(b)}</text>' for i, (a, b) in enumerate(info))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}mm" height="{Hh}mm" font-family="DejaVu Sans, Arial, sans-serif">
<style>.lb{{font-weight:600;fill:#000}}text{{fill:#000}}</style><rect width="{W}" height="{Hh}" fill="#fff"/>
<rect x="10" y="10" width="400" height="277" fill="none" stroke="#000" stroke-width=".7"/><rect x="12" y="12" width="396" height="273" fill="none" stroke="#000" stroke-width=".25"/>
<line x1="198" y1="12" x2="198" y2="285" stroke="#000" stroke-width=".35"/>
{plan}
<text x="205" y="24" font-size="6" font-weight="700">MẶT BẰNG {NAMES[k]}</text><line x1="205" y1="26.5" x2="404" y2="26.5" stroke="#000" stroke-width=".5"/>
{ib}
<text x="205" y="104" font-size="2.6" fill="#555">CÁC PHÒNG TRÊN TẦNG</text><line x1="205" y1="105.2" x2="404" y2="105.2" stroke="#000" stroke-width=".2"/>{rows}
{scalebar}
<text x="205" y="272" font-size="2.6" fill="#333">Bản vẽ minh họa dựng lại từ vector mẫu LK1 của chủ đầu tư, không dùng để thi công. Diện tích quy đổi theo tổng xây dựng 339,1 m² trong bảng hàng.</text>
<text x="205" y="277" font-size="2.6" fill="#333">Căn xẻ khe chưa có bản vẽ riêng, hình dạng mặt bằng lấy theo mẫu liền kề 5 × 18 m.</text>
</svg>'''

if __name__ == '__main__':
    for k in floors:
        open(os.path.join(H, f'{CODE}_T{k.lower()}.svg' if k=='TUM' else f'{CODE}_T{k}.svg'), 'w', encoding='utf8').write(sheet(k))
    print({k: scaled[k] for k in floors}, sum(scaled.values()))

def web_export(path):
    """Dữ liệu cho website: bản vẽ từng tầng (chỉ phần mặt bằng, nét đen) + đa giác tường 3D -> build/cad3d.json"""
    cad = {}
    for k in floors:
        f = D['floors'][k]; x, y, w, h = f['box']; pad = 8
        labels = ''.join(f'<text x="{l["x"]:.1f}" y="{l["y"]:.1f}" text-anchor="middle" font-size="7" font-weight="700" font-family="DejaVu Sans,Arial,sans-serif">{html.escape(l["n"].upper())}</text>' for l in f['labels'])
        cad[k] = {'vb': [round(x - pad, 1), round(y - pad, 1), round(w + 2 * pad, 1), round(h + 2 * pad, 1)], 'svg': bw(f['svg']) + labels,
                  'name': NAMES[k].title(), 'tpl': f['area_m2'], 'area': scaled[k]}
    walls = json.load(open(os.path.join(H, '..', '3d', 'walls3d.json')))
    json.dump({'cad': cad, 'walls': walls, 'k': K}, open(path, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    print(path, os.path.getsize(path) // 1024, 'KB')
