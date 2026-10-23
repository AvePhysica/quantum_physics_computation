import numpy as np
from collections import deque
import pickle

board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
N=19
cols='ABCDEFGHJKLMNOPQRST'
def name(j,i): return f"{cols[i]}{19-j}"
def nbrs(j,i):
    for dj,di in ((1,0),(-1,0),(0,1),(0,-1)):
        nj,ni=j+dj,i+di
        if 0<=nj<N and 0<=ni<N: yield nj,ni

groups = pickle.load(open(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\groups.pkl","rb"))

rows=[]
for color, stones, libs in groups:
    # true eyes: liberty points whose all orthogonal neighbours are the group color or off-board
    eyes=[]
    sset=set(stones)
    for (lj,li) in libs:
        if all((nj,ni) in sset for nj,ni in nbrs(lj,li)):
            eyes.append((lj,li))
    rows.append((len(stones), len(libs), len(eyes), 'B' if color==1 else 'W', stones))

rows.sort(key=lambda r:(r[1], -r[0]))
print(f"{'col':1} {'size':>4} {'libs':>4} {'eyes':>4}  stones")
for size,libs,eyes,c,stones in rows:
    if libs<=4:
        print(f"{c:1} {size:4d} {libs:4d} {eyes:4d}  " + " ".join(name(*s) for s in stones))
print()
print("summary by color: total groups, total stones, groups with libs<=2, groups with libs<=3")
for c,lab in ((1,'B'),(2,'W')):
    gs=[r for r in rows if r[3]==lab]
    print(lab, "groups", len(gs), "stones", sum(r[0] for r in gs),
          "libs<=2:", sum(1 for r in gs if r[1]<=2), "libs==3:", sum(1 for r in gs if r[1]==3),
          "no-eye groups:", sum(1 for r in gs if r[2]==0))
print()
print("big groups (>=5 stones) detail:")
for size,libs,eyes,c,stones in rows:
    if size>=5:
        print(f"  {c} size {size:2d} libs {libs:2d} eyes {eyes}  first stones: " + " ".join(name(*s) for s in stones[:6]))
