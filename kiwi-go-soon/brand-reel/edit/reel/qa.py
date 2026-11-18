"""QA: copy, colour rules, fonts, logo exactness, safe area, faces, export spec, stutter, loop, storyboards."""
import hashlib
import json
import os
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .common import W, H, FPS, EDIT_DIR, GFX_DIR, rp

SAFE = (80, 270, 900, 1250)
NB = ' '
EXPECTED = {   # 07 §1.3 / §1.4 + client decisions 2026-11-18
    'BU-1': 'где моя посылка?', 'BU-2': 'уже отправили?', 'BU-3': '??', 'BU-4': 'Отправлено ✓',
    'BU-5': 'получила, спасибо!',
    'SP-1': ['Заберём у двери'], 'SP-2': ['По всему', 'Кыргызстану'], 'SP-3': ['Видно каждый шаг'],
    'SP-4': ['Вручаем', 'по коду получения'],
    'wordmark': f'Kiwi{NB}Go', 'descriptor': f'Посылка{NB}— как сообщение', 'price': f'от{NB}350{NB}сом',
    'price_note': 'за посылку', 'cta': 'Оформите доставку', 'url_pill': 'kiwigo.kg',
    'whatsapp': f'WhatsApp: +996{NB}224{NB}222{NB}221',
    'chips': ['Забрали ✓', 'В пути', 'В городе', 'У курьера'],
}
PLAN_W = {'BU-1': 591, 'BU-2': 443, 'BU-5': 644, 'CARD-wordmark': 468, 'CARD-descriptor': 603,
          'CARD-price': 566, 'CARD-price_note': 221, 'CARD-cta': 475, 'CARD-url_pill': 272}


def run(cfg, reel, results):
    rep = {'checks': [], 'issues': []}

    def chk(name, ok, detail=''):
        rep['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail})
        if not ok:
            rep['issues'].append(f'{name}: {detail}')

    ui = cfg['ui']
    # ---- copy ----
    for k in ('BU-1', 'BU-2', 'BU-3', 'BU-4', 'BU-5'):
        chk(f'copy {k}', ui['bubbles'][k]['text'] == EXPECTED[k], ui['bubbles'][k]['text'])
    for k in ('SP-1', 'SP-2', 'SP-3', 'SP-4'):
        chk(f'copy {k}', ui['supers'][k]['lines'] == EXPECTED[k], ' / '.join(ui['supers'][k]['lines']))
    for k in ('wordmark', 'descriptor', 'price', 'price_note', 'cta', 'url_pill', 'whatsapp'):
        chk(f'copy card {k} (incl. U+00A0)', ui['card'][k]['text'] == EXPECTED[k], ui['card'][k]['text'].replace(NB, '⍽'))
    chk('copy chips', ui['pip']['chips_active'] == EXPECTED['chips'], ', '.join(ui['pip']['chips_active']))
    chk('PiP title', ui['pip']['title'] == 'Kiwi\u00a0Go' and ui['pip']['subtitle'] == 'для магазинов')
    alltext = json.dumps(ui, ensure_ascii=False)
    chk('«Заберём» keeps ё', 'Заберем' not in alltext and 'Заберём' in alltext)
    chk('single tick ✓ (no ✓✓ / ✔)', '✓✓' not in alltext and '✔' not in alltext)
    chk('no «Вручено» chip', 'Вручено' not in alltext)
    # ---- colours: lime never as text on light ----
    text_cols = [ui['card'][k]['color'] for k in ('wordmark', 'descriptor', 'price', 'price_note', 'cta', 'url_pill', 'whatsapp')]
    chk('no lime text', all(c != 'lime' for c in text_cols), ', '.join(text_cols))
    html = open(os.path.join(EDIT_DIR, 'gfx', 'gfx.html'), encoding='utf-8').read()
    lime_text = re.findall(r"fillStyle = col\('lime'\);\s*ctx\.fillText", html)
    chk('no lime fillText in gfx.html', not lime_text)
    # ---- fonts ----
    meta = reel.gmeta
    chk('Onest Local loaded (600/700) incl. ёЁ«»—…✓', meta['checks']['f600'] and meta['checks']['f700'], json.dumps(meta['checks']))
    try:
        from fontTools.ttLib import TTFont
        for w in ('600', '700'):
            cm = TTFont(rp(cfg['fonts'][w])).getBestCmap()
            miss = [c for c in 'ёЁ«»—✓' + NB if ord(c) not in cm]
            chk(f'Onest {w} cmap has ёЁ«»—✓ NBSP', not miss, ''.join(miss))
    except ImportError:
        pass
    for k, w in PLAN_W.items():
        got = meta['els'][k]['text_w']
        chk(f'width {k} vs plan', abs(got - w) <= 3, f'{got:.1f} vs {w}')
    # ---- logo ----
    svg = open(rp(cfg['logo_svg']), encoding='utf-8').read()
    chk('logo SVG has 12 seeds', svg.count('<ellipse') == 12, hashlib.sha1(svg.encode()).hexdigest()[:12])
    pf = cfg['poster']
    if os.path.exists(rp(pf['out'])):
        poster = np.asarray(Image.open(rp(pf['out']))).astype(np.float32) / 255
        lg = np.asarray(Image.open(os.path.join(GFX_DIR, 'logo_260.png')).convert('RGBA')).astype(np.float32) / 255
        crop = poster[340:600, 360:620]
        full = lg[..., 3] > 0.999
        diff = np.abs(crop[full] - lg[..., :3][full]).max() * 255
        chk('card logo pixel-exact vs SVG render (opaque px)', diff <= 1.0, f'max diff {diff:.2f}/255 over {full.sum()} px')
    # ---- per-frame: safe area, faces, windows ----
    for name, metas in results.items():
        bad, faces, win = [], [], []
        for m in metas:
            for item in m['ui']:
                label, bb = item[0], item[1]
                if bb is None or (len(item) > 2 and item[2] == 'transit'):
                    continue
                if not (bb[0] >= SAFE[0] - 1 and bb[1] >= SAFE[1] - 1 and bb[2] <= SAFE[2] + 1 and bb[3] <= SAFE[3] + 1):
                    bad.append((m['f'], label, bb))
                for fb in m['faces']:
                    if bb[0] < fb[2] and bb[2] > fb[0] and bb[1] < fb[3] and bb[3] > fb[1]:
                        faces.append((m['f'], label))
            if 'window_violation' in m:
                win.append((m['f'], m['window_violation']))
        chk(f'{name}: all UI/text inside x80–900 y270–1250', not bad, str(bad[:6]))
        chk(f'{name}: no text over faces', not faces, str(faces[:6]))
        chk(f'{name}: clips used only inside QA windows', not win, str(win[:4]))
        chk(f'{name}: loop fog f0 == f_last', abs(metas[0]['fog'] - metas[-1]['fog']) < 1e-3, f"{metas[0]['fog']} / {metas[-1]['fog']}")
    # ---- exports ----
    for name in results:
        E = cfg['edits'][name]
        path = rp(E['out'])
        pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path],
                                       capture_output=True, text=True).stdout)
        vs = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]
        aud = [s for s in pr['streams'] if s['codec_type'] == 'audio']
        dur = float(pr['format']['duration'])
        ok = (vs['codec_name'] == 'h264' and vs['profile'] == 'High' and vs['pix_fmt'] == 'yuv420p'
              and vs['width'] == W and vs['height'] == H and vs['r_frame_rate'] == '24/1' and not aud
              and int(vs['nb_frames']) == E['frames'] and abs(dur - E['frames'] / FPS) < 0.01)
        mbps = int(pr['format']['bit_rate']) / 1e6
        chk(f'{name}: export spec', ok, f"{vs['codec_name']} {vs['profile']} {vs['pix_fmt']} {vs['width']}x{vs['height']} "
            f"{vs['r_frame_rate']} frames={vs['nb_frames']} dur={dur:.3f}s audio={len(aud)} {mbps:.1f} Mbps")
        moov = open(path, 'rb').read(4096)
        chk(f'{name}: +faststart (moov before mdat)', moov.find(b'moov') != -1 and (moov.find(b'mdat') == -1 or moov.find(b'moov') < moov.find(b'mdat')))
        fr = decode_small(path)
        d = np.abs(np.diff(fr.astype(np.int16), axis=0)).mean(axis=(1, 2))
        dups = int((d < 0.15).sum())
        chk(f'{name}: duplicate-frame ratio < 2 %', dups / len(d) < 0.02, f'{dups}/{len(d)} = {100 * dups / len(d):.2f} %')
        loop = float(np.abs(fr[0].astype(np.float32).mean(axis=(0, 1)) - fr[-1].astype(np.float32).mean(axis=(0, 1))).mean())
        rep.setdefault('loop_luma_jump_last_to_first_info', {})[name] = round(loop, 2)  # card -> night hook; the loop match is the 20 % fog state, checked above
        storyboard(cfg, name, path)
    rep['sources'] = reel.src_info
    with open(os.path.join(EDIT_DIR, 'out', 'qa_report.json'), 'w', encoding='utf-8') as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=1)
    n_ok = sum(c['ok'] for c in rep['checks'])
    print(f'QA: {n_ok}/{len(rep["checks"])} checks passed')
    for i in rep['issues']:
        print('  ISSUE', i)
    return rep


def decode_small(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', 'scale=135:240', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 240, 135)


def storyboard(cfg, name, path):
    frames = cfg['storyboard'][name]
    sel = '+'.join(f'eq(n\\,{f})' for f in frames)
    tw, th = 324, 576
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f"select='{sel}',scale={tw}:{th}", '-vsync', '0',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    imgs = np.frombuffer(raw, np.uint8).reshape(-1, th, tw, 3)
    cols = 4
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw + (cols + 1) * 8, rows * (th + 30) + 8), (24, 26, 22))
    try:
        font = ImageFont.truetype(rp(cfg['fonts']['600']), 20)
    except OSError:
        font = None
    k = tw / W
    for i, im in enumerate(imgs):
        x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 30)
        p = Image.fromarray(im)
        d = ImageDraw.Draw(p)
        d.rectangle([SAFE[0] * k, SAFE[1] * k, SAFE[2] * k, SAFE[3] * k], outline=(0, 200, 255))
        sheet.paste(p, (x, y + 26))
        f = frames[i]
        ImageDraw.Draw(sheet).text((x, y + 2), f'f{f:03d}  {f / FPS:6.3f}s', fill=(240, 240, 230), font=font)
    out = os.path.join(EDIT_DIR, 'out', f'storyboard_{name}.png')
    sheet.save(out)
    print('  storyboard ->', out)
