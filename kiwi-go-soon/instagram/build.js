// Instagram profile kit: highlight covers (1080x1920) + a dark-mode profile mockup
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const INK = '#111410', LIME = '#B8F03C', CREAM = '#F6F1E4', RIM = '#6BA82B';
const seeds = [...Array(12)].map((_, i) => `<ellipse cx="0" cy="-56.3" rx="5" ry="14" transform="rotate(${i * 30})"/>`).join('');
const LOGO = `<circle r="100" fill="${INK}"/><circle r="86" fill="${RIM}"/><circle r="80.5" fill="${LIME}"/><g fill="${INK}">${seeds}</g><circle r="26" fill="${CREAM}"/><circle r="8.5" fill="${INK}"/>`;
const S = `fill="none" stroke="${INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"`;
// icons drawn in a -100..100 box
const icons = {
  'o-nas':   { label: 'О нас',    svg: `<g transform="scale(0.78)">${LOGO}</g>` },
  'tarify':  { label: 'Тарифы',   svg: `<g ${S}><path d="M-62 -18 L-8 -72 L62 -72 L62 -2 L8 52 Z" transform="translate(0 10)"/><circle cx="36" cy="-36" r="10"/><path d="M-22 18 l26 -26 M-30 2 l10 10 M-6 -22 l10 10"/></g>` },
  'zakaz':   { label: 'Заказ',    svg: `<g ${S}><path d="M-64 -30 L0 -62 L64 -30 L64 42 L0 74 L-64 42 Z"/><path d="M-64 -30 L0 2 L64 -30 M0 2 L0 74"/><path d="M-32 -46 L32 -14"/></g>` },
  'zona':    { label: 'Доставка', svg: `<g ${S}><path d="M0 74 C -40 30 -58 4 -58 -22 A58 58 0 0 1 58 -22 C 58 4 40 30 0 74 Z"/><circle cx="0" cy="-22" r="22"/></g>` },
  'kuryeram':{ label: 'Курьерам', svg: `<g ${S}><circle cx="-48" cy="34" r="30"/><circle cx="52" cy="34" r="30"/><path d="M-48 34 L-12 -26 L36 -26 L52 34 M-12 -26 L8 34 L-48 34 M30 -50 L48 -50 M36 -26 L30 -50"/></g>` },
  'faq':     { label: 'Вопросы',  svg: `<g ${S}><path d="M-70 -50 Q-70 -70 -50 -70 L50 -70 Q70 -70 70 -50 L70 22 Q70 42 50 42 L-6 42 L-40 70 L-34 42 L-50 42 Q-70 42 -70 22 Z"/><path d="M-18 -30 Q-18 -48 0 -48 Q20 -48 20 -30 Q20 -16 0 -10 L0 4"/><circle cx="0" cy="22" r="3" fill="${INK}"/></g>` },
};
const cover = (svg) => `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<rect width="1080" height="1920" fill="${LIME}"/>
<g transform="translate(540 960) scale(2.1)">${svg}</g></svg>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, v] of Object.entries(icons)) {
    fs.writeFileSync(`highlights/${k}.svg`, cover(v.svg));
    await p.setContent(`<body style="margin:0">${cover(v.svg)}</body>`);
    await p.screenshot({ path: `highlights/kiwi-go-highlight-${k}.png` });
  }
  // ---- profile mockup (dark mode, 430pt wide like an iPhone) ----
  const img = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
  const hl = Object.entries(icons).map(([k, v]) => `<div class="hl"><div class="ring"><svg viewBox="-100 -100 200 200"><circle r="100" fill="${LIME}"/><g transform="scale(0.62)">${v.svg}</g></svg></div><span>${v.label}</span></div>`).join('');
  const html = `<html><head><style>
  @font-face{font-family:I;src:url('file:///usr/share/fonts/opentype/inter/Inter-Regular.otf')}
  @font-face{font-family:I;font-weight:600;src:url('file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf')}
  @font-face{font-family:I;font-weight:700;src:url('file:///usr/share/fonts/opentype/inter/Inter-Bold.otf')}
  *{box-sizing:border-box;margin:0}body{width:430px;background:#0c0f14;color:#f5f5f5;font-family:I,sans-serif;font-size:14.5px}
  .top{display:flex;justify-content:center;font-weight:700;font-size:21px;padding:18px 0 10px}
  .head{display:flex;align-items:center;gap:22px;padding:6px 16px}
  .av{width:92px;height:92px;border-radius:50%;background:url(${img('../avatar/logo-b/kiwi-go-avatar-b5-edge-1080.png')}) center/cover}
  .stats{flex:1}.name{font-weight:600;font-size:15px;margin-bottom:8px}.nums{display:flex;gap:26px}.nums b{display:block;font-size:17px}
  .bio{padding:10px 16px 0;line-height:1.38}.cat{color:#a8a8a8}.link{color:#8fa7ff;margin-top:2px}
  .btns{display:flex;gap:6px;padding:14px 16px 0}.btns div{flex:1;background:#2a2d33;border-radius:9px;text-align:center;padding:8px 0;font-weight:600;font-size:13.5px}
  .hls{display:flex;gap:14px;padding:16px 14px 8px;overflow:hidden}.hl{width:66px;flex:none;text-align:center;font-size:12px}
  .ring{width:66px;height:66px;border-radius:50%;border:1.5px solid #3a3d44;padding:3px;margin-bottom:5px}.ring svg{width:100%;height:100%}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:10px}.grid div{aspect-ratio:3/4;background-size:cover;background-position:center}
  </style></head><body>
  <div class="top">kiwigo.kg</div>
  <div class="head"><div class="av"></div><div class="stats"><div class="name">Kiwi Go · Курьерская служба</div><div class="nums"><div><b>6</b>публикаций</div><div><b>0</b>подписчиков</div><div><b>0</b>подписок</div></div></div></div>
  <div class="bio"><div class="cat">Курьерская служба</div>🥝 Курьерская доставка по всему Кыргызстану<br>💸 Платите только за доставку<br>🚀 Скоро запуск — подпишитесь!<div class="link">🔗 kiwigo.kg</div></div>
  <div class="btns"><div>Подписаться</div><div>Сообщение</div><div>Связаться</div></div>
  <div class="hls">${hl}</div>
  <div class="grid">${['banner/kiwi-go-banner-1-post3.png','banner/kiwi-go-banner-2-post2.png','banner/kiwi-go-banner-3-post1.png','../creative/kiwi-go-creative-03.png','../reel/poster.png','../creative/kiwi-go-creative-04.png'].map(f => `<div style="background-image:url(${img(f)})"></div>`).join('')}</div>
  </body></html>`;
  fs.writeFileSync('mockup.html', html);
  const m = await b.newPage({ viewport: { width: 430, height: 820 }, deviceScaleFactor: 2 });
  await m.goto('file://' + path.resolve('mockup.html')); await m.evaluate(() => document.fonts.ready);
  await m.screenshot({ path: 'profile-mockup.png', fullPage: true });
  await b.close();
})();
