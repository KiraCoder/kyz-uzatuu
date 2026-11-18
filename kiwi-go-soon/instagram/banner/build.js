// Instagram grid banner: one panorama split into 3 posts of 1080x1350 (4:5).
// The profile grid shows each post centre-cropped to 3:4 (1012.5x1350), so the panorama is
// laid out on the VISIBLE strip (3 x 1012.5) plus 33.75px of hidden bleed on each side of every tile.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const INK='#111410', LIME='#B8F03C', CREAM='#F6F1E4', RIM='#6BA82B', SAND='#ECE6D6', GINK='#3F6212', PAPER='#FFFDF7';
const V = 1012.5, B = 33.75, W = 3 * V + 2 * B, H = 1350;   // W = 3105
const vx = (x) => B + x;                                    // visible-strip x -> panorama x
const seeds = [...Array(12)].map((_, i) => `<ellipse cx="0" cy="-56.3" rx="5" ry="14" transform="rotate(${i * 30})"/>`).join('');
const LOGO = `<circle r="100" fill="${INK}"/><circle r="86" fill="${RIM}"/><circle r="80.5" fill="${LIME}"/><g fill="${INK}">${seeds}</g><circle r="26" fill="${CREAM}"/><circle r="8.5" fill="${INK}"/>`;
const roadY = 950, roadH = 200, wheelR = 300, wheelX = vx(1.5 * V), wheelY = roadY + 70 - wheelR;
const back = `M0 ${roadY} L0 760 L260 600 L470 720 L720 520 L980 700 L1180 560 L1420 690 L1700 500 L1960 680 L2200 560 L2460 700 L2700 540 L2950 690 L${W} 600 L${W} ${roadY} Z`;
const front = `M0 ${roadY} L0 860 L300 720 L560 840 L860 700 L1120 850 L1500 760 L1900 860 L2150 730 L2420 840 L2740 720 L${W} 850 L${W} ${roadY} Z`;
const snow = [[720,520],[1700,500],[2700,540]].map(([x,y]) => `<path d="M${x-60} ${y+46} L${x} ${y} L${x+64} ${y+48} L${x+30} ${y+36} L${x} ${y+56} L${x-28} ${y+34} Z" fill="${PAPER}"/>`).join('');
const speed = [[-150,240,26,LIME==LIME?INK:INK],[-40,330,16,INK],[60,280,26,INK],[150,200,16,INK]]
  .map(([dy,len,h,c]) => { const end = wheelX - wheelR - 40; return `<rect x="${end-len}" y="${wheelY+dy-h/2}" width="${len}" height="${h}" rx="${h/2}" fill="${c}"/>`; }).join('');
const html = `<html><head><style>
@font-face{font-family:I;font-weight:900;src:url('../../fonts/Inter-Black.otf')}
@font-face{font-family:I;font-weight:700;src:url('../../fonts/Inter-Bold.otf')}
*{margin:0}body{width:${W}px;height:${H}px;background:${LIME};position:relative;overflow:hidden;font-family:I;color:${INK}}
.t{position:absolute;white-space:nowrap;line-height:.95;letter-spacing:-.045em;font-weight:900}
.pill{position:absolute;background:${INK};color:${LIME};font-weight:700;font-size:50px;letter-spacing:-.01em;border-radius:60px;padding:22px 40px;white-space:nowrap}
svg{position:absolute;left:0;top:0}
</style></head><body>
<svg width="${W}" height="${H}">
  <path d="${back}" fill="${SAND}"/>${snow}
  <path d="${front}" fill="${GINK}"/>
  <rect x="0" y="${roadY}" width="${W}" height="${roadH}" fill="${INK}"/>
  <line x1="0" y1="${roadY+roadH/2}" x2="${W}" y2="${roadY+roadH/2}" stroke="${PAPER}" stroke-width="14" stroke-dasharray="80 60"/>
  ${speed}
  <g transform="translate(${wheelX} ${wheelY}) rotate(-12) scale(${wheelR/100})">${LOGO}</g>
</svg>
<div class="t" style="left:${vx(80)}px;top:150px;font-size:250px">Уже<br>в пути</div>
<div class="t" style="left:${vx(V)}px;width:${V}px;text-align:center;top:160px;font-size:150px">Kiwi Go</div>
<div class="t" style="left:${vx(2*V+70)}px;top:150px;font-size:132px;line-height:1">Доставка<br>по всему<br>Кыргызстану</div>
<div class="pill" style="left:${vx(2*V+70)}px;top:1192px">Платите только за доставку</div>
<div class="pill" style="left:${vx(80)}px;top:1192px">Курьерская служба</div>
</body></html>`;
fs.writeFileSync('panorama.html', html);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.ceil(W), height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve('panorama.html')); await p.evaluate(() => document.fonts.ready);
  // overflow check: text must stay inside its tile's visible area with a margin
  const boxes = await p.evaluate(() => [...document.querySelectorAll('.t,.pill')].map(e => { const r = e.getBoundingClientRect(); const rg = document.createRange(); rg.selectNodeContents(e); const q = e.classList.contains('t') ? rg.getBoundingClientRect() : r; return [e.textContent.slice(0,20), Math.round(q.left), Math.round(q.right), Math.round(q.top), Math.round(q.bottom)]; }));
  console.log(JSON.stringify(boxes));
  await p.screenshot({ path: 'panorama.png' });
  await b.close();
})();
