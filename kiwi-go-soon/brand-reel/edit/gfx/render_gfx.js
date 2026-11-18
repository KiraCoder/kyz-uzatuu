// Renders every UI/card element (Onest, canvas in Chromium via Playwright) to transparent 2x PNGs,
// plus the exact logo SVG at several sizes. Usage: node render_gfx.js <brand-reel dir> <out dir>
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(process.argv[2]);
  const outDir = path.resolve(process.argv[3]);
  fs.mkdirSync(outDir, { recursive: true });
  const cfg = JSON.parse(fs.readFileSync(path.join(root, 'edit/config.json'), 'utf8'));
  const svg = fs.readFileSync(path.join(root, cfg.logo_svg), 'utf8');
  const browser = await chromium.launch();

  // 1) UI and card elements
  const page = await browser.newPage({ viewport: { width: 400, height: 300 } });
  await page.goto('file://' + path.join(root, 'edit/gfx/gfx.html'));
  const res = await page.evaluate(async ([c, s]) => await window.renderAll(c, s), [cfg, svg]);
  if (!res.checks.f600 || !res.checks.f700) throw new Error('Onest Local not loaded: ' + JSON.stringify(res.checks));
  const meta = { checks: res.checks, els: {} };
  for (const e of res.els) {
    const b64 = e.png.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(path.join(outDir, e.name + '@2x.png'), Buffer.from(b64, 'base64'));
    delete e.png;
    meta.els[e.name] = e;
  }

  // 2) the exact logo SVG, rendered as-is (render.js pattern), transparent background
  meta.logo = {};
  for (const s of [2400, 300, 260]) {
    const p = await browser.newPage({ viewport: { width: s, height: s } });
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${s}" height="${s}" `)}</body></html>`);
    const f = path.join(outDir, `logo_${s}.png`);
    await p.screenshot({ path: f, omitBackground: true });
    meta.logo[s] = path.basename(f);
    await p.close();
  }
  fs.writeFileSync(path.join(outDir, 'meta.json'), JSON.stringify(meta, null, 1));
  await browser.close();
  console.log('gfx: ' + Object.keys(meta.els).length + ' elements; fonts ' + JSON.stringify(res.checks));
})().catch(e => { console.error(e); process.exit(1); });
