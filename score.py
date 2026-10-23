import numpy as np
from collections import deque
import pickle

board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
N = 19
cols = 'ABCDEFGHJKLMNOPQRST'
def name(j,i): return f"{cols[i]}{19-j}"

def neighbors(j,i):
    for dj,di in ((1,0),(-1,0),(0,1),(0,-1)):
        nj,ni = j+dj, i+di
        if 0 <= nj < N and 0 <= ni < N:
            yield nj,ni

seen = np.zeros((N,N), bool)
regions = []
for j in range(N):
    for i in range(N):
        if board[j,i]==0 and not seen[j,i]:
            q = deque([(j,i)]); seen[j,i]=True
            cells=[]; border=set()
            while q:
                cj,ci=q.popleft(); cells.append((cj,ci))
                for nj,ni in neighbors(cj,ci):
                    if board[nj,ni]==0:
                        if not seen[nj,ni]: seen[nj,ni]=True; q.append((nj,ni))
                    else:
                        border.add(board[nj,ni])
            regions.append((cells, border))

regions.sort(key=lambda r: -len(r[0]))
bt=wt=nt=0
print(f"{'size':>4}  {'owner':<6}  cells")
for cells,border in regions:
    if border == {1}: owner='BLACK'; bt+=len(cells)
    elif border == {2}: owner='WHITE'; wt+=len(cells)
    else: owner='neutral('+('B+W' if border=={1,2} else 'none')+')'; nt+=len(cells)
    if len(cells) >= 3:
        print(f"{len(cells):>4}  {owner:<6}  " + " ".join(name(*c) for c in cells[:40]) + (" ..." if len(cells)>40 else ""))

b_stones = int((board==1).sum()); w_stones = int((board==2).sum())
print()
print("black stones:", b_stones, " black territory:", bt, " => black area:", b_stones+bt)
print("white stones:", w_stones, " white territory:", wt, " => white area:", w_stones+wt)
print("neutral points:", nt)
print()
komi = 7.5
print("Chinese area scoring (area = stones + territory):")
print("  Black:", b_stones+bt, "  White:", w_stones+wt+komi, "(komi 7.5)")
print("  diff (Black - White):", round(b_stones+bt-(w_stones+wt+komi), 1))
