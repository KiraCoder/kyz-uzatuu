// Renders reel.html frame by frame with Playwright (2 sub-frames per frame for light motion blur).
//   node render.js preview 0.3 1.5 ...   -> preview/t_<t>.png
//   node render.js                       -> frames/s_00000.png ...
// Always writes timing.json (sync points for audio.py).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const FPS = 30, DUR = 14.0, SUB = 2, SHUTTER = 0.5;
const DIR = __dirname;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(DIR, 'reel.html'));
  await page.waitForFunction(() => window.READY === true);
  const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family));
  console.log('fonts loaded:', fonts.join(', '));
  const timing = await page.evaluate(() => ({ ...window.TIMING, sizes: { hook: L.hook, sweep: L.sweep, ben: L.ben, wm: L.wm, sub: L.sub, url: L.url } }));
  fs.writeFileSync(path.join(DIR, 'timing.json'), JSON.stringify(timing, null, 1));
  console.log(JSON.stringify(timing.sizes), 'WARN:', JSON.stringify(timing.warn));
  const args = process.argv.slice(2);
  if (args[0] === 'preview') {
    const out = path.join(DIR, 'preview'); fs.mkdirSync(out, { recursive: true });
    for (const a of args.slice(1)) {
      await page.evaluate(t => render(t), +a);
      await page.screenshot({ path: path.join(out, `t_${(+a).toFixed(2)}.png`) });
    }
  } else if (args[0] !== 'timing') {
    const out = path.join(DIR, 'frames');
    fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
    const N = Math.round(FPS * DUR); let idx = 0; const t0 = Date.now();
    for (let f = 0; f < N; f++) {
      for (let k = 0; k < SUB; k++) {
        const t = f / FPS + k * (SHUTTER / FPS) / SUB;
        await page.evaluate(t => render(t), t);
        await page.screenshot({ path: path.join(out, `s_${String(idx++).padStart(5, '0')}.png`) });
      }
      if (f % 60 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(1)}s`);
    }
    console.log('done', idx, 'sub-frames');
  }
  await browser.close();
})();
