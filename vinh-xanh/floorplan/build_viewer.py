"""Dựng trang xem mặt bằng (công cụ cho kỹ sư) từ data/*.json -> viewer.html. Chạy: PYTHONUTF8=1 python build_viewer.py"""
import json, os, glob
H = os.path.dirname(os.path.abspath(__file__))
data = {}
for f in sorted(glob.glob(os.path.join(H, 'data', '*.json'))):
    d = json.load(open(f, encoding='utf8')); data[d['code']] = d
tpl = open(os.path.join(H, 'viewer.tpl.html'), encoding='utf8').read()
open(os.path.join(H, 'viewer.html'), 'w', encoding='utf8').write(tpl.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':'))))
print('viewer.html', os.path.getsize(os.path.join(H, 'viewer.html')) // 1024, 'KB')
