"""Lấy đa giác tường và cột của từng tầng mẫu LK1 (floorplan/data/LK1.json), đổi sang mét, căn các tầng chồng khít -> walls3d.json"""
import json, re, os
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(H, '..', 'floorplan', 'data', 'LK1.json'), encoding='utf8'))
K = D['k']
def subpaths(d):
    toks = re.findall(r'[MLHVhvlmzZC]|-?\d*\.?\d+(?:e-?\d+)?', d)
    out, cur, i, x, y, cmd = [], None, 0, 0, 0, None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in 'zZ':
                if cur: cur.append(cur[0]); out.append(cur); cur = None
            continue
        if cmd == 'M': x, y = float(toks[i]), float(toks[i+1]); i += 2; 
        elif cmd == 'L': x, y = float(toks[i]), float(toks[i+1]); i += 2
        elif cmd == 'h': x += float(toks[i]); i += 1
        elif cmd == 'v': y += float(toks[i]); i += 1
        elif cmd == 'C': x, y = float(toks[i+4]), float(toks[i+5]); i += 6
        else: i += 1; continue
        if cmd == 'M':
            if cur: out.append(cur)
            cur = [(x, y)]
        elif cur is not None: cur.append((x, y))
    if cur: out.append(cur)
    return out
def area(p): return sum(p[i][0]*p[i+1][1]-p[i+1][0]*p[i][1] for i in range(len(p)-1))/2
import numpy as np, cv2
PX = 100   # px / m
res = {}
for k in D['order']:
    sv = D['floors'][k]['svg']; lines = []; polys = []
    for cls in ('WALL', 'CONC'):
        m = re.search(r'<g class="L-%s">(.*?)</g>' % cls, sv, re.S)
        for d in re.findall(r' d="([^"]*)"', m.group(1)):
            for p in subpaths(d):
                lines.append(p)
    res[k] = lines
org = {}
for k, ls in res.items():
    pts = [q for p in ls for q in p]
    org[k] = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
out = {}
for k, ls in res.items():
    ox, oy, x1, y1 = org[k]
    W, Hh = int((x1-ox)/K*PX)+40, int((y1-oy)/K*PX)+40
    img = np.zeros((Hh, W), np.uint8)
    for p in ls:
        pp = np.array([[(q[0]-ox)/K*PX+20, (q[1]-oy)/K*PX+20] for q in p], np.float32)
        cv2.polylines(img, [np.round(pp).astype(np.int32)], False, 255, 2)
        if len(p) >= 4 and abs(p[0][0]-p[-1][0]) < .05 and abs(p[0][1]-p[-1][1]) < .05: cv2.fillPoly(img, [np.round(pp).astype(np.int32)], 255)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)))
    cv2.imwrite(os.path.join(H, f'mask_{k}.png'), img)
    cs, hier = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    shapes = []
    hier = hier[0]
    for i, c in enumerate(cs):
        if hier[i][3] != -1: continue
        if cv2.contourArea(c) < 30: continue
        holes = [cs[j] for j in range(len(cs)) if hier[j][3] == i and cv2.contourArea(cs[j]) > 30]
        f = lambda c: [[round((q[0][0]-20)/PX, 3), round((q[0][1]-20)/PX, 3)] for q in cv2.approxPolyDP(c, 1.2, True)]
        shapes.append({'o': f(c), 'h': [f(h) for h in holes]})
    out[k] = {'shapes': shapes, 'size': [round((x1-ox)/K, 2), round((y1-oy)/K, 2)]}
    print(k, len(shapes), sum(len(s['h']) for s in shapes), out[k]['size'])
json.dump(out, open(os.path.join(H, 'walls3d.json'), 'w'), separators=(',', ':'))
