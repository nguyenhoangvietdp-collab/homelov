# New lots.json: outlines traced from the CĐT plan, data carried over from the old lots by lot code
import json,numpy as np,cv2,collections,shutil,os
G=json.load(open('grid_lots.json'));L=json.load(open('lots.json'))
if not os.path.exists('lots_prev_outline.json'): shutil.copy('lots.json','lots_prev_outline.json')
L=json.load(open('lots_prev_outline.json'))
Ai=np.linalg.inv(np.load('old2new.npy'))
AREA=json.load(open('area_all.json')) if os.path.exists('area_all.json') else {}
EXTRA=json.load(open('area_extra.json'))
old={l['no']:l for l in L if l.get('no')}
laymap=collections.defaultdict(collections.Counter)
for l in L:
    if l.get('lay') and l.get('dt'): laymap[(l['t'],l['dt'])][l['lay']]+=1
def nb(code):
    p,k=code.split('-');k=int(k)
    for d in (2,-2,4,-4,1,-1):
        c=f"{p}-{k+d:02d}" if p.startswith('VX') else f"{p}-{k+d}"
        if c in old: return old[c]
out=[]
for i,g in enumerate(sorted(G,key=lambda g:(g['seed'][1]//40,g['seed'][0]))):
    P=cv2.perspectiveTransform(np.float32([g['poly']]),Ai)[0]
    o=old.get(g['code']);src=o or nb(g['code'])
    dt=AREA.get(g['code']) or EXTRA.get(g['code']) or (o or {}).get('dt')
    l={'p':[[round(float(a),1),round(float(b),1)] for a,b in P],'t':g['t'],
       'f':list(src['f']) if src else [],'s':src['s'] if src else None,'v':list(src['v']) if src else [],
       'code':(o or {}).get('code'),'id':i,'no':g['code'],'dt':dt}
    lay=(o or {}).get('lay') if o and o['t']==g['t'] else None
    if not lay and dt and laymap.get((g['t'],dt)): lay=laymap[(g['t'],dt)].most_common(1)[0][0]
    if lay: l['lay']=lay
    if o and o.get('pair'): l['pair']=o['pair']
    out.append(l)
json.dump(out,open('lots.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(out),collections.Counter(l['t'] for l in out),'sale',[l['code'] for l in out if l['code']],
      'nolay',sum('lay' not in l for l in out),'nodt',sum(not l['dt'] for l in out),'nos',sum(not l['s'] for l in out))
