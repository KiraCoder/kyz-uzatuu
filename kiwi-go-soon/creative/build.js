// Creative "coming soon" set for Kiwi Go: 5 HTML/SVG designs -> 2160x2160 PNGs.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = __dirname;
const C = {
  lime: '#B8F03C', ink: '#111410', paper: '#FFFDF7', cream: '#F6F1E4',
  sand: '#ECE6D6', peel: '#7A5A3C', green: '#3F6212', rim: '#6BA82B',
};
const FONTDIR = 'file:///usr/share/fonts/opentype/inter/';

// ---------- logo (exact geometry from brief) ----------
function logoInner() {
  let seeds = '';
  for (let i = 0; i < 16; i++) {
    const cy = i % 2 === 0 ? -40 : -52;
    seeds += `<ellipse cx="0" cy="${cy}" rx="5.5" ry="11" transform="rotate(${i * 22.5})"/>`;
  }
  return `<circle r="100" fill="${C.ink}"/><circle r="80" fill="${C.rim}"/><circle r="73" fill="${C.lime}"/><g fill="${C.ink}">${seeds}</g><circle r="20" fill="${C.cream}"/><circle r="7" fill="${C.ink}"/>`;
}
function logoSmallInner() {
  let seeds = '';
  for (let i = 0; i < 8; i++) seeds += `<ellipse cx="0" cy="-48" rx="7" ry="14" transform="rotate(${i * 45})"/>`;
  return `<circle r="100" fill="${C.ink}"/><circle r="78" fill="${C.lime}"/><g fill="${C.ink}">${seeds}</g><circle r="24" fill="${C.cream}"/><circle r="8" fill="${C.ink}"/>`;
}
// as an HTML element, centred on (cx,cy)
function logo(d, cx, cy, rot = 0, extra = '') {
  const inner = d < 120 ? logoSmallInner() : logoInner();
  return `<svg class="abs" width="${d}" height="${d}" viewBox="-100 -100 200 200" style="left:${cx - d / 2}px;top:${cy - d / 2}px;transform:rotate(${rot}deg);${extra}">${inner}</svg>`;
}
// as an SVG group inside a scene, centred on (cx,cy)
function logoG(d, cx, cy, rot = 0) {
  const inner = d < 120 ? logoSmallInner() : logoInner();
  return `<g transform="translate(${cx} ${cy}) rotate(${rot}) scale(${d / 200})">${inner}</g>`;
}
function wordmark(x, y, color, size = 64, font = 46) {
  return `<div class="wm" style="left:${x}px;top:${y}px;height:${size}px;color:${color}"><svg width="${size}" height="${size}" viewBox="-100 -100 200 200">${logoSmallInner()}</svg><span style="font-size:${font}px">Kiwi Go</span></div>`;
}

function page(title, body, bg, extraCss = '') {
  const ff = (fam, file, w, st = 'normal') => `@font-face{font-family:'${fam}';src:url('${FONTDIR}${file}') format('opentype');font-weight:${w};font-style:${st}}`;
  return `<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>${title}</title><style>
${ff('Inter', 'Inter-Black.otf', 900)}${ff('Inter', 'Inter-ExtraBold.otf', 800)}${ff('Inter', 'Inter-Bold.otf', 700)}${ff('Inter', 'Inter-SemiBold.otf', 600)}${ff('Inter', 'Inter-Medium.otf', 500)}
${ff('Inter', 'Inter-BlackItalic.otf', 900, 'italic')}${ff('Inter', 'Inter-BoldItalic.otf', 700, 'italic')}
${ff('InterD', 'InterDisplay-Black.otf', 900)}${ff('InterD', 'InterDisplay-ExtraBold.otf', 800)}${ff('InterD', 'InterDisplay-BlackItalic.otf', 900, 'italic')}${ff('InterD', 'InterDisplay-Bold.otf', 700)}${ff('InterD', 'InterDisplay-SemiBold.otf', 600)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden;background:${bg}}
body{font-family:'Inter',sans-serif;color:${C.ink};position:relative;-webkit-font-smoothing:antialiased}
.abs,.t,.wm{position:absolute}
.t{white-space:nowrap;line-height:1}
.D{font-family:'InterD','Inter',sans-serif}
.wm{display:flex;align-items:center;gap:16px}
.wm span{font-weight:900;letter-spacing:-0.02em;line-height:1}
svg.scene{position:absolute;left:0;top:0}
${extraCss}
</style></head><body>${body}</body></html>`;
}

const designs = [];

// ===== 01 — Sunrise over the Tian Shan =====
{
  // mountain ridge polyline from a list of [x,y]; closed to the bottom
  const ridge = (pts, fill) => `<path d="M0 1080 L${pts.map(p => p.join(' ')).join(' L')} L1080 1080 Z" fill="${fill}"/>`;
  const back = [[0,600],[70,560],[150,480],[200,520],[260,440],[320,520],[370,560],[430,660],[500,740],[560,760],[620,720],[680,640],[730,520],[790,430],[850,500],[900,470],[980,540],[1040,520],[1080,560]];
  const mid = [[0,700],[90,630],[170,670],[260,590],[330,650],[400,700],[480,780],[560,800],[640,770],[720,690],[800,610],[880,660],[960,620],[1080,690]];
  const front = [[0,800],[120,750],[220,790],[330,760],[440,820],[540,840],[640,820],[760,770],[880,790],[980,750],[1080,780]];
  // snow caps on back ridge peaks
  const cap = (x, y, w) => `<path d="M${x} ${y} L${x - w} ${y + w * 1.05} L${x - w * 0.45} ${y + w * 0.85} L${x - w * 0.1} ${y + w * 1.15} L${x + w * 0.35} ${y + w * 0.8} L${x + w} ${y + w * 1.0} Z" fill="${C.cream}"/>`;
  // rays
  let rays = '';
  for (let i = 0; i < 24; i++) {
    const a = (i / 24) * Math.PI * 2;
    const a2 = a + Math.PI / 48;
    rays += `<path d="M540 640 L${540 + 1400 * Math.cos(a)} ${640 + 1400 * Math.sin(a)} L${540 + 1400 * Math.cos(a2)} ${640 + 1400 * Math.sin(a2)} Z"/>`;
  }
  // winding road on front layer
  const road = 'M660 1080 C 640 1010, 620 990, 600 940 S 520 880, 545 845';
  designs.push({
    name: 'Рассвет над Тянь-Шанем',
    html: page('Kiwi Go — 01', `
<svg class="scene" width="1080" height="1080">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d1a0b"/><stop offset="0.35" stop-color="${C.green}"/><stop offset="0.6" stop-color="${C.lime}"/><stop offset="0.72" stop-color="#F4FFD6"/>
    </linearGradient>
    <radialGradient id="glow" cx="540" cy="640" r="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFDF7" stop-opacity="0.55"/><stop offset="1" stop-color="#FFFDF7" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#sky)"/>
  <g fill="#FFFDF7" opacity="0.07">${rays}</g>
  <circle cx="540" cy="640" r="520" fill="url(#glow)"/>
  <circle cx="540" cy="640" r="300" fill="none" stroke="${C.paper}" stroke-opacity="0.35" stroke-width="3"/>
  <circle cx="540" cy="640" r="370" fill="none" stroke="${C.paper}" stroke-opacity="0.2" stroke-width="3"/>
</svg>
${logo(440, 540, 650, -18)}
<svg class="scene" width="1080" height="1080">
  ${ridge(back, '#5d8a2a')}
  ${cap(150,480,46)}${cap(260,440,52)}${cap(790,430,62)}${cap(900,470,40)}
  ${ridge(mid, C.green)}
  ${ridge(front, C.ink)}
</svg>
<div class="t" style="left:72px;top:64px;font-weight:600;font-size:30px;letter-spacing:0.18em;color:${C.lime}">KIWI GO · КУРЬЕРСКАЯ СЛУЖБА</div>
<div class="t D" style="left:66px;top:118px;font-weight:900;font-size:150px;letter-spacing:-0.045em;color:${C.paper};line-height:0.92">Скоро<br>запуск</div>
<div class="t" style="left:72px;top:880px;font-weight:800;font-size:54px;letter-spacing:-0.02em;color:${C.paper}">Доставка по всему Кыргызстану</div>
<div class="t" style="left:72px;top:956px;font-weight:600;font-size:34px;color:${C.lime}">от гор до вашей двери</div>
${wordmark(752, 948, C.paper, 56, 40)}
`, C.ink),
  });
}

// ===== 02 — What's inside? (opened parcel, top-down) =====
{
  const cx = 540, cy = 590, s = 190, f = 150; // half-size of opening, flap depth
  const kraft = '#C99A62', kraftD = '#A97A45', kraftL = '#DDB683';
  let rays = '';
  for (let i = 0; i < 18; i++) {
    const a = (i / 18) * Math.PI * 2 + 0.1, w = 0.07;
    rays += `<path d="M${cx} ${cy} L${cx + 900 * Math.cos(a - w)} ${cy + 900 * Math.sin(a - w)} L${cx + 900 * Math.cos(a + w)} ${cy + 900 * Math.sin(a + w)} Z"/>`;
  }
  designs.push({
    name: 'Что внутри?',
    html: page('Kiwi Go — 02', `
<svg class="scene" width="1080" height="1080">
  <rect width="1080" height="1080" fill="${C.lime}"/>
  <g fill="${C.paper}" opacity="0.55">${rays}</g>
  <g transform="rotate(-7 ${cx} ${cy})" stroke="${C.ink}" stroke-width="7" stroke-linejoin="round">
    <!-- flaps: top, bottom, left, right -->
    <polygon points="${cx - s},${cy - s} ${cx + s},${cy - s} ${cx + s - 30},${cy - s - f} ${cx - s + 30},${cy - s - f}" fill="${kraftL}"/>
    <polygon points="${cx - s},${cy + s} ${cx + s},${cy + s} ${cx + s - 30},${cy + s + f} ${cx - s + 30},${cy + s + f}" fill="${kraftL}"/>
    <polygon points="${cx - s},${cy - s} ${cx - s},${cy + s} ${cx - s - f},${cy + s - 30} ${cx - s - f},${cy - s + 30}" fill="${kraft}"/>
    <polygon points="${cx + s},${cy - s} ${cx + s},${cy + s} ${cx + s + f},${cy + s - 30} ${cx + s + f},${cy - s + 30}" fill="${kraft}"/>
    <!-- torn tape on flaps -->
    <rect x="${cx - 36}" y="${cy - s - f + 4}" width="72" height="${f - 40}" fill="${C.peel}" stroke-width="4"/>
    <rect x="${cx - 36}" y="${cy + s + 36}" width="72" height="${f - 40}" fill="${C.peel}" stroke-width="4"/>
    <!-- inside -->
    <rect x="${cx - s}" y="${cy - s}" width="${2 * s}" height="${2 * s}" fill="${kraftD}"/>
    <polygon points="${cx - s},${cy - s} ${cx + s},${cy - s} ${cx + s - 40},${cy - s + 40} ${cx - s + 40},${cy - s + 40}" fill="#7f5a31" stroke-width="5"/>
    <polygon points="${cx - s},${cy - s} ${cx - s + 40},${cy - s + 40} ${cx - s + 40},${cy + s - 40} ${cx - s},${cy + s}" fill="#8e6638" stroke-width="5"/>
    <!-- fragile stamp on right flap -->
    <g transform="translate(${cx + s + f / 2 + 4} ${cy}) rotate(90)" stroke="none">
      <rect x="-128" y="-28" width="256" height="56" rx="8" fill="none" stroke="#B3261E" stroke-width="5"/>
      <text x="0" y="11" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#B3261E" letter-spacing="1">ОСТОРОЖНО</text>
    </g>
  </g>
</svg>
${logo(300, cx + 8, cy + 6, 12, 'filter:drop-shadow(0 18px 0 rgba(17,20,16,0.35))')}
<div class="t D" style="left:64px;top:56px;font-weight:900;font-size:128px;letter-spacing:-0.045em">Что внутри?</div>
<div class="t D" style="left:64px;top:920px;font-weight:900;font-size:92px;letter-spacing:-0.04em">Скоро узнаете.</div>
<div class="t" style="left:68px;top:1022px;font-weight:700;font-size:28px;letter-spacing:0.02em;opacity:0.75">Kiwi Go — курьерская служба</div>
<div class="abs" style="right:48px;top:60px;width:176px;height:176px;border-radius:50%;background:${C.ink};color:${C.lime};display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:26px;line-height:1.08;transform:rotate(12deg)">ОТКРОЙТЕ<br>ПЕРВЫМИ</div>
`, C.lime),
  });
}

// ===== 03 — Kinetic type: the wheel paints the word =====
{
  const rowH = 186, y0 = 24;
  const xs = [-60, -330, 24, -430];
  const wcx = 860, wd = 310;
  const fillRow = 2;
  let rowHtml = '';
  xs.forEach((x, i) => {
    rowHtml += `<div class="t D row" style="left:${x}px;top:${y0 + i * rowH}px">СКОРО СКОРО СКОРО</div>`;
    if (i === fillRow) rowHtml += `<div class="t D row fill" style="left:${x}px;top:${y0 + i * rowH}px;clip-path:inset(0 ${2400 - (wcx - x)}px 0 0)">СКОРО СКОРО СКОРО</div>`;
  });
  const wcy = y0 + fillRow * rowH + 104;
  designs.push({
    name: 'Колесо красит слово',
    html: page('Kiwi Go — 03', `
${rowHtml}
<svg class="scene" width="1080" height="1080">
  <circle cx="${wcx}" cy="${wcy}" r="${wd / 2 + 22}" fill="${C.ink}"/>
  <rect x="0" y="840" width="1080" height="240" fill="${C.lime}"/>
</svg>
${logo(wd, wcx, wcy, -32)}
<div class="t D" style="left:64px;top:888px;font-weight:900;font-size:88px;letter-spacing:-0.04em;color:${C.ink}">Kiwi Go скоро в пути</div>
<div class="t" style="left:68px;top:996px;font-weight:700;font-size:34px;color:${C.ink}">Курьерская доставка по всему Кыргызстану</div>
`, C.ink, `
.row{width:2400px;font-weight:900;font-style:italic;font-size:200px;letter-spacing:-0.035em;color:transparent;-webkit-text-stroke:3px ${C.lime};line-height:1}
.row.fill{color:${C.lime};-webkit-text-stroke:3px ${C.lime}}
`),
  });
}

// ===== 04 — Navigator: route to launch =====
{
  // topographic contour rings
  const topo = (ox, oy, n, base, step, seed) => {
    let out = '';
    for (let k = 0; k < n; k++) {
      const r0 = base + k * step;
      let d = '';
      for (let j = 0; j <= 120; j++) {
        const a = (j / 120) * Math.PI * 2;
        const rr = r0 * (1 + 0.16 * Math.sin(3 * a + seed) + 0.09 * Math.sin(5 * a + seed * 2 + k * 0.15) + 0.05 * Math.cos(2 * a - seed));
        d += `${j ? 'L' : 'M'}${(ox + rr * Math.cos(a)).toFixed(1)} ${(oy + rr * Math.sin(a)).toFixed(1)} `;
      }
      out += `<path d="${d}Z"/>`;
    }
    return out;
  };
  const route = 'M120 1080 C 140 900, 330 930, 360 800 S 220 620, 420 560 S 760 640, 800 470 S 700 330, 790 260';
  designs.push({
    name: 'Маршрут построен',
    html: page('Kiwi Go — 04', `
<svg class="scene" width="1080" height="1080">
  <rect width="1080" height="1080" fill="${C.cream}"/>
  <g fill="none" stroke="#cfc6ae" stroke-width="2.5">
    ${topo(820, 230, 11, 30, 34, 1.3)}${topo(180, 560, 10, 26, 36, 4.1)}${topo(640, 900, 9, 40, 38, 2.2)}
  </g>
  <g fill="none" stroke="#b9ae92" stroke-width="2.5" stroke-dasharray="3 9">
    <path d="M0 380 C 260 320, 420 460, 1080 360"/><path d="M0 760 C 300 700, 700 820, 1080 700"/>
  </g>
  <!-- done part of route (ghost) + route -->
  <path d="${route}" fill="none" stroke="${C.ink}" stroke-width="40" stroke-linecap="round"/>
  <path d="${route}" fill="none" stroke="${C.lime}" stroke-width="22" stroke-linecap="round"/>
  <path d="${route}" fill="none" stroke="${C.ink}" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 26"/>
  <!-- pin -->
  <g transform="translate(790 260)">
    <ellipse cx="0" cy="4" rx="46" ry="14" fill="${C.ink}" opacity="0.25"/>
    <path d="M0 0 C -40 -70, -110 -120, -110 -200 A 110 110 0 1 1 110 -200 C 110 -120, 40 -70, 0 0 Z" fill="${C.ink}"/>
  </g>
  ${logoG(184, 790, 60, 0)}
</svg>
<div class="abs nav-chip" style="left:56px;top:56px">
  <svg width="74" height="74" viewBox="0 0 74 74"><rect width="74" height="74" rx="18" fill="${C.lime}"/><path d="M24 58 V34 Q24 24 34 24 H50" fill="none" stroke="${C.ink}" stroke-width="8" stroke-linecap="round"/><path d="M42 13 L55 24 L42 35" fill="none" stroke="${C.ink}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div><div style="font-weight:600;font-size:24px;color:${C.lime};opacity:0.9">Следующий поворот</div><div style="font-weight:900;font-size:44px;letter-spacing:-0.02em;margin-top:6px">Запуск Kiwi Go</div></div>
</div>
<div class="abs card">
  <div style="font-weight:700;font-size:26px;letter-spacing:0.12em;color:${C.lime}">МАРШРУТ ПОСТРОЕН</div>
  <div class="D" style="font-weight:900;font-size:96px;letter-spacing:-0.04em;margin-top:14px;line-height:1">Прибытие: скоро</div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:22px">
    <div style="font-weight:600;font-size:32px;color:${C.sand}">Доставка по всему Кыргызстану</div>
  </div>
</div>
`, C.cream, `
.nav-chip{display:flex;align-items:center;gap:22px;background:${C.ink};color:${C.paper};border-radius:28px;padding:22px 34px 22px 22px;box-shadow:0 10px 0 rgba(17,20,16,0.15)}
.card{left:56px;right:56px;bottom:56px;background:${C.ink};color:${C.paper};border-radius:40px;padding:40px 48px 44px;box-shadow:0 14px 0 rgba(17,20,16,0.15)}
`),
  });
}

// ===== 05 — Market price tag on a crate of kiwi slices =====
{
  let tiles = '';
  const step = 170;
  let n = 0;
  for (let row = -1; row < 9; row++) {
    for (let col = -1; col < 9; col++) {
      const x = col * step + (row % 2 ? step / 2 : 0) + 40;
      const y = row * (step * 0.87) + 40;
      tiles += logoG(150, x, y, (n * 37) % 360);
      n++;
    }
  }
  designs.push({
    name: 'Ценник',
    html: page('Kiwi Go — 05', `
<svg class="scene" width="1080" height="1080">
  <rect width="1080" height="1080" fill="${C.peel}"/>
  ${tiles}
  <rect width="1080" height="1080" fill="${C.ink}" opacity="0.18"/>
</svg>
<div class="abs tag">
  <div class="hole"></div>
  <div class="row1"><span>Сорт</span><span>курьерская служба</span></div>
  <div class="D big">Kiwi Go</div>
  <div class="rule"></div>
  <div class="lab">Цена</div>
  <div class="D price">Платите только<br>за доставку</div>
  <div class="rule"></div>
  <div class="foot">Доставка по всему Кыргызстану</div>
</div>
<svg class="abs" style="left:640px;top:96px" width="360" height="200" viewBox="0 0 360 200"><path d="M113 140 C 170 50, 260 40, 360 0" fill="none" stroke="${C.cream}" stroke-width="5"/></svg>
<div class="abs sticker"><div>Скоро<br>запуск!</div></div>
`, C.peel, `
.tag{left:150px;top:190px;width:700px;background:${C.paper};border-radius:36px;padding:56px 60px 50px;transform:rotate(-4deg);box-shadow:0 22px 0 rgba(17,20,16,0.35)}
.tag .hole{position:absolute;right:56px;top:46px;width:44px;height:44px;border-radius:50%;background:${C.peel};box-shadow:inset 0 0 0 7px ${C.sand}}
.row1{display:flex;gap:18px;align-items:baseline;font-size:30px}
.row1 span:first-child{font-weight:800;letter-spacing:0.14em;text-transform:uppercase;font-size:24px;color:${C.peel}}
.row1 span:last-child{font-weight:600}
.big{font-weight:900;font-size:170px;letter-spacing:-0.05em;line-height:1;margin-top:10px}
.rule{height:0;border-top:5px dashed ${C.ink};margin:26px 0 22px;opacity:0.85}
.lab{font-weight:800;letter-spacing:0.14em;text-transform:uppercase;font-size:24px;color:${C.peel}}
.price{font-weight:900;font-size:76px;letter-spacing:-0.035em;line-height:1;margin-top:12px}
.foot{font-weight:700;font-size:32px}
.sticker{left:740px;top:740px;width:240px;height:240px;border-radius:50%;background:${C.lime};border:7px solid ${C.ink};display:flex;align-items:center;justify-content:center;text-align:center;transform:rotate(12deg);box-shadow:0 14px 0 rgba(17,20,16,0.35)}
.sticker div{font-weight:900;font-size:52px;letter-spacing:-0.03em;line-height:1.02}
`),
  });
}

(async () => {
  const only = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 2 });
  for (let i = 0; i < designs.length; i++) {
    if (only && !only.includes(i + 1)) continue;
    const nn = String(i + 1).padStart(2, '0');
    const file = path.join(ROOT, 'html', `kiwi-go-creative-${nn}.html`);
    fs.writeFileSync(file, designs[i].html);
    const p = await ctx.newPage();
    await p.goto('file://' + file);
    await p.evaluate(() => document.fonts.ready);
    const fams = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').length);
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(ROOT, `kiwi-go-creative-${nn}.png`) });
    console.log(nn, designs[i].name, 'fonts loaded:', fams);
    await p.close();
  }
  await browser.close();
})();
