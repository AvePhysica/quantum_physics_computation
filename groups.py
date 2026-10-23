import numpy as np
from collections import deque

board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
N = 19
cols = 'ABCDEFGHJKLMNOPQRST'
def name(j, i):
    return f"{cols[i]}{19-j}"

def neighbors(j,i):
    for dj,di in ((1,0),(-1,0),(0,1),(0,-1)):
        nj,ni = j+dj, i+di
        if 0 <= nj < N and 0 <= ni < N:
            yield nj,ni

# groups and liberties
seen = np.zeros((N,N), bool)
groups = []
for j in range(N):
    for i in range(N):
        if board[j,i] != 0 and not seen[j,i]:
            color = board[j,i]
            q = deque([(j,i)]); seen[j,i] = True
            stones = []; libs = set()
            while q:
                cj,ci = q.popleft(); stones.append((cj,ci))
                for nj,ni in neighbors(cj,ci):
                    if board[nj,ni] == 0: libs.add((nj,ni))
                    elif board[nj,ni] == color and not seen[nj,ni]:
                        seen[nj,ni] = True; q.append((nj,ni))
            groups.append((color, stones, libs))

print("total groups:", len(groups))
print()
print("groups with 0 liberties (illegal):")
for color, stones, libs in groups:
    if len(libs) == 0:
        print("  ", "B" if color==1 else "W", len(stones), [name(*s) for s in stones])
print()
print("groups in atari (1 liberty):")
for color, stones, libs in sorted(groups, key=lambda g: len(g[2])):
    if len(libs) == 1:
        print("  ", "B" if color==1 else "W", len(stones), [name(*s) for s in stones], "-> lib", [name(*l) for l in libs])
print()
sizes = sorted([(len(s), c) for c,s,l in groups], reverse=True)
print("largest groups:", [(n, "B" if c==1 else "W") for n,c in sizes[:12]])
print("num black groups:", sum(1 for c,s,l in groups if c==1), " num white groups:", sum(1 for c,s,l in groups if c==2))
import pickle
pickle.dump(groups, open(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\groups.pkl","wb"))
