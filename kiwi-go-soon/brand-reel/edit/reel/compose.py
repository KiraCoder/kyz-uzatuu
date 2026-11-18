"""Per-frame compositor on the 24 fps grid. Layer order (07 §5.2):
plate -> R6 grade (+tilt-shift) -> in-world (trail, kiwi wheels) -> bloom / sweep / camera fx / leak,
haze, glow, flash -> grain -> UI (bubbles, PiP, supers; crisp) -> fog."""
import json
import math
import os

import numpy as np

from .common import (W, H, FPS, GFX_DIR, Colors, Layer, over, alpha_bbox, rp, hex_rgb, lerp,
                     ease_out_cubic, ease_in_cubic, ease_in_out, ease_out_back)
from .look import Look
from .sources import Clip, StillKB, Parallax25D
from .inworld import Logo, Trail, Wheels

CHIP_XFADE = 3


class Reel:
    def __init__(self, cfg, log=print):
        self.cfg = cfg
        self.col = Colors(cfg)
        self.look = Look(cfg)
        meta = json.load(open(os.path.join(GFX_DIR, 'meta.json'), encoding='utf-8'))
        self.gmeta = meta
        self.L = {k: Layer(k, m, os.path.join(GFX_DIR, k + '@2x.png')) for k, m in meta['els'].items()}
        self.logo = Logo()
        self.src, self.src_info = {}, {}
        used = {s['shot'] for e in cfg['edits'].values() for s in e['segments']} - {'CARD'}
        for name in sorted(used):
            sc = cfg['shots'][name]
            src = None
            for c in sc.get('clip') or []:
                if os.path.exists(rp(c)):
                    src = Clip(rp(c), sc.get('reframe', {}), sc.get('window'))
                    self.src_info[name] = 'clip ' + c
                    break
            if src is None and sc.get('plate', {}).get('type') == 'parallax':
                src = Parallax25D(sc['plate'], os.path.join(os.path.dirname(GFX_DIR)))
                self.src_info[name] = '2.5D parallax from ' + sc['plate']['image']
            if src is None:
                ph = sc['placeholder']
                src = StillKB(ph['image'], ph['duration'], ph['kb'])
                self.src_info[name] = 'PLACEHOLDER still ' + ph['image']
            self.src[name] = src
            log(f'  {name}: {self.src_info[name]}')
        s3 = cfg['shots'].get('S3', {})
        self.trail = Trail(s3['trail'], cfg['colors']) if 'trail' in s3 else None
        if 'S3' in self.src and isinstance(self.src['S3'], Clip) and s3['trail'].get('track') in ('orb', 'auto'):
            self.src['S3'].track_camera()
        s6 = cfg['shots']['S6']
        self.wheels = Wheels(s6['wheels'], s6['sweep'], self.logo)
        self.card_bg = self.look.card_bg()

    # ---------------- timeline ----------------
    def segment(self, edit, f):
        for s in edit['segments']:
            if s['start_f'] <= f < s['end_f']:
                return s
        raise ValueError(f)

    @staticmethod
    def src_time(seg, f):
        i = f - seg['start_f']
        n = seg['end_f'] - seg['start_f']
        sp = seg.get('speed', 1.0)
        if seg.get('retime') == 'ease':
            mn = seg.get('min_speed', 1.0)
            a = (sp / mn - 1) * math.pi / 2
            u = i / n
            G = (u + a / math.pi * (1 - math.cos(math.pi * u))) / (1 + 2 * a / math.pi)
            return seg['in'] + sp * (n / FPS) * G
        return seg['in'] + sp * i / FPS

    def seg_time_fn(self, seg):
        """edit time (s) -> source time for a segment (extrapolates linearly outside it)."""
        return lambda t: self.src_time(seg, t * FPS)

    # ---------------- frame ----------------
    def render(self, edit_name, f):
        cfg = self.cfg
        E = cfg['edits'][edit_name]
        fx = E['fx']
        seg = self.segment(E, f)
        t = f / FPS
        meta = {'f': f, 'shot': seg['shot'], 'ui': [], 'faces': [], 'fog': 0.0}
        if seg['shot'] == 'CARD':
            img = self.render_card(E, seg, f, t, meta)
        else:
            img = self.render_shot(E, seg, f, t, meta)
        k = 0.0
        fi = fx.get('fog_in')
        if fi and fi['start_f'] <= f < fi['start_f'] + fi['len_f']:
            u = (f - fi['start_f']) / fi['len_f']
            k = fi['k'] * (1 - ease_out_cubic(u))
        fo = fx.get('fog_out')
        if fo and fo['start_f'] <= f <= fo['end_f']:
            k = fo['k'] * (f - fo['start_f'] + 1) / (fo['end_f'] - fo['start_f'] + 1)
        if k > 0:
            img = self.look.fog(img, k)
        meta['fog'] = round(k, 4)
        return np.clip(img * 255 + 0.5, 0, 255).astype(np.uint8), meta

    def render_shot(self, E, seg, f, t, meta):
        cfg, look, fx = self.cfg, self.look, E['fx']
        name = seg['shot']
        sc = cfg['shots'][name]
        src = self.src[name]
        st = self.src_time(seg, f)
        meta['src_t'] = round(st, 4)
        win = sc.get('window')
        if win and not (win[0] - 1e-6 <= st <= win[1] + 1 / FPS):
            meta['window_violation'] = [st, win]
        plate = src.frame(st)
        u = (f - seg['start_f']) / max(1, seg['end_f'] - seg['start_f'] - 1)
        sat = sc['sat'] if not isinstance(sc['sat'], list) else lerp(sc['sat'][0], sc['sat'][1], u)
        img = look.grade(plate, sat, sc.get('warmth', 0), sc.get('tiltshift'), sc.get('soft_sigma', 0))
        la = None
        if name == 'S3' and self.trail is not None:
            img = self.trail.render(img, src, st)
        if name == 'S6':
            img, la = self.wheels.render(img, src, st, t, E['sweep'], self.seg_time_fn(seg), cfg['colors'])
        bloom = look.g['bloom']['strength']
        fi = fx.get('fog_in')
        if fi and f < fi['start_f'] + fi['len_f']:
            bloom += 0.6 * fi['k'] * (1 - ease_out_cubic(f / fi['len_f']))
        img = look.bloom(img, bloom)
        if name == 'S6':
            img = self.wheels.sweep(img, src, t, E['sweep'], self.seg_time_fn(seg), cfg['colors'], st)
        # camera effects
        w = fx.get('whip')
        if w and w['start_f'] <= f <= w['end_f']:
            if f < w['cut_f']:
                i = f - w['start_f'] + 1
                n = w['cut_f'] - w['start_f']
                img = look.whip(img, w['max_blur'] * i / n, -w['px_per_f'] * i)
            else:
                j = w['end_f'] - f + 1
                n = w['end_f'] - w['cut_f'] + 1
                img = look.whip(img, w['max_blur'] * j / n, w['px_per_f'] * j)
        fp = fx.get('focus')
        if fp:
            if fp['out_start_f'] <= f < fp['cut_f']:
                img = look.defocus(img, fp['sigma'] * (f - fp['out_start_f'] + 1) / (fp['cut_f'] - fp['out_start_f']))
            elif fp['cut_f'] <= f <= fp['in_end_f']:
                img = look.defocus(img, fp['sigma'] * (1 - (f - fp['cut_f']) / (fp['in_end_f'] - fp['cut_f'] + 1)))
        # light transitions
        lk = fx.get('leak')
        if lk and lk['start_f'] <= f <= lk['end_f']:
            img = look.leak(img, (f - lk['start_f']) / (lk['end_f'] - lk['start_f']))
        hz = fx.get('haze')
        if hz:
            wv = 0.0
            if hz['start_f'] <= f <= hz['end_f']:
                wv = 0.85 * (1 - abs(f - hz['peak_f']) / (hz['peak_f'] - hz['start_f'] + 1))
            if hz['peak_f'] <= f < hz['peak_f'] + hz['lift_len_f']:
                wv = max(wv, hz['lift_from'] * (1 - ease_out_cubic((f - hz['peak_f']) / hz['lift_len_f'])))
            if wv > 0:
                img = look.wash(look.bloom(img, 0.5 * wv), wv)
        gl = fx.get('glow')
        if gl and str(f) in gl['weights']:
            img = look.glow(img, gl['weights'][str(f)])
        fl = fx.get('flash')
        if fl and str(f) in fl['weights']:
            wv = fl['weights'][str(f)]
            Wm = np.full((H, W), wv, np.float32)
            if la is not None:
                Wm = wv * (1 - la) + min(wv, fl['logo_cap']) * la
            img = lerp(img, look.paper, Wm[..., None])
        img = look.grain(img, cfg['grade']['grain'], f * 7919 + 13)
        # faces (for QA): fixed boxes in output px for clips
        for fx_, fy, fr in sc.get('faces_out', []):
            meta['faces'].append([fx_ - fr, fy - fr, fx_ + fr, fy + fr])
        self.draw_ui(E, f, t, img, meta)
        return img

    # ---------------- UI ----------------
    def draw_ui(self, E, f, t, img, meta):
        for b in E.get('bubbles', []):
            L = self.L[b['id']]
            fi, fo = round(b['in'] * FPS), round(b['out'] * FPS)
            if not (fi <= f < fo):
                continue
            a = 1.0 if f < fo - 4 else (fo - f) / 5
            s = 0.85 + 0.15 * ease_out_back((f - fi) / 6) if f - fi < 6 else 1.0
            ax, ay = L.meta['anchor']
            dy = b.get('dy', 0)
            im = L.scaled(s)
            x = ax + (L.x - ax) * s
            y = ay + (L.y - ay) * s + dy
            over(img, im, x, y, a)
            meta['ui'].append([b['id'], alpha_bbox(im, round(x), round(y), 0.6), L.meta.get('body')])
        for sp in E.get('supers', []):
            L = self.L[sp['id']]
            fi, fo = round(sp['in'] * FPS), int(math.floor(sp['out'] * FPS + 1e-6))
            if not (fi <= f <= fo):
                continue
            a = 1.0 if f < fo - 3 else (fo - f + 1) / 5
            over(img, L.img, L.x, L.y, a)
            meta['ui'].append([sp['id'], alpha_bbox(L.img, L.x, L.y, 0.6)])
        P = E.get('pip')
        if P:
            fi, fo = round(P['in'] * FPS), round(P['out'] * FPS)
            n = P['slide_f']
            if fi <= f < fo + n:
                base = self.L['PIP']
                dist = base.x + base.w + 40
                if f < fi + n:
                    dx = -dist * (1 - ease_out_cubic((f - fi + 1) / n))
                elif f >= fo:
                    dx = -dist * ease_in_cubic((f - fo + 1) / n)
                else:
                    dx = 0.0
                over(img, base.img, base.x + dx, base.y)
                times = P['chips']
                for i in range(4):
                    self.draw_chip(img, i, times, f, dx)
                meta['ui'].append(['PIP', alpha_bbox(base.img, round(base.x + dx), base.y, 0.6), 'transit' if abs(dx) > 0.01 else None])

    def chip_state(self, i, times, f):
        tf = [round(x * FPS) for x in times]
        if i >= len(tf) or f < tf[i]:
            return 'inactive', None
        if i + 1 < len(tf) and f >= tf[i + 1]:
            return 'past', tf[i + 1]
        return 'active', tf[i]

    def draw_chip(self, img, i, times, f, dx):
        state, since = self.chip_state(i, times, f)
        Lnew = self.L[f'CHIP-{i}-{state}']
        if since is not None and f - since < CHIP_XFADE:
            prev, _ = self.chip_state(i, times, since - 1)
            w = (f - since + 1) / (CHIP_XFADE + 1)
            Lp = self.L[f'CHIP-{i}-{prev}']
            over(img, Lp.img, Lp.x + dx, Lp.y, 1 - w)
            s = 1.0
            if state == 'active':
                s = 0.92 + 0.08 * ease_out_back((f - since) / 6)
            im = Lnew.scaled(s)
            over(img, im, Lnew.x + dx, Lnew.y + (Lnew.h - im.shape[0]) / 2, w)
            return
        if state == 'active' and since is not None and f - since < 6:
            s = 0.92 + 0.08 * ease_out_back((f - since) / 6)
            im = Lnew.scaled(s)
            over(img, im, Lnew.x + dx, Lnew.y + (Lnew.h - im.shape[0]) / 2)
            return
        over(img, Lnew.img, Lnew.x + dx, Lnew.y)

    # ---------------- end card ----------------
    def card_start_icon(self, E):
        """Card icon starts exactly where the in-world rear-wheel kiwi was on the last S6 frame."""
        seg = [s for s in E['segments'] if s['shot'] == 'S6'][0]
        st = self.src_time(seg, seg['end_f'] - 1)
        cx, cy, r = self.wheels.positions(self.src['S6'], st)['rear']
        return cx, cy, 2 * r * self.cfg['shots']['S6']['wheels']['logo_scale']

    def render_card(self, E, seg, f, t, meta):
        C = E['card']
        uc = self.cfg['ui']['card']
        img = self.card_bg.copy()
        fl = E['fx'].get('flash')
        if fl and str(f) in fl['weights']:
            img = lerp(img, self.look.paper, fl['weights'][str(f)])
        img = self.look.grain(img, 0.02, f * 7919 + 13)
        # icon: from the wheel (match cut) to Ø260 at (490, 470), easeInOut over 0.35 s
        x0, y0, d0 = self.card_start_icon(E)
        x1, y1, d1 = uc['icon_final']
        u = (t - C['t0']) / C['icon_ease']
        if u >= 1:
            x, y, d = x1, y1, d1
        else:
            e = ease_in_out(u)
            x, y, d = x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, d0 + (d1 - d0) * e
        lg = self.logo.at(d)
        over(img, lg, x - lg.shape[1] / 2, y - lg.shape[0] / 2)
        meta['logo'] = [x, y, d]
        meta['ui'].append(['ICON', [round(x - d / 2), round(y - d / 2), round(x + d / 2), round(y + d / 2)]])
        # wordmark type-on through a mask over the pre-rendered centred line (glyph steps)
        L = self.L['CARD-wordmark']
        w0, w1 = C['wordmark']
        if t >= w0 - 1e-6:
            steps = L.meta['steps']
            n = len(steps)
            k = min(n, int((t - w0) / ((w1 - w0) / n) + 1e-6) + 1)
            im = L.img
            if k < n:
                cut = int(round((steps[k - 1] + 2 - L.x)))
                im = im.copy()
                im[:, max(cut, 0):] = 0
            over(img, im, L.x, L.y)
            meta['ui'].append(['wordmark', alpha_bbox(im, L.x, L.y, 0.5)])
        for key, dur in (('descriptor', 6), ('price', 4), ('price_note', 4), ('cta', 4), ('url_pill', 4), ('whatsapp', 6)):
            L = self.L['CARD-' + key]
            f0 = round(C[key] * FPS)
            if f < f0:
                continue
            e = ease_out_cubic((f - f0 + 1) / dur)
            over(img, L.img, L.x, L.y + 12 * (1 - e), e)
            meta['ui'].append([key, alpha_bbox(L.img, L.x, L.y, 0.5)])
        return img
