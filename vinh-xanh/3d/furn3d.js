/* Nội thất khối đơn giản cho từng tầng. Toạ độ theo mét trên mặt bằng: x ngang (0..5), y từ phía sau (0) ra mặt tiền (14,6).
   Vị trí đo từ bản vẽ mẫu LK1. Trả về nhóm đặt ở độ cao sàn của tầng. */
function buildFurniture(THREE,k,W,DP){
  const g=new THREE.Group(),cache={};
  const mat=c=>cache[c]||(cache[c]=new THREE.MeshStandardMaterial({color:c,roughness:.85}));
  const C={wood:0xb98a58,dark:0x4a4540,sofa:0x8f98a3,fabric:0xd9d3c6,white:0xf4f2ee,steel:0xaab2b8,green:0x6f9a62,blue:0x6d8fa8,tv:0x1e2023,rug:0xc9bba4,bed:0xe9e4da,pillow:0xffffff,tile:0xdfe6e8};
  const P=(x,y)=>[x-W/2,-(y-DP/2)];
  const box=(x,y,w,d,h,c,e)=>{e=e||0;const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat(c));const[px,pz]=P(x+w/2,y+d/2);m.position.set(px,e+h/2,pz);m.castShadow=m.receiveShadow=true;g.add(m);return m};
  const cyl=(x,y,r,h,c,e,rot)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,20),mat(c));const[px,pz]=P(x,y);m.position.set(px,(e||0)+h/2,pz);if(rot){m.rotation.z=Math.PI/2;m.position.y=(e||0)+r}m.castShadow=true;g.add(m);return m};
  const bed=(x,y,w,d)=>{box(x,y,w,d,.32,C.wood);box(x+.02,y+.02,w-.04,d-.04,.2,C.bed,.32);box(x+w*.45,y+.02,w*.55-.02,d-.04,.06,C.blue,.52);
    box(x+.06,y+.1,.38,.55,.12,C.pillow,.52);box(x+.06,y+d-.65,.38,.55,.12,C.pillow,.52);box(x-.02,y-.02,.08,d+.04,.95,C.wood)};
  const wardrobe=(x,y,w,d)=>box(x,y,w,d,2.3,C.wood);
  const sofa=(x,y,w,d,back)=>{box(x,y,w,d,.4,C.sofa);const t=.2;
    if(back==='n')box(x,y,w,t,.85,C.sofa);else if(back==='s')box(x,y+d-t,w,t,.85,C.sofa);else if(back==='w')box(x,y,t,d,.85,C.sofa);else box(x+w-t,y,t,d,.85,C.sofa)};
  const table=(x,y,w,d,h)=>{box(x,y,w,d,.05,C.wood,h-.05);[[.05,.05],[w-.1,.05],[.05,d-.1],[w-.1,d-.1]].forEach(([a,b])=>box(x+a,y+b,.05,.05,h-.05,C.dark))};
  const chair=(x,y,s)=>{s=s||.42;box(x,y,s,s,.05,C.wood,.42);box(x+.02,y+.02,.04,.04,.42,C.dark);box(x+s-.06,y+.02,.04,.04,.42,C.dark);box(x+.02,y+s-.06,.04,.04,.42,C.dark);box(x+s-.06,y+s-.06,.04,.04,.42,C.dark)};
  const toilet=(x,y,face)=>{box(x,y,.4,.3,.75,C.white);box(x+.03,y+.3,.34,.4,.4,C.white)};
  const basin=(x,y,w)=>{box(x,y,w||.6,.45,.8,C.white);box(x+.05,y+.04,(w||.6)-.1,.37,.04,C.tile,.8)};
  const stairs=(x0,y0,w,d,lenx,h,up)=>{ // thang chữ U: hai vế chạy dọc trục x, chiếu nghỉ ở cuối
    const n=8,sw=lenx/n,rise=h/2/n;
    for(let i=0;i<n;i++){box(x0+i*sw,y0,sw,d/2-.05,rise*(i+1),C.wood)}
    box(x0+lenx,y0,.9,d,h/2,C.wood);
    for(let i=0;i<n;i++){box(x0+lenx-(i+1)*sw,y0+d/2+.05,sw,d/2-.05,h/2+rise*(i+1),C.wood)}};
  const tv=(x,y)=>{box(x,y,.35,2.4,.5,C.wood);box(x+.1,y+.3,.06,1.8,.95,C.tv,.7)};
  const plant=(x,y,r)=>{cyl(x,y,.16,.35,C.dark);cyl(x,y,r||.28,.7,C.green,.35)};
  if(k==='1'){
    box(.05,.3,.62,4.7,.9,C.white);box(.05,.3,.62,4.7,.04,C.dark,.9);box(.12,3.6,.5,.9,.02,C.dark,.94);
    table(3.2,2.1,1.35,1.8,.75);[2.2,2.95,3.7].forEach(yy=>{chair(2.78,yy);chair(4.62,yy)});
    toilet(.15,5.55);basin(3.05,5.5,.6);
    box(.8,5.5,.9,.04,.01,C.tile);
    sofa(1.0,9.35,2.0,.85,'n');box(1.35,10.35,1.2,.6,.38,C.wood);box(.9,10.15,2.0,1.4,.02,C.rug,.01);
    sofa(.55,11.55,.8,.8,'s');sofa(2.4,11.55,.8,.8,'s');tv(4.4,9.4);plant(4.5,13.4)
  }else if(k==='2'){
    bed(.1,1.3,2.4,2.0);box(4.6,2.1,.35,2.4,2.3,C.wood);table(3.9,.7,.9,.5,.75);chair(4.0,1.3);
    toilet(1.5,7.75);basin(2.3,7.8,.6);
    sofa(.1,10.3,.85,2.9,'w');sofa(.1,10.3,2.2,.85,'n');box(1.15,11.3,1.1,1.1,.4,C.wood);sofa(1.0,13.0,.8,.8,'s');sofa(2.0,13.0,.8,.8,'s');tv(4.45,10.6);
    stairs(.6,5.7,3.3,1.9,3.0,3.3)
  }else if(k==='3'){
    table(1.3,1.5,1.2,1.5,.75);chair(.85,2.1);box(.05,.2,.4,2.4,1.9,C.wood);box(.1,3.2,.35,1.6,2.0,C.wood);
    toilet(1.5,7.75);basin(2.3,7.8,.6);
    bed(.1,11.2,2.0,1.9);box(4.55,11.0,.35,2.4,2.3,C.wood);table(3.9,13.0,.9,.5,.75);chair(4.0,12.5);
    stairs(.6,5.7,3.3,1.9,3.0,3.3)
  }else if(k==='4'){
    bed(.1,1.2,2.4,1.9);box(4.6,.9,.3,1.6,2.3,C.wood);
    toilet(1.2,5.2);basin(2.3,5.2,.6);
    toilet(1.5,7.75);basin(2.3,7.8,.6);
    bed(.1,11.2,2.0,1.9);box(4.55,11.0,.35,2.4,2.3,C.wood);table(3.9,13.0,.9,.5,.75);chair(4.0,12.5);
    stairs(.6,5.7,3.3,1.9,3.0,3.3)
  }else{
    cyl(1.1,.8,.5,1.1,C.steel,.15,true);cyl(3.2,.8,.5,1.1,C.steel,.15,true);box(.15,2.0,.8,.8,.6,C.steel);
    box(.1,8.2,.5,.55,.9,C.white);basin(4.1,7.8,.6);table(1.5,9.4,1.2,.7,.75);chair(1.8,10.2);
    plant(.5,13.9);plant(1.8,13.9);plant(3.2,13.9);plant(4.5,13.9);
    stairs(.6,5.7,3.3,1.9,3.0,3.0)
  }
  return g}
