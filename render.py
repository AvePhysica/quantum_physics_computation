import numpy as np
from PIL import Image, ImageDraw

board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
Wp, Hp = 1065, 1062
img = Image.new("RGB", (Wp, Hp), (232, 200, 130))
d = ImageDraw.Draw(img)
xs = [23.5 + 56.25*k for k in range(19)]
ys = [24.5 + (1037.5-24.5)/18*k for k in range(19)]
for x in xs: d.line([(x, ys[0]), (x, ys[-1])], fill=(90,70,40), width=2)
for y in ys: d.line([(xs[0], y), (xs[-1], y)], fill=(90,70,40), width=2)
for j in range(19):
    for i in range(19):
        v = board[j,i]
        if v == 0: continue
        c = (25,25,25) if v==1 else (245,242,232)
        R = 25
        d.ellipse([xs[i]-R, ys[j]-R, xs[i]+R, ys[j]+R], fill=c)
img.save(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\reconstructed.png")

# side-by-side scaled comparison
orig = Image.open(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\go_board.png").convert("RGB")
comp = Image.new("RGB", (Wp*2+20, Hp), (255,255,255))
comp.paste(orig, (0,0)); comp.paste(img, (Wp+20,0))
comp = comp.resize(((Wp*2+20)//2, Hp//2))
comp.save(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\compare.png")
print("ok")
