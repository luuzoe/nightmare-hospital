from PIL import Image, ImageDraw
import math
def make_icon(S):
    img=Image.new('RGB',(S,S),(3,0,0))
    d=ImageDraw.Draw(img,'RGBA')
    cx,cy=S//2,S//2
    u=S/512.0  # scale unit
    # background: near-black with a faint red glow
    for i in range(10,0,-1):
        r=S*0.52*i/10
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(18+i*2,0,0,255))
    # HAIR: black mass behind the face (slightly bigger, so a dark rim frames it)
    d.ellipse([cx-165*u,cy-215*u,cx+165*u,cy+215*u],fill=(6,3,3,255))
    # jagged hair tips at the bottom
    for fx in [cx-140*u,cx-70*u,cx,cx+70*u,cx+140*u]:
        d.polygon([(fx-16*u,cy+180*u),(fx+16*u,cy+180*u),(fx,cy+225*u)],fill=(6,3,3,255))
    # FACE: pale gaunt oval
    d.ellipse([cx-140*u,cy-190*u,cx+140*u,cy+190*u],fill=(180,178,168,255))
    # soft shadow on the right side
    d.ellipse([cx+20*u,cy-180*u,cx+140*u,cy+180*u],fill=(140,138,130,255))
    # thin hair strands over the forehead
    for x0 in [cx-90*u,cx+80*u]:
        d.line([(x0,cy-185*u),(x0+6*u,cy-100*u)],fill=(6,3,3,255),width=max(4,int(6*u)))
    # BROWS: thin, slanted down toward the centre (angry)
    d.line([(cx-112*u,cy-152*u),(cx-32*u,cy-136*u)],fill=(0,0,0,255),width=max(5,int(8*u)))
    d.line([(cx+112*u,cy-152*u),(cx+32*u,cy-136*u)],fill=(0,0,0,255),width=max(5,int(8*u)))
    # EYES: two clearly separate hollow black sockets, red glint pupils
    for sx in (-1,1):
        exx=cx+sx*70*u; eyy=cy-70*u
        d.ellipse([exx-38*u,eyy-62*u,exx+38*u,eyy+62*u],fill=(0,0,0,255))
        d.ellipse([exx-6*u,eyy-22*u,exx+6*u,eyy-10*u],fill=(215,12,12,255))
        # blood drip from the eye
        d.polygon([(exx-9*u,eyy+58*u),(exx+9*u,eyy+58*u),(exx,eyy+108*u)],fill=(150,8,8,255))
        d.ellipse([exx-8*u,eyy+100*u,exx+8*u,eyy+116*u],fill=(150,8,8,255))
    # MOUTH: wide screaming oval, clearly below the eyes
    mx,my=cx,cy+92*u
    d.ellipse([mx-45*u,my-70*u,mx+45*u,my+70*u],fill=(0,0,0,255))
    # blood drip from the mouth
    d.polygon([(mx+30*u,my+60*u),(mx+42*u,my+60*u),(mx+36*u,my+100*u)],fill=(150,8,8,255))
    d.ellipse([mx+28*u,my+92*u,mx+44*u,my+108*u],fill=(150,8,8,255))
    # blood-red frame ring
    d.ellipse([7,7,S-7,S-7],outline=(170,8,8,255),width=9)
    return img
img512=make_icon(512); img512.save('icon-512.png')
img512.resize((192,192),Image.LANCZOS).save('icon-192.png')
print("saved icon-512 + icon-192")
