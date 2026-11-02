import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
m = re.search(r"V73[^<]{0,80}", t)
assert m, "V73 label not found"
t = t.replace(m.group(0), "V74 \u2022 \u1014\u1002\u1036\u101b\u1036 + \u1010\u1036\u1004\u103a\u1021\u1038\u1038 \u101e\u1031\u1038\u1021\u1031\u102c\u1004\u103a \u2014 \u1021\u1000\u102f\u1014\u103a", 1)

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:100]}"
    t = t.replace(old, new, 1)

# --- Wall texture: plainer, darker, less repeating ---
rep("g.fillStyle='#5a5a52';", "g.fillStyle='#4a4a44';")
rep("if(Math.random()<0.35){", "if(Math.random()<0.18){")
rep("g.fillStyle=y<2?'#6e7266':'#4e524a';", "g.fillStyle=y<2?'#5a5e54':'#42463e';")
rep("g.fillStyle='rgba(200,190,170,.35)'; for(let i=0;i<16;i++)", "g.fillStyle='rgba(200,190,170,.25)'; for(let i=0;i<7;i++)")
rep("g.fillStyle='rgba(20,35,20,.5)'; for(let i=0;i<14;i++)", "g.fillStyle='rgba(20,35,20,.4)'; for(let i=0;i<8;i++)")
rep("g.fillStyle='rgba(40,30,20,.35)'; for(let i=0;i<30;i++)", "g.fillStyle='rgba(40,30,20,.35)'; for(let i=0;i<15;i++)")
rep("g.fillStyle='rgba(90,70,40,.3)'; for(let i=0;i<10;i++)", "g.fillStyle='rgba(90,70,40,.3)'; for(let i=0;i<6;i++)")
# wallTex repeat 6,2 -> 2,1 (must be unique to wallTex block; check by context)
wall_idx = t.index("const wallTex=makeTex")
wall_end = t.index("const ceilTex=", wall_idx)
wall_block = t[wall_idx:wall_end]
assert wall_block.count("},6,2);") == 1, "wall repeat not unique"
t = t[:wall_idx] + wall_block.replace("},6,2);", "},2,1);", 1) + t[wall_end:]

# --- Room doors: 2.5 x 3.2 -> 1.4 x 2.2, with visual header above ---
rep("const mesh=new THREE.Mesh(new THREE.BoxGeometry(2.5,3.2,0.3), new THREE.MeshStandardMaterial({color:0x4a1515,roughness:.85,emissive:0x220000}));\n  mesh.position.set(dc,1.6,z); scene.add(mesh);",
    "const mesh=new THREE.Mesh(new THREE.BoxGeometry(1.4,2.2,0.3), new THREE.MeshStandardMaterial({color:0x4a1515,roughness:.85,emissive:0x220000}));\n  mesh.position.set(dc,1.1,z); scene.add(mesh);\n  const header=new THREE.Mesh(new THREE.BoxGeometry(1.4,1.2,0.6), new THREE.MeshStandardMaterial({map:wallTex,roughness:.95})); header.position.set(dc,2.8,z); scene.add(header);")
rep("const w={x:dc,z,w:2.5,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};",
    "const w={x:dc,z,w:1.4,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};")
# Corridor wall segments: gap 2.5 (±1.25) -> 1.4 (±0.7), north and south, both sides
rep("if(dc-1.25>left) addWall((left+dc-1.25)/2,-5,dc-1.25-left,0.6);",
    "if(dc-0.7>left) addWall((left+dc-0.7)/2,-5,dc-0.7-left,0.6);")
rep("if(dc+1.25<right) addWall((dc+1.25+right)/2,-5,right-dc-1.25,0.6);",
    "if(dc+0.7<right) addWall((dc+0.7+right)/2,-5,right-dc-0.7,0.6);")
rep("if(dc-1.25>left) addWall((left+dc-1.25)/2,5,dc-1.25-left,0.6);",
    "if(dc-0.7>left) addWall((left+dc-0.7)/2,5,dc-0.7-left,0.6);")
rep("if(dc+1.25<right) addWall((dc+1.25+right)/2,5,right-dc-1.25,0.6);",
    "if(dc+0.7<right) addWall((dc+0.7+right)/2,5,right-dc-0.7,0.6);")
# Door slide distance matches new width
rep("dw.mesh.position.x=dw.closedX+dw.anim*2.5;", "dw.mesh.position.x=dw.closedX+dw.anim*1.4;")

p.write_text(t, encoding='utf-8')
print('V74 patch applied')
