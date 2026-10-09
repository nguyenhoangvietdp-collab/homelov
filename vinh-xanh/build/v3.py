import base64,json
s=open('template2.html').read()
def R(a,b):
    global s
    assert a in s,a[:70]; s=s.replace(a,b)
R("""  xe_khe:{name:'Liền kề xẻ khe',short:'Xẻ khe',v:'--t-xk',size:'7 × 18 m (điển hình)'},""",
"""  lien_ke:{name:'Nhà vườn Green Garden Homes (liền kề)',short:'Nhà vườn',v:'--t-xk',size:'5 × 18 m (điển hình)'},
  xe_khe:{name:'Liền kề xẻ khe',short:'Xẻ khe',v:'--t-xk',size:'7 × 18 m',hide:1},""")
R("const DN={","""const LAY=__LAY__;
const DN={""")
R("Object.entries(TYPES).forEach(([k,t])=>{","Object.entries(TYPES).filter(([k,t])=>!t.hide).forEach(([k,t])=>{")
R("${counts.song_lap} song lập, ${counts.xe_khe} liền kề xẻ khe,","${counts.song_lap} song lập, ${counts.lien_ke} liền kề,")
# home: policy
R("""  <div class="flist">${items}</div>
  <p class="note" style="margin:0">""","""  <div class="flist">${items}</div>
  ${OVERVIEW}
  ${POLICY}
  <p class="note" style="margin:0">""")
R("function home(){","""const POLICY=`<div class="pol"><div class="eyebrow">Chính sách bán hàng Vịnh Xanh</div><h3>Áp dụng từ 05/10/2026</h3>
<details open><summary>Hỗ trợ lãi suất khi vay</summary>
<p>Vay tối đa 70% tổng giá trị căn (gồm VAT). Miễn phí trả nợ trước hạn trong thời gian hỗ trợ.</p>
<div class="tbl"><table><thead><tr><th>Thời gian hỗ trợ</th><th>Phương án 1<br><small>Khách trả lãi cố định</small></th><th>Phương án 2<br><small>Lãi 0%, giá cộng thêm</small></th></tr></thead><tbody>
<tr><td>18 tháng</td><td>3,0%/năm</td><td>+3,5%</td></tr><tr><td>24 tháng</td><td>4,5%/năm</td><td>+8,0%</td></tr><tr><td>30 tháng</td><td>6,0%/năm</td><td>+13,5%</td></tr><tr><td>36 tháng</td><td>7,5%/năm</td><td>+19,5%</td></tr><tr><td>48 tháng*</td><td>8,5%/năm</td><td>—</td></tr><tr><td>60 tháng*</td><td>9,0%/năm</td><td>—</td></tr></tbody></table></div>
<p class="note">* Áp dụng có điều kiện. Phần lãi ngân hàng vượt mức cố định do chủ đầu tư chi trả.</p></details>
<details><summary>Ưu đãi đang áp dụng</summary><ul>
<li><b>Thanh toán sớm:</b> không vay và thanh toán sớm trong 30 ngày kể từ ký thỏa thuận đặt cọc được chiết khấu 13%/năm; thanh toán trước từng đợt ít nhất 7 ngày được 11%/năm.</li>
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
  return out.join('');
}
let fpBack=null;function closeFP(){const o=document.getElementById('fp');if(o.hidden)return;o.hidden=true;fpBack&&fpBack.focus()}
function openFP(k){fpBack=document.activeElement;const L=LAY[k];const o=document.getElementById('fp');o.querySelector('img').src=L.img;o.querySelector('b').textContent='Mẫu '+L.code+' · '+L.name;o.hidden=false;o.querySelector('button').focus()}
function home(){""")
R("const T=TYPES[l.t],s=l.code&&SALE[l.code];","const s=l.code&&SALE[l.code],T=TYPES[s?s.type:l.t];")
R("`<dt>Kích thước</dt><dd>${T.size}</dd><dt>Tình trạng</dt><dd>Liên hệ để kiểm tra</dd>`","`${l.no?`<dt>Mã căn</dt><dd class=\"code\">${l.no}</dd>`:''}${l.dt?`<dt>Diện tích đất</dt><dd>${l.dt.toLocaleString('vi-VN')} m²</dd>`:''}<dt>Kích thước đất</dt><dd>${l.pair?'7 × 18 m':xk(l)?'7 × 18 m':l.lay&&LAY[l.lay]?LAY[l.lay].land:T.size}</dd>${l.pair?`<dt>Phương án ghép</dt><dd>${l.pair}</dd>`:''}<dt>Tình trạng</dt><dd>Liên hệ để kiểm tra</dd>`")
R("${tr}</div>${photo(l)}${body}`;","${tr}</div>${photo(l)}${body}${layoutBlock(l,s)}`;\n  panel.querySelectorAll('[data-fp]').forEach(b=>b.onclick=()=>openFP(b.dataset.fp));")
# overlay html + css
R('<div class="foot">','''<div class="foot">Mặt bằng mẫu nhà theo tài liệu của chủ đầu tư, chỉ mang tính tương đối và có thể điều chỉnh; cam kết chính thức theo hợp đồng mua bán. ''')
R('</aside>','''</aside>
  <div class="fp" id="fp" hidden role="dialog" aria-modal="true" aria-label="Mặt bằng mẫu nhà"><div class="fph"><b></b><button aria-label="Đóng" onclick="closeFP()">✕</button></div><div class="fpb"><img alt="Mặt bằng mẫu nhà"></div></div>''')
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
@media (max-width:820px){''')
R("addEventListener('resize',","addEventListener('keydown',e=>{if(e.key==='Escape')closeFP()});\naddEventListener('resize',")
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
out=s.replace('__LOTS__',open('lots.json').read()).replace('__IMG__',img).replace('__LAY__',json.dumps(LAY,ensure_ascii=False))
open('ban-do-vinh-xanh.html','w').write(out)
