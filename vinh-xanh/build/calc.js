/* Tính giá từng căn theo Chính sách bán hàng Vịnh Xanh V10 (hiệu lực 05/10/2026).
   Hàm thuần, không đụng DOM, để kiểm tra độc lập bằng Node (xem tests/). Mọi số tiền là đồng (VND) nguyên, làm tròn một lần ở cuối từng đại lượng.
   Giả định (không có trong văn bản CSBH, cần CĐT xác nhận):
   - "Tổng giá" trong bảng hàng đã gồm VAT 10%, chưa gồm KPBT.
   - KPBT = 2% giá trước VAT sau ưu đãi, hiển thị riêng.
   - Chiết khấu thanh toán sớm tính trên số tiền từng đợt (gồm VAT, trừ khoản cọc), mẫu số 365 ngày.
   - Lãi vay PA1 là cận trên: lãi cố định × dư nợ không giảm × số tháng hỗ trợ (gốc trả theo quy định ngân hàng nên thực tế thấp hơn). */
const CSBH = {
  ver: 'V10 · 05/10/2026',
  from: '2026-10-05',
  vat: 0.10, kpbt: 0.02, deposit: 300000000,
  end: { relax: '2026-10-31', vos: '2026-10-31', sqt: '2026-10-31', voucher: '2026-12-31' },
  club: { vc_gold: 0.010, vc_plat: 0.013, vc_dia: 0.017 },       // VinClub: một nửa chiết khấu vào giá, một nửa tích VPoint
  sqt: { sqt_member: 0.010, sqt_gold: 0.030, sqt_plat: 0.039, sqt_dia: 0.051 }, // Siêu quà tặng: 100% chiết khấu vào giá
  vosRate: 0.10,                                                    // Về ở sớm: 5% giảm giá khi ký TTĐC, 5% hoàn tiền sau
  ttsRate: 0.13, ttsFrom: 30,
  voucherCap: 0.30, loanRatio: 0.70,
  pa1: { 18: 0.03, 24: 0.045, 30: 0.06, 36: 0.075, 48: 0.085, 60: 0.09 },
  pa2: { 18: 0.035, 24: 0.08, 30: 0.135, 36: 0.195 },
  std: [[15, 0.20], [30, 0.20], [75, 0.20], [105, 0.15], [130, 0.25]],
  relax: [[30, 0.15], [60, 0.05], [90, 0.05], [130, 0.25], [180, 0.05], [240, 0.05], [300, 0.05], [360, 0.10], [390, 0.25]],
  loan: [[15, 0.20], [30, 0.10]]
};

function calc(F, o) {
  o = o || {};
  const C = CSBH, warn = [];
  const d = o.date || C.from;
  const live = k => d <= C.end[k];
  let pay = o.pay || 'std';
  if (pay === 'relax' && !live('relax')) { pay = 'std'; warn.push('Tiến độ giãn đã hết hạn (đến 31/10/2026), tính theo tiến độ chuẩn.'); }
  let club = o.club || 'none';
  if (club in C.sqt && !live('sqt')) { club = 'none'; warn.push('Siêu quà tặng đã hết hạn (đến 31/10/2026), bỏ qua.'); }
  let vos = !!o.vos;
  if (vos && !live('vos')) { vos = false; warn.push('Về ở sớm đã hết hạn (đến 31/10/2026), bỏ qua.'); }
  const loan = pay === 'pa1' || pay === 'pa2';
  let term = +o.term || 24;
  const table = pay === 'pa2' ? C.pa2 : C.pa1;
  if (loan && !(term in table)) { term = pay === 'pa2' ? 36 : 24; warn.push('Kỳ hạn không áp dụng cho phương án này, đổi thành ' + term + ' tháng.'); }
  const s = pay === 'pa2' ? C.pa2[term] : 0;

  // giá: gốc trước VAT -> cộng phụ phí PA2 -> nhân các hệ số chiết khấu (giao hoán, thứ tự không ảnh hưởng)
  const N0 = F / (1 + C.vat);
  const N1 = N0 * (1 + s);
  const clubDisc = club in C.club ? C.club[club] / 2 : club in C.sqt ? C.sqt[club] : 0;
  const N2 = N1 * (1 - clubDisc) * (vos ? 1 - C.vosRate / 2 : 1);
  const T = Math.round(N2 * (1 + C.vat));          // tổng giá trị BĐS gồm VAT, chưa KPBT
  const kpbt = Math.round(N2 * C.kpbt);

  // lịch thanh toán
  const plan = loan ? C.loan : pay === 'relax' ? C.relax : C.std;
  const rows = [];
  let acc = 0;
  plan.forEach(([day, pct], i) => {
    const last = i === plan.length - 1 && !loan;
    let amt = last ? T - acc : Math.round(pct * T);
    acc += amt;
    rows.push({ day, pct, amt: i === 0 ? amt - C.deposit : amt, kpbt: 0 });
  });
  rows.unshift({ day: 0, pct: null, amt: C.deposit, kpbt: 0, label: 'Đặt cọc' });
  const lastRow = rows[rows.length - 1];
  lastRow.kpbt = kpbt;
  let bank = 0;
  if (loan) { bank = T - acc; }

  // chiết khấu thanh toán sớm: thanh toán đủ trong 30 ngày, các đợt sau ngày 30 được chiết khấu theo số ngày sớm
  let tts = 0;
  if (pay === 'tts') {
    let raw = 0;
    rows.forEach(r => { if (r.day > C.ttsFrom) raw += r.amt * C.ttsRate * (r.day - C.ttsFrom) / 365; });
    tts = Math.round(raw);
  }
  // voucher: dùng thanh toán, tối đa 30% Giá Trị Nhà (gồm VAT, chưa KPBT)
  let voucher = 0;
  if (o.voucher > 0) {
    if (!live('voucher')) warn.push('Voucher chỉ dùng được đến 31/12/2026, bỏ qua.');
    else {
      const cap = Math.round(C.voucherCap * T);
      voucher = Math.min(Math.round(o.voucher), cap);
      if (o.voucher > cap) warn.push('Voucher bị giới hạn ở 30% giá trị nhà.');
    }
  }
  const interest = pay === 'pa1' ? Math.round(C.loanRatio * T * C.pa1[term] * term / 12) : 0;
  const net = T + kpbt - tts - voucher;           // tiền phải nộp (chưa tính lãi vay)
  return {
    pay, club, vos, term, loan, warn, s, N0, N1, N2, T, kpbt, rows, bank,
    selfFund: loan ? T - bank : T, tts, voucher, interest, net, total: net + interest,
    saving: F - T,
    vpoint: club in C.club ? Math.round(C.club[club] / 2 * T) : 0,
    vosRefund: vos ? Math.round(C.vosRate / 2 * N2) : 0
  };
}

/* Phiếu tính giá tạm tính (PTG) theo bảng tính của đại lý cho căn VX2-87, CS 20/9 + ưu đãi đến 31/10/2026.
   Khác calc() ở chỗ: VAT chỉ tính trên phần không phải tiền đất; phí bảo trì lấy theo bảng hàng; thêm chiết khấu từ chối BLNH 0,5%;
   chiết khấu thanh toán sớm quy thành lãi dòng tiền trừ vào giá trước VAT; ưu đãi về ở sớm 5% vào giá và 5% nhận tiền mặt khi hoàn thiện. */
const PTG = {
  vos: 0.05, vosCash: 0.05, blnh: 0.005, loanRatio: 0.70, loanAdd: 0.035, ttsDaily: Math.floor(0.13 / 365 * 1e7) / 1e7,
  deposit: 300000000, vosEnd: '2026-10-31',
  std: [[15, 0.20], [30, 0.20], [75, 0.20], [105, 0.15], [130, 0.25]]
};
function calcPTG(p, o) {
  o = o || {};
  const mode = o.mode || 'std';
  const live = !o.date || o.date <= PTG.vosEnd;
  const vosOn = !!o.vos && live, blnhOn = o.blnh !== false;
  const N8 = p.N0 * (mode === 'loan' ? 1 + PTG.loanAdd : 1);
  const vosDisc = vosOn ? N8 * PTG.vos : 0;
  const blnh = blnhOn ? (N8 - vosDisc) * PTG.blnh : 0;
  const landExempt = p.landPrice * p.land;
  const price = (disc) => { const n = N8 - vosDisc - blnh - disc; const vat = (n - landExempt) * 0.10; return { n, vat, t: n + vat }; };
  const base = price(0);                                 // giá sau ưu đãi, chưa trừ lãi thanh toán sớm
  let tts = 0, ttsEx = 0;
  if (mode === 'tts') {                                  // lãi dòng tiền tính trên các đợt chuẩn sau ngày T+30
    PTG.std.forEach(([day, pct]) => { const d = day - 30; if (d > 0) tts += pct * base.t * (1 - 1 / Math.pow(1 + PTG.ttsDaily, d)); });
    ttsEx = tts / 1.1;
  }
  const pr = price(ttsEx);
  const T = pr.t, kpbt = p.kpbt;
  const vosCash = vosOn ? (N8 - blnh - ttsEx) * PTG.vosCash : 0;
  const rows = [{ day: 0, pct: null, amt: PTG.deposit, kpbt: 0, label: 'Đặt cọc' }];
  let bank = 0;
  if (mode === 'std') {
    let acc = 0;
    PTG.std.forEach(([day, pct], i) => { const last = i === PTG.std.length - 1; const a = last ? T - acc : pct * base.t; acc += a; rows.push({ day, pct, amt: i === 0 ? a - PTG.deposit : a, kpbt: last ? kpbt : 0 }); });
  } else if (mode === 'tts') {
    const a1 = 0.20 * T - PTG.deposit;
    rows.push({ day: 15, pct: 0.20, amt: a1, kpbt: 0 }, { day: 25, pct: 0.80, amt: T - a1 - PTG.deposit, kpbt: kpbt });
  } else {
    bank = PTG.loanRatio * T;
    rows.push({ day: 15, pct: 0.20, amt: 0.20 * T - PTG.deposit, kpbt: 0 }, { day: 30, pct: 0.10, amt: 0.10 * T, kpbt: kpbt });
  }
  const gross = T + kpbt;
  return { mode, vosOn, blnhOn, listed: p.F, N0: p.N0, N8, vosDisc, blnh, ttsEx, tts, n: pr.n, vat: pr.vat, T, kpbt, gross,
           vosCash, final: gross - vosCash, rows, bank, selfFund: gross - bank, live,
           warn: o.vos && !live ? ['Ưu đãi về ở sớm đã hết hạn (đến 31/10/2026), bỏ qua.'] : [] };
}
if (typeof module !== 'undefined') module.exports = { calc, CSBH, calcPTG, PTG };
