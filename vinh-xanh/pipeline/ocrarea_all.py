# Land area printed under every lot code, read at the code's own position on the CĐT plan
import cv2,numpy as np,json,re
from multiprocessing import Pool
AREA=re.compile(r'^(\d{2,3}(?:[.,]\d)?)\s*[mn]')
def init():
    global n,ocr
    from rapidocr_onnxruntime import RapidOCR
    ocr=RapidOCR();n=cv2.imread('new_full.jpg')
def run(g):
    x,y=map(int,g['seed']);best=None
    for rot in (None,cv2.ROTATE_90_CLOCKWISE,cv2.ROTATE_90_COUNTERCLOCKWISE):
        im=n[y-90:y+90,x-90:x+90]
        if rot is not None: im=cv2.rotate(im,rot)
        r,_=ocr(cv2.resize(im,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC))
        for box,t,cf in (r or []):
            m=AREA.match(t.replace(' ','').replace('l','1'))
            if m:
                d=np.hypot(*(np.array(box).mean(0)/2-90))
                if best is None or d<best[0]: best=(d,float(m.group(1).replace(',','.')))
    return g['code'],(best[1] if best else None)
if __name__=='__main__':
    G=json.load(open('grid_lots.json'))
    with Pool(4,init) as p: R=dict(p.map(run,G,chunksize=8))
    json.dump(R,open('area_all.json','w'));print(sum(v is not None for v in R.values()),len(R))
