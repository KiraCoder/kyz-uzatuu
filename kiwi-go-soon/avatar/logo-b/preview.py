from PIL import Image, ImageDraw, ImageFont
import glob
names = ['1-full-bleed','2-lime','3-ink','4-paper']
f = ImageFont.truetype('../../fonts/Inter-Bold.otf', 26)
W, rowh = 1220, 450
sheet = Image.new('RGB', (W, rowh*len(names)), '#ECE6D6'); d = ImageDraw.Draw(sheet)
def circ(im, s):
    im = im.resize((s, s), Image.LANCZOS); m = Image.new('L', (s*4, s*4), 0)
    ImageDraw.Draw(m).ellipse((0,0,s*4-1,s*4-1), fill=255); return im, m.resize((s,s), Image.LANCZOS)
for r, n in enumerate(names):
    y = r*rowh; src = Image.open(f'kiwi-go-avatar-b{n}-1080.png').convert('RGB')
    for bx, bg in ((20, '#FFFFFF'), (620, '#000000')):
        d.rectangle((bx, y+20, bx+580, y+390), fill=bg)
        x = bx+20
        for s in (340, 110, 40):
            im, m = circ(src, s); sheet.paste(im, (x, y+30+(340-s)//2), m); x += s+20
    d.text((24, y+402), f'Б{r+1} · {n.split("-",1)[1]}', font=f, fill='#111410' if True else None)
sheet.save('preview.png')
