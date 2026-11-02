import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
m = re.search(r"V77[^<]{0,80}", t)
assert m, "V77 label not found"
t = t.replace(m.group(0), "V78 PLACEHOLDER", 1)

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:120]}"
    t = t.replace(old, new, 1)

# V78: solid room furniture gets collision (walls array = collide()).
# addProp already records x,z,w,d in props[]; push the same box to walls[]
# for solid labels only. Excluded: debris/rubble (floor rubble, walk-over),
# lockers (hide spots must stay reachable), corpses (flat on floor),
# small/moving props (IV, syringe, poltergeist, dash) which are not addProp.
rep("function addProp(cx,cz,w,d,h,color,label){\n  const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), new THREE.MeshStandardMaterial({color,roughness:.9}));\n  m.position.set(cx,h/2,cz); scene.add(m); props.push({x:cx,z:cz,w,d,label,mesh:m,ox:cx,oz:cz}); return m;\n}",
    "function addProp(cx,cz,w,d,h,color,label){\n  const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), new THREE.MeshStandardMaterial({color,roughness:.9}));\n  m.position.set(cx,h/2,cz); scene.add(m); props.push({x:cx,z:cz,w,d,label,mesh:m,ox:cx,oz:cz}); if(['bed','surgery','cabinet','desk','shelf','slab','bed2','cabinet2','desk2','shelf2','partition','roomprop'].includes(label) && typeof walls!=='undefined') walls.push({x:cx,z:cz,w,d,isFurniture:true}); return m;\n}")

p.write_text(t, encoding='utf-8')
print('V78 patch applied')
