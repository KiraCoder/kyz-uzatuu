"""Kiwi Go brand reel «Отправлено» - original soundtrack (numpy only, no samples, no voices).

Writes, next to this file:
  music.wav  - music bed stem (post master gain, pre limiter)
  sfx.wav    - sound-effects stem (post master gain, pre limiter)
  mix.wav    - final master: 48 kHz, 24-bit stereo, exactly 20.000 s, ~-14 LUFS, true peak <= -1 dBTP

Every time below was checked against the frames of edit/out/kiwigo_reel_master_20s.mp4
(see CUES.md). 120 BPM, beat = 0.5 s, bar = 2 s, grid starts at t = 0.

Loop: the music bus is rendered on a circular 20 s buffer (tails wrap to t=0, reverb is a
circular convolution, the night drone uses only partials that are whole multiples of 1/20 Hz),
so 20.000 -> 0.000 joins without a click, and the last 0.5 s returns to the opening's
drone + clock-tick texture at the same level.
"""
import os, re, subprocess, wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_LUFS = -14.0
rng = np.random.default_rng(2026)

music = np.zeros((N, 2))
sfx = np.zeros((N, 2))
send_m = np.zeros((N, 2))   # reverb send, music
send_s = np.zeros((N, 2))   # reverb send, sfx


# ============================================================ helpers
def tt(d):
    return np.arange(int(SR * d)) / SR


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def to_stereo(sig, pan):
    """mono -> stereo, equal-power; pan scalar or per-sample array (-1 L .. +1 R)."""
    if sig.ndim == 2:
        return sig
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    return np.stack([sig * np.cos(a), sig * np.sin(a)], 1) * np.sqrt(2)


def add(buf, sig, start, gain=1.0, pan=0.0, wrap=False, send=None, send_amt=0.0, fade=0.004):
    sig = np.array(sig, dtype=float)
    nf = min(len(sig), int(fade * SR))
    if nf > 1:  # de-click tail
        f = np.linspace(1, 0, nf)
        sig[-nf:] *= f if sig.ndim == 1 else f[:, None]
    st = to_stereo(sig, pan) * gain
    i = int(round(start * SR))
    for b, amt in ((buf, 1.0), (send, send_amt)):
        if b is None or amt == 0:
            continue
        x = st * amt
        if wrap:
            idx = (i + np.arange(len(x))) % N
            np.add.at(b, idx, x) if len(x) > N else b.__setitem__(idx, b[idx] + x)
        else:
            j0, j1 = max(0, i), min(N, i + len(x))
            if j1 > j0:
                b[j0:j1] += x[j0 - i:j1 - i]


def M(sig, start, gain=1.0, pan=0.0, rev=0.25):
    add(music, sig, start, gain, pan, wrap=True, send=send_m, send_amt=rev)


def S(sig, start, gain=1.0, pan=0.0, rev=0.12):
    add(sfx, sig, start, gain, pan, wrap=False, send=send_s, send_amt=rev)


def fft_filter(x, lo=0.0, hi=None, soft=0.15):
    """Band-pass by spectral mask with soft log edges (circular over the signal length)."""
    n = len(x)
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR) + 1e-9
    m = np.ones_like(f)
    lf = np.log2(f)
    if lo > 0:
        m *= np.clip((lf - np.log2(lo)) / soft + .5, 0, 1)
    if hi:
        m *= np.clip((np.log2(hi) - lf) / soft + .5, 0, 1)
    if x.ndim == 2:
        m = m[:, None]
    return np.fft.irfft(X * m, n, axis=0)


def sweep_noise(d, fc, bw=1.0, block=1024):
    """Noise through a time-varying band-pass. fc(t)->Hz, bw in octaves. Normalised."""
    n = int(SR * d)
    x = rng.standard_normal(n + block)
    out = np.zeros(n + block)
    hop = block // 2
    win = np.hanning(block)
    f = np.fft.rfftfreq(block, 1 / SR) + 1e-9
    for s in range(0, n, hop):
        c = fc(s / SR)
        m = np.exp(-0.5 * (np.log2(f / c) / (bw / 2)) ** 2)
        out[s:s + block] += np.fft.irfft(np.fft.rfft(x[s:s + block] * win) * m, block)
    out = out[:n]
    return out / (np.max(np.abs(out)) + 1e-9)


def kf(t, pts):
    """piecewise-linear keyframes [(time, value), ...] sampled at t."""
    a = np.array(pts, dtype=float)
    return np.interp(t, a[:, 0], a[:, 1])


def phase(freq):
    return 2 * np.pi * np.cumsum(freq) / SR


def adsr(t, a, d_tau, total, rel=0.05):
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d_tau)
    return e * np.clip((total - t) / rel, 0, 1)


def saw_add(f, t, fmax=6000):
    s = np.zeros_like(t)
    k = 1
    while f * k < fmax and k < 60:
        s += np.sin(2 * np.pi * f * k * t + k * 0.7) / k
        k += 1
    return s * 2 / np.pi


# ============================================================ instruments (music)
def marimba(m, d=0.7, bright=1.0):
    t = tt(d)
    f = note(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.38)
    s += 0.22 * bright * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t / 0.07)
    if 9.2 * f < 18000:
        s += 0.06 * bright * np.sin(2 * np.pi * 9.2 * f * t) * np.exp(-t / 0.02)
    mallet = fft_filter(rng.standard_normal(len(t)), 300, 2500) * np.exp(-t / 0.004) * 0.15
    return (s + mallet) * np.minimum(1, t / 0.0015)


def pluck(m, d=0.8, tone=1.0):
    t = tt(d)
    f = note(m)
    s = np.zeros_like(t)
    for k in range(1, 14):
        if f * k > 9000:
            break
        s += np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k)) / k ** 1.4 * np.exp(-t * (2.2 + 1.6 * k / tone))
    return s * np.minimum(1, t / 0.002)


def pad(midis, d, att=0.4, rel=0.6, cutoff=1800, level=1.0):
    """warm detuned-saw pad, stereo (different detune per side)."""
    t = tt(d)
    L = np.zeros_like(t); R = np.zeros_like(t)
    for m in midis:
        f = note(m)
        L += saw_add(f * 2 ** (-6 / 1200), t, cutoff * 2) + saw_add(f * 2 ** (4 / 1200), t, cutoff * 2)
        R += saw_add(f * 2 ** (6 / 1200), t, cutoff * 2) + saw_add(f * 2 ** (-3 / 1200), t, cutoff * 2)
    st = np.stack([L, R], 1) / (2 * len(midis))
    st = fft_filter(st, 90, cutoff, soft=0.6)
    e = np.minimum(1, t / att) ** 1.5 * np.clip((d - t) / rel, 0, 1) ** 1.2
    return st * e[:, None] * level


def bass(m, d, level=1.0, rel=0.04):
    t = tt(d)
    f = note(m)
    s = np.sin(2 * np.pi * f * t) + 0.32 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    s = np.tanh(1.3 * s)
    e = np.minimum(1, t / 0.008) * (0.55 + 0.45 * np.exp(-t / 0.18)) * np.clip((d - t) / rel, 0, 1) ** 1.5
    return s * e * level


def kick(level=1.0, d=0.38):
    level *= 0.6
    t = tt(d)
    f = 50 + 95 * np.exp(-t * 32)
    body = np.sin(phase(f)) * np.exp(-t * 9)
    click = fft_filter(rng.standard_normal(len(t)), 1200, 5000) * np.exp(-t * 400) * 0.25
    return np.tanh(1.3 * (body + click)) * level


def shaker(level=1.0):
    t = tt(0.09)
    nz = fft_filter(rng.standard_normal(len(t)), 4500, 11000)
    nz /= np.max(np.abs(nz))
    return nz * np.minimum(1, t / 0.007) * np.exp(-t * 48) * level


def snap(level=1.0):
    t = tt(0.18)
    nz = fft_filter(rng.standard_normal(len(t)), 1300, 4200)
    nz /= np.max(np.abs(nz))
    e = np.exp(-t * 70) + 0.5 * (t > 0.008) * np.exp(-np.maximum(0, t - 0.008) * 35)
    return (nz * e + 0.25 * np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 90)) * level


def tom(f0, level=1.0):
    t = tt(0.35)
    f = f0 * (1 + 0.35 * np.exp(-t * 25))
    return (np.sin(phase(f)) * np.exp(-t * 9) +
            0.2 * fft_filter(rng.standard_normal(len(t)), 200, 1500) * np.exp(-t * 40)) * level


def bell(f0, d=2.0, level=1.0):
    t = tt(d)
    s = np.zeros_like(t)
    for r, a, dec in [(1, 1, 1.5), (2.0, .45, .9), (2.76, .3, .55), (5.4, .15, .28), (8.93, .07, .14)]:
        if f0 * r < 20000:
            s += a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / dec)
    return s * np.minimum(1, t / 0.0015) * level / 2.0


def soft_crash(d=1.8, level=1.0):
    t = tt(d)
    nz = fft_filter(rng.standard_normal((len(t), 2)), 3500, 13000)
    nz /= np.max(np.abs(nz))
    return nz * (np.minimum(1, t / 0.02) * np.exp(-t / 0.55))[:, None] * level


def tick(hi=True, level=1.0):
    """wooden clock tick / tock."""
    t = tt(0.06)
    f = 2350 if hi else 1720
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 160) + 0.5 * np.sin(2 * np.pi * f * 1.51 * t) * np.exp(-t * 260)
    c = fft_filter(rng.standard_normal(len(t)), 2500, 8000) * np.exp(-t * 900) * 0.6
    return (s + c) * level


def pulse(level=1.0):
    """low 'heartbeat' pulse (lub-dub)."""
    t = tt(0.4)
    def lub(tt_):
        return np.sin(2 * np.pi * 62 * tt_) * np.minimum(1, tt_ / 0.006) * np.exp(-tt_ * 16) * (tt_ >= 0)
    return (lub(t) + 0.55 * lub(t - 0.17)) * level


def boom(level=1.0):
    t = tt(1.4)
    f = 38 + 50 * np.exp(-t * 6)
    s = np.sin(phase(f)) * np.minimum(1, t / 0.004) * np.exp(-t * 3.2)
    thump = fft_filter(rng.standard_normal(len(t)), 40, 260) * np.exp(-t * 18) * 0.25
    return (s + thump) * level


# ============================================================ MUSIC
CH = {
    'Dmaj9': ([50, 57, 61, 64, 66], 38),
    'Gmaj9': ([55, 59, 62, 66, 69], 31),
    'Bm7':   ([59, 62, 66, 69], 35),
    'Asus4': ([57, 62, 64, 69], 33),
    'A':     ([57, 61, 64, 69], 33),
    'Dadd9': ([50, 57, 62, 64, 66, 69], 38),
    'A7sus': ([57, 62, 64, 67], 33),
    'Dpeak': ([50, 57, 62, 66, 69, 74, 76], 38),
    'G6':    ([55, 59, 62, 64, 66], 31),
    'Dres':  ([50, 57, 62, 64, 66], 38),
}
# (start, end, chord)
PROG = [(2.5, 4.5, 'Dmaj9'), (4.5, 6.0, 'Gmaj9'), (6.0, 7.0, 'Bm7'), (7.0, 7.5, 'Asus4'), (7.5, 8.0, 'A'),
        (8.0, 10.0, 'Dadd9'), (10.0, 11.0, 'Gmaj9'), (11.0, 12.0, 'A7sus'),
        (12.5, 13.0, 'Bm7'), (13.0, 13.5, 'Gmaj9'), (13.5, 14.0, 'A'), (14.0, 15.0, 'Dadd9'),
        (15.0, 17.0, 'Dpeak'), (17.0, 18.0, 'G6'), (18.0, 19.2, 'Dres')]


def chord_at(t):
    for a, b, c in PROG:
        if a <= t < b:
            return CH[c]
    return None


# ---- 1. night drone (periodic over 20 s -> seamless loop). Dm(add9) with a C#/D rub.
tN = np.arange(N) / SR
def per(f):  # snap a frequency to a whole multiple of 1/DUR so the partial is 20 s periodic
    return np.round(f * DUR) / DUR

drone = np.zeros((N, 2))
for m, a, sp in [(38, 0.75, 0), (45, .7, -.3), (53, .45, .4), (57, .3, -.5), (61, .12, .6), (62, .16, -.6), (64, .10, .2)]:
    for det, side in ((-0.15, -1), (0.15, 1)):
        f = per(note(m) + det)
        tone_ = np.sin(2 * np.pi * f * tN) + 0.45 * np.sin(2 * np.pi * 2 * f * tN) + 0.18 * np.sin(2 * np.pi * 3 * f * tN)
        pan_ = np.clip(sp * 0.5 + side * 0.3, -1, 1)
        drone += to_stereo(tone_ * a, pan_)
# slow breathing (periodic: 4 cycles over 20 s)
drone *= (0.85 + 0.15 * np.sin(2 * np.pi * (4 / DUR) * tN))[:, None]
air = fft_filter(rng.standard_normal((N, 2)), 250, 1600, soft=0.8)  # circular -> periodic
air /= np.max(np.abs(air))
drone = fft_filter(drone, 40, 1400, soft=0.5) / 6.0 + air * 0.035
night_env = kf(tN, [(0, 1), (1.5, 1.0), (2.35, 1.35), (2.5, 0.0), (18.2, 0.0), (19.0, 0.7), (19.6, 1.0), (20, 1)])
music += drone * night_env[:, None] * 0.55
send_m += drone * night_env[:, None] * 0.55 * 0.2

# ---- 2. clock ticks (8ths) + heartbeat pulse in the night sections
for k in range(10):            # 0.00 .. 2.25
    t0 = k * 0.25
    M(tick(k % 2 == 0, 0.20 if k % 2 == 0 else 0.13), t0, pan=0.25 if k % 2 else -0.25, rev=0.3)
for t0, g in [(19.0, .35), (19.25, .45), (19.5, .75), (19.75, .85)]:  # ticks fade back in -> loop
    M(tick(int(t0 * 4) % 2 == 0, (0.20 if int(t0 * 4) % 2 == 0 else 0.13) * g), t0, pan=0.25 if int(t0 * 4) % 2 else -0.25, rev=0.3)
for t0, g in [(0, 1), (0.5, 1), (1.0, 1), (1.5, 1.1), (2.0, 1.2)]:
    M(pulse(0.30 * g), t0, rev=0.05)
M(pulse(0.18), 19.5, rev=0.05)

# ---- 3. riser 1.5 -> 2.5 into the HIT
t = tt(1.0)
r = sweep_noise(1.0, lambda x: 350 * (7000 / 350) ** (x / 1.0), bw=1.3)
r *= (t / 1.0) ** 2.2
gl = np.sin(phase(note(62) * 2 ** (24 * (t / 1.0) ** 1.6 / 12))) * (t / 1.0) ** 2 * 0.25
M(r * 0.22 + gl * 0.12, 1.5, rev=0.4)

# ---- 4. HIT 2.5: boom + warm bloom
M(boom(0.45), 2.5, rev=0.15)
M(soft_crash(2.2, 0.10), 2.5, rev=0.5)

# ---- 5. harmony pads
for a, b, c in PROG:
    notes, _ = CH[c]
    lvl = {'Dpeak': 0.30, 'Dres': 0.22}.get(c, 0.20)
    cut = 2600 if c == 'Dpeak' else 1900
    att = 0.06 if a in (2.5, 8.0, 14.0, 15.0) else 0.25
    rel = 0.9 if c == 'Dres' else 0.25
    d = (b - a) + (0.25 if b != 12.0 else 0.02)
    M(pad(notes, d, att, rel, cut, lvl), a, rev=0.35)
# swell 6.0 -> 8.0: string-like crescendo + noise air
t = tt(2.0)
sw = pad([59, 62, 66, 69, 74], 2.0, 1.9, 0.05, 3200, 1.0)
sw *= ((t / 2.0) ** 1.6)[:, None]
M(sw * 0.20, 6.0, rev=0.5)
M(sweep_noise(2.0, lambda x: 600 * (5000 / 600) ** (x / 2.0), 1.6) * (t / 2) ** 2.5 * 0.08, 6.0, rev=0.5)
M(soft_crash(2.2, 0.12), 8.0, rev=0.5)
# 15.0 PEAK: shimmer + bell
M(soft_crash(2.6, 0.14), 15.0, rev=0.6)
for k, m in enumerate([86, 90, 93, 98, 93, 90]):
    M(bell(note(m), 1.4, 0.05), 15.0 + 0.0625 * k, pan=-0.5 + 0.2 * k, rev=0.6)
M(bell(note(74), 3.0, 0.12), 15.0, rev=0.6)

# ---- 6. bass
def bass_line():
    ev = []
    for a, b, c in PROG:
        _, root = CH[c]
        tq = a
        while tq < b - 1e-6:
            beat = round(tq * 2) % 4
            if a >= 17.0:            # calm ending: long notes
                ev.append((tq, root, b - a + (0.5 if c == 'Dres' else 0), 0.8)); break
            dur = 0.45 if beat in (0, 2) else 0.22
            ev.append((tq, root + (12 if beat == 3 and (tq * 4) % 2 == 1 else 0), dur, 1.0 if beat in (0, 2) else 0.65))
            tq += 0.5
            if beat == 1:          # pickup on the 'and' of 2
                ev.append((tq - 0.25, root + 7, 0.2, 0.5))
    return ev
for t0, m, d, v in bass_line():
    if t0 < 2.5 or 12.0 <= t0 < 12.5:
        continue
    M(bass(m, d, 0.30 * v, rel=0.9 if t0 >= 18.0 else 0.04), t0, rev=0.03)
M(bass(38, 1.2, 0.30), 2.5, rev=0.03)   # sustained root under the hit

# ---- 7. marimba / pluck arpeggios
ARP = [0, 2, 1, 3, 2, 4, 3, 1]
def arp(t_from, t_to, step, inst, lvl, octave=12, pan_w=0.35):
    k = 0
    tq = t_from
    while tq < t_to - 1e-6:
        c = chord_at(tq)
        if c is not None:
            notes = c[0]
            n = notes[ARP[k % 8] % len(notes)] + octave
            pan_ = pan_w * np.sin(k * 1.3)
            vel = 1.0 if k % 2 == 0 else 0.72
            M(inst(n) * lvl * vel, tq, pan=pan_, rev=0.3)
        k += 1
        tq += step
arp(3.0, 6.0, 0.25, marimba, 0.16)
arp(6.0, 8.0, 0.25, marimba, 0.19)
arp(8.0, 12.0, 0.25, marimba, 0.15)
arp(12.5, 13.0, 0.25, marimba, 0.14)
arp(13.0, 14.0, 0.125, marimba, 0.14)
arp(14.0, 17.0, 0.25, marimba, 0.16)
arp(17.0, 18.75, 0.5, marimba, 0.12)
arp(8.0, 12.0, 0.5, lambda n: pluck(n + 12, 0.9), 0.05, pan_w=0.6)
arp(14.0, 17.0, 0.5, lambda n: pluck(n + 12, 0.9), 0.06, pan_w=0.6)
# hit accents: chord stab of plucks
for t0, c in [(2.5, 'Dmaj9'), (8.0, 'Dadd9'), (14.0, 'Dadd9'), (15.0, 'Dpeak')]:
    for k, m in enumerate(CH[c][0]):
        M(pluck(m + 12, 1.4, 1.4) * 0.06, t0 + 0.012 * k, pan=-0.4 + 0.15 * k, rev=0.4)

# ---- 8. drums
def drums(t_from, t_to, kick_every=1.0, kick_lvl=0.5, snaps=True, shake=0.06, snap_lvl=0.10):
    tq = t_from
    while tq < t_to - 1e-6:
        if abs((tq / kick_every) - round(tq / kick_every)) < 1e-6:
            M(kick(kick_lvl), tq, rev=0.03)
        if snaps and abs(((tq - 0.5) % 1.0)) < 1e-6:
            M(snap(snap_lvl), tq, pan=0.1, rev=0.35)
        tq += 0.25
    tq = t_from
    k = 0
    while tq < t_to - 1e-6:   # shaker 16ths
        acc = [0.55, 0.3, 1.0, 0.4][k % 4]
        M(shaker(shake * acc), tq, pan=0.35, rev=0.15)
        tq += 0.125; k += 1
drums(3.0, 4.5, 1.0, 0.45, snaps=False, shake=0.05)
drums(4.5, 6.0, 1.0, 0.48, shake=0.06)
drums(6.0, 7.0, 1.0, 0.50, shake=0.065)
drums(7.0, 8.0, 0.5, 0.50, shake=0.075)
drums(8.0, 11.0, 1.0, 0.45, shake=0.055, snap_lvl=0.08)
drums(11.0, 12.0, 2.0, 0.40, snaps=False, shake=0.04)
drums(12.5, 13.5, 0.5, 0.42, snaps=False, shake=0.05)
drums(13.5, 14.0, 0.25, 0.30, snaps=False, shake=0.07)
drums(14.0, 15.0, 1.0, 0.52, shake=0.065)
drums(15.0, 17.0, 1.0, 0.50, shake=0.06)
M(kick(0.45, 0.6), 15.0, rev=0.05)
M(boom(0.35), 14.0, rev=0.1)
M(boom(0.26), 15.0, rev=0.1)
for k, f0 in enumerate([165, 147, 131, 110]):      # tom fill into the 8.0 swell-top
    M(tom(f0, 0.22), 7.5 + 0.125 * k, pan=0.3 - 0.2 * k, rev=0.3)
# re-entry: soft reverse breath into 12.5 and a riser into 14.0 / 15.0
t = tt(0.25)
M(sweep_noise(0.25, lambda x: 800 + 4000 * x / 0.25, 1.5) * (t / 0.25) ** 3 * 0.06, 12.25, rev=0.3)
t = tt(1.0)
M(sweep_noise(1.0, lambda x: 500 * (8000 / 500) ** x, 1.2) * t ** 2.5 * 0.10, 13.0, rev=0.4)
t = tt(0.5)
M(sweep_noise(0.5, lambda x: 1500 * (9000 / 1500) ** (x / 0.5), 1.2) * (t / 0.5) ** 3 * 0.08, 14.5, rev=0.4)

# ---- 9. breath 12.0 - 12.5: drop the whole music bus to nearly nothing for one beat
breath = kf(tN, [(0, 1), (11.96, 1), (12.02, 0.05), (12.44, 0.05), (12.5, 1), (20, 1)])

# ============================================================ SFX
def msg_pop(f, level=1.0):
    """chat bubble: soft bubble pop + short notification ping."""
    t = tt(0.32)
    fp = f * 0.5 * (1 + 0.8 * (1 - np.exp(-t * 90)))
    popc = np.sin(phase(fp)) * np.minimum(1, t / 0.002) * np.exp(-t * 55)
    ping = (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)) * np.minimum(1, np.maximum(0, t - 0.012) / 0.003) * np.exp(-np.maximum(0, t - 0.012) * 14)
    return (0.8 * popc + 0.45 * ping) * level


def whoosh_shape(d, f0, fpk, f1, tpk, rise=2.0, fall=1.5, bw=1.2):
    """band-noise whoosh with its loudest point at tpk (seconds from start)."""
    t = tt(d)
    fc = lambda x: (f0 * (fpk / f0) ** (x / tpk)) if x < tpk else (fpk * (f1 / fpk) ** ((x - tpk) / (d - tpk)))
    nz = sweep_noise(d, fc, bw)
    e = np.where(t < tpk, (t / tpk) ** rise, np.exp(-(t - tpk) / ((d - tpk) / 3)) ** fall)
    return nz * e


def click_hit(f_body=420, level=1.0, d=0.15):
    t = tt(d)
    c = fft_filter(rng.standard_normal(len(t)), 2000, 9000) * np.exp(-t * 1200)
    body = np.sin(2 * np.pi * f_body * t) * np.exp(-t * 45) + 0.5 * np.sin(2 * np.pi * f_body * 2.3 * t) * np.exp(-t * 80)
    return (0.7 * c + 0.6 * body) * np.minimum(1, t / 0.0008) * level


def sparkle(notes, start_gap=0.045, level=1.0, d=1.0):
    out = np.zeros(int(SR * (d + start_gap * len(notes))))
    for k, m in enumerate(notes):
        b = bell(note(m), d, 1.0)
        i = int(k * start_gap * SR)
        out[i:i + len(b)] += b * (0.85 ** k)
    return out * level


def chime(m1, m2, level=1.0):
    out = np.zeros(int(SR * 0.9))
    for k, m in enumerate((m1, m2)):
        t = tt(0.8)
        f = note(m)
        s = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)) * np.minimum(1, t / 0.002) * np.exp(-t * 5.5)
        i = int(k * 0.055 * SR)
        out[i:i + len(s)] += s * (1 if k == 0 else 0.8)
    return out * level


def felt_step(level=1.0):
    t = tt(0.16)
    thud = fft_filter(rng.standard_normal(len(t)), 90, 700) * np.minimum(1, t / 0.004) * np.exp(-t * 45)
    thud /= np.max(np.abs(thud)) + 1e-9
    body = np.sin(2 * np.pi * 130 * t) * np.minimum(1, t / 0.004) * np.exp(-t * 40) * 0.4
    scuff = fft_filter(rng.standard_normal(len(t)), 1200, 3500) * np.exp(-((t - 0.03) / 0.025) ** 2) * 0.12
    return (thud + body + scuff) * level


def creak(d=0.4, level=1.0):
    """stick-slip door creak: jittered impulse train through two resonances."""
    n = int(SR * d)
    t = np.arange(n) / SR
    rate = 28 + 30 * np.sin(np.pi * t / d) + 6 * rng.standard_normal(n).cumsum() / np.sqrt(n) * 3
    ph = np.cumsum(np.maximum(rate, 8)) / SR
    imp = np.zeros(n)
    idx = np.where(np.diff(np.floor(ph)) > 0)[0]
    imp[idx] = 1 + 0.3 * rng.standard_normal(len(idx))
    ir_t = tt(0.03)
    ir = np.sin(2 * np.pi * 820 * ir_t) * np.exp(-ir_t * 220) + 0.6 * np.sin(2 * np.pi * 1370 * ir_t) * np.exp(-ir_t * 300) + 0.3 * np.sin(2 * np.pi * 2450 * ir_t) * np.exp(-ir_t * 400)
    s = np.convolve(imp, ir)[:n]
    s *= np.sin(np.pi * t / d) ** 0.7
    return s / (np.max(np.abs(s)) + 1e-9) * level


# ---- S1: bubbles + send
S(msg_pop(1175, 0.42), 0.0, pan=-0.30)     # «где моя посылка?»  D6
S(msg_pop(1245, 0.42), 0.5, pan=-0.30)     # «уже отправили?»   Eb6 (uneasy)
S(msg_pop(1397, 0.45), 1.0, pan=-0.30)     # «??»                F6
w = whoosh_shape(0.42, 500, 3800, 2200, 0.11, rise=1.5, fall=1.2, bw=1.4)   # «Отправлено ✓» send
S(w * 0.32, 1.39, pan=np.linspace(0.0, 0.6, len(w)))
S(click_hit(900, 0.28, 0.08), 1.5, pan=0.35)
S(chime(81, 86, 0.16), 1.5, pan=0.35)      # A5 -> D6 'sent' tick
# ---- T1: light-leak whoosh, peak at the cut 2.50
w = whoosh_shape(0.8, 400, 6500, 1800, 0.30, rise=2.4, fall=1.0, bw=1.6)
S(np.stack([w, np.roll(w, 240)], 1) * 0.30, 2.2, rev=0.3)
t = tt(0.5)
S(np.sin(phase(1760 * 2 ** (np.minimum(t, .3) / .3))) * kf(t, [(0, 0), (0.28, 0.06), (0.3, 0.06), (0.5, 0)]), 2.2, rev=0.5)
# ---- S2: door creak, felt footsteps (contacts read off the frames)
S(creak(0.42, 0.085), 2.68, pan=-0.45, rev=0.25)
steps = [2.917, 3.125, 3.333, 3.583, 3.792, 4.000, 4.208, 4.375]
for k, t0 in enumerate(steps):
    S(felt_step(0.36 * (0.85 if k % 2 else 1.0)), t0, pan=0.10 + 0.6 * k / (len(steps) - 1), rev=0.15)
# ---- whip pan 4.50
w = whoosh_shape(0.46, 700, 3600, 900, 0.22, rise=2.5, fall=1.2, bw=1.1)
S(w * 0.42, 4.28, pan=np.linspace(-0.7, 0.7, len(w)), rev=0.1)
# ---- S3: truck engine + tyre roll, panned with the truck on screen
d = 3.4; t0 = 4.45; t = tt(d); T = t + t0
f0 = 41 + 3 * np.sin(2 * np.pi * 0.35 * t) + 2 * (T > 6.0) * np.minimum(1, (T - 6.0) / 0.6)
ph = phase(f0)
eng = sum(a * np.sin(k * ph + k) for k, a in [(1, 1), (2, .7), (3, .45), (4, .3), (5, .18), (6, .1), (8, .05)])
eng *= 1 + 0.25 * np.sin(ph * 2)          # firing wobble
eng = fft_filter(eng, 38, 380, soft=0.4)
roll = fft_filter(rng.standard_normal(len(t)), 140, 1100, soft=0.5) * (1 + 0.3 * np.sin(2 * np.pi * 9 * t))
truck = eng / np.max(np.abs(eng)) * 0.8 + roll / np.max(np.abs(roll)) * 0.35
lvl = 10 ** (kf(T, [(4.45, -40), (4.52, -12), (5.0, -11), (5.5, -10), (6.0, -7), (6.4, -5.5), (6.65, -4.5),
                    (6.9, -6), (7.2, -14), (7.7, -24), (7.85, -60)]) / 20)
pan_tr = kf(T, [(4.5, 0.25), (4.75, -0.05), (5.1, -0.45), (5.5, -0.45), (6.0, -0.2), (6.3, 0.0),
                (6.55, 0.35), (6.8, 0.6), (7.2, 0.75)])
S(truck * lvl * 0.60, t0, pan=pan_tr, rev=0.05)
# ---- PiP status chips (lime switches start on these frames, complete +2 frames)
for t0, (m1, m2) in zip([5.0, 6.0, 8.0, 9.0], [(78, 81), (81, 86), (83, 88), (86, 90)]):
    S(chime(m1, m2, 0.15), t0 + 0.04, pan=-0.45, rev=0.25)
# ---- cloud layer 6.4-8.75: airy whoosh, cresting as the clouds wipe (6.9) and at the haze bloom (8.5)
d = 2.45; t = tt(d); T = t + 6.35
cl = np.stack([sweep_noise(d, lambda x: 900 * (1 + 1.2 * np.sin(np.pi * x / d)), 2.2),
               sweep_noise(d, lambda x: 1000 * (1 + 1.0 * np.sin(np.pi * x / d)), 2.2)], 1)
ce = kf(T, [(6.35, 0), (6.95, 1.0), (7.4, 0.55), (7.9, 0.45), (8.3, 0.85), (8.5, 1.0), (8.7, 0.25), (8.8, 0)])
S(cl * ce[:, None] * 0.13, 6.35, rev=0.4)
# ---- S4 courtyard ambience 8.45-11.05: distant city + birds
d = 2.6; t = tt(d); T = t + 8.45
city = fft_filter(rng.standard_normal((len(t), 2)), 80, 700, soft=0.8)
city /= np.max(np.abs(city))
amb_e = kf(T, [(8.45, 0), (8.8, 1), (10.75, 1), (11.03, 0)])
S(city * amb_e[:, None] * 0.045, 8.45, rev=0.0)
def chirp(f0, d=0.08):
    t = tt(d)
    f = f0 * (1 + 0.35 * np.sin(np.pi * t / d)) + 120 * np.sin(2 * np.pi * 38 * t)
    return np.sin(phase(f)) * np.sin(np.pi * t / d) ** 2
bt = 8.75
brng = np.random.default_rng(11)
while bt < 10.8:
    f0 = brng.uniform(3000, 4600); p = brng.uniform(-0.8, 0.8); g = brng.uniform(0.025, 0.05)
    for j in range(brng.integers(2, 4)):
        S(chirp(f0 * (1 + 0.06 * j), brng.uniform(0.05, 0.09)), bt + j * 0.11, g * kf(bt, [(8.75, .6), (9.2, 1), (10.6, 1), (10.8, .5)]), pan=p, rev=0.35)
    bt += brng.uniform(0.35, 0.6)
# ---- 11.0 glow cut swell
d = 0.65; t = tt(d)
ge = np.where(t < 0.2, (t / 0.2) ** 2.5, np.exp(-(t - 0.2) / 0.12))
glow = (np.sin(2 * np.pi * note(86) * t) + 0.6 * np.sin(2 * np.pi * note(93) * t) + 0.4 * np.sin(2 * np.pi * note(81) * t)) * ge
glow += sweep_noise(d, lambda x: 2500, 1.8) * ge * 0.6
S(glow * 0.10, 10.8, rev=0.5)
# ---- 11.5 «получила, спасибо!» warm notification
S(msg_pop(587, 0.40), 11.5, pan=-0.15, rev=0.2)
S(chime(74, 78, 0.12), 11.5, pan=-0.15, rev=0.3)
# ---- S6 light sweep 13.4-14.3 (L->R), click-into-place at the front (13.69) and rear (14.00) wheels
d = 0.95; t = tt(d); T = t + 13.4
lsw = sweep_noise(d, lambda x: 4000 + 5000 * x / d, 1.0)
lsw += 0.4 * np.sin(phase(note(93) * 2 ** (12 * t / d / 12)))
lse = kf(T, [(13.4, 0), (13.62, 0.5), (13.95, 1.0), (14.05, 0.7), (14.35, 0)])
S(lsw * lse * 0.09, 13.4, pan=kf(T, [(13.6, -0.75), (14.0, 0.0), (14.35, 0.5)]), rev=0.5)
S(click_hit(380, 0.40), 13.69, pan=-0.6, rev=0.15)
S(sparkle([93, 98], 0.04, 0.06, 0.8), 13.70, pan=-0.6, rev=0.4)
S(click_hit(330, 0.55), 14.0, pan=0.0, rev=0.2)
S(sparkle([90, 93, 98, 102], 0.04, 0.09, 1.0), 14.0, pan=0.1, rev=0.5)
# ---- 15.0 flash whoosh + bell (flash ramps f357-f359, peak f360)
w = whoosh_shape(0.5, 1200, 8000, 3000, 0.25, rise=3.0, fall=1.5, bw=1.6)
S(np.stack([w, np.roll(w, 300)], 1) * 0.22, 14.75, rev=0.3)
S(bell(note(86), 2.2, 0.24), 15.0, pan=0.0, rev=0.5)    # D6 bell
S(bell(note(93), 1.6, 0.12), 15.0, pan=0.2, rev=0.5)    # A6 partner
# ---- card build
def pop_soft(f=500, level=1.0):
    t = tt(0.12)
    fp = f * (0.6 + 0.4 * (1 - np.exp(-t * 70)))
    return np.sin(phase(fp)) * np.minimum(1, t / 0.002) * np.exp(-t * 38) * level
S(pop_soft(420, 0.22), 15.06, rev=0.2)                       # logo lands
for k, t0 in enumerate([15.25, 15.333, 15.417, 15.5, 15.625, 15.708]):   # glyph type-on K-i-w-i-G-o
    S(click_hit(2600 + 150 * (k % 3), 0.09, 0.05), t0, pan=-0.25 + 0.1 * k, rev=0.1)
w = whoosh_shape(0.25, 1500, 4000, 2500, 0.12, rise=2, fall=1.2, bw=1.2)  # tagline fade-rise
S(w * 0.07, 15.80, rev=0.3)
S(click_hit(600, 0.16, 0.08), 16.0, rev=0.1)                 # price: light 'ka-ching'
S(bell(note(95), 0.9, 0.11), 16.0, pan=-0.1, rev=0.4)        # B6
S(bell(note(100), 1.0, 0.10), 16.075, pan=0.15, rev=0.4)     # E7
t = tt(0.4)
S(fft_filter(rng.standard_normal(len(t)), 7000, 15000) * np.exp(-t / 0.09) * (t > 0) * 0.03, 16.07, rev=0.3)
S(pop_soft(330, 0.32), 16.5, rev=0.2)                        # CTA + pill
S(chime(81, 85, 0.08), 16.5, pan=0.1, rev=0.3)
S(pop_soft(700, 0.16), 17.0, rev=0.2)                        # WhatsApp line
S(click_hit(2400, 0.05, 0.04), 17.0, rev=0.1)


# ============================================================ reverb (circular -> loop-safe)
def make_ir(rt=1.6, pre=0.018):
    n = int(SR * (rt + pre))
    t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-6.9 * np.maximum(0, t - pre) / rt)[:, None] * (t >= pre)[:, None]
    ir = fft_filter(ir, 200, 5500, soft=0.8)
    return ir / np.sqrt(np.sum(ir ** 2) / 2)

def circ_conv(x, ir):
    h = np.zeros((N, 2)); h[:len(ir)] = ir
    return np.fft.irfft(np.fft.rfft(x, axis=0) * np.fft.rfft(h, axis=0), N, axis=0)

ir = make_ir()
music_w = music + circ_conv(send_m, ir) * 0.30
sfx_w = sfx + circ_conv(send_s, make_ir(1.1)) * 0.25
music_w *= breath[:, None]

# ============================================================ mix bus
# duck the music a little under the SFX (envelope follower on 5 ms blocks)
blk = 240
env = np.abs(sfx_w).max(1)
nb = N // blk
pk = env[:nb * blk].reshape(nb, blk).max(1)
fol = np.zeros(nb); cur = 0.0
ra, rr = np.exp(-1 / 2), np.exp(-1 / 50)       # ~10 ms attack, ~250 ms release
for i, v in enumerate(pk):
    cur = v if v > cur else rr * cur + (1 - rr) * v
    fol[i] = cur
duck_db = -4.0 * np.clip(fol / 0.25, 0, 1)
duck = 10 ** (np.interp(np.arange(N), np.arange(nb) * blk + blk / 2, duck_db) / 20)
music_d = music_w * duck[:, None]

MUSIC_GAIN, SFX_GAIN = 0.52, 1.0
mus = music_d * MUSIC_GAIN
fx = sfx_w * SFX_GAIN


def master_eq(x):
    """circular EQ (loop-safe): HPF 32 Hz, -2 dB low-mid dip at 250 Hz (anti-mud), +1 dB air shelf."""
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-9
    g_db = -2.0 * np.exp(-0.5 * (np.log2(f / 250) / 0.7) ** 2) + 1.0 / (1 + (9000 / f) ** 2)
    hp = 1 / np.sqrt(1 + (32 / f) ** 8)
    return np.fft.irfft(X * (10 ** (g_db / 20) * hp)[:, None], len(x), axis=0)


mus = master_eq(mus)
fx = master_eq(fx)
mix = mus + fx


# ============================================================ write / measure / limit
def write_wav(path, x):
    x = np.clip(x, -1, 1 - 2 ** -23)
    q = np.round(x * 2 ** 23).astype('<i4')
    b = q.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR)
        w.writeframes(b)


def measure(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true',
                        '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
    tp = float(re.findall(r'Peak:\s+(-?[\d.inf]+) dBFS', r)[-1])
    return I, tp


def limiter(x, ceiling_db, block=48, look=6, release=0.08):
    """look-ahead block limiter; release state wraps once so the loop seam has no gain jump."""
    c = 10 ** (ceiling_db / 20)
    nb = int(np.ceil(len(x) / block))
    p = np.zeros((nb * block, 2)); p[:len(x)] = x
    peaks = np.abs(p).reshape(nb, block, 2).max(axis=(1, 2))
    need = np.minimum(1, c / np.maximum(peaks, 1e-9))
    g = need.copy()
    for k in range(1, look + 1):
        g = np.minimum(g, np.roll(need, -k)); g = np.minimum(g, np.roll(need, k))
    a = np.exp(-block / (SR * release))
    sm = np.empty_like(g); cur = 1.0
    for _ in range(2):                    # 2 passes: the second starts from the end state (circular)
        for i, v in enumerate(g):
            cur = v if v < cur else a * cur + (1 - a) * v
            sm[i] = cur
    gs = np.interp(np.arange(nb * block), np.arange(nb) * block + block / 2, sm, period=nb * block)
    return (p * gs[:, None])[:len(x)]


if __name__ == '__main__':
    print(f'raw peaks: music {np.abs(mus).max():.2f}  sfx {np.abs(fx).max():.2f}  mix {np.abs(mix).max():.2f}')
    tmp = os.path.join(HERE, '_tmp.wav')
    g_total = 0.5 / np.abs(mix).max()
    y = mix * g_total
    ceiling = -1.8
    for it in range(8):
        write_wav(tmp, y)
        I, tp = measure(tmp)
        gain = TARGET_LUFS - I
        print(f'pass {it}: I={I:.2f} LUFS  TP={tp:.2f} dBTP  -> {gain:+.2f} dB')
        if abs(gain) < 0.15 and tp <= -1.2:
            break
        if tp > -1.2 and abs(gain) < 0.15:
            ceiling -= 0.3
        g_total *= 10 ** (gain / 20)
        y = limiter(mix * g_total, ceiling)
    os.replace(tmp, os.path.join(HERE, 'mix.wav'))
    write_wav(os.path.join(HERE, 'music.wav'), mus * g_total)
    write_wav(os.path.join(HERE, 'sfx.wav'), fx * g_total)
    I, tp = measure(os.path.join(HERE, 'mix.wav'))
    print(f'final mix: I={I:.2f} LUFS  TP={tp:.2f} dBTP  master gain {20*np.log10(g_total):+.2f} dB')
