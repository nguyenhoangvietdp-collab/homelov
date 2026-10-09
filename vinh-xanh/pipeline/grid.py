# Lots as cells of each row band: band = one fill colour between roads / long back dividers;
# cut points = columns where the faint divider line covers most of the band depth.
import cv2,numpy as np,json,collections
OX,OY=2031,205
block=np.load('ws_block.npy');dev=np.load('ws_dev.npy');cls=np.load('ws_cls.npy');H,W=block.shape
g=cv2.cvtColor(cv2.imread('new_full.jpg')[OY:OY+H,OX:OX+W],cv2.COLOR_BGR2GRAY)
TYPES=['don_lap','song_lap','lien_ke','shophouse']
AREA=json.load(open('area_all.json'))   # land area printed on each lot
dark=cv2.dilate((g<175).astype(np.uint8),np.ones((5,5),np.uint8))>0
divm=((dev>=5)&(dev<60)&~dark&(block>0)).astype(np.uint8)
# --- seeds (same clustering as ws2)
R=json.load(open('ocrfull.json'));pts=np.array([[r[2],r[3]] for r in R]);used=np.zeros(len(R),bool);seeds=[]
for i in np.argsort([-r[1] for r in R]):
    if used[i]: continue
    m=(np.hypot(*(pts-pts[i]).T)<22)&~used;used|=m;v=collections.Counter()
    for j in np.where(m)[0]: v[R[j][0]]+=R[j][1]
    c,s=v.most_common(1)[0];seeds.append({'code':c,'score':s,'x':pts[m,0].mean()-OX,'y':pts[m,1].mean()-OY})
best={}
for s in sorted(seeds,key=lambda s:-s['score']):
    if s['code'] in best: s['code']=None
    else: best[s['code']]=s
# --- long dividers (back-to-back rows) cut bands apart
segs=cv2.HoughLinesP(divm*255,1,np.pi/720,120,minLineLength=160,maxLineGap=8)
cut=np.zeros((H,W),np.uint8)
pass   # rows are now split by their own back-divider profile
bands=[]
SX=np.array([s['x'] for s in seeds]);SY=np.array([s['y'] for s in seeds])
for c in range(4):
    full=((cls==c)&(dev<45)).astype(np.uint8)
    full=cv2.morphologyEx(full,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    inv=(1-full).astype(np.uint8);nc,cc,st,_=cv2.connectedComponentsWithStats(inv,4)
    for i in range(1,nc):
        if st[i,4]<8000: full[cc==i]=1
    full&=block
    m=full.copy();m[cut>0]=0
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    nc,cc,st,_=cv2.connectedComponentsWithStats(m,4)
    ok=(SX>=0)&(SX<W)&(SY>=0)&(SY<H);sl=np.zeros(nc,int)
    np.add.at(sl,cc[SY[ok].astype(int),SX[ok].astype(int)],1);sl[0]=0
    # a long line that leaves one side without any lot code is a set-back line, not a back divider: glue that piece back
    parent=np.arange(nc)
    for i in range(1,nc):
        if sl[i] or st[i,4]<200: continue
        x,y,w,h=st[i,:4];x0,y0=max(0,x-6),max(0,y-6)
        sub=cc[y0:y+h+6,x0:x+w+6];ring=cv2.dilate((sub==i).astype(np.uint8),np.ones((9,9),np.uint8))>0
        nb=collections.Counter(sub[ring&(sub!=i)&(sub>0)].tolist())
        nb={k:v for k,v in nb.items() if sl[k]}
        if nb: parent[i]=max(nb,key=nb.get)
    for i in range(1,nc):
        if not sl[parent[i]] or parent[i]!=i: continue
        kids=[j for j in range(1,nc) if parent[j]==i]
        x=min(st[j,0] for j in kids);y=min(st[j,1] for j in kids)
        x2=max(st[j,0]+st[j,2] for j in kids);y2=max(st[j,1]+st[j,3] for j in kids)
        bm=np.isin(cc[y:y2,x:x2],kids).astype(np.uint8)
        bm=cv2.morphologyEx(bm,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))&full[y:y2,x:x2]
        bands.append((c,(x,y,x2-x,y2-y),bm>0))
print('bands',len(bands))

from scipy.spatial import Delaunay
KS=np.arange(1,501)
def walk(m,p,v,lim):
    """distance from p along v that stays inside mask m"""
    lim=min(lim,len(KS));q=np.rint(p[None]+KS[:lim,None]*v[None]).astype(int)
    ok=(q[:,0]>=0)&(q[:,0]<m.shape[1])&(q[:,1]>=0)&(q[:,1]<m.shape[0])
    ins=np.zeros(lim,bool);ins[ok]=m[q[ok,1],q[ok,0]]>0
    bad=np.where(~ins)[0];return int(bad[0]) if len(bad) else lim
def irregular(c,x,y,bm,sd):
    """curved or bent rows: cut between each pair of neighbouring codes along the divider line that best crosses the band there"""
    m=bm.astype(np.uint8);dv=divm[y:y+m.shape[0],x:x+m.shape[1]]
    dv=cv2.dilate(dv,np.ones((3,3),np.uint8))
    P=np.array([[s['x']-x,s['y']-y] for s in sd])
    if len(P)==2: E=[(0,1)]
    else:
        try: T=Delaunay(P);E={tuple(sorted((a,b))) for t in T.simplices for a,b in ((t[0],t[1]),(t[1],t[2]),(t[0],t[2]))}
        except Exception: E={(i,i+1) for i in range(len(P)-1)}
    cutl={}
    for a,b in E:
        d=P[b]-P[a];L=np.hypot(*d)
        if L>420 or L<6: continue
        mid=(P[a]+P[b])/2      # Gabriel edge only: no other lot code inside the circle on a-b
        if any(np.hypot(*(P[k]-mid))<L/2*0.98 for k in range(len(P)) if k not in (a,b)): continue
        u=d/L;best=(0,None)
        for t in np.linspace(0.12,0.88,max(8,int(L*0.38))):
            p=P[a]+t*d
            if not m[int(p[1]),int(p[0])]: continue
            for dphi in range(-14,15,2):
                ph=np.radians(dphi);nv=np.array([-u[1]*np.cos(ph)-u[0]*np.sin(ph),u[0]*np.cos(ph)-u[1]*np.sin(ph)])
                k1=walk(m,p,nv,260);k2=walk(m,p,-nv,260)
                if k1+k2<15: continue
                ss=np.arange(-k2,k1+1);q=p[None]+ss[:,None]*nv[None]
                cov=dv[q[:,1].round().astype(int),q[:,0].round().astype(int)].mean()-0.004*abs(dphi)
                if cov>best[0]: best=(cov,(p,nv))
        if best[0]>=0.35: cutl[(a,b)]=best[1]
    def draw(p,nv):
        k1=walk(m,p,nv,260);k2=walk(m,p,-nv,260)
        if k1+k2<10: return False
        cv2.line(bar,tuple(np.int32(np.round(p+k1*nv))),tuple(np.int32(np.round(p-k2*nv))),1,3);return True
    bar=np.zeros_like(m)
    # the lots of this row in order, so widths along the row can follow the printed areas
    adj=collections.defaultdict(list)
    for (a,b) in cutl: adj[a].append(b);adj[b].append(a)
    chain=None
    if cutl and all(len(v)<=2 for v in adj.values()) and len(adj)==len(P):
        st=[i for i in adj if len(adj[i])==1]
        if len(st)==2:
            ch=[st[0]];prev=None
            while True:
                nxt=[j for j in adj[ch[-1]] if j!=prev]
                if not nxt: break
                prev=ch[-1];ch.append(nxt[0])
            if len(ch)==len(P): chain=ch
    dts=[AREA.get(s['code']) or 0 for s in sd]
    if chain and all(dts[i] for i in chain):
        Q=P[chain];seg=np.diff(Q,axis=0);SL=np.hypot(seg[:,0],seg[:,1]);U=np.r_[0,np.cumsum(SL)]
        def at(t):                                  # point and direction at arclength t along the row
            j=int(np.clip(np.searchdirected(U,t) if False else np.searchsorted(U,t)-1,0,len(SL)-1))
            return Q[j]+ (t-U[j])/SL[j]*seg[j], seg[j]/SL[j]
        D=[]
        for j in range(len(chain)-1):
            key=(min(chain[j],chain[j+1]),max(chain[j],chain[j+1]));p,nv=cutl[key]
            D.append(U[j]+float((p-Q[j])@(seg[j]/SL[j])))
        e0=U[0]-walk(m,Q[0],-seg[0]/SL[0],400);eN=U[-1]+walk(m,Q[-1],seg[-1]/SL[-1],400)
        bb=np.r_[e0,D,eN];W=np.diff(bb)
        dd=[dts[i] for i in chain]
        nvs=[cutl[(min(chain[j],chain[j+1]),max(chain[j],chain[j+1]))][1] for j in range(len(chain)-1)]
        # keep the dividers of one row parallel: smooth their angles along the row
        if len(nvs)>2:
            th=np.array([np.arctan2(v[1],v[0])%np.pi for v in nvs])
            th=np.unwrap(th*2)/2
            sm=np.array([np.median(th[max(0,j-2):j+3]) for j in range(len(th))])
            nvs=[np.array([np.cos(a),np.sin(a)]) for a in sm]
        dp=[max(1,walk(m,Q[i],nvs[min(i,len(nvs)-1)],500)+walk(m,Q[i],-nvs[min(i,len(nvs)-1)],500)) for i in range(len(chain))]
        s0=float(np.median([w*q/d for w,q,d in zip(W,dp,dd)]))
        T=[s0*d/q for d,q in zip(dd,dp)]
        # same fit as a straight row: widths follow the printed areas, cuts stay near the drawn dividers
        nL=len(T);rows=[];rhs=[];b0,bN=float(bb[0]),float(bb[-1])
        sT=sum(T);T=[t*(bN-b0)/sT for t in T]
        def colc(j):
            v=np.zeros(max(nL-1,1))
            if 0<j<nL: v[j-1]=1
            return v,(b0 if j==0 else bN if j==nL else 0.0)
        for i in range(nL):
            v1,k1_=colc(i+1);v0,k0_=colc(i)
            rows.append(np.sqrt(3.0)*(v1-v0));rhs.append(np.sqrt(3.0)*(T[i]-k1_+k0_))
        for j in range(1,nL):
            v,k_=colc(j);rows.append(v);rhs.append(float(bb[j])-k_)
        if nL>1:
            sol=np.linalg.lstsq(np.array(rows),np.array(rhs),rcond=None)[0]
            B=np.r_[b0,np.maximum.accumulate(np.clip(sol,b0,bN)),bN]
        else: B=np.array([b0,bN])
        for j in range(1,nL):
            t=B[j]
            if b0+1<t<bN-1: draw(at(np.clip(t,U[0],U[-1]))[0],nvs[min(j-1,len(nvs)-1)])
        stats['fit']+=len(T)
    else:
        for (a,b),(p,nv) in cutl.items(): draw(p,nv)
        stats['nofit']+=len(P)
    cells=(m&(1-bar)).astype(np.uint8)
    nc,cc=cv2.connectedComponents(cells,connectivity=4)
    own=collections.defaultdict(list)
    for i,p in enumerate(P):
        k=cc[int(p[1]),int(p[0])]
        if k==0:          # the code sits on a divider line: take the cell just beside it
            yy0,xx0=np.nonzero(cc[max(0,int(p[1])-12):int(p[1])+13,max(0,int(p[0])-12):int(p[0])+13])
            if len(yy0):
                sub=cc[max(0,int(p[1])-12):int(p[1])+13,max(0,int(p[0])-12):int(p[0])+13]
                j=np.argmin((yy0-min(12,int(p[1])))**2+(xx0-min(12,int(p[0])))**2);k=sub[yy0[j],xx0[j]]
        own[k].append(i)
    # pixels: nearest seed within its own cell (cells holding two codes split by nearest code)
    res=[]
    yy,xx=np.nonzero(m)
    lab=np.full(m.shape,-1,int)
    for k,idx in own.items():
        if k==0: continue
        sel=cc[yy,xx]==k;py,px=yy[sel],xx[sel]
        dd=np.stack([np.hypot(px-P[i,0],py-P[i,1]) for i in idx]);lab[py,px]=np.array(idx)[dd.argmin(0)]
    # unclaimed cells (no code inside) join the neighbouring lot they touch most
    for k in range(1,nc):
        if k in own: continue
        cm=(cc==k).astype(np.uint8)
        if cm.sum()<900: continue      # a narrow strip between two lots is the khe, it belongs to neither
        ring=(cv2.dilate(cm,np.ones((9,9),np.uint8))>0)&(lab>=0)
        if ring.any(): lab[cm>0]=collections.Counter(lab[ring].tolist()).most_common(1)[0][0]
    for i,s in enumerate(sd):
        cm=(lab==i).astype(np.uint8)
        if not cm.any(): continue
        cm=cv2.morphologyEx(cm,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
        cs,_=cv2.findContours(cm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);cnt=max(cs,key=cv2.contourArea)
        ap=cv2.approxPolyDP(cnt,2.0,True)[:,0]+[x+OX,y+OY]
        res.append({'code':s['code'],'t':TYPES[c],'apx':float(cv2.contourArea(cnt)),'w':0,'irr':True,'weak':False,'rectness':0,
                    'poly':ap.astype(float).round(1).tolist(),'seed':[round(s['x']+OX,1),round(s['y']+OY,1)]})
    return res
out=[];stats=collections.Counter()
def process(c,x,y,w,h,bm,lvl=0):
    global out
    sd=[s for s in seeds if x<=s['x']<x+w and y<=s['y']<y+h and bm[int(s['y'])-y,int(s['x'])-x]]
    if not sd: return
    yy,xx=np.nonzero(bm);C=np.cov(np.vstack([xx,yy]));ev,evec=np.linalg.eigh(C);v=evec[:,1]
    th=np.degrees(np.arctan2(v[1],v[0]))
    def hgt(a):
        R=cv2.getRotationMatrix2D((0,0),a,1);q=R[:,:2]@np.vstack([xx,yy]);return np.ptp(q[1])
    ang=min((th,-th),key=hgt)             # rotate so the band's long axis is horizontal
    if 1<len(sd)<=3:
        # short stacks (2-3 lots, often near-square): try the image axes and the band axes, keep the one whose cuts land on real dividers
        def trial(a):
            P=8;M=cv2.getRotationMatrix2D((w/2+P,h/2+P),a,1);cos,sin=abs(M[0,0]),abs(M[0,1])
            Wr,Hr=int((h+2*P)*sin+(w+2*P)*cos),int((h+2*P)*cos+(w+2*P)*sin);M[0,2]+=Wr/2-(w/2+P);M[1,2]+=Hr/2-(h/2+P)
            br=cv2.warpAffine(np.pad(bm.astype(np.uint8),P),M,(Wr,Hr),flags=cv2.INTER_NEAREST)
            dr=cv2.warpAffine(np.pad(divm[y:y+h,x:x+w],P),M,(Wr,Hr),flags=cv2.INTER_NEAREST)
            inner=cv2.erode(br,np.ones((7,7),np.uint8));d=inner.sum(0).astype(float)
            sc=np.where(d>15,(dr&inner).sum(0)/np.maximum(d,1),0)
            sp=sorted((M@[s['x']-x+P,s['y']-y+P,1])[0] for s in sd);tot=0
            for p,q in zip(sp[:-1],sp[1:]):
                lo,hi=int(p)+4,int(q)-3
                tot+=sc[lo:hi].max() if hi>lo else -1
            return tot
        ang=max((0,90,ang,ang+90),key=trial)
        if len(sd)==3 and trial(ang)<0.9:
            out.extend(irregular(c,x,y,bm,sd));stats['irr']+=3;return
    P=8;M=cv2.getRotationMatrix2D((w/2+P,h/2+P),ang,1);cos,sin=abs(M[0,0]),abs(M[0,1])
    Wr,Hr=int((h+2*P)*sin+(w+2*P)*cos),int((h+2*P)*cos+(w+2*P)*sin);M[0,2]+=Wr/2-(w/2+P);M[1,2]+=Hr/2-(h/2+P)
    bmp=np.pad(bm.astype(np.uint8),P);dvp=np.pad(divm[y:y+h,x:x+w],P)
    br=cv2.warpAffine(bmp,M,(Wr,Hr),flags=cv2.INTER_NEAREST);dr=cv2.warpAffine(dvp,M,(Wr,Hr),flags=cv2.INTER_NEAREST)
    ys_,xs_=np.nonzero(br);rect=len(ys_)/max(1,(np.ptp(ys_)+1)*(np.ptp(xs_)+1))
    spy=np.array([(M@[s['x']-x+P,s['y']-y+P,1])[1] for s in sd]);dep=np.ptp(ys_)+1
    ss=np.sort(spy);gi=int(np.argmax(np.diff(ss))) if len(ss)>1 else 0
    if len(sd)>1 and lvl<3 and ss[gi+1]-ss[gi]>0.22*dep:
        # two rows back to back: split along the long back divider between the two rows of codes
        inner=cv2.erode(br,np.ones((7,7),np.uint8));wid=inner.sum(1).astype(float)
        rs=np.where(wid>30,(dr&inner).sum(1)/np.maximum(wid,1),0)
        lo,hi=int(ss[gi])+4,int(ss[gi+1])-3
        if hi>lo:
            k=lo+int(np.argmax(rs[lo:hi]));stats['rowsplit']+=1
            Mi=cv2.invertAffineTransform(M)
            for part in (slice(0,k),slice(k+1,None)):
                hm=np.zeros_like(br);hm[part]=br[part]
                back=cv2.warpAffine(hm,Mi,(w+2*P,h+2*P),flags=cv2.INTER_NEAREST)[P:P+h,P:P+w]
                back=(back>0)&bm
                if back.any(): process(c,x,y,w,h,back,lvl+1)
            return
    if len(sd)>3 and rect<0.85:
        out+=irregular(c,x,y,bm,sd);stats['irr']+=len(sd);return
    inner=cv2.erode(br,np.ones((7,7),np.uint8))
    depth=inner.sum(0).astype(float);score=np.where(depth>15,(dr&inner).sum(0)/np.maximum(depth,1),0)
    sc=np.maximum(score,np.maximum(np.r_[0,score[:-1]],np.r_[score[1:],0]))   # 1-2 px wide lines
    xs=np.where(br.any(0))[0];x0r,x1r=xs.min(),xs.max()+1
    Mi=cv2.invertAffineTransform(M)
    sp=[(M@[s['x']-x+P,s['y']-y+P,1])[0] for s in sd];order=np.argsort(sp);sd=[sd[k] for k in order];sp=[sp[k] for k in order]
    dts=[AREA.get(s['code']) or 0 for s in sd]
    def peaks(lo,hi):
        return [k for k in range(max(lo,1),min(hi,len(sc)-1)) if sc[k]>=0.22 and sc[k]>=sc[k-1] and sc[k]>sc[k+1]]
    gaps=[]
    for a,b in zip(sp[:-1],sp[1:]):
        lo,hi=int(a)+4,int(b)-3
        ps=sorted(peaks(lo,hi),key=lambda k:-sc[k])
        if not ps: gaps.append({'k':(a+b)/2,'wt':0.08,'pair':None});stats['noline']+=1;continue
        k=ps[0];pair=None
        for k2 in ps[1:]:
            if 5<=abs(k2-k)<=46: pair=(min(k,k2),max(k,k2));break
        gaps.append({'k':float(k),'wt':1.0 if sc[k]>=0.3 else 0.35,'pair':pair})
        stats['weak' if sc[k]<0.3 else 'ok']+=1
    # in one row the depth is the same for every lot, so a lot's width is proportional to its printed area
    w0=np.diff([float(x0r)]+[g['k'] for g in gaps]+[float(x1r)])
    dep=np.maximum(cv2.medianBlur(np.float32(br.sum(0)).reshape(1,-1),5).ravel(),1)
    dpi=[float(dep[int(np.clip(p,0,len(dep)-1))]) for p in sp]
    s0=float(np.median([wi*q/d for wi,q,d in zip(w0,dpi,dts) if d>0])) if any(d>0 for d in dts) else None
    TW=[s0*d/q if s0 and d else None for d,q in zip(dts,dpi)]
    items=[];bd=[];wt=[]
    for i,s in enumerate(sd):
        items.append(('lot',s,TW[i]))
        if i>=len(gaps): break
        g=gaps[i];k=g['k'];slot=False
        if g['pair'] and TW[i] and TW[i+1]:
            k1,k2=g['pair'];T1,T2=TW[i],TW[i+1]
            es=abs(w0[i]-T1)+abs(w0[i+1]-T2)
            ep=abs(w0[i]+(k1-k)-T1)+abs(w0[i+1]+(k-k2)-T2)
            # a narrow strip belonging to neither neighbour is the slot of a lô xẻ khe
            if ep<es-3: slot=True
        if slot:
            k1,k2=g['pair'];bd+=[float(k1),float(k2)];wt+=[g['wt'],g['wt']]
            items.append(('slot',None,float(k2-k1)));stats['slot']+=1
        else: bd.append(k);wt.append(g['wt'])
    # place the cuts: widths want to match the printed areas, positions want to sit on the drawn dividers
    m=len(items);rows=[];rhs=[];b0,bm=float(x0r),float(x1r)
    def col(j):
        v=np.zeros(m-1)
        if 0<j<m: v[j-1]=1
        return v,(b0 if j==0 else bm if j==m else 0.0)
    for i,it in enumerate(items):
        if it[2] is None: continue
        al=np.sqrt(3.0 if it[0]=='lot' else 0.4)
        v1,k1_=col(i+1);v0,k0_=col(i)
        rows.append(al*(v1-v0));rhs.append(al*(it[2]-k1_+k0_))
    for j,(d,wj) in enumerate(zip(bd,wt),1):
        v,k_=col(j);rows.append(np.sqrt(wj)*v);rhs.append(np.sqrt(wj)*(d-k_))
    if m>1:
        sol=np.linalg.lstsq(np.array(rows),np.array(rhs),rcond=None)[0]
        B=np.r_[b0,np.maximum.accumulate(np.clip(sol,b0,bm)),bm]
    else: B=np.array([b0,bm])
    Mi=cv2.invertAffineTransform(M)
    for i,it in enumerate(items):
        if it[0]!='lot': continue
        a,bb=int(round(B[i])),int(round(B[i+1]))
        cell=np.zeros_like(br);cell[:,a:bb+1]=br[:,a:bb+1]
        cs,_=cv2.findContours(cell,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        if not cs: continue
        cnt=max(cs,key=cv2.contourArea);ap=cv2.approxPolyDP(cnt,2.0,True)[:,0].astype(float)
        q=np.c_[ap,np.ones(len(ap))]@Mi.T-[P,P]+[x+OX,y+OY]
        out.append({'code':it[1]['code'],'t':TYPES[c],'apx':float(cv2.contourArea(cnt)),'w':int(bb-a),
                    'slot':bool((i>0 and items[i-1][0]=='slot') or (i+1<m and items[i+1][0]=='slot')),
                    'poly':q.round(1).tolist(),'seed':[round(it[1]['x']+OX,1),round(it[1]['y']+OY,1)]})
for c,(x,y,w,h),bm in bands: process(c,x,y,w,h,bm)
json.dump(out,open('grid_lots.json','w'),ensure_ascii=False)
print(len(out),stats,collections.Counter(o['t'] for o in out),'missing',len(seeds)-len(out))
