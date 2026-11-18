"""Kiwi Go remix of the black/white text-card trend video.
Keeps the original hook footage and audio; replaces every text card with Kiwi Go copy,
animated word-by-word on the music hits, and ends on the exact logo."""
import subprocess, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source.mp4')
FONTS = os.path.join(HERE, '..', 'brand-reel', 'edit', 'fonts')
LOGO = Image.open(os.path.join(HERE, '..', 'logo', 'kiwi-go-logo-1024.png')).convert('RGBA')
W, H, FPS = 1080, 1920, 30
DUR = 6.685
N = int(round(DUR * FPS))
INK, PAPER, LIME, WHITE, BLACK = (17, 20, 16), (255, 253, 247), (184, 240, 60), (255, 255, 255), (0, 0, 0)
F700 = lambda s: ImageFont.truetype(os.path.join(FONTS, 'onest-700.ttf'), s)
F600 = lambda s: ImageFont.truetype(os.path.join(FONTS, 'onest-600.ttf'), s)

def clamp(x): return min(max(x, 0.0), 1.0)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back_out(x, s=1.7):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1

# ---- source frames (hook footage) --------------------------------------------
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'scale={W}:{H}:flags=lanczos,fps={FPS}',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
SRCF = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)

# ---- cards: (start, end, bg, lines[[(word, accent)]], hit) ---------------------
# Background switches at the original cut times; words land on the measured audio hits.
CARDS = [
    (2.133, 3.133, 'W', [[('Нужно', 0), ('отправить', 0)], [('посылку?', 1)]], 2.37),
    (3.133, 4.067, 'B', [[('Заберём', 0)], [('у', 0), ('двери.', 1)]], 3.25),
    (4.067, 4.833, 'W', [[('По', 0), ('всему', 0)], [('Кыргызстану.', 1)]], 4.10),
    (4.833, 5.533, 'B', [[('от', 0), ('350', 1), ('сом.', 0)]], 4.95),
]
END = (5.533, DUR, 5.78)
SIZE = 112; GAP = 26; LEAD = 136; STAGGER = 0.07

def word_img(text, size, color):
    f = F700(size); bb = f.getbbox(text)
    im = Image.new('RGBA', (bb[2] - bb[0] + 8, size + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - bb[0], 10), text, font=f, fill=color)
    return im

def layout(lines, size):
    """Return list of (word, accent, x, y, w) centred on the frame."""
    f = F700(size); out = []
    total_h = LEAD * (len(lines) - 1)
    y0 = 900 - total_h / 2
    for li, line in enumerate(lines):
        widths = [f.getbbox(w)[2] - f.getbbox(w)[0] + 8 for w, _ in line]
        lw = sum(widths) + GAP * (len(line) - 1)
        x = W / 2 - lw / 2
        for (w, acc), ww in zip(line, widths):
            out.append((w, acc, x, y0 + li * LEAD, ww)); x += ww + GAP
    return out

def draw_card(t, card):
    s, e, bg, lines, hit = card
    base = Image.new('RGB', (W, H), WHITE if bg == 'W' else BLACK)
    fg = BLACK if bg == 'W' else WHITE
    zoom = 1 + 0.035 * clamp((t - hit) / (e - hit))          # slow push on the text block
    items = layout(lines, SIZE)
    for k, (w, acc, x, y, ww) in enumerate(items):
        tw = hit + k * STAGGER
        p = (t - tw) / 0.16
        if p <= 0: continue
        sc = 1.25 - 0.25 * back_out(p); a = clamp(p * 2.2)
        col = fg
        if acc and bg == 'B': col = LIME                        # lime text only on black
        img = word_img(w, SIZE, col)
        # lime highlighter band behind accent words on white cards
        if acc and bg == 'W':
            band_p = ease_out((t - tw - 0.08) / 0.22)
            if band_p > 0:
                band = Image.new('RGBA', img.size, (0, 0, 0, 0))
                bw = int(img.width * band_p)
                ImageDraw.Draw(band).rounded_rectangle((0, int(SIZE * 0.55), bw, int(SIZE * 1.12)), 14, fill=LIME + (255,))
                band.alpha_composite(img); img = band
        sc *= zoom
        img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.LANCZOS)
        if a < 1: img.putalpha(img.split()[3].point(lambda v: int(v * a)))
        cx = W / 2 + (x + ww / 2 - W / 2) * zoom; cy = 960 + (y + SIZE / 2 - 960) * zoom - 18 * (1 - ease_out(p))
        base.paste(img, (int(cx - img.width / 2), int(cy - img.height / 2)), img)
    return base

def draw_end(t):
    s, e, hit = END
    base = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(base)
    # logo rolls in from the left and lands on the hit with a small squash
    p = ease_out((t - s) / (hit - s))
    size = 330; cx = -200 + (540 + 200) * p; cy = 760
    rot = -540 * (1 - p)
    lg = LOGO.resize((size, size), Image.LANCZOS).rotate(rot, resample=Image.BICUBIC)
    sq = 1.0
    if t >= hit:
        q = (t - hit) / 0.22
        sq = 1 + 0.10 * math.sin(math.pi * clamp(q)) * (1 - clamp(q))
    lw, lh = int(size * sq), int(size / sq)
    lg = lg.resize((lw, lh), Image.LANCZOS)
    base.paste(lg, (int(cx - lw / 2), int(cy + size / 2 - lh)), lg)
    # ground line under the wheel
    gl = ease_out((t - s) / 0.35)
    d.rounded_rectangle((int(540 - 260 * gl), 932, int(540 + 260 * gl), 942), 5, fill=INK)
    # «Доставляй с» then «Kiwi Go» on lime band, then kiwigo.kg
    for text, size_, y, t0, accent in (('Доставляй с', 84, 1010, hit + 0.06, 0), ('Kiwi Go', 132, 1110, hit + 0.16, 1)):
        q = (t - t0) / 0.16
        if q <= 0: continue
        img = word_img(text, size_, INK)
        if accent:
            band = Image.new('RGBA', (img.width + 40, img.height), (0, 0, 0, 0))
            bw = int((img.width + 40) * ease_out((t - t0 - 0.06) / 0.22))
            ImageDraw.Draw(band).rounded_rectangle((0, int(size_ * 0.5), bw, int(size_ * 1.12)), 18, fill=LIME + (255,))
            band.paste(img, (20, 0), img); img = band
        sc = 1.2 - 0.2 * back_out(q)
        img = img.resize((int(img.width * sc), int(img.height * sc)), Image.LANCZOS)
        if q < 0.5: img.putalpha(img.split()[3].point(lambda v: int(v * clamp(q * 2.2))))
        base.paste(img, (int(540 - img.width / 2), int(y - 10 * (1 - ease_out(q)))), img)
    q = (t - (hit + 0.36)) / 0.2
    if q > 0:
        f = F600(58); txt = 'kiwigo.kg'; tw = d.textlength(txt, font=f)
        col = tuple(int(255 + (c - 255) * clamp(q)) for c in INK)
        d.text((540 - tw / 2, 1290 + 12 * (1 - ease_out(q))), txt, font=f, fill=col)
    return base

def hook_caption(img, t):
    """Meme-style caption over the original hook footage."""
    p = ease_out((t - 0.15) / 0.25)
    if p <= 0: return img
    d = ImageDraw.Draw(img); f = F700(66)
    lines = ['Когда отправил посылку', '«с водителем»…']
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f); y = 300 + i * 84 - 14 * (1 - p)
        d.text((540 - tw / 2, y), ln, font=f, fill=WHITE, stroke_width=7, stroke_fill=BLACK)
    return img

def frame(i):
    t = i / FPS
    for c in CARDS:
        if c[0] <= t < c[1]: return draw_card(t, c)
    if t >= END[0]: return draw_end(t)
    img = Image.fromarray(SRCF[min(i, len(SRCF) - 1)].copy())
    return img  # hook stays clean: no text on the original footage

out_v = os.path.join(HERE, '_video.mp4')
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                        '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', out_v],
                       stdin=subprocess.PIPE)
for i in range(N):
    enc.stdin.write(np.asarray(frame(i), np.uint8).tobytes())
enc.stdin.close(); enc.wait()
final = os.path.join(HERE, 'kiwi-go-remix.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out_v, '-i', SRC, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-t', f'{DUR}', '-movflags', '+faststart', final], check=True)
os.remove(out_v)
print('wrote', final)
