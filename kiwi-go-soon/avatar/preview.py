# "Instagram reality check": each avatar circle-cropped at 340/110/40 on white and black app backgrounds,
# plus a full-vs-small logo test at 40 px.
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__))
names = [l.split('\t') for l in open(os.path.join(D, 'svg', 'names.tsv')).read().split('\n') if l]
F = '/usr/share/fonts/opentype/inter/'
fB = ImageFont.truetype(F + 'Inter-Bold.otf', 26); fS = ImageFont.truetype(F + 'Inter-SemiBold.otf', 18)

def circ(img, size):
    im = img.convert('RGB').resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size * 4, size * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    out = Image.new('RGBA', (size, size)); out.paste(im, (0, 0), m.resize((size, size), Image.LANCZOS)); return out

SIZES = [340, 110, 40]
PAD = 30; HALF = PAD + 340 + 30 + 110 + 30 + 40 + PAD   # one app-background panel
ROW = 340 + 80
W = 220 + HALF * 2; H = 70 + ROW * len(names) + 260
sheet = Image.new('RGB', (W, H), '#ECE6D6'); d = ImageDraw.Draw(sheet)
d.text((24, 22), 'Kiwi Go — Instagram avatar reality check (circle crop at 340 / 110 / 40 px)', font=fB, fill='#111410')
for i, (nn, name) in enumerate(names):
    y = 70 + i * ROW
    d.text((24, y + 150), nn, font=ImageFont.truetype(F + 'Inter-Black.otf', 56), fill='#111410')
    d.text((24, y + 220), name, font=fS, fill='#111410')
    src = Image.open(os.path.join(D, f'kiwi-go-avatar-{nn}-1080.png'))
    for p, bgc in enumerate(['#FFFFFF', '#000000']):
        x0 = 220 + p * HALF
        sheet.paste(bgc, (x0, y, x0 + HALF, y + ROW - 20))
        x = x0 + PAD
        for s in SIZES:
            sheet.paste(circ(src, s), (x, y + 20 + (340 - s) // 2), circ(src, s))
            d.text((x, y + 20 + (340 + s) // 2 + 6 if s < 340 else y + 362), f'{s}', font=fS, fill='#888888')
            x += s + 30
# logo full vs small at 40 / 56 / 110 on white + black
y = 70 + ROW * len(names) + 10
d.text((24, y), 'Logo test: FULL vs SMALL version at 40 / 56 / 110 px', font=fB, fill='#111410')
x = 24
for kind in ('full', 'small'):
    lg = Image.open(os.path.join(D, 'logo', f'kiwi-go-logo-{kind}-1024.png'))
    for bgc in ('#FFFFFF', '#000000', '#B8F03C'):
        sheet.paste(bgc, (x, y + 50, x + 290, y + 230))
        xx = x + 14
        for s in (40, 56, 110):
            l = lg.resize((s, s), Image.LANCZOS); sheet.paste(l, (xx, y + 50 + (180 - s) // 2), l); xx += s + 24
        d.text((x + 6, y + 206), kind, font=fS, fill='#888888')
        x += 300
    x += 40
sheet.save(os.path.join(D, 'preview.png'))
print(sheet.size)
