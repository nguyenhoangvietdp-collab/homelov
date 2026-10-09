"""Đối chiếu độc lập calc.js với bản tính chính xác bằng phân số (Fraction), viết lại từ văn bản CSBH V10.
Chạy: PYTHONUTF8=1 python check_calc.py   (cần Node)"""
import json, os, subprocess, itertools
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
LOTS = {'VX2-19': 18205977986, 'VX3-52': 20473235785, 'VX5-124': 20395531823, 'VX5-126': 20395531823, 'VX3-87': 46467762362}
END = {'relax': '2026-10-31', 'vos': '2026-10-31', 'sqt': '2026-10-31', 'voucher': '2026-12-31'}
CLUB = {'vc_gold': Fr(10, 1000), 'vc_plat': Fr(13, 1000), 'vc_dia': Fr(17, 1000)}
SQT = {'sqt_member': Fr(10, 1000), 'sqt_gold': Fr(30, 1000), 'sqt_plat': Fr(39, 1000), 'sqt_dia': Fr(51, 1000)}
PA1 = {18: Fr(3, 100), 24: Fr(45, 1000), 30: Fr(6, 100), 36: Fr(75, 1000), 48: Fr(85, 1000), 60: Fr(9, 100)}
PA2 = {18: Fr(35, 1000), 24: Fr(8, 100), 30: Fr(135, 1000), 36: Fr(195, 1000)}
STD = [(15, 20), (30, 20), (75, 20), (105, 15), (130, 25)]
RELAX = [(30, 15), (60, 5), (90, 5), (130, 25), (180, 5), (240, 5), (300, 5), (360, 10), (390, 25)]


def rnd(x):  # làm tròn nửa lên như Math.round
    return int((x + Fr(1, 2)).__floor__())


def ref(F, o):
    d = o['date']
    pay = o['pay']
    if pay == 'relax' and d > END['relax']: pay = 'std'
    club = o.get('club', 'none')
    if club in SQT and d > END['sqt']: club = 'none'
    vos = o.get('vos', False) and d <= END['vos']
    loan = pay in ('pa1', 'pa2')
    term = o.get('term', 24)
    tab = PA2 if pay == 'pa2' else PA1
    if loan and term not in tab: term = 36 if pay == 'pa2' else 24
    s = PA2[term] if pay == 'pa2' else Fr(0)
    N2 = Fr(F) / Fr(11, 10) * (1 + s)
    N2 *= 1 - (CLUB[club] / 2 if club in CLUB else SQT.get(club, Fr(0)))
    if vos: N2 *= Fr(95, 100)
    T = rnd(N2 * Fr(11, 10))
    kpbt = rnd(N2 * Fr(2, 100))
    plan = [(15, 20), (30, 10)] if loan else (RELAX if pay == 'relax' else STD)
    amts = []; acc = 0
    for i, (day, pct) in enumerate(plan):
        a = (T - acc) if (i == len(plan) - 1 and not loan) else rnd(Fr(pct, 100) * T)
        acc += a; amts.append((day, a))
    amts[0] = (amts[0][0], amts[0][1] - 300000000)
    tts = 0
    if pay == 'tts':
        tts = rnd(sum(Fr(a) * Fr(13, 100) * (day - 30) / 365 for day, a in amts if day > 30))
    vch = 0
    if o.get('voucher', 0) > 0 and d <= END['voucher']:
        vch = min(rnd(Fr(o['voucher'])), rnd(Fr(30, 100) * T))
    interest = rnd(Fr(7, 10) * T * PA1[term] * term / 12) if pay == 'pa1' else 0
    net = T + kpbt - tts - vch
    return {'T': T, 'kpbt': kpbt, 'tts': tts, 'voucher': vch, 'interest': interest, 'net': net, 'total': net + interest,
            'bank': (T - acc) if loan else 0, 'sum_rows': sum(a for _, a in amts) + 300000000}


def cases():
    base = {'date': '2026-10-09'}
    out = []
    for lot, F in LOTS.items():
        for pay, term in [('std', 0), ('relax', 0), ('tts', 0), ('pa1', 18), ('pa1', 36), ('pa1', 60), ('pa2', 18), ('pa2', 36), ('pa2', 48)]:
            for club in ['none', 'vc_dia', 'sqt_gold']:
                for vos in (False, True):
                    for vch in (0, 2000000000):
                        out.append((lot, F, dict(base, pay=pay, term=term, club=club, vos=vos, voucher=vch)))
    for lot, F in LOTS.items():   # sau hạn: các ưu đãi hết hiệu lực
        out.append((lot, F, dict(date='2026-11-01', pay='relax', club='sqt_dia', vos=True, voucher=1000000000, term=24)))
        out.append((lot, F, dict(date='2027-01-02', pay='std', club='vc_gold', vos=False, voucher=1000000000, term=24)))
    return out


def main():
    cs = cases()
    js = "const {calc}=require('../calc.js');const cs=JSON.parse(require('fs').readFileSync(0,'utf8'));console.log(JSON.stringify(cs.map(c=>{const r=calc(c[1],c[2]);return {T:r.T,kpbt:r.kpbt,tts:r.tts,voucher:r.voucher,interest:r.interest,net:r.net,total:r.total,bank:r.bank,sum_rows:r.rows.reduce((a,x)=>a+x.amt,0)}})))"
    res = json.loads(subprocess.run(['node', '-e', js], input=json.dumps(cs), cwd=HERE, text=True, encoding='utf8', capture_output=True, check=True).stdout)
    worst = 0; bad = 0
    for (lot, F, o), r in zip(cs, res):
        e = ref(F, o)
        for k in ('T', 'kpbt', 'tts', 'voucher', 'interest', 'net', 'total'):
            dlt = abs(e[k] - r[k]); worst = max(worst, dlt)
            if dlt > 0: bad += 1; print('LỆCH', lot, o, k, 'ref', e[k], 'js', r[k])
        if not o['pay'] in ('pa1', 'pa2') and o['pay'] != 'tts':
            assert r['sum_rows'] == r['T'], ('tổng các đợt khác T', lot, o, r['sum_rows'], r['T'])
    print(len(cs), 'ca, lệch tối đa', worst, 'đồng, số ô lệch', bad)
    # kiểm tra tay hệ số TTS tiêu chuẩn: ~1,6116% tổng các đợt sau ngày 30 (không tính cọc)
    f = Fr(13, 100) * (Fr(20, 100) * 45 + Fr(15, 100) * 75 + Fr(25, 100) * 100) / 365
    print('hệ số TTS chuẩn', float(f))


main()
