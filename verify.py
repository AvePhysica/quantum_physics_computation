import numpy as np
from PIL import Image

# Independent verification: annulus sampling at radius ~20 px
orig = Image.open(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\go_board.png").convert("RGB")
a = np.asarray(orig).astype(float)
board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
xs = [23.5 + 56.25*k for k in range(19)]
ys = [24.5 + (1037.5-24.5)/18*k for k in range(19)]
mism = 0
for j in range(19):
    for i in range(19):
        pts = []
        for t in np.linspace(0, 2*np.pi, 48, endpoint=False):
            for R in (18, 20, 22):
                x = int(round(xs[i] + R*np.cos(t))); y = int(round(ys[j] + R*np.sin(t)))
                if 0 <= x < a.shape[1] and 0 <= y < a.shape[0]:
                    pts.append(a[y, x])
        pts = np.array(pts)
        med = np.median(pts, axis=0)
        L = med.mean(); s = med.max()-med.min()
        if L < 100: v = 1
        elif s < 70: v = 2
        else: v = 0
        if v != board[j, i]:
            mism += 1
            print("MISMATCH row", 19-j, "col", "ABCDEFGHJKLMNOPQRST"[i], "patch=", board[j,i], "annulus=", v, "L,s=", round(L), round(s))
print("total mismatches:", mism)
