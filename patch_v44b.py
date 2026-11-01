import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
miss = []
def rep(old, new, name):
    global t
    if old not in t:
        miss.append(name); print('MISS:', name)
    else:
        t = t.replace(old, new, 1); print('OK:', name)

rep("// Door gap = centre +-1 (2m wide). Room dividing walls at each boundary, north z-24..-3, south z3..24.",
    "// Door gap = centre +-1.5 (3m wide, so BFS 1m grid + 0.6 margin always finds a cell through the door). Room dividing walls at each boundary, north z-24..-3, south z3..24.",
    "door gap comment")
rep("""    if(dc-1>left) addWall((left+dc-1)/2,z,dc-1-left,0.6);
    if(dc+1<right) addWall((dc+1+right)/2,z,right-dc-1,0.6);""",
    """    if(dc-1.5>left) addWall((left+dc-1.5)/2,z,dc-1.5-left,0.6);
    if(dc+1.5<right) addWall((dc+1.5+right)/2,z,right-dc-1.5,0.6);""",
    "door gap 3m")
rep("    const mesh=new THREE.Mesh(new THREE.BoxGeometry(2,3.2,0.3), new THREE.MeshStandardMaterial({color:0x5a1a1a,roughness:.8,emissive:0x220000}));",
    "    const mesh=new THREE.Mesh(new THREE.BoxGeometry(3,3.2,0.3), new THREE.MeshStandardMaterial({color:0x5a1a1a,roughness:.8,emissive:0x220000}));",
    "door mesh 3m")
rep("    const w={x:dc,z,w:2,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};",
    "    const w={x:dc,z,w:3,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};",
    "door wall 3m")
rep("      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*2.0;",
    "      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*3.0;",
    "door slide 3m")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V44b patch applied')
