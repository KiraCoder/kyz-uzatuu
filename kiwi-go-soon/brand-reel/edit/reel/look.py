"""R6 grade (07 §2.3) and the light/camera effects: bloom, grain, fog (R1/R7), leak (R2),
whip, haze, glow, focus pull, R5 flash."""
import math

import cv2
import numpy as np
from scipy.interpolate import CubicSpline

from .common import W, H, luma, lerp, screen, smoothstep, hex_rgb


class Look:
    def __init__(self, cfg):
        g = cfg['grade']
        self.g = g
        pts = np.array(g['curve'])
        cs = CubicSpline(pts[:, 0], pts[:, 1], bc_type='natural')
        self.lut = np.clip(cs(np.linspace(0, 1, 4096)), 0, 1).astype(np.float32)
        self.cream = hex_rgb(cfg['colors']['cream'])
        self.paper = hex_rgb(cfg['colors']['paper'])
        self.C = cfg['colors']
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot(xx - W / 2, yy - H / 2) / math.hypot(W / 2, H / 2)
        v = np.cos(np.clip(g['vignette_angle'] * r * 2.2, 0, math.pi / 2)) ** 4
        self.vig = (1 - g['vignette_mix'] + g['vignette_mix'] * v).astype(np.float32)[..., None]
        self.card_vig = (r ** 2).astype(np.float32)[..., None]
        self.ys = np.arange(H, dtype=np.float32)

    # ---------------- R6 grade ----------------
    def grade(self, img, sat, warmth, band, soft_sigma=0.0):
        g = self.g
        if soft_sigma > 0:
            img = lerp(img, cv2.GaussianBlur(img, (0, 0), soft_sigma), 0.85)
        bandmask = None
        if band:
            ramp = g['tiltshift_ramp_px']
            d = np.maximum(band[0] - self.ys, self.ys - band[1])
            m = np.clip(d / ramp, 0, 1)
            m = (m * m * (3 - 2 * m))[:, None, None]
            blur = cv2.GaussianBlur(img, (0, 0), g['tiltshift_sigma'])
            img = lerp(img, blur, m)
            bandmask = 1 - m
        idx = np.clip(img * 4095, 0, 4095).astype(np.int32)
        out = self.lut[idx]
        if warmth:
            L = luma(out)[..., None]
            out = out + warmth * np.array([1.0, 0.25, -1.0], np.float32) * (0.4 + 0.6 * L)
        L = luma(out)[..., None]
        s = sat if bandmask is None else sat * (1 + (g['tiltshift_band_sat'] - 1) * bandmask)
        out = L + (out - L) * s
        # cream highlight pass: values above ~0.8 pulled toward #F6F1E4 with soft-light at 20 %
        L = luma(out)[..., None]
        hm = smoothstep(g['cream_highlight']['threshold'] - 0.05, 1.0, L)
        c = self.cream
        sl = (1 - 2 * c) * out * out + 2 * c * out
        out = lerp(out, sl, g['cream_highlight']['amount'] * hm)
        out = out * self.vig
        return np.clip(out, 0, 1).astype(np.float32)

    # ---------------- light layers ----------------
    def bloom(self, img, strength):
        b = self.g['bloom']
        L = luma(img)[..., None]
        bright = img * np.clip((L - b['threshold']) / (1 - b['threshold']), 0, 1)
        q = cv2.resize(bright, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        q = cv2.GaussianBlur(q, (0, 0), b['sigma_full_px'] / 4)
        q = cv2.resize(q, (W, H), interpolation=cv2.INTER_LINEAR)
        return screen(img, np.clip(q * strength * 2.5, 0, 1))

    def grain(self, img, amount, seed):
        rng = np.random.default_rng(seed)
        n = rng.standard_normal((H // 2, W // 2), dtype=np.float32)
        n = cv2.resize(n, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        return np.clip(img + n * amount, 0, 1)

    def fog(self, img, k):
        return lerp(img, self.cream, k) if k > 0 else img

    def leak(self, img, p, seed=7):
        """R2: 3 Gaussian blobs on wobbly L->R paths (#FFB347, #FFD27A, cream) add-blended with
        sin(pi p); lime fringe at 25 % on the trailing blob; global lift to luma ~230 at the peak;
        one soft bokeh disc bottom-left."""
        I = math.sin(math.pi * min(max(p, 0), 1))
        if I <= 0:
            return img
        w, h = W // 4, H // 4
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        acc = np.zeros((h, w, 3), np.float32)
        cols = [hex_rgb(self.C['leak1']), hex_rgb(self.C['leak2']), self.cream]
        specs = [(0.60, 0.30, -0.9, 1.3), (0.80, 0.55, -1.1, 1.5), (1.00, 0.78, -1.4, 1.2)]
        trailing = None
        for i, (rad, yc, x0, x1) in enumerate(specs):
            cx = (x0 + (x1 - x0) * p + 0.06 * math.sin(6.1 * p + i * 1.7)) * w
            cy = (yc + 0.05 * math.sin(4.3 * p + i)) * h
            R = rad * w
            d = np.hypot(xx - cx, yy - cy)
            acc += cols[i] * np.exp(-2.0 * (d / R) ** 2)[..., None] * 0.85
            if trailing is None or cx < trailing[0]:
                trailing = (cx, cy, R, d)
        cx, cy, R, d = trailing
        ring = np.exp(-((d - 0.8 * R) / (0.12 * R)) ** 2) * (xx < cx)
        acc += hex_rgb(self.C['lime']) * (0.25 * ring)[..., None]
        bd = np.hypot(xx - 0.2 * w, yy - 0.84 * h)
        acc += self.cream * (0.5 * smoothstep(0.17 * w, 0.13 * w, bd))[..., None]
        acc = cv2.resize(cv2.GaussianBlur(acc, (0, 0), 3), (W, H), interpolation=cv2.INTER_LINEAR)
        out = img + acc * I
        m = float(luma(np.clip(out, 0, 1)).mean())
        if m < 0.9:
            s = 1 - 0.1 / (1 - m)
            out = screen(np.clip(out, 0, 1), s * I ** 2)
        return np.clip(out, 0, 1)

    def whip(self, img, blur, shift):
        if shift:
            M = np.float32([[1, 0, shift], [0, 1, 0]])
            img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        k = int(round(blur / 2))
        if k > 1:
            img = cv2.blur(cv2.blur(img, (k, 1)), (k, 1))
        return img

    def defocus(self, img, sigma):
        return cv2.GaussianBlur(img, (0, 0), sigma) if sigma > 0.3 else img

    def glow(self, img, w):
        warm = hex_rgb(self.C['glow'])
        out = self.bloom(img, 0.2 + 0.8 * w)
        return screen(out, warm * (0.85 * w))

    def wash(self, img, w, target=None):
        return lerp(img, self.cream if target is None else target, w)

    def card_bg(self):
        return lerp(self.paper, self.cream, 0.9 * self.card_vig).astype(np.float32) * np.ones((H, W, 3), np.float32)
