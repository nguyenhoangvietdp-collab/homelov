const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const head='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>';
const fs=require('fs');fs.writeFileSync('wrapped.html',head+fs.readFileSync(process.argv[2]||'ban-do-vinh-xanh.html','utf8')+'</body></html>');
const R=[];
for(const [n,w,h,touch] of [['desk',1400,900,false],['phone',390,844,true]]){
 const p=await b.newPage({viewport:{width:w,height:h},hasTouch:touch,isMobile:touch});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+process.cwd()+'/wrapped.html');await p.waitForTimeout(600);
 // pick lots: first lot (id 0), a SH1 lot, a pair lot, VX3-52
 const picks=await p.evaluate(()=>[LOTS[0],LOTS.find(l=>l.lay==='SH1'),LOTS.find(l=>l.pair),LOTS.find(l=>l.code==='VX3-52'),LOTS.find(l=>l.lay==='DL1-06')].map(l=>l.id));
 for(const id of picks){
   await p.evaluate(()=>document.getElementById('zfit').click());await p.waitForTimeout(500);
   if(touch){await p.evaluate(id=>{focusLot(LOTS.find(l=>l.id===id));document.getElementById('aside').classList.add('collapsed')},id);await p.waitForTimeout(500)}
   await p.waitForTimeout(300);
   const pt=await p.evaluate(id=>{const n=document.querySelector(`.lot[data-id="${id}"]`);const r=n.getBoundingClientRect();
     // find a point inside the path that hits it
     for(let k=0;k<40;k++){const x=r.left+r.width*(0.3+0.4*Math.random()),y=r.top+r.height*(0.3+0.4*Math.random());const t=document.elementFromPoint(x,y);if(t===n)return[x,y]}
     return [r.left+r.width/2,r.top+r.height/2,'nohit',document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)?.className?.baseVal||document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)?.tagName]},id);
   if(touch) await p.touchscreen.tap(pt[0],pt[1]); else await p.mouse.click(pt[0],pt[1]);
   await p.waitForTimeout(600);
   const got=await p.evaluate(()=>({sel:state.sel,title:document.querySelector('#panel h2')?.textContent,lay:document.querySelector('.lay h3')?.textContent||null}));
   const want=await p.evaluate(id=>{const l=LOTS.find(x=>x.id===id);return{t:l.t,lay:l.lay||null,code:l.code}},id);
   R.push([n,'tap',id,pt[2]||'',JSON.stringify(want),JSON.stringify(got)]);
 }
 await p.screenshot({path:'probe_'+n+'.png'});
 // drag test
 const vb0=await p.evaluate(()=>svg.getAttribute('viewBox'));
 const box=await p.evaluate(()=>{const r=svg.getBoundingClientRect();return[r.left+r.width/2,r.top+80]});
 await p.mouse.move(box[0],box[1]);await p.mouse.down();await p.mouse.move(box[0]+3000,box[1]+2000,{steps:5});await p.mouse.up();
 R.push([n,'drag-far',vb0,await p.evaluate(()=>svg.getAttribute('viewBox'))]);
 // filter chip hides song lap: callouts stay?
 await p.evaluate(()=>document.getElementById('zfit').click());await p.waitForTimeout(500);
 await p.evaluate(()=>document.getElementById('f-song_lap').click());await p.waitForTimeout(400);
 R.push([n,'filter',await p.evaluate(()=>[document.querySelectorAll('.lot.dim').length,[...document.querySelectorAll('.co')].filter(c=>getComputedStyle(c).opacity!=='1').length])]);
 await p.screenshot({path:'probe_'+n+'_f.png'});
 R.push([n,'errs',errs]);
 await p.close();
}
console.log(R.map(r=>r.join(' | ')).join('\n'));await b.close();})();
