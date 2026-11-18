"""Contact sheet of preview stills: python3 sheet.py out.png file1.png file2.png ..."""
import sys
from PIL import Image, ImageDraw
files = sys.argv[2:]; tw, th = 270, 480
sheet = Image.new('RGB', (tw * min(4, len(files)), th * ((len(files) + 3) // 4)), (128, 128, 128))
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle([110, 260, 950, 1480], outline=(255, 0, 255), width=4)   # safe zone
    sheet.paste(im.resize((tw, th), Image.LANCZOS), ((i % 4) * tw, (i // 4) * th))
sheet.save(sys.argv[1])
