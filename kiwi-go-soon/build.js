// Builds 5 "Скоро запуск" designs as HTML/SVG, renders them at 2x with Playwright,
// and verifies that every text node is rendered with Inter (no Cyrillic fallback).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = __dirname;
const C = {
  lime: '#B8F03C', ink: '#111410', paper: '#FFFDF7', cream: '#F6F1E4',
  sand: '#ECE6D6', peel: '#7A5A3C', rim: '#6BA82B',
};

// ---------- logos ----------
function logoFull(size, x = 0, y = 0, extra = '') {
  let seeds = '';
  for (let i = 0; i < 16; i++) {
    const cy = i % 2 === 0 ? -40 : -52;
    seeds += `<ellipse cx="0" cy="${cy}" rx="5.5" ry="11" transform="rotate(${i * 22.5})"/>`;
  }
  return `<svg class="logo" width="${size}" height="${size}" viewBox="-100 -100 200 200" style="left:${x}px;top:${y}px;${extra}" xmlns="http://www.w3.org/2000/svg">
  <circle r="100" fill="${C.ink}"/><circle r="80" fill="${C.rim}"/><circle r="73" fill="${C.lime}"/>
  <g fill="${C.ink}">${seeds}</g><circle r="20" fill="${C.cream}"/><circle r="7" fill="${C.ink}"/></svg>`;
}
function logoSmallInner() {
  let seeds = '';
  for (let i = 0; i < 8; i++) seeds += `<ellipse cx="0" cy="-48" rx="7" ry="14" transform="rotate(${i * 45})"/>`;
  return `<circle r="100" fill="${C.ink}"/><circle r="78" fill="${C.lime}"/><g fill="${C.ink}">${seeds}</g><circle r="24" fill="${C.cream}"/><circle r="8" fill="${C.ink}"/>`;
}
function logoSmall(size, style = '') {
  return `<svg class="logo" width="${size}" height="${size}" viewBox="-100 -100 200 200" style="${style}" xmlns="http://www.w3.org/2000/svg">${logoSmallInner()}</svg>`;
}
// wordmark lockup: small logo + «Kiwi Go»
function wordmark(x, y, size = 64, font = 46) {
  return `<div class="wm" style="left:${x}px;top:${y}px;height:${size}px">${logoSmall(size, 'position:static')}<span style="font-size:${font}px">Kiwi Go</span></div>`;
}

// ---------- page shell ----------
function page(title, body, extraCss = '') {
  return `<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>${title}</title>
<style>
@font-face{font-family:'Inter';src:url('../fonts/Inter-Black.otf') format('opentype');font-weight:900}
@font-face{font-family:'Inter';src:url('../fonts/Inter-ExtraBold.otf') format('opentype');font-weight:800}
@font-face{font-family:'Inter';src:url('../fonts/Inter-Bold.otf') format('opentype');font-weight:700}
@font-face{font-family:'Inter';src:url('../fonts/Inter-SemiBold.otf') format('opentype');font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden;background:${C.paper}}
body{font-family:'Inter',sans-serif;color:${C.ink};position:relative;-webkit-font-smoothing:antialiased}
.abs,.logo,.t,.wm{position:absolute}
.t{white-space:nowrap;line-height:1}
.wm{display:flex;align-items:center;gap:16px}
.wm span{font-weight:900;letter-spacing:-0.02em;line-height:1}
svg.scene{position:absolute;left:0;top:0}
${extraCss}
</style></head><body>${body}</body></html>`;
}

// ---------- designs ----------
const designs = [];

// 01 — Big type, minimal
designs.push({
  dir: 'Big type, minimal',
  text: '«Скоро» · «Доставка по всему Кыргызстану»',
  html: page('Kiwi Go — 01', `
${wordmark(80, 80)}
<div class="t" id="big" style="left:66px;top:262px;font-weight:900;font-size:300px;letter-spacing:-0.055em">Скоро<span id="bl" style="display:inline-block;width:0;height:0"></span></div>
<svg class="scene" width="1080" height="1080">
  <!-- one lime shape: the full stop, a rolling dot -->
  <circle id="dot" cx="0" cy="0" r="44" fill="${C.lime}"/>
  <!-- road band under the word -->
  <rect x="80" y="676" width="920" height="124" rx="62" fill="${C.ink}"/>
  <line x1="150" y1="738" x2="930" y2="738" stroke="${C.paper}" stroke-width="10" stroke-linecap="round" stroke-dasharray="44 34"/>
</svg>
<div class="t" style="left:80px;top:900px;font-weight:700;font-size:50px;letter-spacing:-0.01em">Доставка по всему Кыргызстану</div>
<script>
// place the lime full stop right after the word, sitting on the baseline
document.fonts.ready.then(() => {
  const big = document.getElementById('big'), rg = document.createRange(); rg.selectNodeContents(big.firstChild);
  const r = rg.getBoundingClientRect();
  const base = document.getElementById('bl').getBoundingClientRect().bottom;
  const dot = document.getElementById('dot');
  dot.setAttribute('cx', r.right + 22 + 44); dot.setAttribute('cy', base - 44);
  document.body.dataset.ready = '1';
});
</script>
`),
});

// 02 — Logo hero, rolling in
{
  const cx = 600, cy = 410, d = 432, r = d / 2;
  const lines = [
    { y: cy - 120, len: 170, h: 26, c: C.lime },
    { y: cy - 50, len: 230, h: 14, c: C.ink },
    { y: cy + 15, len: 260, h: 30, c: C.lime },
    { y: cy + 90, len: 210, h: 14, c: C.ink },
    { y: cy + 150, len: 130, h: 26, c: C.lime },
  ];
  const svgLines = lines.map(l => {
    // end each line a fixed gap before the wheel's left edge at that height
    const dx = Math.sqrt(Math.max(0, r * r - (l.y - cy) ** 2));
    const end = cx - dx - 34;
    return `<rect x="${end - l.len}" y="${l.y - l.h / 2}" width="${l.len}" height="${l.h}" rx="${l.h / 2}" fill="${l.c}"/>`;
  }).join('');
  designs.push({
    dir: 'Logo hero',
    text: '«Скоро запуск» · «Доставка по всему Кыргызстану»',
    html: page('Kiwi Go — 02', `
${wordmark(80, 64)}
<svg class="scene" width="1080" height="1080">${svgLines}
  <rect x="150" y="${cy + r + 4}" width="800" height="10" rx="5" fill="${C.ink}"/>
</svg>
${logoFull(d, cx - r, cy - r, 'transform:rotate(-14deg)')}
<div class="t" style="left:0;width:1080px;text-align:center;top:722px;font-weight:900;font-size:128px;letter-spacing:-0.045em">Скоро запуск</div>
<div class="t" style="left:0;width:1080px;text-align:center;top:900px;font-weight:700;font-size:46px;letter-spacing:-0.01em">Доставка по всему Кыргызстану</div>
`),
  });
}

// 03 — Lime sticker
{
  const sx = 806, sy = 520, R = 200, r2 = 181, n = 24;
  let pts = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (Math.PI * i) / n - Math.PI / 2;
    const rr = i % 2 === 0 ? R : r2;
    pts.push(`${(sx + rr * Math.cos(a)).toFixed(1)},${(sy + rr * Math.sin(a)).toFixed(1)}`);
  }
  // dotted road: kiwi-peel brown dots along a gentle curve
  const road = `M 80 838 C 330 790, 640 880, 1000 822`;
  designs.push({
    dir: 'Lime sticker',
    text: '«Kiwi Go скоро в пути» · «Скоро!» · «Доставка по всему Кыргызстану»',
    html: page('Kiwi Go — 03', `
${wordmark(80, 72)}
<div class="t" style="left:72px;top:206px;font-weight:900;font-size:158px;letter-spacing:-0.05em;line-height:0.96;white-space:normal;width:600px">Kiwi Go<br>скоро<br>в пути</div>
<svg class="scene" width="1080" height="1080">
  <path d="${road}" fill="none" stroke="${C.peel}" stroke-width="16" stroke-linecap="round" stroke-dasharray="0.1 32"/>
  <g transform="rotate(-12 ${sx} ${sy})">
    <polygon points="${pts.join(' ')}" fill="${C.lime}"/>
    <circle cx="${sx}" cy="${sy}" r="${r2 - 18}" fill="none" stroke="${C.ink}" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round"/>
  </g>
</svg>
<div class="t" style="left:${sx - 200}px;width:400px;text-align:center;top:${sy - 38}px;font-weight:900;font-size:76px;letter-spacing:-0.04em;transform:rotate(-12deg)">Скоро!</div>
${logoFull(140, 400, 686, 'transform:rotate(30deg)')}
<div class="t" style="left:80px;top:926px;font-weight:700;font-size:46px;letter-spacing:-0.01em">Доставка по всему Кыргызстану</div>
`),
  });
}

// 04 — Loading bar
{
  const bx = 70, by = 444, bw = 940, bh = 224, sw = 12, pad = 16;
  const innerW = bw - 2 * pad;
  const fillW = Math.round(innerW * 0.9);
  const endX = bx + pad + fillW;
  const wheel = bh - 2 * pad;
  designs.push({
    dir: 'Loading bar',
    text: '«Скоро запуск» · «90%» · «Доставка по всему Кыргызстану»',
    html: page('Kiwi Go — 04', `
${wordmark(80, 72)}
<div class="t" style="left:0;width:1080px;text-align:center;top:236px;font-weight:900;font-size:140px;letter-spacing:-0.045em">Скоро запуск</div>
<svg class="scene" width="1080" height="1080">
  <rect x="${bx + sw / 2}" y="${by + sw / 2}" width="${bw - sw}" height="${bh - sw}" rx="${(bh - sw) / 2}" fill="${C.paper}" stroke="${C.ink}" stroke-width="${sw}"/>
  <rect x="${bx + pad}" y="${by + pad}" width="${fillW}" height="${bh - 2 * pad}" rx="${(bh - 2 * pad) / 2}" fill="${C.lime}"/>
</svg>
<div class="t" style="left:${bx + 64}px;top:${by + bh / 2 - 36}px;font-weight:900;font-size:72px;letter-spacing:-0.03em">90%</div>
${logoFull(wheel, endX - wheel, by + pad, 'transform:rotate(-20deg)')}
<div class="t" style="left:0;width:1080px;text-align:center;top:790px;font-weight:700;font-size:52px;letter-spacing:-0.01em">Доставка по всему Кыргызстану</div>
`),
  });
}

// 05 — Parcel label
{
  // front face
  const fx = 230, fy = 410, fw = 560, fh = 360, dx = 100, dy = 84;
  const lw = 400, lh = 228, lx = fx + (fw - lw) / 2, ly = fy + 74;
  designs.push({
    dir: 'Parcel label',
    text: '«Скоро поедем» · «Скоро» (на этикетке) · «Платите только за доставку»',
    html: page('Kiwi Go — 05', `
<div class="t" style="left:0;width:1080px;text-align:center;top:110px;font-weight:900;font-size:124px;letter-spacing:-0.045em">Скоро поедем</div>
<svg class="scene" width="1080" height="1080" stroke-linejoin="round">
  <!-- top lid -->
  <polygon points="${fx},${fy} ${fx + fw},${fy} ${fx + fw + dx},${fy - dy} ${fx + dx},${fy - dy}" fill="${C.sand}" stroke="${C.ink}" stroke-width="7"/>
  <!-- tape on lid (kiwi-peel brown) -->
  <polygon points="${fx + fw / 2 - 34},${fy} ${fx + fw / 2 + 34},${fy} ${fx + fw / 2 + 34 + dx},${fy - dy} ${fx + fw / 2 - 34 + dx},${fy - dy}" fill="${C.peel}" stroke="${C.ink}" stroke-width="5"/>
  <!-- right side -->
  <polygon points="${fx + fw},${fy} ${fx + fw + dx},${fy - dy} ${fx + fw + dx},${fy + fh - dy} ${fx + fw},${fy + fh}" fill="${C.sand}" stroke="${C.ink}" stroke-width="7"/>
  <!-- front -->
  <rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" fill="${C.cream}" stroke="${C.ink}" stroke-width="7"/>
  <!-- tape running down the front -->
  <rect x="${fx + fw / 2 - 34}" y="${fy}" width="68" height="${ly - fy - 18}" fill="${C.peel}" stroke="${C.ink}" stroke-width="5"/>
  <!-- label -->
  <rect x="${lx}" y="${ly}" width="${lw}" height="${lh}" rx="18" fill="${C.paper}" stroke="${C.ink}" stroke-width="6"/>
  <line x1="${lx + 28}" y1="${ly + 112}" x2="${lx + lw - 28}" y2="${ly + 112}" stroke="${C.ink}" stroke-width="4" stroke-dasharray="10 10"/>
  <!-- this-side-up arrows on the side -->
  <g fill="none" stroke="${C.ink}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M ${fx + fw + 50} ${fy + 140} l 0 -48 m -14 16 l 14 -16 l 14 16"/>
  </g>
  <!-- ground -->
  <rect x="150" y="${fy + fh + 26}" width="780" height="10" rx="5" fill="${C.ink}"/>
</svg>
${wordmark(lx + 32, ly + 26, 64, 44)}
<div class="t" style="left:${lx}px;width:${lw}px;text-align:center;top:${ly + 136}px;font-weight:900;font-size:68px;letter-spacing:-0.04em">Скоро</div>
<div class="t" style="left:0;width:1080px;text-align:center;top:910px;font-weight:700;font-size:48px;letter-spacing:-0.01em">Платите только за доставку</div>
`),
  });
}

module.exports = { designs };

(async () => {
  const only = process.argv.slice(2).map(Number);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 2 });
  const report = [];
  for (let i = 0; i < designs.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    if (only.length && !only.includes(i + 1)) continue;
    const htmlPath = path.join(ROOT, 'html', `kiwi-go-soon-${n}.html`);
    fs.writeFileSync(htmlPath, designs[i].html);
    const pg = await ctx.newPage();
    await pg.goto('file://' + htmlPath);
    await pg.evaluate(() => document.fonts.ready);
    // geometry check: every text/logo element inside the canvas with >=40px margin from edges
    const geo = await pg.evaluate(() => [...document.querySelectorAll('.t,.wm,.logo')].map(e => {
      let r = e.getBoundingClientRect();
      if (e.classList && e.classList.contains('t')) { const rg = document.createRange(); rg.selectNodeContents(e); r = rg.getBoundingClientRect(); }
      return { txt: (e.textContent || '').trim().slice(0, 30) || e.className.baseVal || e.className, l: Math.round(r.left), t: Math.round(r.top), r: Math.round(r.right), b: Math.round(r.bottom),
        sw: e.scrollWidth, cw: e.clientWidth };
    }));
    // font check through CDP: which platform font actually painted each text node
    const cdp = await ctx.newCDPSession(pg);
    await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
    const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
    const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: '.t, .wm span' });
    const fonts = new Set();
    for (const id of nodeIds) {
      const { fonts: f } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId: id });
      f.forEach(x => fonts.add(x.familyName + (x.isCustomFont ? ' (webfont)' : ' (SYSTEM FALLBACK)')));
    }
    await pg.screenshot({ path: path.join(ROOT, `kiwi-go-soon-${n}.png`) });
    report.push({ n, fonts: [...fonts], geo });
    await pg.close();
  }
  await browser.close();
  for (const r of report) {
    console.log(`#${r.n} fonts: ${r.fonts.join(', ')}`);
    for (const g of r.geo) {
      const bad = g.l < 40 || g.t < 40 || g.r > 1040 || g.b > 1040;
      if (bad) console.log(`   EDGE ${JSON.stringify(g)}`);
    }
  }
})();
