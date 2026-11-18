"""Extracts frames from the final MP4 -> storyboard.png (8 frames) and poster.png."""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
TIMES = [0.60, 1.40, 2.60, 3.70, 5.00, 6.40, 7.95, 9.70]
POSTER_T = 7.95
def grab(t, path):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{t:.3f}', '-i', 'kiwi-go-reel-05-po-vsemu-kg.mp4',
                    '-frames:v', '1', path], check=True)
os.makedirs('_sb', exist_ok=True)
tw, th, g, m, lab = 360, 640, 28, 40, 70
sheet = Image.new('RGB', (m * 2 + tw * 4 + g * 3, m + (th + lab) * 2 + g), (0xEC, 0xE6, 0xD6))
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 30)
for i, t in enumerate(TIMES):
    p = f'_sb/{i}.png'; grab(t, p)
    im = Image.open(p).convert('RGB').resize((tw, th), Image.LANCZOS)
    x = m + (i % 4) * (tw + g); y = m + (i // 4) * (th + lab + g)
    sheet.paste(im, (x, y)); d.rectangle([x - 1, y - 1, x + tw, y + th], outline=(0x11, 0x14, 0x10), width=2)
    d.text((x + tw / 2, y + th + lab / 2), f'{i + 1} · {t:.2f} s', font=font, fill=(0x11, 0x14, 0x10), anchor='mm')
sheet.save('storyboard.png')
grab(POSTER_T, 'poster.png')
for f in os.listdir('_sb'): os.remove(os.path.join('_sb', f))
os.rmdir('_sb')
print(sheet.size)
