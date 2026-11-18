from PIL import Image, ImageDraw, ImageFont
T, G, M, LAB = 640, 48, 64, 120
W = M*2 + T*5 + G*4; H = M + T + LAB
sheet = Image.new('RGB', (W, H), (0x11, 0x14, 0x10))
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype('../fonts/Inter-Black.otf', 64)
for i in range(5):
    im = Image.open(f'kiwi-go-creative-0{i+1}.png').convert('RGB').resize((T, T), Image.LANCZOS)
    x = M + i*(T+G)
    sheet.paste(im, (x, M))
    d.text((x + T/2, M + T + LAB/2), f'0{i+1}', font=font, fill=(0xB8,0xF0,0x3C), anchor='mm')
sheet.save('contact-sheet.png'); print(sheet.size)
