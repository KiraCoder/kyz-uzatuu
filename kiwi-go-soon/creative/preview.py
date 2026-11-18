import sys
from PIL import Image
for n in sys.argv[1:]:
    Image.open(f'kiwi-go-creative-{n}.png').resize((1000,1000), Image.LANCZOS).save(f'/tmp/claude-0/-home-user-kyz-uzatuu/70f874b5-f664-5bb7-81c4-002190694b11/scratchpad/p{n}.png')
