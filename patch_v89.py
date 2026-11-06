import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V88[^<]{0,80}", t)
assert m, "V88 label not found"
t = t.replace(m.group(0), "V89 PLACEHOLDER", 1)

# Real scanned woman's hand replaces the MakeHuman hand (bbox Z ~24 units -> scale 0.008 = ~0.19 m)
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1.15,1.15,1.15);",
    "handLoader.load('hand-woman.glb', g=>{ const inner=g.scene; inner.scale.set(0.008,0.008,0.008);")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1.15,1.15,1.15);",
    "handLoader.load('hand-woman.glb', g=>{ const inner=g.scene; inner.scale.set(-0.008,0.008,0.008);")

# Real textured flashlight replaces the code cylinder + lens
rep("const flashBody=new THREE.Mesh(new THREE.CylinderGeometry(0.022,0.026,0.14,12), new THREE.MeshStandardMaterial({color:0x1a1a1a,roughness:0.4,metalness:0.3})); flashBody.rotation.x=Math.PI/2; flashMeshGroup.add(flashBody);\nconst flashLens=new THREE.Mesh(new THREE.CircleGeometry(0.02,12), new THREE.MeshBasicMaterial({color:0xfff2cc})); flashLens.position.set(0,0,-0.075); flashLens.rotation.y=Math.PI; flashMeshGroup.add(flashLens);",
    "const flashLoader=new GLTFLoader(); flashLoader.load('flashlight-real.glb', g=>{ const inner=g.scene; inner.scale.set(0.000125,0.000125,0.000125); flashMeshGroup.add(inner); }, undefined, ()=>{});")

p.write_text(t, encoding='utf-8')
print('V89 patch applied')
