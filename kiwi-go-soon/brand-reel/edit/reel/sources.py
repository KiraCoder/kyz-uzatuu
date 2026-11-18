"""Plate sources. Each returns float32 RGB [0,1] frames of 1080x1920 for a source time (s),
plus a 3x3 transform `xform(t)` from the source's reference coordinates into output pixels
(used to glue the S3 trail and the S6 wheels)."""
import os
import subprocess

import cv2
import numpy as np

from .common import W, H, FPS, rp, ease_out_cubic


def _cover_matrix(sw, sh, zoom=1.0, dx=0.0, dy=0.0):
    s = max(W / sw, H / sh) * zoom
    tx = (W - sw * s) / 2 + dx
    ty = (H - sh * s) / 2 + dy
    return np.array([[s, 0, tx], [0, s, ty], [0, 0, 1]], np.float64)


class Clip:
    """A real clip (gate3/*.mp4). Frames are cover-fitted to 1080x1920 (1912-px clips are scaled
    by 1920/1912 and centre-cropped). Frame-drop/hold retime: index = round(t * fps)."""
    kind = 'clip'

    def __init__(self, path, reframe, window=None):
        self.path = path
        probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries',
                                'stream=width,height,r_frame_rate', '-of', 'csv=p=0', path],
                               capture_output=True, text=True, check=True).stdout.strip().split(',')
        sw, sh = int(probe[0]), int(probe[1])
        num, den = probe[2].split('/')
        self.fps = float(num) / float(den)
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                             capture_output=True, check=True).stdout
        frames = np.frombuffer(raw, np.uint8).reshape(-1, sh, sw, 3)
        self.M = _cover_matrix(sw, sh, reframe.get('zoom', 1.0), reframe.get('dx', 0), reframe.get('dy', 0))
        self.n = len(frames)
        self.window = window or [0.0, self.n / self.fps]
        lo = max(0, int(self.window[0] * self.fps) - 2)
        hi = min(self.n, int(np.ceil(self.window[1] * self.fps)) + 2)
        self.frames = {}
        for i in range(lo, hi):
            self.frames[i] = cv2.warpAffine(frames[i], self.M[:2], (W, H), flags=cv2.INTER_CUBIC,
                                            borderMode=cv2.BORDER_REFLECT)
        self.H_track = None  # optional per-index homographies (frame0-out -> frame i-out)

    def index(self, t):
        i = int(round(t * self.fps))
        return min(max(i, min(self.frames)), max(self.frames))

    def frame(self, t):
        return self.frames[self.index(t)].astype(np.float32) / 255.0

    def native_to_out(self):
        return self.M

    def xform(self, t):
        """Clip frame-0 output coords -> frame(t) output coords (camera move)."""
        if self.H_track is None:
            return np.eye(3)
        return self.H_track.get(self.index(t), np.eye(3))

    def track_camera(self, mask_y=(0.30, 0.62), savgol=9):
        """ORB + RANSAC homography of the far ground/hills, chained to frame 0 and smoothed (07 §5.3)."""
        from scipy.signal import savgol_filter
        orb = cv2.ORB_create(3000)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        idx = sorted(self.frames)
        mask = np.zeros((H, W), np.uint8)
        mask[int(mask_y[0] * H):int(mask_y[1] * H)] = 255
        g0 = cv2.cvtColor(self.frames[idx[0]], cv2.COLOR_RGB2GRAY)
        k0, d0 = orb.detectAndCompute(g0, mask)
        Hs = []
        for i in idx:
            g = cv2.cvtColor(self.frames[i], cv2.COLOR_RGB2GRAY)
            k, d = orb.detectAndCompute(g, mask)
            Hm = None
            if d is not None and len(k) > 30:
                m = bf.match(d0, d)
                if len(m) > 30:
                    a = np.float32([k0[x.queryIdx].pt for x in m])
                    b = np.float32([k[x.trainIdx].pt for x in m])
                    Hm, inl = cv2.findHomography(a, b, cv2.RANSAC, 3.0)
                    if Hm is not None and inl.sum() < 40:
                        Hm = None
            Hs.append(Hm if Hm is not None else (Hs[-1] if Hs else np.eye(3)))
        P = np.array([h.flatten() / h[2, 2] for h in Hs])
        if len(P) >= savgol:
            P = savgol_filter(P, savgol, 2, axis=0)
        self.H_track = {i: P[j].reshape(3, 3) for j, i in enumerate(idx)}


class StillKB:
    """Placeholder: a still with a slow Ken-Burns push over a virtual clip duration."""
    kind = 'still'

    def __init__(self, image, dur, kb):
        im = cv2.cvtColor(cv2.imread(rp(image)), cv2.COLOR_BGR2RGB)
        self.sh, self.sw = im.shape[:2]
        self.dur = dur
        self.z = kb.get('zoom', [1.0, 1.05])
        self.c = kb.get('center', [[0.5, 0.5], [0.5, 0.5]])
        self.cover = max(W / self.sw, H / self.sh)
        self.pre = self.cover * max(self.z)
        self.img = cv2.resize(im, (int(round(self.sw * self.pre)), int(round(self.sh * self.pre))),
                              interpolation=cv2.INTER_AREA)

    def M(self, t):
        u = min(max(t / self.dur, 0), 1)
        z = self.z[0] + (self.z[1] - self.z[0]) * u
        cx = self.c[0][0] + (self.c[1][0] - self.c[0][0]) * u
        cy = self.c[0][1] + (self.c[1][1] - self.c[0][1]) * u
        s = self.cover * z
        hw, hh = W / 2 / s, H / 2 / s                     # keep the window inside the image
        cx = min(max(cx * self.sw, hw), self.sw - hw)
        cy = min(max(cy * self.sh, hh), self.sh - hh)
        return np.array([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s], [0, 0, 1]])

    def frame(self, t):
        M = self.M(t) @ np.diag([1 / self.pre, 1 / self.pre, 1])
        out = cv2.warpAffine(self.img, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return out.astype(np.float32) / 255.0

    def native_to_out(self):
        return self.M(0)

    def xform(self, t):
        return self.M(t) @ np.linalg.inv(self.M(0))


class Parallax25D:
    """S6 0-credit 2.5D fallback (07 §3.6): GrabCut splits gate2/S6-c.png into a truck layer and a
    background layer (truck hole inpainted). The plate is shifted up so the rear-wheel centre sits at
    ~42 % height, the blurred paving is extended below and the background on the right. A lateral
    camera move right: the truck (and the paving it stands on) moves at 1.0, the far background at
    `bg_speed`, the foreground bush at `fg_speed` (row-wise, so the contact shadow stays glued).
    Wheels are known circles, so their track is exact geometry."""
    kind = 'parallax'

    def __init__(self, p, cache_dir):
        self.p = p
        im = cv2.cvtColor(cv2.imread(rp(p['image'])), cv2.COLOR_BGR2RGB)
        sh, sw = im.shape[:2]
        s = p['scale']
        self.s = s
        # wheel centres + tyre radius measured once with HoughCircles on the still
        self.wheels_src = detect_wheels_still(im, p)
        # ---- layers in source pixels, padded right and bottom ----
        pr, pb = p['pad_right_src'], p['pad_bottom_src']
        mask = truck_mask(im, p, cache_dir)                                # float 0..1
        bg = inpaint_bg(im, mask)
        ext = np.zeros((sh + pb, sw + pr, 3), np.uint8)
        y0 = p['paving_from_src_y']
        ext[:y0, :sw] = bg[:y0]
        ext[y0:, :sw] = cv2.resize(bg[y0:], (sw, sh + pb - y0), interpolation=cv2.INTER_CUBIC)   # extend the blurred paving
        # right extension: mirror of the truck-free background layer, softened (it is out of focus anyway)
        mirror = ext[:, sw - pr:sw][:, ::-1].astype(np.float32)
        ext[:, sw:] = np.clip(cv2.GaussianBlur(mirror, (0, 0), 6), 0, 255).astype(np.uint8)
        blend = ext[:, sw - 60:sw + 60].astype(np.float32)
        soft = cv2.GaussianBlur(blend, (0, 0), 8)
        wgt = (1 - np.abs(np.linspace(-1, 1, 120)))[None, :, None]
        ext[:, sw - 60:sw + 60] = np.clip(blend * (1 - wgt) + soft * wgt, 0, 255).astype(np.uint8)
        tr = np.zeros((sh + pb, sw + pr, 4), np.uint8)
        tr[:sh, :sw, :3] = im
        tr[:sh, :sw, 3] = (mask * 255).astype(np.uint8)
        # pre-scale to output resolution
        size = (int(round((sw + pr) * s)), int(round((sh + pb) * s)))
        self.bg = cv2.resize(ext, size, interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        trs = cv2.resize(tr, size, interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        trs[..., :3] *= trs[..., 3:4]
        self.truck = trs
        self.bg_h, self.bg_w = self.bg.shape[:2]
        # row-wise speed for the background (far 0.6 -> paving 1.0 at the truck's base -> fg bush 1.3)
        rw = np.array(self.wheels_src['rear'][:2]) * s
        ry, r = rw[1], self.wheels_src['tyre_r'] * s
        ys = np.arange(self.bg_h, dtype=np.float32)
        base = ry + r
        v = np.where(ys < base - 220, p['bg_speed'],
                     np.where(ys < base, p['bg_speed'] + (1 - p['bg_speed']) * (ys - (base - 220)) / 220,
                              1.0 + (p['fg_speed'] - 1.0) * np.clip((ys - base) / (self.bg_h - base), 0, 1)))
        self.row_speed = v.astype(np.float32)

    def rear_pos(self, t):
        """Rear-wheel centre in output pixels at source time t (pan eases out and lands at t_land)."""
        p = self.p
        u = min(max(t / p['t_land'], 0.0), 1.0)
        e = (1 - p['ease_out']) * u + p['ease_out'] * ease_out_cubic(u)
        a, b = np.array(p['rear_from'], float), np.array(p['rear_to'], float)
        return a + (b - a) * e

    def offset(self, t):
        rw = np.array(self.wheels_src['rear'][:2]) * self.s
        return self.rear_pos(t) - rw          # translation of the truck layer (output px)

    def frame(self, t):
        off = self.offset(t)
        off0 = self.offset(0.0)
        travel = off[0] - off0[0]
        # background: per-row horizontal shift with parallax speed
        xs = np.arange(W, dtype=np.float32)[None, :]
        ys = np.arange(H, dtype=np.float32)[:, None] - off[1]
        rows = np.clip(ys, 0, self.bg_h - 1).astype(np.int32)
        shift = off0[0] + travel * self.row_speed[rows]
        mapx = (xs - shift).astype(np.float32)
        mapy = np.repeat(ys, W, axis=1).astype(np.float32)
        out = cv2.remap(self.bg, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        M = np.float32([[1, 0, off[0]], [0, 1, off[1]]])
        tr = cv2.warpAffine(self.truck, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        return tr[..., :3] + out * (1 - tr[..., 3:4])

    def wheels(self, t):
        off = self.offset(t)
        r = self.wheels_src['tyre_r'] * self.s
        rear = np.array(self.wheels_src['rear'][:2]) * self.s + off
        front = np.array(self.wheels_src['front'][:2]) * self.s + off
        return {'rear': (rear[0], rear[1], r), 'front': (front[0], front[1], r)}

    def export_start_frame(self, path, rear_at=(640, 800)):
        """Repositioned S6 start frame at 1520x2688 (9:16) for any future I2V retry."""
        k = 1520 / W
        off = np.array(rear_at) - np.array(self.wheels_src['rear'][:2]) * self.s
        fr = self.frame_with_offset(off)
        cv2.imwrite(path, cv2.cvtColor((cv2.resize(fr, (1520, 2688), interpolation=cv2.INTER_CUBIC) * 255).clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR))

    def frame_with_offset(self, off):
        M = np.float32([[1, 0, off[0]], [0, 1, off[1]]])
        bg = cv2.warpAffine(self.bg, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        tr = cv2.warpAffine(self.truck, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        return tr[..., :3] + bg * (1 - tr[..., 3:4])


def detect_wheels_still(im, p):
    """HoughCircles on the hub discs (crisp cream-on-ink edge) and on the tyres of the still."""
    g = cv2.medianBlur(cv2.cvtColor(im, cv2.COLOR_RGB2GRAY), 7)
    hubs = cv2.HoughCircles(g, cv2.HOUGH_GRADIENT, dp=1, minDist=300, param1=80, param2=30,
                            minRadius=p['hub_r_src'][0], maxRadius=p['hub_r_src'][1])
    tyres = cv2.HoughCircles(g, cv2.HOUGH_GRADIENT, dp=1, minDist=300, param1=80, param2=30,
                             minRadius=p['tyre_r_src'][0], maxRadius=p['tyre_r_src'][1])
    if hubs is None or len(hubs[0]) < 2:
        raise RuntimeError('S6: HoughCircles did not find both hubs; set wheels.keys manually')
    hubs = sorted(hubs[0][:2].tolist(), key=lambda c: c[0])
    front, rear = hubs[0], hubs[1]
    if p.get('rear_wheel_src'):                      # sanity: closest hub to the expected rear
        ex = np.array(p['rear_wheel_src'])
        assert np.hypot(rear[0] - ex[0], rear[1] - ex[1]) < 40, (rear, ex)
    tyre_r = float(np.median([c[2] for c in tyres[0][:2]])) if tyres is not None else rear[2] / 0.625
    # refine hub centres with an ellipse fit on the cream disc; also gives the axis ratio
    out = {'tyre_r': tyre_r}
    for name, c in (('front', front), ('rear', rear)):
        x, y, r = c
        pad = int(r * 1.3)
        roi = g[int(y) - pad:int(y) + pad, int(x) - pad:int(x) + pad]
        _, th = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        best = None
        for cn in cnts:
            if len(cn) >= 20 and cv2.pointPolygonTest(cn, (pad, pad), False) >= 0:
                best = cn
        if best is not None:
            (ex, ey), (a, b), _ = cv2.fitEllipse(best)
            out[name] = [x - pad + ex, y - pad + ey, min(a, b) / max(a, b)]
        else:
            out[name] = [x, y, 1.0]
    return out


def truck_mask(im, p, cache_dir):
    path = os.path.join(cache_dir, 'S6_truck_mask.png')
    if os.path.exists(path):
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    sh, sw = im.shape[:2]
    k = 0.5
    sm = cv2.resize(im, (int(sw * k), int(sh * k)), interpolation=cv2.INTER_AREA)
    x0, y0, x1, y1 = [int(v * k) for v in p['truck_rect_src']]
    m = np.zeros(sm.shape[:2], np.uint8)
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(cv2.cvtColor(sm, cv2.COLOR_RGB2BGR), m, (x0, y0, x1 - x0, y1 - y0), bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    fg = np.where((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # keep the largest component, fill holes, smooth edge
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
    if n > 1:
        big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        fg = np.where(lab == big, 255, 0).astype(np.uint8)
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fg = np.zeros_like(fg)
    cv2.drawContours(fg, cnts, -1, 255, -1)
    fg = cv2.resize(fg, (sw, sh), interpolation=cv2.INTER_LINEAR)
    # the wheels are exact circles: force them into the matte (GrabCut can nibble dark tyres)
    w = detect_wheels_still(im, p)
    for name in ('front', 'rear'):
        cv2.circle(fg, (int(w[name][0]), int(w[name][1])), int(w['tyre_r'] + 6), 255, -1)
    fg = cv2.GaussianBlur(fg, (0, 0), 2.0)
    cv2.imwrite(path, fg)
    return fg.astype(np.float32) / 255.0


def inpaint_bg(im, mask):
    sh, sw = im.shape[:2]
    k = 0.25
    sm = cv2.resize(im, (int(sw * k), int(sh * k)), interpolation=cv2.INTER_AREA)
    mk = cv2.resize((mask > 0.05).astype(np.uint8) * 255, (sm.shape[1], sm.shape[0]))
    mk = cv2.dilate(mk, np.ones((9, 9), np.uint8))
    fill = cv2.inpaint(sm, mk, 12, cv2.INPAINT_TELEA)
    fill = cv2.GaussianBlur(fill, (0, 0), 3)
    fill = cv2.resize(fill, (sw, sh), interpolation=cv2.INTER_CUBIC)
    m = cv2.GaussianBlur(cv2.dilate((mask > 0.05).astype(np.uint8), np.ones((25, 25), np.uint8)).astype(np.float32), (0, 0), 6)[..., None]
    return (im * (1 - m) + fill * m).astype(np.uint8)
