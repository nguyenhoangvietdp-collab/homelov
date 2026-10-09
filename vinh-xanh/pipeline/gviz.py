import cv2,numpy as np,json,sys
n=cv2.imread('new_full.jpg');S=json.load(open(sys.argv[1]))
for o in S: cv2.polylines(n,[np.int32(o['poly'])],True,(0,0,255) if o.get('weak') else (255,0,0),2)
for nm,(x0,y0,w,h) in {'z1':(2700,2280,500,260),'z2':(2031,1500,2300,1500),'z3':(5800,2400,1984,1396),'z4':(4300,1500,2200,1500),'z5':(2031,205,1300,1400),'z6':(3500,3000,2400,796)}.items():
    f=2 if nm=='z1' else 0.45
    cv2.imwrite(nm+'.png',cv2.resize(n[y0:y0+h,x0:x0+w],None,fx=f,fy=f,interpolation=cv2.INTER_AREA))
