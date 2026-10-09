const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>await chromium.launch());
const head='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>';
require('fs').writeFileSync('wrapped.html',head+require('fs').readFileSync('ban-do-vinh-xanh.html','utf8')+'</body></html>');
for(const [n,w,h,dark,touch] of [['desk',1400,900,false],['phone',390,844,false,true]]){
 const p=await b.newPage({viewport:{width:w,height:h},colorScheme:dark?'dark':'light',hasTouch:!!touch,isMobile:!!touch});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('file://'+process.cwd()+'/wrapped.html');await p.waitForTimeout(800);
 await p.evaluate(()=>{const a=document.getElementById('aside');a.scrollTop=600});await p.waitForTimeout(200);
 await p.screenshot({path:n+'0.png'});
 await p.evaluate(()=>select(LOTS.find(l=>l.code==='VX3-52').id));await p.waitForTimeout(700);
 await p.evaluate(()=>{document.getElementById('aside').scrollTop=900});await p.waitForTimeout(200);
 await p.screenshot({path:n+'1.png'});
 await p.evaluate(()=>{select(LOTS.find(l=>l.pair).id)});await p.waitForTimeout(700);
 await p.evaluate(()=>openFP('SL2-01G'));await p.waitForTimeout(300);
 await p.screenshot({path:n+'2.png'});
 console.log(n,errs);
}
await b.close();})();
