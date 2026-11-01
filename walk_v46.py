import math
from collections import deque

# V46 spec walls, same as index.html
walls = []  # (x,z,w,d,isDoor)
def add(x,z,w,d,isDoor=False):
    walls.append((x,z,w,d,isDoor))
# outer
add(0,-23,114.6,0.6); add(0,23,114.6,0.6)
add(-57,-13,0.6,20); add(-57,13,0.6,20); add(57,-13,0.6,20); add(57,13,0.6,20)
NORTH_C=[-52,-42,-32,-22,-12,2,12,22,32,42,52]
NORTH_B=[-57,-47,-37,-27,-17,-7,-3,7,17,27,37,47,57]
SOUTH_C=[-52,-42,-32,-22,-12,-2,8,18,28,38,48]
SOUTH_B=[-57,-47,-37,-27,-17,-7,3,13,23,33,43,53,57]
NORTH_R=[(-57,-47),(-47,-37),(-37,-27),(-27,-17),(-17,-7),(-3,7),(7,17),(17,27),(27,37),(37,47),(47,57)]
for i,dc in enumerate(NORTH_C):
    L,R=NORTH_R[i]
    if dc-1>L: add((L+dc-1)/2,-3,dc-1-L,0.6)
    if dc+1<R: add((dc+1+R)/2,-3,R-dc-1,0.6)
for i,dc in enumerate(SOUTH_C):
    L,R=SOUTH_B[i],SOUTH_B[i+1]
    if dc-1>L: add((L+dc-1)/2,3,dc-1-L,0.6)
    if dc+1<R: add((dc+1+R)/2,3,R-dc-1,0.6)
for i in range(1,len(NORTH_B)-1): add(NORTH_B[i],-13,0.6,20)
for i in range(1,len(SOUTH_B)-1): add(SOUTH_B[i],13,0.6,20)
doors=[]
for dc in NORTH_C: doors.append((dc,-3))
for dc in SOUTH_C: doors.append((dc,3))
for dc,z in doors: add(dc,z,2,0.6,True)
# entrance block west
add(-57,0,0.6,6)
print("walls", len(walls), "doors", len(doors))

def collide(x,z,r,open_doors):
    # game collide: push out of wall rects, door assist for corridor walls
    for (wx,wz,ww,wd,isDoor) in walls:
        if isDoor and (wx,wz) in open_doors: continue
        if not isDoor and wz in (-3,3):
            near=False
            for (dx,dz) in open_doors:
                if dz==wz and abs(x-dx)<1.3: near=True; break
            if near: continue
        nx=max(wx-ww/2, min(x, wx+ww/2)); nz=max(wz-wd/2, min(z, wz+wd/2))
        dx=x-nx; dz=z-nz; dd=dx*dx+dz*dz
        if dd<r*r:
            if dd==0: x+=r; continue
            dist=math.sqrt(dd); x=nx+dx/dist*r; z=nz+dz/dist*r
    x=max(-56,min(56,x)); z=max(-22,min(22,z))
    return x,z

def door_rect_dist(px,pz,dx,dz):
    return math.hypot(max(abs(px-dx)-1.0,0), abs(pz-dz))

def walk_to(sx,sz,tx,tz):
    # BFS on 0.5m grid, walkable if collide does not push >0.1m, doors treated passable
    # then step walk following BFS path with exact collide + door open logic
    def key(x,z): return (round(x*2), round(z*2))
    # BFS
    start=key(sx,sz); goal=key(tx,tz)
    q=deque([start]); prev={start:None}
    def walkable(gx,gz):
        x=gx/2; z=gz/2
        # check collide with all doors open (passable)
        cx,cz=collide(x,z,0.45,set(doors))
        return math.hypot(cx-x,cz-z)<0.2
    if not walkable(*start): print("  start not walkable", sx,sz)
    found=False
    while q:
        cur=q.popleft()
        if cur==goal: found=True; break
        for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]:
            nb=(cur[0]+dx,cur[1]+dz)
            if nb in prev: continue
            if not (-114 <= nb[0] <= 114 and -46 <= nb[1] <= 46): continue
            if not walkable(*nb): continue
            prev[nb]=cur; q.append(nb)
    if not found:
        print("  BFS NO PATH", (sx,sz),"->",(tx,tz)); return None
    path=[]; cur=goal
    while cur: path.append((cur[0]/2,cur[1]/2)); cur=prev[cur]
    path.reverse()
    # step walk: follow path points, with door open logic
    px,pz=sx,sz; steps=0; dist=0
    for (wx,wz) in path[1:]:
        # move toward waypoint in small steps
        for _ in range(20):
            dx=wx-px; dz=wz-pz; d=math.hypot(dx,dz)
            if d<0.1: break
            step= min(0.5, d)
            nx=px+dx/d*step; nz=pz+dz/d*step
            # update open doors by rect distance <4m (game logic)
            open_doors=set()
            for (dxd,dzd) in doors:
                if door_rect_dist(nx,nz,dxd,dzd)<4: open_doors.add((dxd,dzd))
            cx,cz=collide(nx,nz,0.45,open_doors)
            dist+=math.hypot(cx-px,cz-pz); px,pz=cx,cz; steps+=1
            if steps>5000: break
        if steps>5000: break
    endd=math.hypot(px-tx,pz-tz)
    print(f"  walk {(sx,sz)} -> {(tx,tz)}: BFS steps {len(path)} ({len(path)*0.5:.1f}m grid), walk steps {steps}, walked {dist:.1f}m, end {px:.1f},{pz:.1f} dist to target {endd:.2f}m {'TAKEABLE' if endd<3.0 else 'FAIL'}")
    return endd<3.0

print("Ep1 keys, nearest-first from west spawn (-54,0):")
ok=True
ok &= walk_to(-54,0,-32,-12)  # Key1 north room3
ok &= walk_to(-32,-12,-12,12) # Key2 south room5 (exit north room, corridor, enter south room)
ok &= walk_to(-12,12,32,-12)  # Key3 north room9
print("Staircase hall entry: corridor (-5,0) -> hall (-5,-13):")
ok &= walk_to(-5,0,-5,-13)
print("Staircase hall exit back to corridor:")
ok &= walk_to(-5,-13,-5,0)
print("ALL OK" if ok else "SOME FAILED")
