import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V85[^<]{0,80}", t)
assert m, "V85 label not found"
t = t.replace(m.group(0), "V86 PLACEHOLDER", 1)

# New wandering ghost: Shazia, realistic 3D scan, white hooded dress,
# CC-BY, 50k tris. Bbox Y 0.88 (tallest) -> standing; scale 1.6 * 1.25
# = 2.0 effective -> 1.76m tall; yOffset 0.9 puts feet on the floor.
rep("    {name:'Scary Halloween Ghost', src:'scary-halloween-ghost.glb', real:true, scale:0.6, yOffset:1.0, pos:[-40,0], wps:[[-40,0],[-20,0],[0,0],[-40,0]], speed:3.9, radius:13, floatY:0.2, chaseTime:8, sound:'growl'},",
    "    {name:'Scary Halloween Ghost', src:'scary-halloween-ghost.glb', real:true, scale:0.6, yOffset:1.0, pos:[-40,0], wps:[[-40,0],[-20,0],[0,0],[-40,0]], speed:3.9, radius:13, floatY:0.2, chaseTime:8, sound:'growl'},\n    {name:'Shazia Ghost', src:'shazia-ghost.glb', real:true, scale:1.6, yOffset:0.9, pos:[-35,-12], wps:[[-35,-12],[-20,-12],[0,0],[-35,0]], speed:3.6, radius:13, floatY:0.2, chaseTime:8, sound:'scream'},")

# Shazia is always active, like the other new ghosts.
rep("const newNames=['Cloth Ghost','A-Pose Ghost Woman','Scary Halloween Ghost'];",
    "const newNames=['Cloth Ghost','A-Pose Ghost Woman','Scary Halloween Ghost','Shazia Ghost'];")

# Real corpse: replace the CesiumMan fallback slot (index 5) with the
# Sketchfab Dead Body (CC-BY, 16.4k tris). Bbox lying flat: Z 3.16 long,
# X 2.0 wide, Y 0.56 tall; scale 0.55 -> 1.74m long, 0.31m tall.
rep("    {src:'cesium-man.glb',scale:PLAYER_BASE,real:false},",
    "    {src:'dead-body-real.glb',scale:0.55,ox:0,oy:0.05,oz:0,real:true},")

p.write_text(t, encoding='utf-8')
print('V86 patch applied')
