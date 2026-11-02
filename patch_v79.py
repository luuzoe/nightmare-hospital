import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
m = re.search(r"V78[^<]{0,80}", t)
assert m, "V78 label not found"
t = t.replace(m.group(0), "V79 PLACEHOLDER", 1)

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:120]}"
    t = t.replace(old, new, 1)

# collide(): 5th param skipFurniture — ghosts/monsters pass through low
# furniture (they are ghosts, and it avoids them getting stuck behind beds),
# while the player still collides with furniture (V78 fix preserved).
rep("function collide(x,z,r,allowStair){\n  for(const w of walls){\n    if(w.isDoor && w.doorOpen) continue;",
    "function collide(x,z,r,allowStair,skipFurniture){\n  for(const w of walls){\n    if(skipFurniture && w.isFurniture) continue;\n    if(w.isDoor && w.doorOpen) continue;")
rep("const nm=collide(monsterPos.x+dx/dl*mSpeed*dt, monsterPos.z+dz/dl*mSpeed*dt, 1.0);",
    "const nm=collide(monsterPos.x+dx/dl*mSpeed*dt, monsterPos.z+dz/dl*mSpeed*dt, 1.0, false, true);")
rep("const nm=collide(wg.outer.position.x+dx/dl*wg.def.speed*dt, wg.outer.position.z+dz/dl*wg.def.speed*dt, 1.0);",
    "const nm=collide(wg.outer.position.x+dx/dl*wg.def.speed*dt, wg.outer.position.z+dz/dl*wg.def.speed*dt, 1.0, false, true);")
# wandering chase movement (nm2) also skips furniture
i = t.index("const nm2=collide(wg.outer.position.x+cdx/cdl*")
j = t.index(";", i)
old_nm2 = t[i:j+1]
assert "1.0)" in old_nm2, old_nm2[:200]
new_nm2 = old_nm2.replace("1.0)", "1.0, false, true)", 1)
t = t.replace(old_nm2, new_nm2, 1)
# lineBlockedFine(): low furniture does not block sight (monster/ghost
# can see over a 0.7-1m bed/cabinet), and it cuts sight-check cost.
rep("for(const w of walls){ if(w.isDoor) continue;", "for(const w of walls){ if(w.isDoor || w.isFurniture) continue;")
# GPU: pixelRatio cap 1.5 -> 1.25 (~30% fewer pixels, smoother on phone)
rep("renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));", "renderer.setPixelRatio(Math.min(devicePixelRatio,1.25));")

p.write_text(t, encoding='utf-8')
print('V79 patch applied')
