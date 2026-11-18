import sys, glob
from PIL import Image
import numpy as np
for f in sorted(glob.glob('kiwi-go-soon-0*.png')):
    a = np.asarray(Image.open(f).convert('RGB')).astype(int)
    w = ((a[...,0]>240)&(a[...,1]>240)&(a[...,2]>235)).mean()*100
    flag = 'OK' if 70<=w<=80 else 'OUT OF RANGE'
    print(f"{f}  {a.shape[1]}x{a.shape[0]}  white={w:.1f}%  {flag}")
