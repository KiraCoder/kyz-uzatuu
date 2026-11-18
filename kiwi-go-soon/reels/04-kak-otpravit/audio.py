"""Original sound design for the Kiwi Go reel (numpy only, no samples).
Reel 04 «Как отправить посылку». Writes audio.wav — 44.1 kHz, 16-bit stereo, 12 s, ~-14 LUFS, peak <= -1 dBFS.
Hit times mirror the timeline constants in reel.html.
"""
import subprocess, re, wave, os
import numpy as np

SR = 44100
DUR = 12.0
N = int(SR * DUR)
rng = np.random.default_rng(404)
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
S = [1.8, 3.85, 5.9, 7.95]; END = 10.0
BEAT = (S[1] - S[0]) / 4          # 0.5125 s (~117 BPM), steps land on bar lines
TYPE0, TYPE1, NCH = 0.42, 1.12, 39


def key_tick(level=1.0, bright=1.0):
    t = tt(.035)
    nz = fft_filter(rng.standard_normal(len(t)), 1800 * bright, 9000)
    nz /= np.max(np.abs(nz)) + 1e-9
    body = np.sin(2 * np.pi * (1400 + 400 * rng.random()) * t) * .3
    return (nz + body) * np.exp(-t * 160) * level


def pluck(midi, level=1.0, d=.7):   # marimba-ish arpeggio note
    t = tt(d)
    f = note(midi)
    s = np.sin(2 * np.pi * f * t) + .45 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 18) + .2 * np.sin(2 * np.pi * 2 * f * t)
    return s * env_ad(t, .002, .22) * level


def thud(level=1.0):
    t = tt(.18)
    f = 90 + 120 * np.exp(-t * 40)
    body = np.sin(osc_phase(f)) * np.exp(-t * 22)
    card = fft_filter(rng.standard_normal(len(t)), 300, 2000) * np.exp(-t * 50) * .5
    return (body + card) * level


# --- HOOK 0–1.8: typing dots, keyboard ticks, send click, "sent" swoosh
add(pop(), .08, .45)
add(blip(88, d=.06), .10, .12, .3)
for k in range(3):
    add(blip(91 + k * 2, d=.05), .14 + k * .07, .08, .3)   # dots bouncing
add(pop(1.1), .36, .5, .1)                                 # bubble expands
dt = (TYPE1 - TYPE0) / NCH
for i in range(0, NCH, 2):
    tj = TYPE0 + i * dt + (rng.random() - .5) * .006
    add(key_tick(bright=.8 + .5 * rng.random()), tj, .55 + .25 * rng.random(), (rng.random() - .5) * .6)
add(key_tick(1.0, .6), TYPE1 + .02, .7)                    # last key
t = tt(.06)                                                # send-button click
add(np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 120), 1.18, .45, .4); add(key_tick(), 1.18, .55, .4)
add(blip(93, d=.08), 1.26, .25, .4)                         # ✓
add(blip(98, d=.1), 1.33, .25, .4)                          # ✓✓
w = whoosh(.42, 600, 5000, bw=1.0, shape=lambda u: np.clip(u / .35, 0, 1) ** 1.5 * np.clip((1 - u) / .65, 0, 1))
pan = np.linspace(.6, -.2, len(w))
add(np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2), 1.38, .75)
add(np.sin(osc_phase(500 + 1500 * (tt(.25) / .25))) * np.exp(-tt(.25) * 6) * .3, 1.40, .4)  # "fwip" up
add(thud(.9), 1.74, .6)
add(pop(), 1.74, .35)

# --- groove under the steps (1.8 – 10.0)
nb = int(round((END - S[0]) / BEAT))
for b in range(nb):
    tb = S[0] + b * BEAT
    add(kick(.7, .35), tb, .55)
    add(hat(.55), tb + BEAT / 2, .28, .35)
    add(hat(.3), tb + BEAT / 4, .12, -.25)
    add(hat(.3), tb + 3 * BEAT / 4, .12, -.25)
    if b % 2 == 1:
        add(clap(.8), tb, .28, .1)
bassline = [48, 48, 55, 48,  52, 52, 55, 52,  55, 55, 62, 55,  60, 60, 55, 60]   # C / E / G / C, one bar per step
for i in range(nb * 2):
    add(bass(bassline[(i // 2) % 16], BEAT / 2 - .02), S[0] + i * BEAT / 2, .38)

# --- step hits: pop + rising note (C5 E5 G5 C6 = happy arpeggio)
for k, m in enumerate([72, 76, 79, 84]):
    add(pop(1.2), S[k], .55, -.15)
    add(pluck(m), S[k], .55, .15)
    add(pluck(m + 12, d=.4), S[k] + .02, .14, .3)
    add(kick(.9, .4), S[k], .5)

# step 1: form fills (3 pen scribbles), button check, label flight + slap
for k, t0 in enumerate([S[0] + .3, S[0] + .5, S[0] + .7]):
    d = .17
    sc = sweep_noise(d, lambda x: 2500 + 1500 * np.sin(2 * np.pi * 18 * x), .8) * np.sin(np.pi * tt(d) / d)
    add(sc, t0, .22, -.3)
add(blip(84, d=.12), S[0] + .95, .35, -.2); add(blip(91, d=.15), S[0] + 1.02, .3, -.2)
add(whoosh(.3, 800, 3000, bw=1.2), S[0] + 1.18, .35, -.2)
add(thud(.7), S[0] + 1.48, .5); add(pop(), S[0] + 1.48, .3)

# step 2: wheel rolls in, stops; parcel hops on (boing) and lands; short roll to centre
add(rumble(.6, rate=14) * np.linspace(1, .3, int(.6 * SR)), S[1], .5)
add(whoosh(.4, 300, 1500, bw=1.4), S[1] - .05, .35, -.5)
add(kick(.6, .3), S[1] + .6, .4)
add(boing(.9), 4.7, .4)
add(thud(.8), 5.15, .55)
add(rumble(.55, rate=12) * np.sin(np.pi * tt(.55) / .55), 5.3, .3)

# step 3: rolling rumble on the road, whoosh as the hills rise
d = S[3] + .5 - S[2]
r = rumble(d, rate=13)
env = np.clip(tt(d) / .3, 0, 1) * np.clip((d - tt(d)) / .5, 0, 1)
add(r * env, S[2], .45)
add(whoosh(.45, 250, 2000, bw=1.2), S[2], .4)
for b in range(4):   # little tyre bump on each beat
    add(kick(.35, .15), S[2] + .2 + b * BEAT + BEAT, .25)

# step 4: brake, door, hop, land, check + bell chime
add(sweep_noise(.4, lambda x: 2600 - 900 * x / .4, .3) * np.sin(np.pi * tt(.4) / .4), S[3] + .05, .15, -.3)
t = tt(.2); add(np.sin(osc_phase(300 + 200 * t / .2)) * np.exp(-t * 15) * .6, 8.22, .25, .3)  # door
add(boing(.8), 8.45, .3)
add(thud(.8), 8.82, .55, .3)
add(pop(1.3), 8.85, .5, .3)
add(bell(2093, 2.2), 8.85, .6, .25)      # C7
add(bell(2637, 1.8), 8.97, .4, -.2)      # E7
add(bell(3136, 1.5), 9.09, .3, .1)       # G7
add(kick(.5, .3), 9.4, .35)              # wheel happy-hop landing

# --- end card
add(whoosh(.32, 400, 4000, bw=1.0, shape=lambda u: u ** 2), 9.70, .55)   # iris
add(rumble(.62, rate=16) * np.linspace(1, 0, int(.62 * SR)) ** .5, END, .35)
add(kick(1.0, .7), END + .55, .95)
add(clap(1.1), END + .55, .4)
add(pad([48, 60, 64, 67, 72], 1.45), END + .55, .6)
add(stab([60, 64, 67, 72], .9, bright=4500), END + .55, .35)
add(pluck(84), END + .55, .3)
add(pop(1.3), END + .78, .5)
add(blip(91, d=.25), END + .78, .3)
add(bell(4186, .9), END + .8, .1)

# ---------------------------------------------------------------- master
# gentle glue: soft saturation + fades
print(f"raw mix peak {np.max(np.abs(mix)):.2f}")
mix *= 0.8 / np.max(np.abs(mix))   # v2: scale first so the soft saturation only rounds the very top, keeping transients
mix = np.tanh(mix * 1.1) / 1.1
fi, fo = int(.015 * SR), int(.45 * SR)
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


def limiter(x, ceiling_db=-1.7, block=32, look=4, release=.06):
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
