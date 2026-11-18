// Renders reel.html frame by frame with Playwright.
//   node render.js preview 0.3 1.5 ...   -> preview/t_<t>.png (single sharp stills)
//   node render.js                       -> sub/s_00000.png ... (SUB sub-frames per frame, for motion blur via ffmpeg tmix)
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const FPS = 30, DUR = 9.6, SUB = 4, SHUTTER = 0.5; // 180° shutter, 4 samples
const DIR = __dirname;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(DIR, 'reel.html'));
  await page.waitForFunction(() => window.READY === true);
  // verify the webfonts are really in use
  const ok = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family));
  console.log('fonts loaded:', ok.join(', '));

  const args = process.argv.slice(2);
  if (args[0] === 'preview') {
    const out = path.join(DIR, 'preview');
    fs.mkdirSync(out, { recursive: true });
    for (const a of args.slice(1)) {
      await page.evaluate(t => render(t), +a);
      await page.screenshot({ path: path.join(out, `t_${(+a).toFixed(2)}.png`) });
    }
  } else {
    const out = path.join(DIR, 'sub');
    fs.rmSync(out, { recursive: true, force: true });
    fs.mkdirSync(out, { recursive: true });
    const N = Math.round(FPS * DUR);
    let idx = 0;
    const t0 = Date.now();
    for (let f = 0; f < N; f++) {
      for (let k = 0; k < SUB; k++) {
        const t = f / FPS + k * (SHUTTER / FPS) / SUB;
        await page.evaluate(t => render(t), t);
        await page.screenshot({ path: path.join(out, `s_${String(idx++).padStart(5, '0')}.png`) });
      }
      if (f % 30 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(1)}s`);
    }
    console.log('done', idx, 'sub-frames');
  }
  await browser.close();
})();
