"""Original sound design for Kiwi Go Reel 01 «Мы запустились!» (numpy only, no samples).
Writes audio.wav: 44.1 kHz, 16-bit stereo, 12.0 s, about -14 LUFS, true peak about -1 dBFS.
Hit times match the visual beats in reel.html (120 BPM grid, beats on whole/half seconds).
"""
import subprocess, re, wave, os
import numpy as np

SR = 44100
DUR = 12.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
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


# ---------------------------------------------------------------- extra instruments
def paper_tear(d=.42, level=1.0):
    """Ripping paper: dense random crackle grains through a bright band + a lower rip body."""
    n = int(SR * d)
    t = tt(d)
    env = np.zeros(n)
    k = 0.0
    while k < d:
        i = int(k * SR)
        g = np.exp(-np.arange(n - i) / SR * rng.uniform(250, 700)) * rng.uniform(.3, 1.0)
        env[i:] += g
        k += rng.exponential(.004 + .02 * (k / d) ** 2)
    env = np.minimum(env, 1.6) * (np.minimum(1, t / .01)) * np.exp(-t * 3)
    hi = fft_filter(rng.standard_normal(n), 1500, 9000)
    hi /= np.max(np.abs(hi))
    body = sweep_noise(d, lambda x: 1400 * (1 - .6 * x / d) + 300, 1.3)
    return (hi * env * .8 + body * env * .5) * level


def crash(d=2.2, level=1.0):
    t = tt(d)
    nz = fft_filter(rng.standard_normal(len(t)), 3500, 16000)
    nz /= np.max(np.abs(nz))
    met = np.zeros_like(t)
    for f in [3120, 4470, 5310, 6890, 8030, 9650]:
        met += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * rng.uniform(.3, 1)
    met = met / 6 * np.exp(-t * 3.5)
    e = np.minimum(1, t / .002) * (np.exp(-t * 2.2) * .8 + np.exp(-t * 25) * .6)
    return (nz * e + met * .35) * level


def stamp_thud(level=1.0):
    t = tt(.9)
    f = 42 + 110 * np.exp(-t * 22)
    sub = np.sin(osc_phase(f)) * np.exp(-t * 5.5)
    knock = np.sin(osc_phase(170 + 60 * np.exp(-t * 40))) * np.exp(-t * 28) * .6
    body = fft_filter(rng.standard_normal(len(t)), 60, 700)
    body = body / np.max(np.abs(body)) * np.exp(-t * 20) * .7
    slap = fft_filter(rng.standard_normal(len(t)), 900, 4000)
    slap = slap / np.max(np.abs(slap)) * np.exp(-t * 90) * .55
    room = fft_filter(rng.standard_normal(len(t)), 200, 2500)
    room = room / np.max(np.abs(room)) * np.exp(-t * 7) * .08
    return np.tanh(1.8 * (sub + knock + body + slap + room)) * level


def popper(level=1.0):
    """Party-popper: sharp pop + crinkly paper confetti tail."""
    t = tt(.6)
    pop_ = fft_filter(rng.standard_normal(len(t)), 600, 6000) * np.exp(-t * 120)
    pop_ /= np.max(np.abs(pop_))
    crin = fft_filter(rng.standard_normal(len(t)), 4000, 14000)
    crin /= np.max(np.abs(crin))
    am = (rng.random(len(t)) < .02).astype(float)
    am = np.convolve(am, np.exp(-np.arange(200) / 30), 'same')
    return (pop_ + crin * np.minimum(am, 1) * np.exp(-t * 4) * .45) * level


def snare(level=1.0):
    t = tt(.2)
    nz = fft_filter(rng.standard_normal(len(t)), 1200, 9000)
    nz /= np.max(np.abs(nz))
    tone = np.sin(osc_phase(190 + 60 * np.exp(-t * 50))) * np.exp(-t * 30)
    return (nz * np.exp(-t * 28) + tone * .5) * level


def stereo_whoosh(d, f0, f1, level, l2r=True):
    w = whoosh(d, f0, f1, bw=1.0)
    pan = np.linspace(-.8, .8, len(w)) * (1 if l2r else -1)
    return np.stack([w * np.cos((pan + 1) * np.pi / 4), w * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2) * level


# ---------------------------------------------------------------- arrangement
# 0.00–0.70 BUILD-UP under the sign: noise riser, rising saw, accelerating snare roll, creaking rumble
add(kick(.8, .4), 0.0, .6)
t = tt(.72)
add(whoosh(.72, 250, 7000, bw=1.1, shape=lambda u: .15 + .85 * u ** 2), 0.0, .55)
fr = 110 * 2 ** (2.2 * (t / .72) ** 1.4)
riser = np.zeros_like(t)
ph = osc_phase(fr)
for k in range(1, 10):
    riser += np.sin(k * ph) / k
add(np.tanh(1.5 * riser) * (.2 + .8 * (t / .72) ** 2) * .35, 0.0, .55)
add(rumble(.72, rate=9) * (t / .72) ** 1.5, 0.0, .5)
rt, step = .12, .12
while rt < .69:
    add(snare(.5 + .5 * rt / .7), rt, .2 + .35 * rt / .7, .15 * np.sin(rt * 40))
    step = max(.03, step * .8)
    rt += step

# 0.70 BURST: heavy kick, paper tear/crash, sparkle
add(kick(1.0, .7), .70, 1.0)
add(crash(2.2), .70, .5, .2)
add(paper_tear(.45), .70, .8, -.25)
add(paper_tear(.35), .73, .55, .35)
add(fft_filter(rng.standard_normal(int(.3 * SR)), 80, 600) * np.exp(-tt(.3) * 12), .70, .5)  # boom air
add(stab([62, 66, 69, 74], .7, bright=5000), .70, .45)
for i, m in enumerate([86, 90, 93]):
    add(blip(m, d=.12), .74 + i * .045, .2, (-.4, 0, .4)[i])

# 0.86–1.00 stamp falls (descending whoosh), 1.00 STAMP THUD
add(whoosh(.16, 3000, 400, bw=1.2, shape=lambda u: u ** 1.5), .85, .45)
add(stamp_thud(), 1.00, 1.15)
add(kick(.9, .5), 1.00, .5)

# 1.45–1.75 push transition whoosh, groove pickup
add(stereo_whoosh(.32, 500, 4000, 1.0), 1.44, .55)
for k in range(4):
    add(hat(.4), 1.5 + k * .125, .2, .3)
add(bass(45, .2), 1.75, .4)

# 2.00–4.50 rolling groove, 120 BPM
BEAT = .5
riff = [38, 38, 50, 38, 43, 43, 45, 47]  # D2 D2 D3 D2 G2 G2 A2 B2 (8ths)
for b in range(6):                       # 2.0 … 4.5
    tb = 2.0 + b * BEAT
    add(kick(.85), tb, .85)
    add(hat(.6), tb + .25, .3, .35)
    add(hat(.35), tb + .125, .15, -.25)
    add(hat(.35), tb + .375, .15, -.25)
    if b % 2 == 1:
        add(clap(), tb, .4, .1)
    add(fft_filter(rng.standard_normal(int(.08 * SR)), 300, 1800) * np.exp(-tt(.08) * 60), tb, .22, -.15)  # parcel 'tok'
for i in range(10):
    add(bass(riff[i % 8], .23), 2.0 + i * .25, .55)
add(rumble(2.6, rate=13), 2.0, .2)      # tyre on the road
add(stab([62, 66, 69], .5), 2.0, .4)    # «Kiwi Go»
add(popper(), 2.0, .55, -.5)            # confetti cannons
add(popper(), 2.02, .55, .5)
add(pop(1.2), 2.0, .4)
add(blip(86), 2.25, .3, .2); add(pop(), 2.25, .35)      # «запустился!»
add(boing(), 2.5, .35, .4)              # parcel beside the wheel lands
add(blip(93, d=.1), 3.0, .25, -.2); add(boing(1.1), 3.0, .25, -.2)  # small parcel stacks
add(stab([59, 62, 66], .5), 3.0, .25)

# 4.50–5.05 riser into the hub zoom
rt, step = 4.5, .125
while rt < 5.0:
    add(snare(.7), rt, .15 + .35 * (rt - 4.5))
    step = max(.035, step * .8)
    rt += step
t = tt(.55)
add(whoosh(.55, 300, 7000, bw=1.0, shape=lambda u: u ** 2), 4.5, .55)
add(np.sin(osc_phase(220 * 2 ** (t / .55 * 2))) * (t / .55) ** 2 * .3, 4.5, .4)

# 5.05 «Доставка» HIT, 5.25 «по всему», 5.50 «Кыргызстану» HIT + ding
add(kick(1.0, .6), 5.05, 1.0)
add(clap(1.2), 5.05, .5)
add(stab([62, 66, 69, 74], .7, bright=5000), 5.05, .5)
add(crash(1.2), 5.05, .22)
add(pop(), 5.25, .45); add(blip(83), 5.25, .3, .2)
add(kick(1.0, .6), 5.5, .95)
add(clap(1.2), 5.5, .45)
add(stab([66, 69, 74, 78], .8, bright=6000), 5.5, .45)
add(bell(1568, 2.0), 5.5, .45, .15)
for b in range(3):                        # groove under the hold 6.0 – 6.5
    tb = 6.0 + b * .5
    if tb >= 6.9: break
    add(kick(.8), tb, .75)
    add(hat(.5), tb + .25, .3, .35)
    add(hat(.3), tb + .125, .15, -.25)
    if b % 2: add(clap(), tb, .35)
for i in range(6):
    add(bass(riff[i], .23), 5.5 + i * .25, .5)
add(rumble(1.8, rate=13), 5.1, .15)
add(whoosh(.2, 600, 5000, bw=1.2), 6.8, .45)

# 7.00 «от 350» BIG HIT + confetti, 7.30 «сом» pop + ching
add(kick(1.0, .7), 7.0, 1.0)
add(clap(1.3), 7.0, .55)
add(crash(2.0), 7.0, .4, -.2)
add(stab([62, 66, 69, 74, 78], .9, bright=6000), 7.0, .5)
add(popper(), 7.0, .5, -.5); add(popper(), 7.02, .5, .5)
add(pop(1.3), 7.3, .5); add(bell(2637, .9), 7.3, .3, .2); add(bell(3520, .6), 7.36, .18, -.2)
for b in range(4):                        # 7.5 – 8.5
    tb = 7.5 + b * .5
    add(kick(.85), tb, .8)
    add(hat(.6), tb + .25, .3, .35)
    add(hat(.35), tb + .125, .15, -.25)
    add(hat(.35), tb + .375, .15, -.25)
    if b % 2 == 0: add(clap(), tb, .4, .1)
for i in range(8):                        # 7.0 – 8.75
    add(bass(riff[i % 8], .23), 7.0 + i * .25, .5)
add(rumble(1.8, rate=13), 7.0, .15)

# 8.80–9.50 iris whoosh + wheel spin-in, 9.50 BELL + final chord, 9.60 «Kiwi Go», 9.95 pill
add(whoosh(.3, 400, 3000, bw=1.4), 8.82, .5)
t = tt(.5)
add(whoosh(.5, 2500, 500, bw=1.0, shape=lambda u: np.sin(np.pi * u) ** .8), 9.0, .45)
add(np.sin(osc_phase(900 - 500 * t / .5)) * np.sin(np.pi * t / .5) * np.abs(np.sin(2 * np.pi * (24 - 30 * t) * t)) * .2, 9.0, .5)  # spinning whirr
add(kick(1.0, .7), 9.5, .95)
add(bike_bell(), 9.5, .9, .25)
add(bike_bell(), 9.66, .75, .25)
add(bell(1568, 2.4), 9.5, .35, -.1)
add(pad([50, 62, 66, 69, 76], 2.5), 9.5, .6)
add(stab([62, 66, 69, 74], .9, bright=4500), 9.5, .35)
add(pop(1.2), 9.6, .5); add(clap(), 9.6, .25)
add(pop(1.3), 9.95, .5); add(blip(93, d=.3), 9.95, .3); add(bell(3136, .9), 9.97, .15)
for b in range(3):                        # light outro groove 10.0 – 11.0
    tb = 10.0 + b * .5
    add(kick(.6), tb, .55)
    add(hat(.45), tb + .25, .25, .35)
add(pad([47, 59, 62, 66, 74], 1.8), 11.0, .35)
add(bike_bell(.7), 11.0, .35, .3)

# ---------------------------------------------------------------- master
# gentle glue: soft saturation + fades
print(f"raw mix peak {np.max(np.abs(mix)):.2f}")
mix *= 0.8 / np.max(np.abs(mix))   # v2: scale first so the soft saturation only rounds the very top, keeping transients
mix = np.tanh(mix * 1.1) / 1.1
fi, fo = int(.015 * SR), int(.6 * SR)
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
