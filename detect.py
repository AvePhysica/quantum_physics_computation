import numpy as np
from PIL import Image

im = Image.open(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\go_board.png").convert("RGB")
a = np.asarray(im).astype(float)

xs = np.array([23.5 + 56.25*k for k in range(19)])
ys = np.array([24.5 + (1037.5-24.5)/18*k for k in range(19)])

board = np.zeros((19,19), dtype=int)
data = []
r = 13
for j, y in enumerate(ys):
    for i, x in enumerate(xs):
        patch = a[int(y-r):int(y+r), int(x-r):int(x+r)].reshape(-1,3)
        med = np.median(patch, axis=0)
        L = float(med.mean()); s = float(med.max()-med.min())
        data.append((L, s, j, i))
        if L < 100: v = 1
        elif s < 70 and L > 190: v = 2
        else: v = 0
        board[j,i] = v

data.sort()
print("sorted (L,sat) samples every 12th:")
print([(round(d[0]),round(d[1])) for d in data[::12]])
print()
print("near-boundary cells (100<=L<=190 or 70<=sat<=90):")
for L,s,j,i in data:
    if (100 <= L <= 190) or (70 <= s <= 90) or (185 <= L <= 200 and s<80):
        print("  j,i", j, i, round(L,1), round(s,1))

print("black:", int((board==1).sum()), "white:", int((board==2).sum()))
sym = {0:'.',1:'X',2:'O'}
cols = 'ABCDEFGHJKLMNOPQRST'
print("   " + " ".join(cols))
for j in range(19):
    print(f"{19-j:2d} " + " ".join(sym[board[j,i]] for i in range(19)) + f" {19-j:2d}")
print("   " + " ".join(cols))
np.save(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy", board)
