import math
from collections import deque
walls=[]
def add(x,z,w,d,isDoor=False): walls.append((x,z,w,d,isDoor))
add(0,-30,169.6,0.6); add(0,30,169.6,0.6)
add(-84.5,-17.5,0.6,25); add(-84.5,17.5,0.6,25); add(84.5,-17.5,0.6,25); add(84.5,17.5,0.6,25)
NC=[-77,-62,-47,-32,-17,2,17,32,47,62,77]; NR=[(-84.5,-69.5),(-69.5,-54.5),(-54.5,-39.5),(-39.5,-24.5),(-24.5,-9.5),(-5.5,9.5),(9.5,24.5),(24.5,39.5),(39.5,54.5),(54.5,69.5),(69.5,84.5)]
SC=[-77,-62,-47,-32,-17,-2,13,28,43,58,73]; SB=[-84.5,-69.5,-54.5,-39.5,-24.5,-9.5,5.5,20.5,35.5,50.5,65.5,80.5,84.5]
for i,dc in enumerate(NC):
    L,R=NR[i]
    if dc-1.25>L: add((L+dc-1.25)/2,-5,dc-1.25-L,0.6)
    if dc+1.25<R: add((dc+1.25+R)/2,-5,R-dc-1.25,0.6)
for i,dc in enumerate(SC):
    L,R=SB[i],SB[i+1]
    if dc-1.25>L: add((L+dc-1.25)/2,5,dc-1.25-L,0.6)
    if dc+1.25<R: add((dc+1.25+R)/2,5,R-dc-1.25,0.6)
for bx in [-69.5,-54.5,-39.5,-24.5,-9.5,-5.5,9.5,24.5,39.5,54.5,69.5]: add(bx,-17.5,0.6,25)
for bx in [-69.5,-54.5,-39.5,-24.5,-9.5,5.5,20.5,35.5,50.5,65.5,80.5]: add(bx,17.5,0.6,25)
doors=[]
for dc in NC: doors.append((dc,-5))
for dc in SC: doors.append((dc,5))
for dc,z in doors: add(dc,z,2.5,0.6,True)
add(-84.5,0,0.6,10)
print("walls",len(walls),"doors",len(doors))
def collide(x,z,r,open_doors):
    for (wx,wz,ww,wd,isDoor) in walls:
        if isDoor and (wx,wz) in open_doors: continue
        if not isDoor and wz in (-5,5):
            if any(dz==wz and abs(x-dx)<1.5 for dx,dz in open_doors): continue
        nx=max(wx-ww/2,min(x,wx+ww/2)); nz=max(wz-wd/2,min(z,wz+wd/2)); dx=x-nx; dz=z-nz; dd=dx*dx+dz*dz
        if dd<r*r:
            if dd==0: x+=r; continue
            dist=math.sqrt(dd); x=nx+dx/dist*r; z=nz+dz/dist*r
    return max(-83,min(83,x)), max(-29,min(29,z))
def walk_to(sx,sz,tx,tz):
    def key(x,z): return (round(x*2),round(z*2))
    start,goal=key(sx,sz),key(tx,tz); q=deque([start]); prev={start:None}
    def walkable(gx,gz):
        cx,cz=collide(gx/2,gz/2,0.45,set(doors)); return math.hypot(cx-gx/2,cz-gz/2)<0.2
    found=False
    while q:
        cur=q.popleft()
        if cur==goal: found=True; break
        for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
            nb=(cur[0]+dx,cur[1]+dz)
            if nb in prev or not (-169<=nb[0]<=169 and -60<=nb[1]<=60): continue
            if not walkable(*nb): continue
            prev[nb]=cur; q.append(nb)
    if not found: print("  NO PATH", (sx,sz),"->",(tx,tz)); return False
    path=[]; cur=goal
    while cur: path.append((cur[0]/2,cur[1]/2)); cur=prev[cur]
    path.reverse(); px,pz=sx,sz; steps=0; dist=0
    for wx,wz in path[1:]:
        for _ in range(20):
            dx,dy=wx-px,wz-pz; d=math.hypot(dx,dy)
            if d<0.1: break
            step=min(0.5,d); nx,nz=px+dx/d*step,pz+dy/d*step
            open_doors=set((dxd,dzd) for dxd,dzd in doors if math.hypot(max(abs(nx-dxd)-1.25,0),abs(nz-dzd))<4)
            cx,cz=collide(nx,nz,0.45,open_doors); dist+=math.hypot(cx-px,cz-pz); px,pz=cx,cz; steps+=1
    endd=math.hypot(px-tx,pz-tz); print(f"  {(sx,sz)} -> {(tx,tz)}: BFS {len(path)*0.5:.1f}m, walked {dist:.1f}m, end dist {endd:.2f}m {'TAKEABLE' if endd<3 else 'FAIL'}"); return endd<3
ok=True
ok&=walk_to(-81,0,-47,-16)
ok&=walk_to(-47,-16,-17,16)
ok&=walk_to(-17,16,47,-16)
ok&=walk_to(-7.5,0,-7.5,-17.5)
ok&=walk_to(-7.5,-17.5,-7.5,0)
print("ALL OK" if ok else "SOME FAILED")
