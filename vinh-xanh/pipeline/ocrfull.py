# OCR every lot code on the CĐT plan, keeping absolute positions (new-image px) for watershed seeds
import cv2,numpy as np,json,re
from multiprocessing import Pool
OX,OY,X1,Y1=2031,205,7784,3796;T=900;ST=700
CODE=re.compile(r'^(VX\d{1,2}|VXI|VXL|[DĐ]L[BH][MD])[-–.]?(\d{1,3})$')
def init():
    global new,ocr
    from rapidocr_onnxruntime import RapidOCR
    new=cv2.imread('new_full.jpg');ocr=RapidOCR()
def run(job):
    tx,ty,ang=job;im=new[ty:ty+T,tx:tx+T];h,w=im.shape[:2]
    c=(w/2,h/2);M=cv2.getRotationMatrix2D(c,ang,2.0)
    cos,sin=abs(M[0,0]),abs(M[0,1]);W=int(h*sin+w*cos);H=int(h*cos+w*sin)
    M[0,2]+=W/2-c[0];M[1,2]+=H/2-c[1]
    r=cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
    out,_=ocr(r);Mi=cv2.invertAffineTransform(M);res=[]
    for box,txt,conf in (out or []):
        t=txt.replace(' ','').upper().replace('Đ','D')
        m=CODE.match(t)
        if not m or float(conf)<0.5: continue
        p=m.group(1).replace('VXI','VX1').replace('VXL','VX1');code=f"{p}-{int(m.group(2)):02d}"
        b=np.array(box,float).mean(0);q=Mi@[b[0],b[1],1]
        res.append((code,round(float(conf),3),round(q[0]+tx,1),round(q[1]+ty,1),ang))
    return res
if __name__=='__main__':
    jobs=[(x,y,a) for a in (0,90,-90,45,-45) for y in range(OY,Y1,ST) for x in range(OX,X1,ST)]
    with Pool(4,init) as p: R=p.map(run,jobs,chunksize=4)
    R=[r for rr in R for r in rr];json.dump(R,open('ocrfull.json','w'))
    print(len(R),len(set(r[0] for r in R)))
