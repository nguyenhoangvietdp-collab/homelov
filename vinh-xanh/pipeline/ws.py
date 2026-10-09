# Redraw every lot from the CĐT plan: watershed from OCR'd code positions over the flat fill, stopped by the faint divider lines
import cv2,numpy as np,json,collections
n=cv2.imread('new_full.jpg');OX,OY,X1,Y1=2031,205,7784,3796
r=n[OY:Y1,OX:X1].astype(np.int16);H,W=r.shape[:2]
FILL={'don_lap':(138,166,246),'song_lap':(188,218,188),'lien_ke':(138,242,254),'shophouse':(238,162,238)}
D=np.stack([np.abs(r-np.array(c,np.int16)).sum(2) for c in FILL.values()]);dev=D.min(0);cls=D.argmin(0)
gray=cv2.cvtColor(n[OY:Y1,OX:X1],cv2.COLOR_BGR2GRAY)
fillish=(dev<45)
text=(gray<170)                                   # lot labels are near-black serif text
block=cv2.morphologyEx(fillish.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
block=cv2.morphologyEx(block,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
# fill enclosed holes
inv=(1-block).astype(np.uint8);nc,cc,st,_=cv2.connectedComponentsWithStats(inv,4)
for i in range(1,nc):
    if st[i,4]<20000: block[cc==i]=1
np.save('ws_block.npy',block)
elev=np.clip(dev,0,70).astype(np.uint8)
tx=cv2.dilate(text.astype(np.uint8),np.ones((5,5),np.uint8))>0
elev[tx&(block>0)]=0
elev[block==0]=255
np.save('ws_elev.npy',elev);np.save('ws_dev.npy',dev.astype(np.int16));np.save('ws_cls.npy',cls.astype(np.uint8))
print('ok',block.mean())
