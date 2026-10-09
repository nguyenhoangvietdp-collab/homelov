import base64,json
s=open('template2.html').read()
def R(a,b):
    global s
    assert a in s,a[:70]; s=s.replace(a,b)
R("""  xe_khe:{name:'Liền kề xẻ khe',short:'Xẻ khe',v:'--t-xk',size:'7 × 18 m (điển hình)'},""",
"""  lien_ke:{name:'Nhà vườn Green Garden Homes (liền kề)',short:'Nhà vườn',v:'--t-xk',size:'5 × 18 m (điển hình)'},
  xe_khe:{name:'Liền kề xẻ khe',short:'Xẻ khe',v:'--t-xk',size:'7 × 18 m',hide:1},""")
R("const DN={","""const LAY=__LAY__;
const PLANZ="__PLANZ__";
const DN={""")
R("Object.entries(TYPES).forEach(([k,t])=>{","Object.entries(TYPES).filter(([k,t])=>!t.hide).forEach(([k,t])=>{")
# home: policy
R("""  <div class="flist">${items}</div>
  <p class="note" style="margin:0">""","""  <div class="flist">${items}</div>
  <details class="more"><summary>Tổng quan phân khu</summary>${OVERVIEW}</details>
  <details class="more"><summary>Chính sách bán hàng</summary>${POLICY}</details>
  <p class="note" style="margin:0">""")
R("function home(){","""const POLICY=`<div class="pol"><div class="eyebrow">Chính sách bán hàng Vịnh Xanh</div><h3>Áp dụng từ 05/10/2026</h3>
<details><summary>Hỗ trợ lãi suất khi vay</summary>
<p>Vay tối đa 70% tổng giá trị căn (gồm VAT). Miễn phí trả nợ trước hạn trong thời gian hỗ trợ.</p>
<div class="tbl"><table><thead><tr><th>Thời gian hỗ trợ</th><th>Phương án 1<br><small>Khách trả lãi cố định</small></th><th>Phương án 2<br><small>Lãi 0%, giá cộng thêm</small></th></tr></thead><tbody>
<tr><td>18 tháng</td><td>3,0%/năm</td><td>+3,5%</td></tr><tr><td>24 tháng</td><td>4,5%/năm</td><td>+8,0%</td></tr><tr><td>30 tháng</td><td>6,0%/năm</td><td>+13,5%</td></tr><tr><td>36 tháng</td><td>7,5%/năm</td><td>+19,5%</td></tr><tr><td>48 tháng*</td><td>8,5%/năm</td><td>—</td></tr><tr><td>60 tháng*</td><td>9,0%/năm</td><td>—</td></tr></tbody></table></div>
<p class="note">* Áp dụng có điều kiện. Phần lãi ngân hàng vượt mức cố định do chủ đầu tư chi trả.</p></details>
<details><summary>Ưu đãi đang áp dụng</summary><ul>
<li><b>Thanh toán sớm:</b> không vay và thanh toán sớm trong 30 ngày kể từ ký thỏa thuận đặt cọc được chiết khấu 13%/năm; thanh toán trước từng đợt ít nhất 7 ngày được 11%/năm.</li>
<li><b>Siêu quà tặng 33 năm VGR</b> (đến 31/10/2026): thành viên VinClub đã xác thực, chiết khấu 100% vào giá theo hạng: Member 1,0%, Vàng 3,0%, Bạch kim 3,9%, Kim cương 5,1%. Không đi cùng VinClub, không áp dụng kênh đại lý.</li>
<li><b>Về ở sớm</b> (đến 31/10/2026): ưu đãi 10%, trừ 50% khi ký đặt cọc và hoàn 50% sau khi hoàn thiện nhà và về ở trong 5 tháng kể từ ngày bàn giao mặt bằng. Không áp dụng cho quỹ căn Khu phố thương mại.</li>
<li><b>Thành viên VinClub:</b> Vàng 1,0%, Bạch kim 1,3%, Kim cương 1,7% (một nửa chiết khấu vào giá, một nửa tích điểm).</li>
<li><b>Voucher Đặc quyền sở hữu nhà Vinhomes:</b> dùng thanh toán tối đa 30% giá trị nhà, đến 31/12/2026.</li>
<li><b>Quỹ căn Khu phố thương mại</b> (theo danh sách): chọn cam kết thuê 6%/năm trong 36 tháng, hoặc chiết khấu 10% kèm hỗ trợ hoàn thiện 2.095.000 đ/m² sàn tầng 1 và 1.555.000 đ/m² sàn tầng 2.</li></ul></details>
<details><summary>Tiến độ thanh toán</summary>
<p>Đặt cọc <b>300 triệu đồng/căn</b> khi ký thỏa thuận đặt cọc (ngày T).</p>
<div class="tbl"><table><thead><tr><th>Tiến độ chuẩn</th><th>Tỷ lệ</th></tr></thead><tbody>
<tr><td>T + 15 ngày (gồm cọc)</td><td>20%</td></tr><tr><td>T + 30 ngày</td><td>20%</td></tr><tr><td>T + 75 ngày</td><td>20%</td></tr><tr><td>T + 105 ngày</td><td>15%</td></tr><tr><td>T + 130 ngày, kèm 100% phí bảo trì</td><td>25%</td></tr></tbody></table></div>
<div class="tbl"><table><thead><tr><th>Tiến độ giãn (ký đến 31/10/2026)</th><th>Tỷ lệ</th></tr></thead><tbody>
<tr><td>T + 30 ngày (gồm cọc)</td><td>15%</td></tr><tr><td>T + 60 / 90 ngày</td><td>5% mỗi đợt</td></tr><tr><td>T + 130 ngày</td><td>25%</td></tr><tr><td>T + 180 / 240 / 300 ngày</td><td>5% mỗi đợt</td></tr><tr><td>T + 360 ngày</td><td>10%</td></tr><tr><td>T + 390 ngày, kèm 100% phí bảo trì</td><td>25%</td></tr></tbody></table></div></details>
<p class="note">Tóm tắt từ chính sách bán hàng Vịnh Xanh bản V10 hiệu lực từ 05/10/2026. Điều kiện chi tiết theo chính sách và hợp đồng.</p></div>`;
function layoutBlock(l,s){
  if(s&&l.code==='VX2-19')return '';
  const out=[];const keys=[];if(l.lay)keys.push(l.lay);if(l.pair)keys.push('SL2-01G');
  keys.forEach(k=>{const L=LAY[k];if(!L)return;
    const floors=L.f.map((v,i)=>`<div>${['Tầng 1','Tầng 2','Tầng 3','Tầng 4','Tầng tum'][i]}</div><div class="v">${v.toLocaleString('vi-VN')} m²</div>`).join('');
    out.push(`<div class="lay"><div class="eyebrow">${k==='SL2-01G'?'Phương án ghép 2 căn':'Mẫu nhà áp dụng cho căn này'}</div>
    <h3>Mẫu ${L.code} · ${L.name}</h3>
    <button class="fpbtn" data-fp="${k}" aria-label="Xem mặt bằng mẫu ${L.code}"><img src="${L.img}" alt="Mặt bằng các tầng mẫu ${L.code}" loading="lazy"><span>Chạm để xem lớn</span></button>
    <div class="price"><div class="total">Tổng diện tích sàn</div><div class="v total">${L.total.toLocaleString('vi-VN')} m²</div>${floors}<div>Kích thước đất</div><div class="v">${L.land}</div></div>
    ${L.note?`<p class="note">${L.note}</p>`:''}</div>`)});
  return out.length?'<details class="more"><summary>Mặt bằng mẫu nhà</summary>'+out.join('')+'</details>':'';
}
let fpBack=null,PLANS=null,fpSt=null;
function closeFP(){const o=document.getElementById('fp');if(o.hidden)return;o.hidden=true;fpBack&&fpBack.focus()}
async function loadPlans(){if(PLANS!==null)return PLANS;try{const b=Uint8Array.from(atob(PLANZ),c=>c.charCodeAt(0));PLANS=await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).json()}catch(e){PLANS=false}return PLANS}
function openFP(k){fpBack=document.activeElement;const L=LAY[k];const o=document.getElementById('fp');
  o.querySelector('img').src=L.img;o.querySelector('b').textContent='Mẫu '+L.code+' · '+L.name;
  o.classList.remove('vec');o.hidden=false;o.querySelector('button').focus();
  loadPlans().then(P=>{if(P&&P[k]&&!o.hidden&&o.querySelector('b').textContent.includes(L.code))showPlan(k,P[k],'1')})}
function showPlan(k,D,fk){const o=document.getElementById('fp'),f=D.floors[fk];o.classList.add('vec');
  const st=document.getElementById('fps');st.innerHTML=`<svg xmlns="${NS}" viewBox="${f.box.join(' ')}" role="img" aria-label="Mặt bằng ${f.name}"><g class="plan">${f.svg}</g><g class="nl">${f.labels.map(l=>`<text x="${l.x}" y="${l.y+2}">${esc(l.n)}</text>`).join('')}</g></svg>`;
  const tabs=document.getElementById('fpt');tabs.innerHTML=D.order.map(x=>`<button data-f="${x}" aria-pressed="${x===fk}">${D.floors[x].name}</button>`).join('')+`<span class="fpa">${f.area_m2.toLocaleString('vi-VN',{minimumFractionDigits:1})} m² sàn</span><label><input type="checkbox" id="fpn" checked> Tên phòng</label><label><input type="checkbox" id="fpf" checked> Nội thất</label>`;
  tabs.querySelectorAll('button').forEach(b=>b.onclick=()=>showPlan(k,D,b.dataset.f));
  const sv=st.firstChild,base=f.box.slice();let vb=base.slice();const set=()=>sv.setAttribute('viewBox',vb.join(' '));
  const apply=()=>{sv.querySelector('.nl').style.display=document.getElementById('fpn').checked?'':'none';const fu=sv.querySelector('.L-FURN');if(fu)fu.style.display=document.getElementById('fpf').checked?'':'none'};
  document.getElementById('fpn').onchange=apply;document.getElementById('fpf').onchange=apply;
  const pt=e=>{const r=st.getBoundingClientRect(),sc=Math.min(r.width/vb[2],r.height/vb[3]);return[vb[0]+(e.clientX-r.left-(r.width-vb[2]*sc)/2)/sc,vb[1]+(e.clientY-r.top-(r.height-vb[3]*sc)/2)/sc,sc]};
  const zoom=(x,y,f2)=>{const nw=Math.min(base[2]*1.2,Math.max(base[2]/30,vb[2]*f2)),g=nw/vb[2];vb=[x-(x-vb[0])*g,y-(y-vb[1])*g,nw,vb[3]*g];set()};
  const P=new Map();let d0=null;
  st.onwheel=e=>{e.preventDefault();const[x,y]=pt(e);zoom(x,y,Math.exp(e.deltaY*.0015))};
  st.onpointerdown=e=>{st.setPointerCapture(e.pointerId);P.set(e.pointerId,[e.clientX,e.clientY]);d0=null};
  st.onpointermove=e=>{if(!P.has(e.pointerId))return;const o2=P.get(e.pointerId);P.set(e.pointerId,[e.clientX,e.clientY]);
    if(P.size===2){const a=[...P.values()],d=Math.hypot(a[0][0]-a[1][0],a[0][1]-a[1][1]);if(d0){const[x,y]=pt({clientX:(a[0][0]+a[1][0])/2,clientY:(a[0][1]+a[1][1])/2});zoom(x,y,d0/d)}d0=d;return}
    const sc=pt(e)[2];vb[0]-=(e.clientX-o2[0])/sc;vb[1]-=(e.clientY-o2[1])/sc;set()};
  st.onpointerup=st.onpointercancel=e=>{P.delete(e.pointerId);d0=null};st.ondblclick=()=>{vb=base.slice();set()}}
function home(){""")
R("const T=TYPES[l.t],s=l.code&&SALE[l.code];","const s=l.code&&SALE[l.code],T=TYPES[s?s.type:l.t];")
R("`<dt>Kích thước</dt><dd>${T.size}</dd><dt>Tình trạng</dt><dd>Liên hệ để kiểm tra</dd>`","`${l.no?`<dt>Mã căn</dt><dd class=\"code\">${l.no}</dd>`:''}${l.dt?`<dt>Diện tích đất</dt><dd>${l.dt.toLocaleString('vi-VN')} m²</dd>`:''}<dt>Kích thước đất</dt><dd>${l.pair?'7 × 18 m':xk(l)?'7 × 18 m':l.lay&&LAY[l.lay]?LAY[l.lay].land:T.size}</dd>${l.pair?`<dt>Phương án ghép</dt><dd>${l.pair}</dd>`:''}<dt>Tình trạng</dt><dd>Liên hệ để kiểm tra</dd>`")
R("${tr}</div>${hero}${calcBox(l,s)}${photo(l)}${body}`;","${tr}</div>${hero}${calcBox(l,s)}${photo(l)}${body}${layoutBlock(l,s)}`;\n  panel.querySelectorAll('[data-fp]').forEach(b=>b.onclick=()=>openFP(b.dataset.fp));")
# overlay html + css
R('<div class="foot">','''<div class="foot">Mặt bằng mẫu nhà theo tài liệu của chủ đầu tư, chỉ mang tính tương đối và có thể điều chỉnh; cam kết chính thức theo hợp đồng mua bán. ''')
R('</aside>','''</aside>
  <div class="fp" id="fp" hidden role="dialog" aria-modal="true" aria-label="Mặt bằng mẫu nhà"><div class="fph"><b></b><button aria-label="Đóng" onclick="closeFP()">✕</button></div><div class="fpt" id="fpt"></div><div class="fpb"><img alt="Mặt bằng mẫu nhà"></div><div class="fps" id="fps"></div></div>''')
R('@media (max-width:820px){','''.pol{display:flex;flex-direction:column;gap:8px;padding:14px;border-radius:14px;background:var(--bg);border:1px solid var(--line)}
.pol h3,.lay h3{margin:2px 0 4px;font-size:16px}
.pol details{border-top:1px solid var(--line);padding-top:8px}
.pol summary{cursor:pointer;font-weight:700;color:var(--accent);padding:4px 0}
.pol p,.pol li{margin:6px 0;font-size:13px}
.pol ul{padding-left:18px;margin:4px 0}
.amen{list-style:none;padding:0;margin:4px 0;display:grid;grid-template-columns:1fr 1fr;gap:2px 10px}.amen li{margin:2px 0;font-size:12.5px}.amen .code{display:inline-block;min-width:20px;color:var(--accent-2)}
.tbl{overflow-x:auto;margin:6px 0}
.tbl table{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}
.tbl th,.tbl td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.tbl th{font-size:12px;color:var(--muted);font-weight:600}
.tbl th small{font-weight:500}
.lay{display:flex;flex-direction:column;gap:8px}
.fpbtn{position:relative;padding:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;cursor:zoom-in}
.fpbtn img{display:block;width:100%;height:auto}
.fpbtn span{position:absolute;right:8px;bottom:8px;background:var(--accent);color:var(--accent-ink);font:600 11px var(--font-ui);padding:3px 9px;border-radius:999px}
.fp[hidden]{display:none}
.fp{position:fixed;inset:0;z-index:50;background:rgba(6,20,19,.92);display:flex;flex-direction:column;padding-top:env(safe-area-inset-top,0px)}
.fph{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;color:#fff}
.fph button{width:38px;height:38px;border-radius:10px;border:0;background:#ffffff22;color:#fff;font-size:18px;cursor:pointer}
.fpb{flex:1;overflow:auto;padding:0 16px 16px;-webkit-overflow-scrolling:touch}
.fpb img{display:block;width:100%;min-width:640px;height:auto;background:#fff;border-radius:8px}
.fpt,.fps{display:none}.fp.vec .fpb{display:none}.fp.vec .fpt{display:flex}.fp.vec .fps{display:block}
.fpt{gap:6px;align-items:center;flex-wrap:wrap;padding:0 16px 10px;color:#fff;font-size:12.5px}
.fpt button{width:auto;height:auto;padding:5px 11px;border-radius:999px;border:0;background:#ffffff22;color:#fff;font:600 12.5px var(--font-ui);cursor:pointer}
.fpt button[aria-pressed=true]{background:#fff;color:#2a2420}
.fpt label{display:flex;gap:4px;align-items:center;cursor:pointer}.fpa{margin-left:auto;font-weight:600}
.fps{flex:1;min-height:0;margin:0 16px 16px;border-radius:8px;background:#fff;touch-action:none;cursor:grab;overflow:hidden}
.fps svg{display:block;width:100%;height:100%;overflow:hidden}
.fps .nl text{font:700 7px var(--font-ui);fill:#b3123f;paint-order:stroke;stroke:#fff;stroke-width:2.4px;text-anchor:middle;pointer-events:none}
@media (max-width:820px){''')
R("addEventListener('resize',","addEventListener('keydown',e=>{if(e.key==='Escape'){const o=document.getElementById('fp');if(!o.hidden)closeFP();else closePop()}});\naddEventListener('resize',")
import re
s=re.sub(r'<div class="foot">(.*?)</div>',lambda m:'<div class="foot"><details><summary>Lưu ý và nguồn thông tin</summary>'+m.group(1)+'</details></div>',s,count=1,flags=re.S)
s=s.replace('Hưng Đông','Hừng Đông')
open('template3.html','w').write(s)
LAY={
 'DL1-02':dict(code='HL-DL1-02',name='Biệt thự đơn lập',land='12 × 20 m',total=399.5,f=[97.5,98.8,98.6,91.0,13.6]),
 'DL1-06':dict(code='HL-DL1-06',name='Đơn lập góc view sông',land='13 × 20 m',total=431.7,f=[98.5,108.2,110.1,98.6,16.3]),
 'SL2-01':dict(code='HL-SL2-01',name='Biệt thự song lập',land='7 × 18 m',total=248.9,f=[57.2,58.2,60.8,61.6,11.1],note='Mẫu có căn đối xứng.'),
 'SL2-01G':dict(code='HL-SL2-01 ghép SL2-01M',name='Ghép 2 căn song lập',land='14 × 18 m',total=499.2,f=[113.4,117.8,121.6,124.2,22.2],note='Phương án đập thông cặp căn VX1-81 và VX1-83 thành một căn.'),
 'SL2-02':dict(code='HL-SL2-02',name='Biệt thự song lập',land='8 × 18 m',total=294.0,f=[67.8,68.8,71.8,72.6,13.0],note='Mẫu có căn đối xứng.'),
 'LK1':dict(code='HL-LK1-5X18-01',name='Nhà liền kề',land='5 × 18 m',total=358.9,f=[72.9,72.8,78.4,75.9,59.0],note='Căn được đánh dấu trên keyplan của bản vẽ mẫu.'),
 'SH1':dict(code='HL-SH1-5.5x20-01',name='Liền kề kinh doanh',land='5,5 × 20 m',total=434.1,f=[88.0,83.3,95.7,89.5,77.5],note='Tầng 1 là không gian kinh doanh.'),
}
for k,v in LAY.items():
    v['img']='data:image/jpeg;base64,'+base64.b64encode(open('pdf/fp_'+k+'.jpg','rb').read()).decode()
img=base64.b64encode(open('base.jpg','rb').read()).decode()
import gzip,os
PL={}
for k in LAY:
    p='../floorplan/data/'+k+'.json'
    if not os.path.exists(p): continue
    d=json.load(open(p,encoding='utf8'))
    got=[d['floors'][x]['area_m2'] for x in d['order']]
    assert got==LAY[k]['f'],(k,got,LAY[k]['f'])   # diện tích từng tầng đọc từ PDF phải khớp bảng đã có
    PL[k]={'order':d['order'],'floors':{x:{'name':f['name'],'area_m2':f['area_m2'],'box':f['box'],'svg':f['svg'],'labels':[{'n':l['n'],'x':l['x'],'y':l['y']} for l in f['labels']]} for x,f in d['floors'].items()}}
PLANZ=base64.b64encode(gzip.compress(json.dumps(PL,ensure_ascii=False,separators=(',',':')).encode(),9)).decode()
out=s.replace('__LOTS__',open('lots.json').read()).replace('__IMG__',img).replace('__LAY__',json.dumps(LAY,ensure_ascii=False)).replace('__PLANZ__',PLANZ).replace('/*__CALC__*/',open('calc.js',encoding='utf8').read())
open('ban-do-vinh-xanh.html','w').write(out)
