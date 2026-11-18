"""Original sound design for Kiwi Go Reel 05 «По всему Кыргызстану» (numpy only, no samples).
Writes audio.wav — 44.1 kHz, 16-bit stereo, 10.0 s, ~-14 LUFS, peak <= -1 dBFS.
All hit times match the visual beats in reel.html (0.55 s beat grid, see reel.html).
"""
import subprocess, re, wave, os
import numpy as np

SR = 44100
DUR = 10.0
TARGET_LUFS = -14.0
N = int(SR * DUR)
rng = np.random.default_rng(17)
mix = np.zeros((N, 2))
HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- helpers
def tt(d):
    return np.arange(int(SR * d)) / SR


def add(sig, start, gain=1.0, pan=0.0):
    """Mix mono (or stereo) sig at time `start` seconds. pan -1..1 (equal power)."""
    i = int(round(start * SR))
    sig = np.array(sig, dtype=float)
    tail = min(len(sig), int(.02 * SR))
    fade = np.linspace(1, 0, tail)
    if sig.ndim == 1:
        sig[-tail:] *= fade
    else:
        sig[-tail:] *= fade[:, None]
    if sig.ndim == 1:
        a = (pan + 1) * np.pi / 4
        sig = np.stack([sig * np.cos(a), sig * np.sin(a)], 1) * np.sqrt(2)
    j = min(N, i + len(sig))
    if j > i:
        mix[i:j] += sig[: j - i] * gain


def fft_filter(x, lo=0.0, hi=None, soft=0.15):
    """Static band-pass by spectral mask with smooth (log-cosine) edges."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR) + 1e-9
    m = np.ones_like(f)
    lf = np.log2(f)
    if lo > 0:
        m *= np.clip((lf - np.log2(lo)) / soft + .5, 0, 1)
    if hi:
        m *= np.clip((np.log2(hi) - lf) / soft + .5, 0, 1)
    return np.fft.irfft(X * m, n)


def sweep_noise(d, fc, bw=1.0, block=1024):
    """Noise through a time-varying band-pass. fc(t)->Hz, bw in octaves."""
    n = int(SR * d)
    x = rng.standard_normal(n + block)
    out = np.zeros(n + block)
    hop = block // 2
    win = np.hanning(block)
    f = np.fft.rfftfreq(block, 1 / SR) + 1e-9
    for s in range(0, n, hop):
        c = fc(s / SR)
        oc = np.log2(f / c)
        m = np.exp(-0.5 * (oc / (bw / 2)) ** 2)
        seg = np.fft.irfft(np.fft.rfft(x[s:s + block] * win) * m, block)
        out[s:s + block] += seg
    out = out[:n]
    return out / (np.max(np.abs(out)) + 1e-9)


def env_ad(n_or_t, a, d):
    t = n_or_t
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d)


def osc_phase(freq):
    return 2 * np.pi * np.cumsum(freq) / SR


def saw(freq_hz, t, harm=30):
    ph = 2 * np.pi * freq_hz * t
    s = np.zeros_like(t)
    for k in range(1, harm + 1):
        if freq_hz * k > 9000:
            break
        s += np.sin(k * ph) / k
    return s * 2 / np.pi


def note(n):  # MIDI -> Hz
    return 440 * 2 ** ((n - 69) / 12)


# ---------------------------------------------------------------- instruments
def kick(level=1.0, d=.45):
    t = tt(d)
    f = 48 + 140 * np.exp(-t * 28)
    body = np.sin(osc_phase(f)) * np.exp(-t * 7)
    click = fft_filter(rng.standard_normal(len(t)), 1500, 8000) * np.exp(-t * 300) * .5
    return np.tanh(1.6 * (body + click)) * level


def clap(level=1.0):
    t = tt(.35)
    nz = fft_filter(rng.standard_normal(len(t)), 900, 5000)
    nz /= np.max(np.abs(nz))
    e = np.zeros_like(t)
    for k, o in enumerate([0, .011, .022]):
        e += (t >= o) * np.exp(-np.maximum(0, t - o) * (180 if k < 2 else 22))
    return nz * e * .8 * level


def hat(level=1.0, open_=False):
    t = tt(.25 if open_ else .07)
    nz = fft_filter(rng.standard_normal(len(t)), 7000, 16000)
    nz /= np.max(np.abs(nz))
    return nz * np.exp(-t * (14 if open_ else 70)) * level


def blip(midi, level=1.0, d=.16):
    t = tt(d)
    f = note(midi)
    s = np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)
    return s * env_ad(t, .003, .05) * level


def pop(level=1.0):  # mouth-pop / bubble for text slams
    t = tt(.09)
    f = 900 * np.exp(-t * 25) + 250
    return np.sin(osc_phase(f)) * env_ad(t, .002, .025) * level


def boing(level=1.0):
    t = tt(.55)
    f = 150 + 140 * np.exp(-t * 6) + 40 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)
    s = np.sin(osc_phase(f)) + .3 * np.sin(2 * osc_phase(f))
    return s * env_ad(t, .004, .16) * level


def bass(midi, d, level=1.0):
    t = tt(d)
    f = note(midi)
    s = saw(f, t, 20)
    s = fft_filter(s, 30, 700 + 0 * f)
    s += .6 * np.sin(2 * np.pi * f * t)
    e = np.minimum(1, t / .004) * np.exp(-t * 5) * np.clip((d - t) / .02, 0, 1)
    return np.tanh(1.4 * s) * e * level


def stab(midis, d=.6, level=1.0, bright=4500):
    t = tt(d)
    s = np.zeros_like(t)
    for m in midis:
        for det in (-0.12, 0.0, 0.12):
            s += saw(note(m + det), t, 40)
    s = fft_filter(s / (3 * len(midis)), 80, bright)
    return s * env_ad(t, .005, .18) * level


def pad(midis, d, level=1.0):
    t = tt(d)
    s = np.zeros_like(t)
    for m in midis:
        for det in (-0.08, 0.08):
            s += saw(note(m + det), t, 30)
    s = fft_filter(s / (2 * len(midis)), 100, 2600)
    e = np.minimum(1, t / .03) * np.exp(-t * .9)
    return s * e * level


def bell(f0, d=1.6, level=1.0):
    t = tt(d)
    s = np.zeros_like(t)
    for r, a, dec in [(1, 1, 1.4), (2.0, .5, .9), (2.76, .35, .6), (5.4, .2, .3), (8.93, .1, .15)]:
        s += a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / dec)
    return s * np.minimum(1, t / .002) * level / 2.1


def bike_bell(level=1.0):
    """Two-strike 'дзынь-дзынь': metallic partials + fast clapper tremolo."""
    t = tt(.9)
    f0 = 2150
    s = np.zeros_like(t)
    for r, a, dec in [(1, 1, .5), (1.41, .55, .35), (2.37, .35, .22), (3.9, .2, .12)]:
        s += a * np.sin(2 * np.pi * f0 * r * t + 3 * np.sin(2 * np.pi * 6 * t) * .02)
    trem = .65 + .35 * np.sin(2 * np.pi * 24 * t)
    strike = fft_filter(rng.standard_normal(len(t)), 3000, 12000) * np.exp(-t * 400) * .4
    return (s * trem * np.exp(-t * 3.2) + strike) * np.minimum(1, t / .001) * level / 2.0


def whoosh(d, f_from, f_to, level=1.0, bw=1.2, shape=None):
    t = tt(d)
    fc = lambda x: f_from * (f_to / f_from) ** (x / d)
    nz = sweep_noise(d, fc, bw)
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 if shape is None else shape(t / d)
    return nz * e * level


def rumble(d, level=1.0, rate=11.0):
    t = tt(d)
    nz = fft_filter(rng.standard_normal(len(t)), 30, 180)
    nz /= np.max(np.abs(nz))
    am = 1 + .5 * np.sin(2 * np.pi * rate * t)
    tex = fft_filter(rng.standard_normal(len(t)), 400, 1600) * .08
    return (nz * am + tex) * level


# ---------------------------------------------------------------- arrangement
# timings mirror reel.html
PING = [3.0 + i * .55 for i in range(7)]
LIT = 6.85
BEAT = .55


def pen_scratch(d):
    """Nib on paper: band-passed noise, scribble AM following the pen speed, plus fibre grains."""
    t = tt(d)
    u = np.clip(t / d, 0, 1)
    speed = 6 * u * (1 - u)                                   # derivative of smoothstep (pen speed)
    fc = lambda x: 3200 + 1400 * np.sin(2 * np.pi * 2.3 * x) + 900 * np.sin(2 * np.pi * 7.1 * x)
    nz = sweep_noise(d, fc, 1.3)
    scrib = .55 + .45 * np.abs(np.sin(2 * np.pi * 9.5 * t + 2 * np.sin(2 * np.pi * 1.7 * t)))
    grains = np.zeros_like(t)
    idx = rng.integers(0, len(t), int(d * 260))
    grains[idx] = rng.uniform(-1, 1, len(idx))
    grains = fft_filter(grains, 1800, 9000)
    grains /= np.max(np.abs(grains)) + 1e-9
    body = fft_filter(rng.standard_normal(len(t)), 500, 1400)
    body /= np.max(np.abs(body))
    s = (nz * .8 + grains * .5 + body * .18) * scrib * (.25 + .75 * speed / 1.5)
    return s * np.minimum(1, t / .03)


def ping(midi, level=1.0):
    """Glassy ping: sine + bright partial + a short echo."""
    t = tt(1.1)
    f = note(midi)
    s = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 9)
         + .12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 14))
    s *= env_ad(t, .002, .28)
    e = np.zeros_like(s)
    k = int(.165 * SR)
    e[k:] = s[:-k] * .32
    return (s + e) * level


def swish(d=.42, level=1.0):
    return whoosh(d, 1200, 5200, bw=1.6, shape=lambda u: np.clip(u / .7, 0, 1) ** 1.5 * np.clip((1 - u) / .3, 0, 1)) * level


# 0.00 paper flick as the pen lands
add(whoosh(.2, 2500, 800, bw=1.5), 0.0, .25)
add(fft_filter(rng.standard_normal(int(.05 * SR)), 2000, 9000) * np.exp(-tt(.05) * 90), .14, .35, -.2)

# 0.15–1.85 pen-scratch while the outline draws (panned with the pen W→E)
sc = pen_scratch(1.72)
pan = np.linspace(-.5, .5, len(sc))
add(np.stack([sc * np.cos((pan + 1) * np.pi / 4), sc * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2), .15, .55)
# low "tension" bed under the drawing
t = tt(1.9)
add(np.sin(2 * np.pi * note(38) * t) * np.minimum(1, t / .6) * .5 + .25 * np.sin(2 * np.pi * note(45) * t) * np.minimum(1, t / .9), .0, .22)
for k in range(3):                                       # soft ticks on the grid
    add(blip(86, d=.06), .35 + k * .55, .18, .3)

# 1.85 outline closes: tap + kick; 2.00 hub pop; 2.30 wheel pops in
add(kick(.9, .5), 1.86, .85)
add(pop(1.2), 1.86, .4)
add(fft_filter(rng.standard_normal(int(.08 * SR)), 1500, 7000) * np.exp(-tt(.08) * 70), 1.86, .3)
add(pop(1.3), 2.0, .5, .1)
add(blip(81), 2.0, .3)
add(boing(.9), 2.3, .3, -.2)
add(pop(), 2.3, .35, -.2)

# 2.45–6.85 groove on the 0.55 s grid (≈109 BPM)
riff = [38, 38, 50, 38, 43, 43, 45, 47]                  # D2 D2 D3 D2 G2 G2 A2 B2 (8ths)
for b in range(8):                                       # 2.45, 3.00 … 6.30
    tb = 2.45 + b * BEAT
    add(kick(.85), tb, .78)
    add(hat(.6), tb + BEAT / 2, .3, .35)
    add(hat(.35), tb + BEAT / 4, .14, -.25)
    add(hat(.35), tb + 3 * BEAT / 4, .14, -.25)
    if b % 2 == 1:
        add(clap(), tb, .36, .1)
for i in range(16):
    add(bass(riff[i % 8], .26), 2.45 + i * BEAT / 2, .5)
# rolling tyre texture while the wheel travels (2.45–6.55), slight W→E pan
rl = rumble(4.1, rate=9.5)
pan = np.linspace(-.6, .6, len(rl))
add(np.stack([rl * np.cos((pan + 1) * np.pi / 4), rl * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2), 2.45, .2)
add(stab([62, 66, 69], .5), 2.45, .28)

# routes: swish while each dashed line draws; rising pings as each region lights up
PNOTES = [74, 76, 78, 81, 83, 86, 88]                    # D major pentatonic, climbing
for i, tp in enumerate(PING):
    add(swish(), tp - .42, .16, (-1) ** i * .4)
    add(ping(PNOTES[i]), tp, .42 + .03 * i, (-1) ** i * -.3)
    add(blip(PNOTES[i] - 12, d=.12), tp, .14)

# 6.30–6.85 riser
roll_t, step = 6.3, .11
while roll_t < 6.82:
    add(clap(.6), roll_t, .1 + .3 * (roll_t - 6.3))
    step = max(.035, step * .8)
    roll_t += step
add(whoosh(.55, 400, 7000, bw=1.0, shape=lambda u: u ** 2), 6.3, .5)

# 6.85 WHOLE COUNTRY LIT: big chord + bell + crash + wheel hop
add(kick(1.0, .8), LIT, 1.0)
add(clap(1.2), LIT, .45)
add(pad([50, 57, 62, 66, 69, 76], 3.1), LIT, .75)
add(stab([62, 66, 69, 74, 78], 1.0, bright=6000), LIT, .55)
add(bell(1175, 2.8), LIT, .55, .15)                      # D6
add(bell(1760, 2.0), LIT + .005, .3, -.2)                # A6
add(fft_filter(rng.standard_normal(int(1.6 * SR)), 4500, 15000) * np.exp(-tt(1.6) * 3), LIT, .16)
add(boing(.8), LIT, .25)

# 7.00 map glides up; 7.20/7.36/7.52 headline pops; 7.52 marker swipe
add(whoosh(.4, 700, 2600, bw=1.4), 6.98, .3)
for tp, m in [(7.2, 81), (7.36, 83), (7.52, 86)]:
    add(pop(), tp, .35)
    add(blip(m), tp, .25, .2)
add(whoosh(.28, 2500, 6000, bw=1.2), 7.52, .22, .3)
for b in range(3):                                        # light groove under the headline
    tb = 7.4 + b * BEAT
    add(kick(.6), tb, .5)
    add(hat(.5), tb + BEAT / 2, .25, .35)
for i in range(6):
    add(bass(riff[i], .26), 7.4 + i * BEAT / 2, .38)

# 8.42 headline out, 8.55–9.00 logo spins in & lands, 8.90 price pill, 9.20 url
add(whoosh(.5, 600, 3500, bw=1.2), 8.4, .4)
add(kick(.9, .6), 9.0, .8)
add(boing(.8), 9.0, .3)
add(pop(1.3), 8.9, .45)
add(blip(90, d=.25), 8.9, .3)
add(bell(2349, 1.0), 8.92, .14)
add(blip(93, d=.2), 9.2, .2, .2)
add(pad([50, 62, 66, 69, 74], 1.1), 9.0, .45)
add(bell(1175, 1.0), 9.05, .3)

# ---------------------------------------------------------------- master
# gentle glue: soft saturation + fades
print(f"raw mix peak {np.max(np.abs(mix)):.2f}")
mix *= 0.8 / np.max(np.abs(mix))   # v2: scale first so the soft saturation only rounds the very top, keeping transients
mix = np.tanh(mix * 1.1) / 1.1
fi, fo = int(.015 * SR), int(.35 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())


def measure(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
    pk = float(re.findall(r'Peak:\s+(-?[\d.inf]+) dBFS', r)[-1])
    return I, pk


def limiter(x, ceiling_db=-1.3, block=32, look=4, release=.06):
    c = 10 ** (ceiling_db / 20)
    nb = int(np.ceil(len(x) / block))
    pad_ = np.zeros((nb * block, 2)); pad_[:len(x)] = x
    peaks = np.abs(pad_).reshape(nb, block, 2).max(axis=(1, 2))
    need = np.minimum(1, c / np.maximum(peaks, 1e-9))
    g = need.copy()
    for k in range(1, look + 1):           # look-ahead: take the min over neighbouring blocks
        g[:-k] = np.minimum(g[:-k], need[k:]); g[k:] = np.minimum(g[k:], need[:-k])
    a = np.exp(-block / (SR * release))
    sm = np.empty_like(g); cur = 1.0
    for i, v in enumerate(g):
        cur = v if v < cur else a * cur + (1 - a) * v
        sm[i] = cur
    gs = np.interp(np.arange(nb * block), np.arange(nb) * block + block / 2, sm)
    return (pad_ * gs[:, None])[:len(x)]


tmp = os.path.join(HERE, '_tmp.wav')
out = os.path.join(HERE, 'audio.wav')
mix /= np.max(np.abs(mix))
mix *= 10 ** (-6 / 20)
write_wav(tmp, mix)
for it in range(6):
    I, pk = measure(tmp)
    gain = TARGET_LUFS - I
    print(f'pass {it}: I={I:.2f} LUFS  peak={pk:.2f} dBFS  -> gain {gain:+.2f} dB')
    if abs(gain) < .25 and pk <= -1.0:
        break
    mix = limiter(mix * 10 ** (gain / 20))
    write_wav(tmp, mix)
os.replace(tmp, out)
I, pk = measure(out)
print(f'final: I={I:.2f} LUFS  true-peak={pk:.2f} dBFS  -> {out}')
