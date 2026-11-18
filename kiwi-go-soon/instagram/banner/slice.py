from PIL import Image, ImageDraw
pano = Image.open('panorama.png').convert('RGB')
V, B = 1012.5, 33.75
tiles = []
for i in range(3):
    x0 = round(i * V)            # tile i spans [i*V, i*V+1080) in panorama coords (incl. bleed)
    t = pano.crop((x0, 0, x0 + 1080, 1350)); tiles.append(t)
    # post order: right tile is posted FIRST
    t.save(f'kiwi-go-banner-{i+1}-post{3-i}.png')
# grid preview: each tile centre-cropped to 3:4 like the profile grid, 2px gaps, on a dark app bg
w = 360; h = 480; g = 2
prev = Image.new('RGB', (3*w + 2*g, h), '#0c0f14')
for i, t in enumerate(tiles):
    c = t.crop((B, 0, 1080 - B, 1350)).resize((w, h), Image.LANCZOS)
    prev.paste(c, (i*(w+g), 0))
prev.save('grid-preview.png')
