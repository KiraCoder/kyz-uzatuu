// Instagram avatars built from logo option Б (full version, lime palette)
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const seeds = [...Array(12)].map((_, i) =>
  `<ellipse cx="0" cy="-56.3" rx="5" ry="14" transform="rotate(${i * 30})"/>`).join('');
// exact logo Б geometry (measured from the approved logo)
const logo = (r) => `<g transform="scale(${r / 100})">
  <circle r="100" fill="#111410"/><circle r="86" fill="#6BA82B"/><circle r="80.5" fill="#B8F03C"/>
  <g fill="#111410">${seeds}</g><circle r="26" fill="#F6F1E4"/><circle r="8.5" fill="#111410"/></g>`;
// viewBox -170..170 (340 units); Instagram crops to the inscribed circle r=170
const V = {
  '1-full-bleed': { bg: '#FFFDF7', body: logo(160) },             // logo fills the circle
  '2-lime':       { bg: '#B8F03C', body: logo(128) },
  '3-ink':        { bg: '#111410', body: `<circle r="134" fill="#FFFDF7"/>${logo(122)}` },
  '4-paper':      { bg: '#FFFDF7', body: logo(118) },
};
(async () => {
  const b = await chromium.launch();
  for (const [name, v] of Object.entries(V)) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-170 -170 340 340"><rect x="-170" y="-170" width="340" height="340" fill="${v.bg}"/>${v.body}</svg>`;
    fs.writeFileSync(`kiwi-go-avatar-b${name}.svg`, svg);
    for (const [size, dsf] of [[340, 1], [1080, 1]]) {
      const p = await b.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: dsf });
      await p.setContent(`<html><body style="margin:0">${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}</body></html>`);
      await p.screenshot({ path: `kiwi-go-avatar-b${name}-${size}.png` });
      await p.close();
    }
  }
  await b.close();
})();
