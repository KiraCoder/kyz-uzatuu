"""In-world composites: the S3 lime-white light trail (07 §5.3) and the S6 kiwi-wheel logos with the
light sweep (07 §5.5). Both are re-targetable from config.json."""
import os

import cv2
import numpy as np
from PIL import Image

from .common import W, H, FPS, GFX_DIR, hex_rgb, luma, premul, screen, smoothstep, ease_out_cubic


# ---------------- exact logo ----------------
class Logo:
    def __init__(self):
        self.master = premul(np.asarray(Image.open(os.path.join(GFX_DIR, 'logo_2400.png')).convert('RGBA')).astype(np.float32) / 255)
        self.exact = {s: premul(np.asarray(Image.open(os.path.join(GFX_DIR, f'logo_{s}.png')).convert('RGBA')).astype(np.float32) / 255)
                      for s in (260, 300)}

    def at(self, d):
        """Premultiplied RGBA of the unaltered SVG render at diameter d (exact render for 260/300)."""
        di = int(round(d))
        if abs(d - di) < 0.02 and di in self.exact:
            return self.exact[di]
        return cv2.resize(self.master, (max(2, di), max(2, di)), interpolation=cv2.INTER_AREA)


# ---------------- S3 light trail ----------------
def catmull(points, n=24):
    P = np.asarray(points, np.float64)
    P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out), n


class Trail:
    def __init__(self, tcfg, colors):
        self.c = tcfg
        self.dense, self.n = catmull(tcfg['path'])
        seg = np.hypot(*np.diff(self.dense, axis=0).T)
        self.arc = np.concatenate([[0], np.cumsum(seg)])
        self.core_col = hex_rgb(colors['trail_core'])
        self.lime = hex_rgb(colors['lime'])

    def head_index(self, t):
        keys = self.c['head_keys_idx']
        if t <= keys[0][0]:
            k = keys[0][1]
        elif t >= keys[-1][0]:
            k = keys[-1][1]
        else:
            for (t0, i0), (t1, i1) in zip(keys, keys[1:]):
                if t0 <= t <= t1:
                    u = (t - t0) / (t1 - t0)
                    k = i0 + (i1 - i0) * u
                    break
        return min(k * self.n, len(self.dense) - 1)

    def opacity(self, t):
        a, b = self.c['fade_out']
        return float(1 - smoothstep(a, b, t))

    def render(self, img, src, t):
        op = self.opacity(t)
        if op <= 0.001:
            return img
        M = src.xform(t) @ src.native_to_out()
        pts = np.hstack([self.dense, np.ones((len(self.dense), 1))]) @ M.T
        pts = pts[:, :2] / pts[:, 2:3]
        hi = self.head_index(t)
        h_arc = np.interp(hi, np.arange(len(self.arc)), self.arc)
        tail = self.c['tail_frac'] * self.arc[-1]
        core = np.zeros((H, W), np.uint8)
        last = int(np.floor(hi))
        P = np.round(pts * 4).astype(np.int32)           # 2-bit subpixel precision for LINE_AA
        for i in range(last):
            a = np.clip(1 - (h_arc - self.arc[i]) / tail, 0, 1) ** 1.3
            if a <= 0.01:
                continue
            cv2.line(core, tuple(P[i]), tuple(P[i + 1]), int(255 * a), self.c['core_px'], cv2.LINE_AA, shift=2)
        c = core.astype(np.float32) / 255 * op
        small = cv2.resize(c, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
        glow = cv2.resize(cv2.GaussianBlur(small, (0, 0), self.c['glow_sigma'] / 2), (W, H))
        outer = cv2.resize(cv2.GaussianBlur(small, (0, 0), self.c['outer_sigma'] / 2), (W, H))
        # scene tint: modulate 10 % by the plate's local luminance (in-world integration)
        tint = 0.9 + 0.1 * cv2.resize(cv2.GaussianBlur(cv2.resize(luma(img), (W // 8, H // 8)), (0, 0), 3), (W, H))
        glow_k = np.clip(glow * 6.0 * self.c['glow_alpha'], 0, 1)[..., None] * tint[..., None]
        outer_k = np.clip(outer * 10.0 * self.c['outer_alpha'], 0, 1)[..., None] * tint[..., None]
        out = screen(img, self.lime * outer_k * 0.6 + self.core_col * outer_k * 0.25)
        out = screen(out, self.lime * glow_k)
        out = screen(out, self.core_col * (c * tint)[..., None])
        return np.clip(out, 0, 1)


# ---------------- S6 kiwi wheels + light sweep ----------------
class Wheels:
    def __init__(self, wcfg, scfg, logo):
        self.w, self.s, self.logo = wcfg, scfg, logo

    def positions(self, src, t):
        if self.w['mode'] == 'manual' and self.w['keys']:
            k = np.array(self.w['keys'], float)
            v = [np.interp(t, k[:, 0], k[:, j]) for j in range(1, 6)]
            return {'rear': (v[0], v[1], v[2]), 'front': (v[3], v[4], v[2])}
        return src.wheels(t)

    def band_x(self, src, edit_t, sweep, seg_time):
        """Band centre x (at the wheel row): passes the front wheel at sweep.front and the rear wheel
        at sweep.rear (edit times), moving at constant speed in frame."""
        xf = self.positions(src, seg_time(sweep['front']))['front'][0]
        xr = self.positions(src, seg_time(sweep['rear']))['rear'][0]
        v = (xr - xf) / (sweep['rear'] - sweep['front'])
        return xr + v * (edit_t - sweep['rear'])

    def render(self, img, src, src_t, edit_t, sweep, seg_time, colors):
        """Returns (image, logo alpha full-frame) — alpha used to cap the R5 flash over the kiwi."""
        pos = self.positions(src, src_t)
        D = 2 * pos['rear'][2] * self.w['logo_scale']
        bw = self.s['width_factor'] * D
        xb = self.band_x(src, edit_t, sweep, seg_time)
        cyr = pos['rear'][1]
        slope = self.s['slope']
        la_full = np.zeros((H, W), np.float32)
        plate_L = luma(img)
        out = img.copy()
        for name, t_rev in (('front', sweep['front']), ('rear', sweep['rear'])):
            cx, cy, r = pos[name]
            pf = self.s['pop_frames'] / FPS
            u = (edit_t - t_rev) / pf
            sc = self.s['pop_from'] + (1 - self.s['pop_from']) * ease_out_cubic(u) if u > 0 else self.s['pop_from']
            d = D * sc
            lg = self.logo.at(d)
            n = lg.shape[0]
            x0, y0 = int(round(cx - n / 2)), int(round(cy - n / 2))
            X0, Y0, X1, Y1 = max(x0, 0), max(y0, 0), min(x0 + n, W), min(y0 + n, H)
            if X1 <= X0 or Y1 <= Y0:
                continue
            L = lg[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0].copy()
            yy, xx = np.mgrid[Y0:Y1, X0:X1].astype(np.float32)
            bx = xb + slope * (cyr - yy)
            reveal = 1 - smoothstep(bx - 0.45 * bw, bx - 0.05 * bw, xx)
            # integration: 8 % multiply from the plate's wheel luminance, sun from the right
            pl = plate_L[Y0:Y1, X0:X1]
            pl = cv2.GaussianBlur(pl, (0, 0), 9)
            shade = 1 - 0.08 * (1 - pl / max(pl.max(), 1e-3))
            shade *= 1 - 0.04 * np.clip((cx + r - xx) / (2 * r), 0, 1)
            a = L[..., 3] * reveal
            rgb = L[..., :3] * reveal[..., None] * shade[..., None]
            dst = out[Y0:Y1, X0:X1]
            dst[...] = rgb + dst * (1 - a[..., None])
            # 1 px contact shadow at the tyre's bottom
            sy = int(round(cy + d / 2))
            if 0 <= sy < H:
                xs0, xs1 = int(max(cx - 0.32 * d, 0)), int(min(cx + 0.32 * d, W))
                out[sy:sy + 1, xs0:xs1] *= (1 - 0.35 * reveal.max())
            la_full[Y0:Y1, X0:X1] = np.maximum(la_full[Y0:Y1, X0:X1], a)
        return out, la_full

    def sweep(self, img, src, edit_t, sweep, seg_time, colors, src_t):
        pos = self.positions(src, src_t)
        D = 2 * pos['rear'][2] * self.w['logo_scale']
        bw = self.s['width_factor'] * D
        xb = self.band_x(src, edit_t, sweep, seg_time)
        if xb < -1.5 * bw - 800 or xb > W + 1.5 * bw + 800:
            return img
        q = 4
        yy, xx = np.mgrid[0:H // q, 0:W // q].astype(np.float32) * q
        cyr = pos['rear'][1]
        bx = xb + self.s['slope'] * (cyr - yy)
        core = np.exp(-((xx - bx) / (bw / 4)) ** 2)
        fringe = np.exp(-((xx - (bx - 0.35 * bw)) / (0.12 * bw)) ** 2) * self.s['fringe']
        vert = np.exp(-((yy - (cyr - 160)) / 620) ** 2)
        core = cv2.resize(core * vert, (W, H))
        fringe = cv2.resize(fringe * vert, (W, H))
        L = luma(img)
        k = self.s['add'] * (0.35 + 0.65 * L)
        out = img + (hex_rgb(colors['trail_core']) * core[..., None] + hex_rgb(colors['lime']) * fringe[..., None]) * k[..., None]
        return np.clip(out, 0, 1)
