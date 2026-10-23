import numpy as np
from PIL import Image, ImageDraw, ImageFont

board = np.load(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board.npy")
N=19
COLS='ABCDEFGHJKLMNOPQRST'
SGF='abcdefghijklmnopqrs'

# ---------- SGF ----------
ab=[]; aw=[]
for j in range(N):
    for i in range(N):
        p = SGF[i]+SGF[j]
        if board[j,i]==1: ab.append(p)
        elif board[j,i]==2: aw.append(p)
sgf = "(;GM[1]FF[4]CA[UTF-8]SZ[19]KM[7.5]RU[Chinese]\n"
sgf += "C[Position read from image. Black 70 / White 69. Black's last move: L7 (triangle) -> puts White M7N7 in atari. White to play. Warning: the position has no settled territory and no eyes at all, which is not typical of a real game record.]\n"
sgf += "AB" + "".join("["+p+"]" for p in ab) + "\n"
sgf += "AW" + "".join("["+p+"]" for p in aw) + "\n"
sgf += "PL[W]\n)\n"
open(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board_position.sgf","w",encoding="utf-8").write(sgf)

# ---------- diagram ----------
S = 44; M = 56
Wp = Hp = M*2 + S*18
img = Image.new("RGB",(Wp,Hp),(238,206,138))
d = ImageDraw.Draw(img)
def X(i): return M + S*i
def Y(j): return M + S*j
for k in range(N):
    d.line([(X(0),Y(k)),(X(18),Y(k))], fill=(120,90,50), width=2)
    d.line([(X(k),Y(0)),(X(k),Y(18))], fill=(120,90,50), width=2)
for (jj,ii) in [(3,3),(3,15),(15,3),(15,15),(9,9)]:
    d.ellipse([X(ii)-5,Y(jj)-5,X(ii)+5,Y(jj)+5], fill=(120,90,50))
R = 19
last = (12,10)  # L7
for j in range(N):
    for i in range(N):
        if board[j,i]==0: continue
        if board[j,i]==1:
            d.ellipse([X(i)-R,Y(j)-R,X(i)+R,Y(j)+R], fill=(28,28,28), outline=(0,0,0))
        else:
            d.ellipse([X(i)-R,Y(j)-R,X(i)+R,Y(j)+R], fill=(248,245,236), outline=(150,150,150))
if board[last]==1:
    j,i = last
    d.polygon([(X(i)-11,Y(j)+7),(X(i)+7,Y(j)+7),(X(i)-2,Y(j)-9)], fill=(255,255,255))
try:
    font = ImageFont.truetype("arial.ttf", 20)
except Exception:
    font = ImageFont.load_default()
for i in range(N):
    d.text((X(i)-7, Hp-M+10), COLS[i], fill=(60,40,20), font=font)
    d.text((X(i)-7, M-32), COLS[i], fill=(60,40,20), font=font)
for j in range(N):
    t = str(19-j)
    d.text((M-38, Y(j)-11), t, fill=(60,40,20), font=font)
    d.text((Wp-M+14, Y(j)-11), t, fill=(60,40,20), font=font)
img.save(r"C:\Users\33552\Desktop\物理\计算\量子计算方法\board_readout.png")
print("black",len(ab),"white",len(aw))
print("sgf written")
