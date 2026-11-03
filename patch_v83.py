import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V82[^<]{0,80}", t)
assert m, "V82 label not found"
t = t.replace(m.group(0), "V83 PLACEHOLDER", 1)

# Broken chairs: static, visual-only before. Add a small furniture collider
# so the player stops before the chair instead of walking into it and
# having the camera clip inside the dark chair mesh.
rep("function brokenChair(x,z,ry){ const g=new THREE.Group(); const seat=new THREE.Mesh(new THREE.BoxGeometry(0.55,0.08,0.55), new THREE.MeshStandardMaterial({color:0x1a1a1a})); seat.position.y=0.25; const back=new THREE.Mesh(new THREE.BoxGeometry(0.55,0.6,0.08), seat.material); back.position.set(0,0.5,-0.25); g.add(seat,back); g.position.set(x,0.12,z); g.rotation.set(0,ry,1.35); scene.add(g); }",
    "function brokenChair(x,z,ry){ const g=new THREE.Group(); const seat=new THREE.Mesh(new THREE.BoxGeometry(0.55,0.08,0.55), new THREE.MeshStandardMaterial({color:0x1a1a1a})); seat.position.y=0.25; const back=new THREE.Mesh(new THREE.BoxGeometry(0.55,0.6,0.08), seat.material); back.position.set(0,0.5,-0.25); g.add(seat,back); g.position.set(x,0.12,z); g.rotation.set(0,ry,1.35); scene.add(g); if(typeof walls!=='undefined') walls.push({x:x,z:z,w:0.7,d:0.7,isFurniture:true}); }")

# Real GLB wheelchairs: static placeAsset instances. Add colliders for
# the same 4 positions, right after their placement loop.
rep("for(const [wx,wz] of [[-50,0],[50,0],[-47,-22],[43,22]]) placeAsset('wheelchair-real.glb',1.0,0.34,wx,0,wz,0.6,0);",
    "for(const [wx,wz] of [[-50,0],[50,0],[-47,-22],[43,22]]) placeAsset('wheelchair-real.glb',1.0,0.34,wx,0,wz,0.6,0);\n  if(typeof walls!=='undefined'){ for(const [wx,wz] of [[-50,0],[50,0],[-47,-22],[43,22]]) walls.push({x:wx,z:wz,w:0.8,d:0.8,isFurniture:true}); }")

p.write_text(t, encoding='utf-8')
print('V83 patch applied')
