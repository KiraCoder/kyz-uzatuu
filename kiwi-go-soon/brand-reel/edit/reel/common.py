"""Shared helpers: config, paths, colours, easing, premultiplied RGBA layers."""
import json
import math
import os

import cv2
import numpy as np
from PIL import Image

EDIT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(EDIT_DIR)            # brand-reel/
BUILD = os.path.join(EDIT_DIR, 'build')
GFX_DIR = os.path.join(BUILD, 'gfx')
W, H, FPS = 1080, 1920, 24


def rp(p):
    """Resolve a config path (relative to brand-reel/)."""
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def load_config():
    with open(os.path.join(EDIT_DIR, 'config.json'), encoding='utf-8') as f:
        return json.load(f)


def hex_rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], np.float32)


class Colors:
    def __init__(self, cfg):
        for k, v in cfg['colors'].items():
            setattr(self, k, hex_rgb(v))


# ---------------- easing ----------------
def clamp01(x):
    return min(1.0, max(0.0, x))


def ease_out_cubic(t):
    t = clamp01(t)
    return 1 - (1 - t) ** 3


def ease_in_cubic(t):
    t = clamp01(t)
    return t ** 3


def ease_in_out(t):
    t = clamp01(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _back(c1):
    return lambda t: 1 + (c1 + 1) * (clamp01(t) - 1) ** 3 + c1 * (clamp01(t) - 1) ** 2


# easeOutBack tuned so a 0.85 -> 1.0 pop peaks at ~1.03 (≤ 5 % overshoot of the final size)
def _tune_back(target=0.20):
    best = None
    for c1 in np.linspace(0.1, 2.0, 400):
        f = _back(c1)
        ov = max(f(t) for t in np.linspace(0, 1, 400)) - 1
        if best is None or abs(ov - target) < abs(best[1] - target):
            best = (c1, ov)
    return _back(best[0])


ease_out_back = _tune_back(0.20)


# ---------------- layers ----------------
class Layer:
    """Premultiplied float32 RGBA element placed at (x, y) in the 1080x1920 frame.
    Keeps the 2x master so scale animations resample from the high-res render."""

    def __init__(self, name, meta, png2x):
        self.name, self.meta = name, meta
        im = Image.open(png2x).convert('RGBA')
        self.hi = premul(np.asarray(im).astype(np.float32) / 255.0)
        w, h = meta['w'], meta['h']
        lo = im.convert('RGBa').resize((w, h), Image.LANCZOS).convert('RGBA')   # 2x -> 1x Lanczos, premultiplied
        self.img = premul(np.asarray(lo).astype(np.float32) / 255.0)
        self.x, self.y, self.w, self.h = meta['x'], meta['y'], w, h

    def scaled(self, s):
        if abs(s - 1.0) < 1e-4:
            return self.img
        w = max(1, int(round(self.w * s)))
        h = max(1, int(round(self.h * s)))
        return cv2.resize(self.hi, (w, h), interpolation=cv2.INTER_AREA)


def premul(rgba):
    out = rgba.copy()
    out[..., :3] *= out[..., 3:4]
    return out


def over(dst, src, x, y, opacity=1.0):
    """Composite premultiplied src (h,w,4) over dst RGB (in place) at integer (x, y). Returns the clipped rect."""
    x, y = int(round(x)), int(round(y))
    h, w = src.shape[:2]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0 or opacity <= 0:
        return None
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] * opacity
    d = dst[y0:y1, x0:x1]
    d[...] = s[..., :3] * opacity + d * (1 - a)
    return (x0, y0, x1, y1)


def alpha_bbox(img, x, y, thr=0.5):
    """Bounding box (frame coords) of the visibly opaque part of a layer (ignores soft shadows)."""
    a = img[..., 3]
    ys, xs = np.where(a > thr)
    if len(xs) == 0:
        return None
    return [int(x + xs.min()), int(y + ys.min()), int(x + xs.max() + 1), int(y + ys.max() + 1)]


def luma(img):
    return img[..., 0] * 0.2126 + img[..., 1] * 0.7152 + img[..., 2] * 0.0722


def lerp(a, b, t):
    return a + (b - a) * t


def screen(a, b):
    return 1 - (1 - a) * (1 - b)
