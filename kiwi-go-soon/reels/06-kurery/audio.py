"""Original sound design for the Kiwi Go reel 06 (couriers) (numpy only, no samples).
Writes audio.wav — 44.1 kHz, 16-bit stereo, 12 s, ~-14 LUFS, peak <= -1 dBFS.
All hit times match the visual beats in reel.html (137.14 BPM grid from t=2.0).
"""
import subprocess, re, wave, os
import numpy as np

SR = 44100
DUR = 12.0
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


# ---------------------------------------------------------------- reel-06 instruments
def thud(level=1.0):
    """Rubber-stamp slam: deep body + wooden knock + paper slap."""
    t = tt(.6)
    f = 42 + 110 * np.exp(-t * 35)
    body = np.sin(osc_phase(f)) * np.exp(-t * 9)
    knock = fft_filter(rng.standard_normal(len(t)), 250, 1400) * np.exp(-t * 55) * .9
    slap = fft_filter(rng.standard_normal(len(t)), 1800, 9000) * np.exp(-t * 90) * .5
    return np.tanh(2.0 * (body + knock + slap)) * level


def formant_voice(d, f0, formants, seed_detune=0.0):
    """Synthetic vowel ('hey!'-like) — glottal saw through moving formant peaks. No recorded voice."""
    n = int(SR * d)
    t = np.arange(n) / SR
    f0t = f0(t) * (1 + seed_detune)
    ph = osc_phase(f0t)
    src = np.zeros(n)
    for k in range(1, 40):
        src += np.sin(k * ph) / k
    block, hop = 1024, 256
    out = np.zeros(n + block)
    win = np.hanning(block)
    fr = np.fft.rfftfreq(block, 1 / SR) + 1e-9
    x = np.concatenate([src, np.zeros(block)])
    for s in range(0, n, hop):
        u = s / max(1, n)
        m = np.zeros_like(fr)
        for (fa, fb, bw, g) in formants:
            fc = fa + (fb - fa) * u
            m += g * np.exp(-0.5 * ((fr - fc) / bw) ** 2)
        out[s:s + block] += np.fft.irfft(np.fft.rfft(x[s:s + block] * win) * m, block) * (hop / block * 2.6)
    out = out[:n]
    return out / (np.max(np.abs(out)) + 1e-9)


def hey(level=1.0):
    d = .32
    t = tt(d)
    voices = np.zeros(len(t))
    for i, det in enumerate([-0.03, 0.0, 0.025, 0.05]):
        v = formant_voice(d, lambda x: 230 + 170 * np.minimum(1, x / .07) - 90 * np.maximum(0, x - .12) / .2,
                          [(650, 380, 90, 1.0), (1750, 2250, 140, .7), (2600, 2900, 220, .35)], det)
        voices += np.roll(v, int(i * .006 * SR))
    breath = fft_filter(rng.standard_normal(len(t)), 1200, 6000) * np.exp(-t * 40) * .6
    e = np.minimum(1, t / .015) * np.clip((d - t) / .12, 0, 1) ** 1.3
    return (voices / 4 * e + breath) * level


def tick(level=1.0, f=2600):
    t = tt(.05)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 90) * level


def engine(d, level=1.0, f_from=70, f_to=110):
    t = tt(d)
    f = f_from + (f_to - f_from) * (t / d)
    ph = osc_phase(f)
    s = np.zeros_like(t)
    for k in range(1, 14):
        s += np.sin(k * ph) / k * (1 if k % 2 else .5)
    s = fft_filter(s, 40, 1800) * (1 + .3 * np.sin(2 * np.pi * 22 * t))
    return np.tanh(1.8 * s) * level


# ---------------------------------------------------------------- arrangement
B = 60 / 137.142857                     # 0.4375 s
T0 = 2.0
TB = [T0 + 4 * B * i for i in range(4)]  # 2.00 3.75 5.50 7.25
TEND = T0 + 16 * B                       # 9.00

# 0.00–0.30 stamp descends: short air swell, then THUD at 0.30
add(whoosh(.18, 600, 200, bw=1.2, shape=lambda u: u ** 2), .12, .35)
add(thud(1.0), .30, 1.0)
add(fft_filter(rng.standard_normal(int(.3 * SR)), 3000, 12000) * np.exp(-tt(.3) * 25), .30, .12)
# 0.56–0.70 second descend, 0.70 bigger THUD + synth "hey!" + stab
add(whoosh(.16, 700, 220, bw=1.2, shape=lambda u: u ** 2), .55, .35)
add(thud(1.15), .70, 1.0)
add(kick(1.0, .6), .70, .7)
add(hey(), .70, .55, 0)
add(stab([57, 61, 64, 69], .5, bright=5000), .70, .3)
add(fft_filter(rng.standard_normal(int(1.0 * SR)), 5000, 15000) * np.exp(-tt(1.0) * 5), .70, .12)  # crash air
# 0.95–1.50 courier zips in: engine buzz + whoosh, little horn beep at 1.5
add(engine(.6, f_from=80, f_to=140) * np.minimum(1, tt(.6) / .1) * np.clip((.6 - tt(.6)) / .2, 0, 1), .95, .25, -.4)
add(whoosh(.5, 300, 2600, bw=1.1), .95, .45)
for k, m in enumerate([76, 76]):
    add(blip(m, d=.09) + .5 * blip(m + 4, d=.09), 1.52 + k * .12, .25, .3)
# 1.55–2.0 build: 16th hats crescendo + rising tone into the drop
for k in range(8):
    tk = 1.55 + k * B / 4 * .95
    add(hat(.4 + .08 * k), tk, .18 + .03 * k, .3 if k % 2 else -.3)
t = tt(.45)
add(np.sin(osc_phase(300 * 2 ** (t / .45 * 1.5))) * (t / .45) ** 2 * .3, 1.55, .3)
add(whoosh(.3, 500, 3500, bw=1.3), 1.82, .4)    # paper iris

# 2.00–9.00 upbeat groove (A major-ish), 4 bars of 4 beats
riff = [45, 45, 57, 45, 42, 42, 54, 52]          # A1 A1 A2 A1 F#1 F#1 F#2 E2 (8ths)
chords = [[57, 61, 64], [54, 57, 61], [50, 54, 57], [52, 56, 59]]   # A  F#m  D  E
for b in range(16):
    tb = T0 + b * B
    add(kick(.9), tb, .8)
    add(hat(.6), tb + B / 2, .3, .35)
    add(hat(.35), tb + B / 4, .13, -.25)
    add(hat(.35), tb + 3 * B / 4, .13, -.25)
    if b % 2 == 1:
        add(clap(), tb, .38, .1)
    add(stab(chords[b // 4], .3, bright=3800), tb + B / 2, .14, -.2 if b % 2 else .2)   # off-beat skank
for i in range(32):
    add(bass(riff[i % 8] + [0, -3, -7, -5][i // 8], B / 2 - .02), T0 + i * B / 2, .55)
add(rumble(7.0, rate=13), T0, .1)

# benefit changes: pop + bright chord + line blips
lines = [2, 3, 2, 3]
for i, tb in enumerate(TB):
    add(pop(1.3), tb, .6)
    add(stab([c + 12 for c in chords[i]], .4, bright=6000), tb, .3)
    add(whoosh(.14, 2500, 700, bw=1.2), tb - .14, .25)     # previous card leaves
    for k in range(lines[i] + (1 if i == 2 else 0)):
        add(blip([81, 85, 88, 93][k]), tb + .1 + k * .09, .3, -.2 + .2 * k)
        add(pop(), tb + .1 + k * .09, .25)
# calendar checkmarks, phone pin arrives
for j in range(4):
    add(tick(.9, 2200 + 300 * j), TB[1] + .18 + j * B / 2, .3, .3)
add(blip(88, d=.2) + blip(93, d=.2) * .6, TB[3] + 1.0, .3, .3)

# 8.70–9.10 courier rides off: whoosh + engine rev
add(engine(.45, f_from=110, f_to=240) * np.minimum(1, tt(.45) / .05), 8.70, .25, .3)
w = whoosh(.45, 400, 4500, bw=1.0)
pan = np.linspace(-.6, .9, len(w))
add(np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2), 8.68, .55)

# 9.00 end card: lime iris + logo spin-in, bell as the logo settles
add(kick(1.0, .7), TEND, .9)
add(fft_filter(rng.standard_normal(int(1.2 * SR)), 5000, 15000) * np.exp(-tt(1.2) * 4), TEND, .14)
add(whoosh(.6, 3000, 600, bw=1.4), TEND, .3)
add(bell(1760, 2.6), TEND + .7, .5, .1)      # A6 bell
add(bell(2637, 1.4), TEND + .7, .22, -.2)    # E7 sparkle
add(pad([45, 57, 61, 64, 69], 3.0), TEND, .5)
# 9.425 / 9.64 title pops, 9.875 logo hop lands
T = TEND + 2 * B
add(pop(1.3), T - .45, .5); add(blip(81), T - .45, .25)
add(pop(1.3), T - .45 + B / 2, .5); add(blip(85), T - .45 + B / 2, .25)
# light groove under the end card
for b in range(5):
    tb = TEND + 2 * B + b * B
    add(kick(.75), tb, .55)
    add(hat(.5), tb + B / 2, .25, .35)
    if b % 2 == 1:
        add(clap(.8), tb, .25)
for i in range(10):
    add(bass(riff[i % 8], B / 2 - .02), TEND + 2 * B + i * B / 2, .4)
# 10.31 CTA line 1, 10.75 pill pop + bell, 10.95 courier parks with a bike-bell "дзынь"
add(pop(1.2), TEND + 3 * B, .45); add(blip(88), TEND + 3 * B, .25)
add(pop(1.4), TEND + 4 * B, .55); add(blip(93, d=.3), TEND + 4 * B, .3)
add(bell(3136, .9), TEND + 4 * B + .02, .15)
add(rumble(.5, rate=16) * np.clip(1 - tt(.5) / .5, 0, 1) ** .5, 10.45, .3)
add(bike_bell(), 10.95, .7, .25)
add(bike_bell(), 11.11, .55, .25)

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


TARGET_LUFS = -14.0
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
