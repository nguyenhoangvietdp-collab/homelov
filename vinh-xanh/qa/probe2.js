const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/wrapped.html');await p.waitForTimeout(600);
const R=[];
// search
await p.fill('#q','vx4-10');await p.press('#q','Enter');await p.waitForTimeout(600);
R.push(['vv',await p.evaluate(()=>[visualViewport.scale,visualViewport.offsetLeft,visualViewport.offsetTop,scrollX,scrollY,document.activeElement.id])]);R.push(['search',await p.evaluate(()=>document.querySelector('#panel h2').textContent)]);
await p.screenshot({path:'p2_search.png'});
// open floor plan, escape closes and focus returns
await p.evaluate(()=>document.querySelector('[data-fp]').click());await p.waitForTimeout(200);
R.push(['fp open',await p.evaluate(()=>!document.getElementById('fp').hidden)]);
await p.keyboard.press('Escape');R.push(['fp closed',await p.evaluate(()=>document.getElementById('fp').hidden),await p.evaluate(()=>document.activeElement.className)]);
// grab toggles
await p.tap('#grab');await p.waitForTimeout(300);R.push(['collapsed',await p.evaluate(()=>aside.classList.contains('collapsed'))]);
// callout tap at fit view
await p.evaluate(()=>{home();vb=startVB();setVB()});await p.waitForTimeout(300);
const c=await p.evaluate(()=>{const g=[...document.querySelectorAll('.pin')].find(g=>{const r=g.getBoundingClientRect();return r.left>0&&r.right<innerWidth&&r.top>100});const r=g.getBoundingClientRect();return[r.left+r.width/2,r.top+r.height/2,g.dataset.id]});
await p.evaluate(()=>{window.LOG=[];['pointerdown','pointerup','pointercancel'].forEach(t=>svg.addEventListener(t,e=>LOG.push([t,e.pointerId,ptrs.size,moved,!!drag]),true))});R.push(['hit',await p.evaluate(c=>{const e=document.elementFromPoint(c[0],c[1]);return [e&&e.tagName,e&&String(e.className.baseVal??e.className),svg.className.baseVal,svg.getAttribute('viewBox')]},c),c]);await p.evaluate(()=>{window.ALL=[];addEventListener('pointerdown',e=>ALL.push(['win',e.target.tagName,e.pointerType]),true);addEventListener('touchstart',e=>ALL.push(['ts',e.target.tagName]),true)});await p.touchscreen.tap(c[0],c[1]);await p.waitForTimeout(600);R.push(['all',await p.evaluate(()=>JSON.stringify(ALL))]);R.push(['callout tap',c[2],await p.evaluate(()=>[state.sel,JSON.stringify(LOG),[...ptrs.keys()]])]);
await p.screenshot({path:'p2_zoomed.png'});
console.log(R,errs);await b.close()})();
