import numpy as np
from collections import deque
from PIL import Image, ImageDraw

board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
N = 19

# BFS distance from each color's stones
def dist_map(color):
    D = np.full((N,N), 99, dtype=float)
    q = deque()
    for j in range(N):
        for i in range(N):
            if board[j,i]==color:
                D[j,i]=0; q.append((j,i))
    while q:
        cj,ci=q.popleft()
        for dj,di in ((1,0),(-1,0),(0,1),(0,-1)):
            nj,ni=cj+dj,ci+di
            if 0<=nj<N and 0<=ni<N and D[nj,ni]>D[cj,ci]+1:
                D[nj,ni]=D[cj,ci]+1; q.append((nj,ni))
    return D

Db = dist_map(1); Dw = dist_map(2)
inf = np.where(board==0, np.clip(Dw-Db, -8, 8), 0.0)

bt=wt=nt=0
terr = np.zeros((N,N), int)
for j in range(N):
    for i in range(N):
        if board[j,i]!=0: continue
        v = inf[j,i]
        if v >= 2: terr[j,i]=1; bt+=1
        elif v <= -2: terr[j,i]=2; wt+=1
        else: nt+=1
print("influence-based (margin>=2): black terr", bt, "white terr", wt, "neutral", nt)
b=(board==1).sum(); w=(board==2).sum()
print("black area", b+bt, "white area", w+wt, "+komi7.5 =", w+wt+7.5, " -> diff", b+bt-(w+wt+7.5))

# quadrant balance: stones+estimated territory per quadrant
print()
regions = {"top-left(rows19-10,A-J)":(0,10,0,9), "top-right(rows19-10,K-T)":(0,10,9,19),
           "bottom-left(rows9-1,A-J)":(10,19,0,9), "bottom-right(rows9-1,K-T)":(10,19,9,19)}
for nm,(r0,r1,c0,c1) in regions.items():
    bs=int((board[r0:r1,c0:c1]==1).sum()); ws=int((board[r0:r1,c0:c1]==2).sum())
    tb=int((terr[r0:r1,c0:c1]==1).sum()); tw=int((terr[r0:r1,c0:c1]==2).sum())
    print(f"{nm:32s} B stones {bs:2d} terr {tb:2d} | W stones {ws:2d} terr {tw:2d}")

# picture
img = Image.new("RGB",(19*40+40, 19*40+40),(232,200,130))
d = ImageDraw.Draw(img)
for j in range(N):
    for i in range(N):
        x = 20+40*i; y = 20+40*j
        d.line([(x,20),(x,20+38*40)],fill=(150,120,80))
        d.line([(20,y),(20+38*40,y)],fill=(150,120,80))
for j in range(N):
    for i in range(N):
        x = 20+40*i; y = 20+40*j
        if board[j,i]==1: d.ellipse([x-17,y-17,x+17,y+17],fill=(20,20,20))
        elif board[j,i]==2: d.ellipse([x-17,y-17,x+17,y+17],fill=(250,248,240),outline=(120,120,120))
        elif terr[j,i]==1: d.ellipse([x-4,y-4,x+4,y+4],fill=(40,40,40))
        elif terr[j,i]==2: d.ellipse([x-4,y-4,x+4,y+4],fill=(255,255,255),outline=(0,0,0))
img.save(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\influence.png")
print("saved influence.png")
