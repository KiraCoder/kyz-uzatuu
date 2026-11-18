// Renders avatar SVGs to 340 and 1080 PNGs, and logos to transparent 512/1024 PNGs.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const D = __dirname;
const html = (svg, size, transparent) => `<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0}html,body{width:${size}px;height:${size}px;overflow:hidden;background:${transparent ? 'transparent' : '#fff'}}
svg{display:block;width:${size}px;height:${size}px}</style></head><body>${svg}</body></html>`;
(async () => {
  const browser = await chromium.launch();
  const shot = async (svg, size, out, transparent = false) => {
    const pg = await browser.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: 1 });
    await pg.setContent(html(svg, size, transparent));
    await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot({ path: out, omitBackground: transparent });
    await pg.close();
  };
  const files = fs.readdirSync(path.join(D, 'svg')).filter(f => /^kiwi-go-avatar-\d+\.svg$/.test(f)).sort();
  for (const f of files) {
    const nn = f.match(/(\d+)/)[1];
    const svg = fs.readFileSync(path.join(D, 'svg', f), 'utf8');
    await shot(svg, 340, path.join(D, `kiwi-go-avatar-${nn}-340.png`));
    await shot(svg, 1080, path.join(D, `kiwi-go-avatar-${nn}-1080.png`));
  }
  for (const kind of ['full', 'small']) {
    const svg = fs.readFileSync(path.join(D, 'logo', `kiwi-go-logo-${kind}.svg`), 'utf8');
    for (const s of [512, 1024]) await shot(svg, s, path.join(D, 'logo', `kiwi-go-logo-${kind}-${s}.png`), true);
  }
  await browser.close();
  console.log('rendered', files.length);
})();
