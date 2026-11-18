"""Original sound design for the Kiwi Go reel (numpy only, no samples).
Reel 03 «Платите только за доставку» — 10.0 s, ~-14 LUFS, peak <= -1 dBFS.
All hit times match reel.html (03-tolko-dostavka).
"""
import subprocess, re, wave, os
import numpy as np

SR = 44100
DUR = 10.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
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


# ---------------------------------------------------------------- reel-03 instruments
def ka_ching(level=1.0):
    """Cash register: key clack + drawer thunk + bright double bell + coin shimmer."""
    out = np.zeros(int(1.4 * SR))
    clack = fft_filter(rng.standard_normal(int(.05 * SR)), 1200, 6000) * np.exp(-tt(.05) * 120)
    out[:len(clack)] += clack * .6
    th = np.sin(osc_phase(110 * np.exp(-tt(.18) * 9) + 60)) * np.exp(-tt(.18) * 22)
    i = int(.06 * SR); out[i:i + len(th)] += th * .9
    for st, f0, g in [(.09, 2637, .8), (.17, 3520, .9)]:
        b = bell(f0, 1.1)
        j = int(st * SR); out[j:j + len(b)] += b[:len(out) - j] * g
    t = tt(.5)
    sh = fft_filter(rng.standard_normal(len(t)), 6000, 14000) * np.exp(-t * 7)
    sh *= .6 + .4 * (np.sin(2 * np.pi * 38 * t) > 0)
    j = int(.17 * SR); out[j:j + len(sh)] += sh * .18
    return out * level


def question(level=1.0):
    """Two-note 'hmm?' — soft square-ish tone gliding up on the second note."""
    out = np.zeros(int(.75 * SR))
    for st, d, f_a, f_b in [(0, .22, note(67), note(67)), (.24, .45, note(67), note(76))]:
        t = tt(d)
        f = f_a + (f_b - f_a) * np.clip((t - .05) / (d - .1), 0, 1) ** 1.5
        ph = osc_phase(f + 4 * np.sin(2 * np.pi * 6 * t))
        s = np.sin(ph) + .3 * np.sin(3 * ph) + .12 * np.sin(5 * ph)
        e = np.minimum(1, t / .015) * np.clip((d - t) / .06, 0, 1)
        j = int(st * SR); out[j:j + len(t)] += s * e
    return fft_filter(out, 150, 4000) * level * .5


def scratch(d=.25, level=1.0):
    """Marker strike: scratchy band-noise with a fast fibrous AM, sweeping up."""
    t = tt(d)
    nz = sweep_noise(d, lambda x: 1800 + 2600 * x / d, 1.3)
    am = .55 + .45 * np.abs(np.sin(2 * np.pi * 55 * t + 3 * np.sin(2 * np.pi * 7 * t)))
    grit = fft_filter(rng.standard_normal(len(t)), 3000, 9000) * (rng.random(len(t)) > .93) * .8
    e = np.minimum(1, t / .015) * np.clip((d - t) / .05, 0, 1)
    return (nz * am + grit) * e * level


def splat(level=1.0):
    """Wheel squashes the text: deep kick + crunchy low noise + rubbery boing."""
    out = np.zeros(int(.8 * SR))
    k = kick(1.0, .7); out[:len(k)] += k
    t = tt(.3)
    cr = fft_filter(rng.standard_normal(len(t)), 120, 2500)
    cr = np.tanh(3 * cr / np.max(np.abs(cr))) * np.exp(-t * 14)
    out[:len(cr)] += cr * .5
    b = boing(); out[:len(b)] += b * .5
    return out * level


def fall_whistle(d, f0=2400, f1=500, level=1.0):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d)
    return np.sin(osc_phase(f)) * np.minimum(1, t / .03) * level


def crash(d=1.4, level=1.0):
    t = tt(d)
    return fft_filter(rng.standard_normal(len(t)), 4000, 15000) * np.exp(-t * 3.5) * level


# ---------------------------------------------------------------- arrangement
TARGET_LUFS = -14.0
BEAT = .5
riff = [41, 41, 53, 41, 38, 38, 50, 48]   # F2 F2 F3 F2 D2 D2 D3 C3

# 0.00–0.30 hanger drops in, 0.30 KA-CHING on the tag
add(whoosh(.3, 2500, 600, bw=1.3), 0.0, .35)
add(fall_whistle(.3, 1800, 700), 0.0, .12)
add(kick(.7, .4), .30, .7)
add(ka_ching(), .30, .8, .15)
add(pop(), .30, .3, -.2)
# light tick under the hook (wood blips on 8ths)
for k in range(4):
    add(blip(84 if k % 2 == 0 else 79, d=.07), .5 + k * .125 * 2, .25, (-1) ** k * .3)
# 0.85 / 1.00 question words pop, 1.18 pill + questioning tone
add(pop(), .85, .45, -.2); add(blip(76), .85, .2)
add(pop(), 1.00, .45, .2); add(blip(79), 1.00, .2)
add(pop(1.2), 1.18, .5); add(clap(.6), 1.18, .2)
add(question(), 1.22, .75, .1)
# 1.95–2.12 vertical swipe
add(whoosh(.25, 500, 5000, bw=1.0, shape=lambda u: np.clip(u / .7, 0, 1) ** 2 * np.clip((1 - u) / .3, 0, 1)), 1.88, .6)

# 2.0–4.0 groove (120 BPM), «%» hit at 2.10
for b in range(4):
    tb = 2.0 + b * BEAT
    add(kick(.8), tb, .7)
    add(hat(.6), tb + .25, .3, .35)
    add(hat(.35), tb + .125, .15, -.25); add(hat(.35), tb + .375, .15, -.25)
    if b % 2 == 1:
        add(clap(), tb, .35, .1)
for i in range(8):
    add(bass(riff[i % 8], .23), 2.0 + i * .25, .5)
add(clap(1.1), 2.10, .4); add(stab([65, 68, 72], .5), 2.10, .3)   # F minor: “hmm, a percentage…”
add(pop(), 2.40, .35, -.2); add(blip(77), 2.40, .2)
add(pop(), 2.60, .35, .2); add(blip(80), 2.60, .2)
# 3.05 & 3.42 marker strikes
add(scratch(.27), 3.04, .75, -.3)
add(scratch(.25), 3.41, .75, .3)
add(fft_filter(rng.standard_normal(int(.06 * SR)), 300, 2000) * np.exp(-tt(.06) * 80), 3.30, .3)
# 3.5–4.0 groove drops out; falling whistle as the wheel drops
add(kick(.6), 3.5, .5); add(hat(.5), 3.75, .3)
add(fall_whistle(.24, 2600, 600), 3.77, .35, .1)
add(whoosh(.22, 3000, 600, bw=1.2), 3.78, .35)
# 4.00 SPLAT
add(splat(), 4.0, 1.0)
add(fft_filter(rng.standard_normal(int(.4 * SR)), 200, 3000) * np.exp(-tt(.4) * 12), 4.0, .25)
# 4.30–4.78 roll off right + 4.86 suck-in riser
add(rumble(.5, rate=18), 4.28, .35)
w = whoosh(.45, 400, 3500, bw=1.0)
pan = np.linspace(0, .9, len(w))
add(np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2), 4.32, .5)
t = tt(.3)
add(sweep_noise(.3, lambda x: 800 * 2 ** (x / .3 * 3), 1.0) * (t / .3) ** 2.5, 4.70, .45)

# 5.00 «0%» PUNCH
add(kick(1.0, .8), 5.0, 1.0)
add(clap(1.3), 5.0, .6)
add(stab([65, 69, 72, 77], .9, bright=6000), 5.0, .55)
add(crash(1.6), 5.0, .2)
add(bass(29, .8, 1.0), 5.0, .7)            # sub drop
add(fall_whistle(.5, 900, 120) * np.exp(-tt(.5) * 3), 5.0, .2)
# groove 5.5–7.9 (major now: F major)
for b in range(5):
    tb = 5.5 + b * BEAT
    add(kick(.8), tb, .7)
    add(hat(.6), tb + .25, .3, .35)
    add(hat(.35), tb + .125, .15, -.25); add(hat(.35), tb + .375, .15, -.25)
    if b % 2 == 0:
        add(clap(), tb, .35, .1)
for i in range(10):
    add(bass([41, 41, 53, 41, 46, 46, 58, 48][i % 8], .23), 5.5 + i * .25, .5)
add(pop(), 5.5, .4); add(blip(81), 5.5, .25)
# 6.30 words out, 6.5 / 6.75 words in, 7.0 pill hit
add(whoosh(.2, 1200, 4000, bw=1.2), 6.25, .3)
add(pop(), 6.5, .4, -.2); add(blip(81), 6.5, .3)
add(pop(), 6.75, .4, .2); add(blip(84), 6.75, .3)
add(kick(.9), 7.0, .5); add(clap(1.2), 7.0, .5)
add(stab([65, 69, 72, 77], .7, bright=5000), 7.0, .45)
add(blip(89, d=.25), 7.0, .3)
# 7.5–7.9 riser into the end card
add(whoosh(.45, 500, 6000, bw=1.0, shape=lambda u: u ** 2), 7.45, .4)

# 7.90 iris whoosh, 7.98–8.5 roll-in, 8.50 wheel stops: BELL
add(whoosh(.3, 600, 2500, bw=1.4), 7.88, .4)
t = tt(.55)
add(rumble(.55, rate=16) * np.clip(1 - t / .55, 0, 1) ** .5, 7.98, .4)
add(kick(1.0, .7), 8.5, .9)
add(bike_bell(), 8.48, .8, .2)
add(bell(1397, 2.2), 8.5, .5, -.1)          # F6 ding
add(pad([41, 53, 57, 60, 65], 1.5), 8.5, .55)
add(stab([65, 69, 72, 77], .9, bright=4500), 8.55, .35)
add(pop(1.3), 8.55, .45)
add(blip(89), 8.85, .25, -.2)
add(bell(2794, .9), 8.86, .15, .2)
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
