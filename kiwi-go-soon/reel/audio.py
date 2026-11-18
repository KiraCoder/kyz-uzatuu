"""Original sound design for the Kiwi Go reel (numpy only, no samples).
Writes reel/audio.wav — 44.1 kHz, 16-bit stereo, 9.6 s, ~-14 LUFS, peak <= -1 dBFS.
All hit times match the visual beats in reel.html (120 BPM grid from t=0).
"""
import subprocess, re, wave, os
import numpy as np

SR = 44100
DUR = 9.6
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


# ---------------------------------------------------------------- arrangement
# 0.00–0.22 fall: descending whistle + air
t = tt(.24)
whistle = np.sin(osc_phase(2200 * np.exp(-t * 6) + 300)) * np.minimum(1, t / .02) * .25
add(whistle, 0.0, .5)
add(whoosh(.24, 900, 300, bw=1.4), 0.0, .35)

# 0.22 LAND: kick + boing + dust + pop (line 1), 0.32 pop (line 2)
add(kick(1.0, .6), .22, 1.0)
add(boing(), .22, .45)
add(fft_filter(rng.standard_normal(int(.25 * SR)), 200, 3000) * np.exp(-tt(.25) * 18), .22, .25)
add(pop(), .22, .45, -.2)
add(pop(), .32, .45, .2)

# 0.5–1.3: tension ticks (hats on 8ths + woodblock on beats)
for k in range(2):
    add(blip(84, d=.08), .5 + k * .5, .4, .3)        # wood-ish tick
for k in range(4):
    add(hat(.5), .5 + k * .25 + .125, .45, .4)
    add(bass(38 if k < 3 else 40, .2), .5 + k * .25, .45)  # muted D pulse, steps up into the drop
add(hat(.6), .5, .25, -.3)

# 1.30 «Это колесо!»: kick + clap + pops, then burn-out rev 1.30–1.88
add(kick(.9), 1.30, .9)
add(clap(), 1.30, .55)
add(pop(), 1.30, .45)
add(pop(1.2), 1.38, .5)
t = tt(.6)
rev_f = 55 + 210 * (t / .6) ** 1.6
ph = osc_phase(rev_f)
rev = np.zeros_like(t)
for k in range(1, 18):
    rev += np.sin(k * ph) / k * (1 if k % 2 else .6)
rev = fft_filter(rev, 40, 2500) * np.minimum(1, t / .05) * (.5 + .5 * t / .6)
add(np.tanh(2 * rev) * .9, 1.30, .35)
squeal = sweep_noise(.6, lambda x: 2400 + 1800 * x / .6, .25) * np.minimum(1, t / .1) * (.4 + .6 * t / .6)
add(squeal, 1.30, .22, -.3)
add(rumble(.6, rate=30), 1.30, .35)

# 1.85–2.10 launch whoosh (pans L→R) + whip
w = whoosh(.3, 400, 4500, bw=1.0, shape=lambda u: np.clip(u / .6, 0, 1) ** 2 * np.clip((1 - u) / .4, 0, 1))
pan = np.linspace(-.8, .8, len(w))
st = np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2)
add(st, 1.80, .7)

# 2.00–4.95 groove, 120 BPM (beat = 0.5 s)
BEAT = .5
for b in range(6):                       # 2.0, 2.5, ... 4.5
    tb = 2.0 + b * BEAT
    add(kick(.85), tb, .8)
    add(hat(.6), tb + .25, .3, .35)
    add(hat(.35), tb + .125, .15, -.25)
    add(hat(.35), tb + .375, .15, -.25)
    if b % 2 == 1:
        add(clap(), tb, .38, .1)
    if b >= 1:                           # parcel lands on the beat: cardboard 'tok'
        add(fft_filter(rng.standard_normal(int(.08 * SR)), 300, 1800) * np.exp(-tt(.08) * 60), tb, .2, -.1)
riff = [38, 38, 50, 38, 35, 35, 47, 45]  # D2 D2 D3 D2 B1 B1 B2 A2 (8ths)
for i in range(12):
    add(bass(riff[i % 8], .23), 2.0 + i * .25, .55)
add(rumble(3.0, rate=13), 2.0, .18)      # tyre on the road
# text pops: «Курьерская» «служба» «Платите» «только за» «доставку»
for tp, m in [(2.0, 81), (2.25, 86), (3.5, 81), (3.75, 83), (4.0, 86)]:
    add(blip(m), tp, .32, .2)
    add(pop(), tp, .25)
add(stab([62, 66, 69], .5), 2.0, .35)    # D major stab on the drop
add(stab([59, 62, 66], .5), 3.5, .3)     # B minor colour on text change

# 4.50–5.40 riser into the zoom: snare roll + noise sweep up + pitch rise
roll_t = 4.5
step = .125
while roll_t < 5.38:
    add(clap(.6), roll_t, .12 + .25 * (roll_t - 4.5))
    step = max(.04, step * .82)
    roll_t += step
t = tt(.9)
add(whoosh(.9, 300, 7000, bw=1.0, shape=lambda u: u ** 2.2), 4.5, .55)
add(np.sin(osc_phase(200 * 2 ** (t / .9 * 2.5))) * (t / .9) ** 2 * .3, 4.5, .45)

# 5.40 suck-in silence (tiny gap), 5.50 «Скоро» HIT, 6.00 «запуск» HIT + ding
add(kick(1.0, .7), 5.5, 1.0)
add(clap(1.2), 5.5, .55)
add(stab([62, 66, 69, 74], .8, bright=5000), 5.5, .55)
add(fft_filter(rng.standard_normal(int(1.2 * SR)), 5000, 15000) * np.exp(-tt(1.2) * 4), 5.5, .12)  # crash air
add(kick(1.0, .7), 6.0, 1.0)
add(clap(1.2), 6.0, .5)
add(stab([66, 69, 74, 78], .8, bright=6000), 6.0, .5)
add(bell(1568, 2.6), 6.0, .55, .15)        # bright ding (G6)
add(bell(2349, 1.2), 6.0, .25, -.2)        # sparkle (D7)
for b in range(2):                         # light groove under the hold
    tb = 6.5 + b * .5
    add(kick(.7), tb, .6)
    add(hat(.5), tb + .25, .3, .35)
for i in range(4):
    add(bass(riff[i], .23), 6.5 + i * .25, .45)

# 7.00 iris whoosh, 7.15–7.95 roll-in rumble, 7.92 + 8.08 bike bell
add(whoosh(.35, 500, 2500, bw=1.4), 6.95, .45)
t = tt(.8)
add(rumble(.8, rate=16) * np.clip(1 - t / .8, 0, 1) ** .5, 7.15, .4)
add(bike_bell(), 7.90, .75, .25)
add(bike_bell(), 8.06, .6, .25)

# 8.00 «Kiwi Go» slam + final chord; 8.25/8.37 tagline blips; 8.32 hop landing; 8.50 pill pop
add(kick(1.0, .7), 8.0, .95)
add(clap(), 8.0, .35)
add(pad([50, 62, 66, 69, 76], 1.6), 8.0, .6)
add(stab([62, 66, 69, 74], .9, bright=4000), 8.0, .35)
add(blip(86), 8.25, .25, -.2)
add(blip(90), 8.37, .25, .2)
add(kick(.5, .3), 8.32, .35)
add(pop(1.3), 8.5, .5)
add(blip(93, d=.3), 8.5, .3)
add(bell(3136, .9), 8.52, .12)

# ---------------------------------------------------------------- master
# gentle glue: soft saturation + fades
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
for it in range(4):
    I, pk = measure(tmp)
    gain = -14.0 - I
    print(f'pass {it}: I={I:.2f} LUFS  peak={pk:.2f} dBFS  -> gain {gain:+.2f} dB')
    if abs(gain) < .25 and pk <= -1.0:
        break
    mix = limiter(mix * 10 ** (gain / 20))
    write_wav(tmp, mix)
os.replace(tmp, out)
I, pk = measure(out)
print(f'final: I={I:.2f} LUFS  true-peak={pk:.2f} dBFS  -> {out}')
