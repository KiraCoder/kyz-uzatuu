"""Kiwi Go brand film — edit / composite.

Takes 3 logo-free AI clips (clip-0/1/2.mp4) and builds a 16 s 9:16 film in the style of the
reference: light-leak open, light-leak transitions, the EXACT logo rising out of the clouds,
a clean paper end card with type-on text, flare, fade to black. No music (added later).
"""
import subprocess, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1080, 1920, 30, 17.0
N = int(DUR * FPS)
FONTS = os.path.join(HERE, '..', '..', 'fonts')
LOGO = Image.open(os.path.join(HERE, '..', '..', 'logo', 'kiwi-go-logo-1024.png')).convert('RGBA')
PAPER = (255, 253, 247); INK = (17, 20, 16)

def ease(x):  # easeInOutCubic
    x = min(max(x, 0.0), 1.0)
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def ease_out(x):
    x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def ramp(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)

def load_clip(path):
    """Decode a clip to a list of 1080x1920 RGB uint8 frames at 30 fps."""
    cmd = ['ffmpeg', '-v', 'error', '-i', path, '-vf',
           f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)

clips = [load_clip(os.path.join(HERE, f'clip-{i}.mp4')) for i in range(3)]
print('clip frames:', [len(c) for c in clips])

def clip_frame(i, t_local, speed=1.0):
    c = clips[i]; k = int(round(t_local * speed * FPS))
    return c[min(max(k, 0), len(c) - 1)].astype(np.float32)

# --- timeline (seconds) ------------------------------------------------------------
# clip0 0.0–4.6 | leak 4.1–4.9 | clip1 4.5–8.9 | dissolve 8.5–9.1 | clip2 8.7–13.4
# logo rises in clouds 11.4–13.2 | flash 13.0–13.6 | end card 13.4–16.0 | flare 15.0 | black 15.5–16.0
SEG = [(0, 0.0, 4.6, 0.15), (1, 4.5, 8.9, 0.0), (2, 8.7, 13.6, 0.0)]  # (clip, start, end, src offset)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def leak(t, cx, cy, r, color, strength):
    """Warm additive light-leak blob."""
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / r) ** 2)
    a = np.clip(1 - d, 0, 1) ** 1.6 * strength
    return a[..., None] * np.array(color, np.float32)[None, None, :]

def scene(t):
    """Base AI footage with cross-dissolves."""
    acc = None; wsum = 0.0
    for (ci, s, e, off) in SEG:
        if t < s - 1e-6 or t > e + 1e-6: continue
        w = min(ramp(t, s, s + 0.4) if s > 0 else 1.0, 1 - ramp(t, e - 0.4, e) if e < 13.6 else 1.0)
        f = clip_frame(ci, t - s + off)
        acc = f * w if acc is None else acc + f * w; wsum += w
    if acc is None: return np.zeros((H, W, 3), np.float32)
    return acc / max(wsum, 1e-6)

def logo_img(size, rot):
    im = LOGO.resize((size, size), Image.LANCZOS)
    return im.rotate(rot, resample=Image.BICUBIC, expand=False)

f_word = ImageFont.truetype(os.path.join(FONTS, 'Inter-Black.otf'), 150)
f_tag = ImageFont.truetype(os.path.join(FONTS, 'Inter-Bold.otf'), 64)
WORD = 'Kiwi Go'; TAG1 = 'Доставка по всему'; TAG2 = 'Кыргызстану'

def end_card(t):
    """Clean paper card: logo, type-on wordmark and tagline."""
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    p = ease_out(ramp(t, 13.4, 14.0))
    size = int(380 + 40 * (1 - p)); rot = -90 * (1 - p)
    lg = logo_img(size, rot); a = lg.split()[3].point(lambda v: int(v * p))
    im.paste(lg, (W // 2 - size // 2, 640 - size // 2), a)
    # wordmark types in
    n = int(len(WORD) * ramp(t, 13.9, 14.5) + 0.999) if t >= 13.9 else 0
    if n:
        full = d.textlength(WORD, font=f_word)
        d.text((W / 2 - full / 2, 900), WORD[:n], font=f_word, fill=INK)
    for line, y, a0 in ((TAG1, 1110, 14.4), (TAG2, 1190, 14.75)):
        n = int(len(line) * ramp(t, a0, a0 + 0.35) + 0.999) if t >= a0 else 0
        if n:
            full = d.textlength(line, font=f_tag)
            d.text((W / 2 - full / 2, y), line[:n], font=f_tag, fill=INK)
    return np.asarray(im, np.float32)

def bloom(fr, amount=0.18):
    small = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).resize((W // 8, H // 8))
    blur = np.asarray(small.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR), np.float32)
    return 255 - (255 - fr) * (255 - blur * amount) / 255  # screen blend

def frame(t):
    if t < 13.4:
        fr = scene(t)
        # logo rises out of the clouds (upper centre), rolling, with glow
        if t >= 11.4:
            p = ease(ramp(t, 11.4, 13.0)); size = int(200 + 220 * p)
            cy = 1040 - 200 * p; rot = 360 * (1 - p) * 0.75
            lg = logo_img(size, rot)
            glow = lg.split()[3].filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.8 * p))
            base = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
            warm = Image.new('RGB', lg.size, (255, 236, 190))
            base.paste(warm, (W // 2 - size // 2, int(cy - size / 2)), glow)
            alpha = lg.split()[3].point(lambda v: int(v * min(1, p * 1.6)))
            base.paste(lg, (W // 2 - size // 2, int(cy - size / 2)), alpha)
            fr = np.asarray(base, np.float32)
        fr = bloom(fr)
    else:
        fr = end_card(t)
    # light leaks / flashes (additive, warm)
    add = np.zeros_like(fr)
    if t < 0.7:   # open from white light leak
        k = 1 - ease(ramp(t, 0.0, 0.7)); fr = fr * (1 - k) + np.array([255, 246, 230]) * k
    for (a, b, cx, cy, col) in ((4.0, 5.0, 300, 1300, (255, 170, 70)), (12.9, 13.8, 540, 700, (255, 230, 190))):
        if a <= t <= b:
            s = math.sin(math.pi * ramp(t, a, b))
            add += leak(t, cx + 500 * ramp(t, a, b), cy, 1100, col, 1.4 * s)
            fr = fr * (1 - 0.45 * s) + 255 * 0.45 * s
    if 15.7 <= t <= 16.5:   # lens flare sweep on the end card
        s = math.sin(math.pi * ramp(t, 15.7, 16.5))
        add += leak(t, 200 + 700 * ramp(t, 15.7, 16.5), 1600, 420, (255, 200, 140), 0.6 * s)
    fr = fr + add
    if t >= 16.3:   # fade to black
        fr = fr * (1 - ease(ramp(t, 16.3, 16.95)))
    return np.clip(fr, 0, 255).astype(np.uint8)

out = os.path.join(HERE, 'kiwi-go-brand-film.mp4')
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                        '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow',
                        '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for i in range(N):
    enc.stdin.write(frame(i / FPS).tobytes())
    if i % 60 == 0: print('frame', i, flush=True)
enc.stdin.close(); enc.wait()
print('wrote', out)
