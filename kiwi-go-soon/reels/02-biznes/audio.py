"""Original sound design for Kiwi Go Reel 02 «Продаёте в Instagram?» (numpy only, no samples).
Writes audio.wav — 44.1 kHz 16-bit stereo, 14 s, ~-14 LUFS, true peak ~-1 dBFS.
Sync points come from timing.json, written by render.js from reel.html.
Instruments/master chain adapted from ../../reel/audio.py.
"""
import subprocess, re, wave, os, json
import numpy as np

SR = 44100
DUR = 14.0
N = int(SR * DUR)
rng = np.random.default_rng(22)
mix = np.zeros((N, 2))
HERE = os.path.dirname(os.path.abspath(__file__))
TM = json.load(open(os.path.join(HERE, 'timing.json')))

# ---------------------------------------------------------------- helpers
def tt(d):
    return np.arange(int(SR * d)) / SR


def add(sig, start, gain=1.0, pan=0.0, _k=[0]):
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


# ---------------------------------------------------------------- extra instruments
def ping(midi, level=1.0):
    """Generic two-tone chat notification ping (original)."""
    t = tt(.32)
    s = np.zeros_like(t)
    for k, (m, o) in enumerate([(midi, 0), (midi + 7, .06)]):
        tk = np.maximum(0, t - o)
        f = note(m)
        s += (t >= o) * (np.sin(2 * np.pi * f * tk) + .25 * np.sin(2 * np.pi * 2 * f * tk)) * np.exp(-tk * 16)
    return s * np.minimum(1, t / .002) * level * .6


def buzz(d, level=1.0):
    """Phone vibration: 150 Hz rough tone, gated."""
    t = tt(d)
    s = np.sign(np.sin(2 * np.pi * 150 * t)) * .4 + np.sin(2 * np.pi * 150 * t)
    s = fft_filter(s, 60, 900)
    return s * np.clip(t / .01, 0, 1) * np.clip((d - t) / .02, 0, 1) * level


def coin(level=1.0):
    t = tt(.6)
    s = np.zeros_like(t)
    for f, a in [(2637, 1), (3520, .6), (5274, .3)]:
        s += a * np.sin(2 * np.pi * f * t) * np.exp(-t * 7)
    s2 = np.zeros_like(t); o = .07
    tk = np.maximum(0, t - o)
    for f, a in [(3136, 1), (4186, .5)]:
        s2 += (t >= o) * a * np.sin(2 * np.pi * f * tk) * np.exp(-tk * 6)
    return (s + s2) * level * .35


# ---------------------------------------------------------------- arrangement
spawns = TM['spawns']
# 0.00 headline slam: kick + pops
add(kick(.9, .5), .06, 1.3)
add(pop(1.2), .06, .45, -.2)
add(pop(1.2), .20, .45, .2)
# rising notification chaos: each bubble pings higher, louder, wider; buzz under it
for i, s in enumerate(spawns):
    add(ping(76 + (i % 5) * 2 + i // 3, 1.0), s, .32 + .025 * i, (-.7 if i % 2 else .7) * min(1, .2 + i * .08))
    add(buzz(.16), s, .16 + .02 * i)
    add(pop(), s, .2)
# tension drone rising 0.4 -> 1.98 (stops dead at the sweep)
t = tt(1.58)
f = 70 * 2 ** (t / 1.58 * 1.6)
dr = np.zeros_like(t); ph = osc_phase(f)
for k in range(1, 10): dr += np.sin(k * ph) / k
dr = fft_filter(dr, 40, 2200) * (t / 1.58) ** 1.6
add(np.tanh(1.5 * dr), .4, .35)
add(whoosh(1.0, 400, 5000, bw=1.0, shape=lambda u: u ** 2.5), .98, .25)
# 1.98 SWEEP: big L->R whoosh + low impact; little pops where bubbles are knocked away
w = whoosh(.75, 250, 3200, bw=1.1, shape=lambda u: np.clip(u / .25, 0, 1) * np.clip((1 - u) / .75, 0, 1) ** 1.3)
pan = np.linspace(-.9, .9, len(w))
st = np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2)
add(st, 1.94, .9)
add(kick(1.0, .8), 1.98, 1.3)
add(rumble(.6, rate=22), 1.98, .4)
for i, h in enumerate(sorted(TM['bubbleHits'] + [TM['phoneHit']] + TM['hookLineHits'])):
    if h < 90:
        add(pop(.9), h, .18, -.6 + 1.2 * min(1, (h - 1.98) / .6))
# calm: warm pad + soft bell blips on «Отдайте» «доставку» «нам»
add(pad([50, 57, 62, 66, 69], 2.0), 2.45, .5)
for tp, m in [(2.6875, 74), (2.90625, 78), (3.125, 81)]:
    add(bell(note(m), 1.0), tp, .22, 0)
    add(pop(.8), tp, .25)
add(stab([62, 66, 69], .7, bright=3000), 3.125, .22)
for k in range(3):                                   # light hats lead-in
    add(hat(.5), 3.125 + .21875 * (2 * k + 1), .18, .3)
add(rumble(.55, rate=14) * np.linspace(.3, 1, int(.55 * SR)), 3.45, .3)   # small wheel rolls in
add(whoosh(.55, 300, 6000, bw=1.0, shape=lambda u: u ** 2.2), 3.45, .4)   # riser into the drop

# 4.00–11.00 confident groove, 137.14 BPM (beat = 0.4375 s), HIT on each benefit
BEAT = 1.75 / 4
riff = [38, 38, 50, 38, 43, 43, 45, 47]                 # D2 D2 D3 D2 G2 G2 A2 B2 (8ths)
chords = [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]  # D  Bm  G  A
for b in range(16):
    tb = 4.0 + b * BEAT
    add(kick(.9), tb, .8)
    add(hat(.6), tb + BEAT / 2, .3, .35)
    add(hat(.35), tb + BEAT / 4, .12, -.25)
    add(hat(.35), tb + 3 * BEAT / 4, .12, -.25)
    if b % 2 == 1:
        add(clap(), tb, .38, .1)
for i in range(32):
    add(bass(riff[i % 8] + [0, -3, -7, -5][i // 8], .2), 4.0 + i * BEAT / 2, .55)
for i, tb in enumerate(TM['benefits']):
    add(kick(1.0, .7), tb, 1.1)
    add(clap(1.2), tb, .5)
    add(stab([m + 12 for m in chords[i]] , .7, bright=5000), tb, .45)
    add(fft_filter(rng.standard_normal(int(1.0 * SR)), 5000, 15000) * np.exp(-tt(1.0) * 5), tb, .1)  # crash air
    add(pad(chords[i], 1.75), tb, .22)
    for j in range(3):                               # text pops
        add(blip(81 + 2 * j + i), tb + .1 + j * .09, .14, (-.3, 0, .3)[j])
    if i > 0:                                        # wheel rolls to the next stop
        add(whoosh(.42, 500, 2400, bw=1.4), tb - .42, .25)
# icon accents
add(fft_filter(rng.standard_normal(int(.3 * SR)), 150, 900) * np.exp(-tt(.3) * 10), 4.22, .25)  # door opens
add(boing(.8), 5.75 + .5, .18)                       # parcel lands in hands
add(blip(93, d=.2), 5.75 + .62, .25)                 # check
add(coin(), 7.5 + .4, .5)                            # money + clock
for r in range(3):                                   # status ticks
    add(blip(88 + 2 * r, d=.12), 9.25 + .2 + r * BEAT / 2, .3, (-.3, 0, .3)[r])

# 10.55–11.0 riser, 11.0 iris whoosh, 11.5 landing bell, 11.6 brand slam
roll_t, step = 10.55, .11
while roll_t < 10.98:
    add(clap(.6), roll_t, .12 + .3 * (roll_t - 10.55)); step = max(.04, step * .8); roll_t += step
add(whoosh(.5, 600, 4000, bw=1.2), 10.95, .5)
add(kick(.6, .4), 11.5, .5)
add(bike_bell(), 11.5, .7, .25)
add(bike_bell(), 11.66, .55, .25)
add(bell(1568, 2.6), 11.5, .45, -.1)
add(kick(1.0, .8), 11.6, 1.4)
add(clap(), 11.6, .3)
add(pad([50, 62, 66, 69, 74, 78], 2.4), 11.6, .6)
add(stab([62, 66, 69, 74], 1.0, bright=4000), 11.6, .35)
add(blip(86), 11.78, .25, -.2)
add(pop(1.3), 12.0, .45)
add(blip(90, d=.3), 12.0, .28, .2)
add(bell(3136, 1.2), 12.02, .12)
for b in range(3):                                   # gentle groove tail under the hold
    tb = 12.4 + b * BEAT * 2
    add(kick(.5), tb, .4)
    add(hat(.4), tb + BEAT, .2, .3)

# ---------------------------------------------------------------- master
# no master saturation: keep transients so peaks land near -1 dBFS at -14 LUFS
fi, fo = int(.015 * SR), int(.9 * SR)
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


TARGET_LUFS = -14.0


def limiter(x, ceiling_db=-1.2, block=32, look=4, release=.06):
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
