# Base image from the clean CĐT site plan (8000px): crop the map area into the existing map frame (x47–1236, y116–858) at 3×
import cv2,numpy as np
A=np.load('old2new.npy'); new=cv2.imread('new_full.jpg')
X0,Y0,X1,Y1=47,116,1236,858; S=3
T=np.array([[1/S,0,X0],[0,1/S,Y0],[0,0,1]])          # base px -> old coords
M=A@T                                                  # base px -> new px
W,H=(X1-X0)*S,(Y1-Y0)*S
out=cv2.warpPerspective(new,M,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_AREA)
# remove compass and the small key plan (they sit on the cream area, top right)
m=np.zeros((H,W),np.uint8)
for x0,y0,x1,y1 in [(800,118,955,268),(985,116,1236,345)]:
    m[(y0-Y0)*S:(y1-Y0)*S,(x0-X0)*S:(x1-X0)*S]=255
cream=out[m>0]; hsv=cv2.cvtColor(cream[None],cv2.COLOR_BGR2HSV)[0]
# only repaint pixels that aren't the cream background (keep river/land edges intact)
bg=np.median(cream[(hsv[:,1]<25)&(hsv[:,2]>225)],0)
diff=np.abs(out.astype(int)-bg).sum(2)>30
paint=((m>0)&diff).astype(np.uint8)*255
# keep land/river: only inside the cream region (low-sat bright neighbourhood)
hs=cv2.cvtColor(out,cv2.COLOR_BGR2HSV); creamish=cv2.dilate(((hs[...,1]<25)&(hs[...,2]>215)).astype(np.uint8),np.ones((25,25),np.uint8))
paint&=creamish*255
kp=np.zeros((H,W),np.uint8);kp[(116-Y0)*S:(345-Y0)*S,(985-X0)*S:(1236-X0)*S]=255
paint|=(((kp>0)&diff).astype(np.uint8)*255)
out=cv2.inpaint(out,cv2.dilate(paint,np.ones((5,5),np.uint8)),5,cv2.INPAINT_TELEA)
hsv=cv2.cvtColor(out,cv2.COLOR_BGR2HSV).astype(np.float32)
hsv[...,1]=np.clip(hsv[...,1]*1.18,0,255); hsv[...,2]=np.clip(hsv[...,2]*1.03+4,0,255)
out=cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2BGR)
cv2.imwrite('base.jpg',out,[cv2.IMWRITE_JPEG_QUALITY,76])
cv2.imwrite('base_prev.jpg',cv2.resize(out,None,fx=0.35,fy=0.35))
print(out.shape)
