# Generates Kiwi Go avatar SVG sources (text converted to outlines, logo used verbatim).
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
C = dict(lime='#B8F03C', ink='#111410', paper='#FFFDF7', cream='#F6F1E4', sand='#ECE6D6',
         peel='#7A5A3C', green='#3F6212', rim='#6BA82B')
S = 1080; CX = CY = 540

# ---------- logos (verbatim geometry from the brand guide) ----------
def logo_full_inner():
    seeds = ''.join(f'<ellipse cx="0" cy="{-40 if i % 2 == 0 else -52}" rx="5.5" ry="11" transform="rotate({i*22.5})"/>' for i in range(16))
    return (f'<circle r="100" fill="{C["ink"]}"/><circle r="80" fill="{C["rim"]}"/><circle r="73" fill="{C["lime"]}"/>'
            f'<g fill="{C["ink"]}">{seeds}</g><circle r="20" fill="{C["cream"]}"/><circle r="7" fill="{C["ink"]}"/>')

def logo_small_inner():
    seeds = ''.join(f'<ellipse cx="0" cy="-48" rx="7" ry="14" transform="rotate({i*45})"/>' for i in range(8))
    return (f'<circle r="100" fill="{C["ink"]}"/><circle r="78" fill="{C["lime"]}"/>'
            f'<g fill="{C["ink"]}">{seeds}</g><circle r="24" fill="{C["cream"]}"/><circle r="8" fill="{C["ink"]}"/>')

def logo(cx, cy, r, rot=0, kind='small'):
    inner = logo_small_inner() if kind == 'small' else logo_full_inner()
    rt = f' rotate({rot})' if rot else ''
    return f'<g transform="translate({cx} {cy}) scale({r/100}){rt}">{inner}</g>'

# ---------- text to outlines (Inter Black) ----------
FONT = TTFont('/usr/share/fonts/opentype/inter/Inter-Black.otf')
GS = FONT.getGlyphSet(); CMAP = FONT.getBestCmap(); UPM = FONT['head'].unitsPerEm
HMTX = FONT['hmtx']

def glyph(ch):
    name = CMAP[ord(ch)]
    pen = SVGPathPen(GS); GS[name].draw(pen)
    return pen.getCommands(), HMTX[name][0]

def text_width(s, size, track=0):
    return sum(glyph(ch)[1] for ch in s) * size / UPM + track * size * (len(s) - 1)

def text_path(s, x, y, size, fill, anchor='middle', track=0):
    """Return outlined text; y is the baseline."""
    w = text_width(s, size, track)
    x0 = x - w / 2 if anchor == 'middle' else x
    k = size / UPM; out = []; pen_x = x0
    for ch in s:
        d, adv = glyph(ch)
        if d:
            out.append(f'<path transform="translate({pen_x:.2f} {y}) scale({k:.5f} {-k:.5f})" d="{d}"/>')
        pen_x += adv * k + track * size
    return f'<g fill="{fill}">{"".join(out)}</g>'

def ring_text(s, r, size, fill, start_deg=0, track=0):
    """Outlined text set on a circle of radius r (baseline), reading clockwise from the top."""
    k = size / UPM; out = []
    arc = 0.0
    for ch in s:
        d, adv = glyph(ch)
        a = adv * k
        mid = arc + a / 2
        ang = start_deg + math.degrees(mid / r)
        if d:
            out.append(f'<g transform="translate({CX} {CY}) rotate({ang:.3f}) translate({-a/2:.2f} {-r})">'
                       f'<path transform="scale({k:.5f} {-k:.5f})" d="{d}"/></g>')
        arc += a + track * size
    return f'<g fill="{fill}">{"".join(out)}</g>', arc

def svg(body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
            f'<title>{title}</title>{body}</svg>\n')

def bg(color):
    return f'<rect width="{S}" height="{S}" fill="{color}"/>'

V = []

# 01 Paper — logo alone on paper
V.append(('Paper', bg(C['paper']) + logo(CX, CY, 360)))

# 02 Ink — logo on ink; the ink rim melts into the ground, leaving a glowing lime slice
V.append(('Ink', bg(C['ink']) + logo(CX, CY, 420)))

# 03 Lime — logo on lime: the ink rim becomes a bold outline
V.append(('Lime', bg(C['lime']) + logo(CX, CY, 360)))

# 04 Rolling — rotated logo with ink speed lines and ground line, on cream
def pill(x1, x2, y, h, fill):
    return f'<rect x="{x1}" y="{y-h/2}" width="{x2-x1}" height="{h}" rx="{h/2}" fill="{fill}"/>'
ox, oy, orr = 600, 510, 290
roll = bg(C['cream'])
roll += pill(128, 300, 420, 34, C['ink']) + pill(176, 290, 510, 34, C['ink']) + pill(128, 300, 600, 34, C['ink'])
roll += pill(230, 940, oy + orr + 22, 26, C['ink'])
roll += logo(ox, oy, orr, rot=-20)
V.append(('Rolling', roll))

# 05 Lockup — logo + «Kiwi Go» wordmark on lime
lk = bg(C['lime']) + logo(CX, 405, 250)
lk += text_path('Kiwi Go', CX, 845, 190, C['ink'], track=-0.02)
V.append(('Lockup', lk))

# 06 Скоро ring — launch-period ring of lime type around the logo on ink
ring_r = 400; size = 96
unit = 'СКОРО • '
# fit an integer number of repeats; compute natural length and adjust tracking to close the ring exactly
_, natural = ring_text(unit * 3, ring_r, size, C['lime'])
circ = 2 * math.pi * ring_r
reps = max(1, round(circ / natural * 3))
s = unit * reps
nat = text_width(s, size) + 0
track = (circ - nat) / (len(s) * size)
rt, _ = ring_text(s, ring_r, size, C['lime'], start_deg=-math.degrees(text_width('СКОРО', size)/2/ring_r), track=track)
V.append(('Skoro ring', bg(C['ink']) + rt + logo(CX, CY, 300)))

# 07 Kiwi skin — kiwi-peel brown with a scatter of seed/fuzz marks, logo on a sand halo
import random
random.seed(7)
pat = ''
step = 72
for gy in range(-1, S // step + 2):
    for gx in range(-1, S // step + 2):
        x = gx * step + (step / 2 if gy % 2 else 0) + random.uniform(-14, 14)
        y = gy * step + random.uniform(-14, 14)
        a = random.uniform(0, 180)
        pat += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="5" ry="11" transform="rotate({a:.0f} {x:.1f} {y:.1f})"/>'
skin = bg(C['peel']) + f'<g fill="{C["ink"]}" opacity="0.28">{pat}</g>'
skin += f'<circle cx="{CX}" cy="{CY}" r="372" fill="{C["sand"]}"/>' + logo(CX, CY, 340)
V.append(('Kiwi skin', skin))

# 08 Bullseye — feed-stopper: ink ground, huge lime halo, logo inside
be = bg(C['ink']) + f'<circle cx="{CX}" cy="{CY}" r="455" fill="{C["lime"]}"/>' + logo(CX, CY, 375)
V.append(('Bullseye', be))

os.makedirs(os.path.join(HERE, 'svg'), exist_ok=True)
names = []
for i, (name, body) in enumerate(V, 1):
    nn = f'{i:02d}'
    with open(os.path.join(HERE, 'svg', f'kiwi-go-avatar-{nn}.svg'), 'w') as f:
        f.write(svg(body, f'Kiwi Go avatar {nn} — {name}'))
    names.append(f'{nn}\t{name}')
with open(os.path.join(HERE, 'svg', 'names.tsv'), 'w') as f:
    f.write('\n'.join(names) + '\n')

# standalone logos
for kind in ('full', 'small'):
    inner = logo_full_inner() if kind == 'full' else logo_small_inner()
    with open(os.path.join(HERE, 'logo', f'kiwi-go-logo-{kind}.svg'), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -100 200 200" width="200" height="200">'
                f'<title>Kiwi Go logo — {kind}</title>{inner}</svg>\n')
print('\n'.join(names))
