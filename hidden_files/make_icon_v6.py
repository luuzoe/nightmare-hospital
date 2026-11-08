from PIL import Image, ImageDraw
import math
def make_icon(S):
    img=Image.new('RGB',(S,S),(8,1,1))
    d=ImageDraw.Draw(img,'RGBA')
    cx,cy=S//2,S//2
    for i in range(12,0,-1):
        r=S*0.52*i/12
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(40+i*3,2,2,255))
    cw=S*0.16; ch=S*0.62
    d.rectangle([cx-cw//2,cy-ch//2,cx+cw//2,cy+ch//2],fill=(110,8,8,255))
    d.rectangle([cx-ch//2,cy-cw//2,cx+ch//2,cy+cw//2],fill=(110,8,8,255))
    d.line([cx-cw//2,cy-ch//2+40,cx+cw//2,cy+20],fill=(20,0,0,255),width=4)
    d.line([cx+cw//2,cy-ch//2+80,cx-cw//2,cy+60],fill=(20,0,0,255),width=3)
    gw=S*0.56; gh=S*0.66
    gx0=cx-gw/2; gx1=cx+gw/2; gy0=cy-gh/2; gy1=cy+gh/2
    pts=[(gx0,gy1-40),(gx0,gy0+gw*0.28)]
    for a in range(180,361,10):
        rad=math.radians(a)
        pts.append((cx+math.cos(rad)*gw/2, gy0+gw*0.28+math.sin(rad)*gw*0.28))
    pts.append((gx1,gy1-40))
    pts.append((gx1-gw*0.18,gy1));pts.append((cx+gw*0.08,gy1-55));pts.append((cx-gw*0.05,gy1));pts.append((gx0+gw*0.18,gy1-45))
    glow=[(x,y+14) for x,y in pts]
    d.polygon(glow,fill=(90,5,5,255))
    d.polygon(pts,fill=(213,213,204,255))
    ex=S*0.13; ey=S*0.20
    d.ellipse([cx-ex*1.6,cy-ey*0.55,cx-ex*0.6,cy+ey*0.55],fill=(0,0,0,255))
    d.ellipse([cx+ex*0.6,cy-ey*0.55,cx+ex*1.6,cy+ey*0.55],fill=(0,0,0,255))
    mw=S*0.09; mh=S*0.16
    d.ellipse([cx-mw,cy+ey*0.75,cx+mw,cy+ey*0.75+mh],fill=(0,0,0,255))
    for sx in (-1,1):
        exx=cx+sx*ex*1.1
        d.polygon([(exx-10,cy+ey*0.55),(exx+10,cy+ey*0.55),(exx,cy+ey*0.55+S*0.14)],fill=(150,10,10,255))
        d.ellipse([exx-8,cy+ey*0.55+S*0.12,exx+8,cy+ey*0.55+S*0.12+16],fill=(150,10,10,255))
    d.polygon([(cx+mw*0.5,cy+ey*0.75+mh),(cx+mw*0.5+14,cy+ey*0.75+mh),(cx+mw*0.5+7,cy+ey*0.75+mh+S*0.08)],fill=(150,10,10,255))
    d.line([gx0+30,gy0+gw*0.3,gx0+90,gy0+gw*0.3+70],fill=(60,60,55,255),width=3)
    d.ellipse([8,8,S-8,S-8],outline=(180,10,10,255),width=10)
    return img
img512=make_icon(512); img512.save('icon-512.png')
img512.resize((192,192),Image.LANCZOS).save('icon-192.png')
print("icons done")
