from PIL import Image, ImageDraw, ImageFont
T, G, M, LAB = 640, 48, 64, 120
W = M*2 + T*5 + G*4; H = M + T + LAB
sheet = Image.new('RGB', (W, H), (0xEC, 0xE6, 0xD6))
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype('fonts/Inter-Black.otf', 64)
for i in range(5):
    im = Image.open(f'kiwi-go-soon-0{i+1}.png').convert('RGB').resize((T, T), Image.LANCZOS)
    x = M + i*(T+G)
    sheet.paste(im, (x, M))
    d.rectangle([x-1, M-1, x+T, M+T], outline=(0x11,0x14,0x10), width=2)
    d.text((x + T/2, M + T + LAB/2), f'0{i+1}', font=font, fill=(0x11,0x14,0x10), anchor='mm')
sheet.save('contact-sheet.png'); print(sheet.size)
