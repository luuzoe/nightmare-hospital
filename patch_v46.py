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

rep("V45 • တံခါး 1.5m + တံခါး ရွှေဘောင် + compass တံခါးဘက် အရင် ညွှန် — အကုန်",
    "V46 • ဆေးရုံအဟောင်း အသစ်: အခန်း 22 ခန်း 10x20m, တံခါး 2m, လှေကား 4m N5-N6 ကြား, အခန်း 15 ထပ် အပေါ်ဆုံးက စ — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • အခန်း 5.8x21m, တံခါး 1.5m ရွှေဘောင်, compass တံခါးဘက် အရင် ညွှန်</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • ဆေးရုံအဟောင်း: အခန်း 10x20m, တံခါး 2m, လှေကား 4m, အပေါ်ဆုံး 15 ထပ်က စ</p>",
    "start hint")
# ROOM constants: north/south centres, bounds, zones, types order north then south
rep("const ROOM_CENTRES=[-29.1,-23.3,-17.5,-11.7,-5.9,-0.1,5.7,11.5,17.3,23.1,29];",
    "const NORTH_CENTRES=[-52,-42,-32,-22,-12,2,12,22,32,42,52];\nconst SOUTH_CENTRES=[-52,-42,-32,-22,-12,-2,8,18,28,38,48];\nconst NORTH_BOUNDS=[-57,-47,-37,-27,-17,-7,-3,7,17,27,37,47,57];\nconst SOUTH_BOUNDS=[-57,-47,-37,-27,-17,-7,3,13,23,33,43,53,57];\nconst ROOM_CENTRES=NORTH_CENTRES;",
    "room centres")
rep("const ROOM_ZONES=[{x:-17.5,z:-13.5},{x:17.3,z:-13.5},{x:-17.5,z:13.5},{x:17.3,z:13.5}];",
    "const ROOM_ZONES=[{x:-32,z:-13},{x:32,z:-13},{x:-32,z:13},{x:28,z:13}];",
    "room zones")
rep("const ITEM_SPAWNS=[[-29,-13],[-23,-13],[-17,-13],[-11,-13],[-5,-13],[0,-13],[7,-13],[13,-13],[19,-13],[25,-13],[29,-13],[-29,13],[-23,13],[-17,13],[-11,13],[0,13],[55,0]];",
    "const ITEM_SPAWNS=[[-52,-13],[-42,-13],[-32,-13],[-22,-13],[-12,-13],[2,-13],[12,-13],[22,-13],[32,-13],[42,-13],[52,-13],[-52,13],[-42,13],[-32,13],[-22,13],[-12,13],[-5,0]];",
    "item spawns")
# Minimap: scale 1.6, origin -57/-23
rep("  const sc=1.85;",
    "  const sc=1.6;",
    "minimap scale")
rep("    const x=(w.x-w.w/2+32)*sc;\n    const y=(w.z-w.d/2+24)*sc;",
    "    const x=(w.x-w.w/2+57)*sc;\n    const y=(w.z-w.d/2+23)*sc;",
    "minimap walls")
rep("    const bx=(S.beaconX+32)*sc;\n    const by=(S.beaconZ+24)*sc;",
    "    const bx=(S.beaconX+57)*sc;\n    const by=(S.beaconZ+23)*sc;",
    "minimap beacon")
rep("  const px=(playerPos.x+32)*sc;\n  const py=(playerPos.z+24)*sc;",
    "  const px=(playerPos.x+57)*sc;\n  const py=(playerPos.z+23)*sc;",
    "minimap player")
# Floor / ceiling size 114x46
rep("const floor=new THREE.Mesh(new THREE.PlaneGeometry(64,48), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9}));",
    "const floor=new THREE.Mesh(new THREE.PlaneGeometry(114,46), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9}));",
    "floor size")
rep("const ceil=new THREE.Mesh(new THREE.PlaneGeometry(64,48), new THREE.MeshStandardMaterial({map:ceilTex,roughness:1}));",
    "const ceil=new THREE.Mesh(new THREE.PlaneGeometry(114,46), new THREE.MeshStandardMaterial({map:ceilTex,roughness:1}));",
    "ceil size")
# Outer walls + internal walls + doors + staircase: replace whole V44 block
rep("""// outer walls (south has exit gap -2..2 for the exit door)
addWall(0,-24,64.6,0.6);
addWall(-27,24,10,0.6); addWall(-9,24,14,0.6); addWall(17,24,30,0.6); addWall(-32,-13.5,0.6,21); addWall(-32,13.5,0.6,21); // V44 west wall gap z-3..3 = corridor entrance addWall(32,-13.5,0.6,21); addWall(32,13.5,0.6,21); // V12 east wall gap z-3..3 to east wing corridor
// V44 22 ROOMS: central corridor z-3..3 (east-west walkway), north 11 rooms + south 11 rooms.
// Corridor walls at z=-3 (north rooms, door at room centre) and z=3 (south rooms, door at room centre).
// Door gap = centre +-0.75 (1.5m wide, Zaw ordered). Room dividing walls at each boundary, north z-24..-3, south z3..24.
const ROOM_BOUNDS=[-32,-26.2,-20.4,-14.6,-8.8,-3,2.8,8.6,14.4,20.2,26,32];
for(const z of [-3,3]){
  for(let i=0;i<ROOM_CENTRES.length;i++){
    const dc=ROOM_CENTRES[i];
    const left=ROOM_BOUNDS[i], right=ROOM_BOUNDS[i+1];
    if(dc-0.75>left) addWall((left+dc-0.75)/2,z,dc-0.75-left,0.6);
    if(dc+0.75<right) addWall((dc+0.75+right)/2,z,right-dc-0.75,0.6);
  }
}
for(let i=1;i<ROOM_BOUNDS.length-1;i++){
  const bx=ROOM_BOUNDS[i];
  addWall(bx,-13.5,0.6,21); addWall(bx,13.5,0.6,21);
}
// V44 DOORS: one per room, closed by default, opens when player/monster within 3.5m, closes beyond 5m.
// Door wall entries are in walls[] with isDoor=true; collide() respects closed doors, pathfinding treats doors as passable (they will open on approach).
const doorWalls=[];
for(let i=0;i<ROOM_CENTRES.length;i++){
  const dc=ROOM_CENTRES[i];
  for(const z of [-3,3]){
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(1.5,3.2,0.3), new THREE.MeshStandardMaterial({color:0x5a1a1a,roughness:.8,emissive:0x220000}));
    for(const fx of [dc-0.75,dc+0.75]){ const fr=new THREE.Mesh(new THREE.BoxGeometry(0.25,3.2,0.5), new THREE.MeshBasicMaterial({color:0xffcc00})); fr.position.set(fx,1.6,z); scene.add(fr); }
    mesh.position.set(dc,1.6,z); scene.add(mesh);
    const w={x:dc,z,w:1.5,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};
    walls.push(w); doorWalls.push(w);
  }
}
// V44 MIDDLE STAIRCASE: visual steps at corridor centre (0,0), 4x4 area, corridor still passable around it (1m gaps north/south).
for(let i=0;i<6;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(4,0.28,0.7), new THREE.MeshStandardMaterial({color:0x555555,roughness:.9})); st.position.set(0,-i*0.12+0.14,-1.4+i*0.55); scene.add(st); }
const stairSign=makePlaque(); stairSign.position.set(0,3.6,0); scene.add(stairSign); stairSign.userData.set('အလယ် လှေကား ↓');""",
    """// V46 OLD HOSPITAL REBUILD, exact Zaw spec, all 15 floors same:
// Floor 114m (x -57..57) x 46m (z -23..23). Corridor z-3..3 (6m, east-west).
// North (left, facing east) 11 rooms, each 10m wide x 20m deep (z -23..-3), door 2m at room centre.
// Between north room 5 (-17..-7) and room 6 (-3..7) is the staircase hall x -7..-3 (4m wide), z -23..-3, open to corridor, steps down north.
// South (right) 11 rooms in a row, each 10m x 20m (z 3..23), door 2m, plus 4m landing x 53..57 open to corridor (so total length matches north 114m).
addWall(0,-23,114.6,0.6);
addWall(0,23,114.6,0.6);
addWall(-57,-13,0.6,20); addWall(-57,13,0.6,20);
addWall(57,-13,0.6,20); addWall(57,13,0.6,20);
for(let i=0;i<NORTH_CENTRES.length;i++){
  const dc=NORTH_CENTRES[i];
  const left=NORTH_BOUNDS[i], right=NORTH_BOUNDS[i+1];
  if(dc-1>left) addWall((left+dc-1)/2,-3,dc-1-left,0.6);
  if(dc+1<right) addWall((dc+1+right)/2,-3,right-dc-1,0.6);
}
for(let i=0;i<SOUTH_CENTRES.length;i++){
  const dc=SOUTH_CENTRES[i];
  const left=SOUTH_BOUNDS[i], right=SOUTH_BOUNDS[i+1];
  if(dc-1>left) addWall((left+dc-1)/2,3,dc-1-left,0.6);
  if(dc+1<right) addWall((dc+1+right)/2,3,right-dc-1,0.6);
}
for(let i=1;i<NORTH_BOUNDS.length-1;i++){ const bx=NORTH_BOUNDS[i]; addWall(bx,-13,0.6,20); }
for(let i=1;i<SOUTH_BOUNDS.length-1;i++){ const bx=SOUTH_BOUNDS[i]; addWall(bx,13,0.6,20); }
const doorWalls=[];
function addRoomDoor(dc,z){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(2,3.2,0.3), new THREE.MeshStandardMaterial({color:0x4a1515,roughness:.85,emissive:0x220000}));
  for(const fx of [dc-1,dc+1]){ const fr=new THREE.Mesh(new THREE.BoxGeometry(0.3,3.2,0.5), new THREE.MeshBasicMaterial({color:0xffcc00})); fr.position.set(fx,1.6,z); scene.add(fr); }
  mesh.position.set(dc,1.6,z); scene.add(mesh);
  const w={x:dc,z,w:2,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};
  walls.push(w); doorWalls.push(w);
}
for(const dc of NORTH_CENTRES) addRoomDoor(dc,-3);
for(const dc of SOUTH_CENTRES) addRoomDoor(dc,3);
// V46 STAIRCASE HALL: x -7..-3 (4m), z -23..-3, steps down north, sign at corridor entrance.
for(let i=0;i<12;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(4,0.28,1.5), new THREE.MeshStandardMaterial({color:0x3a3a3a,roughness:.95})); st.position.set(-5,-i*0.25-0.14,-4.5-i*1.5); scene.add(st); }
const stairSign=makePlaque(); stairSign.position.set(-5,3.6,-2.6); stairSign.rotation.y=Math.PI; scene.add(stairSign); stairSign.userData.set('⬇️ အောက်ထပ် လှေကား');""",
    "outer + rooms + doors + staircase")
# Exit door: hide south door, move entrance to west
rep("const exitDoor=new THREE.Mesh(new THREE.BoxGeometry(4,3.2,0.4), new THREE.MeshStandardMaterial({color:0x7a1010,roughness:.8,emissive:0x330000}));\nexitDoor.position.set(0,1.6,24); scene.add(exitDoor);",
    "const exitDoor=new THREE.Mesh(new THREE.BoxGeometry(4,3.2,0.4), new THREE.MeshStandardMaterial({color:0x7a1010,roughness:.8,emissive:0x330000}));\nexitDoor.position.set(0,1.6,24); exitDoor.visible=false; scene.add(exitDoor);",
    "exit door hidden")
rep("exitGlow.position.set(0,3.15,23.7); exitGlow.rotation.y=Math.PI; scene.add(exitGlow);",
    "exitGlow.position.set(0,3.15,23.7); exitGlow.visible=false; exitGlow.rotation.y=Math.PI; scene.add(exitGlow);",
    "exit glow hidden")
rep("const entranceDoor=new THREE.Mesh(new THREE.BoxGeometry(6,3.2,0.4), new THREE.MeshStandardMaterial({color:0x1a5a2a,roughness:.8,emissive:0x003300}));\nentranceDoor.position.set(-19,1.6,24); scene.add(entranceDoor);",
    "const entranceDoor=new THREE.Mesh(new THREE.BoxGeometry(0.4,3.2,6), new THREE.MeshStandardMaterial({color:0x1a5a2a,roughness:.8,emissive:0x003300}));\nentranceDoor.position.set(-57,1.6,0); scene.add(entranceDoor);",
    "entrance door west")
rep("entranceGlow.position.set(-19,3.15,23.7); entranceGlow.rotation.y=Math.PI; scene.add(entranceGlow);",
    "entranceGlow.position.set(-56.7,3.15,0); entranceGlow.rotation.y=Math.PI/2; scene.add(entranceGlow);",
    "entrance glow west")
rep("exitBlock={x:0,z:24,w:4,d:0.6}; walls.push(exitBlock);",
    "exitBlock={x:0,z:24,w:4,d:0.6};",
    "exit block no wall")
rep("entranceBlock={x:-19,z:24,w:6,d:0.6}; walls.push(entranceBlock);",
    "entranceBlock={x:-57,z:0,w:0.6,d:6}; walls.push(entranceBlock);",
    "entrance block west")
rep("entrancePlaque=makePlaque(); entrancePlaque.position.set(-19,3.6,23.7); scene.add(entrancePlaque);",
    "entrancePlaque=makePlaque(); entrancePlaque.position.set(-56.7,3.6,0); entrancePlaque.rotation.y=Math.PI/2; scene.add(entrancePlaque);",
    "entrance plaque west")
rep("exitPlaque=makePlaque(); exitPlaque.position.set(0,3.6,23.7); scene.add(exitPlaque);",
    "exitPlaque=makePlaque(); exitPlaque.position.set(-5,3.6,-2.6); exitPlaque.rotation.y=Math.PI; scene.add(exitPlaque);",
    "exit plaque staircase")
rep("for(let i=0;i<ROOM_CENTRES.length;i++){ const dc=ROOM_CENTRES[i]; const rpN=makePlaque(); rpN.position.set(dc,3.6,-3.4); scene.add(rpN); roomPlaques.push(rpN); const rpS=makePlaque(); rpS.position.set(dc,3.6,3.4); rpS.rotation.y=Math.PI; scene.add(rpS); roomPlaques.push(rpS); }",
    "for(const dc of NORTH_CENTRES){ const rpN=makePlaque(); rpN.position.set(dc,3.6,-3.4); scene.add(rpN); roomPlaques.push(rpN); }\nfor(const dc of SOUTH_CENTRES){ const rpS=makePlaque(); rpS.position.set(dc,3.6,3.4); rpS.rotation.y=Math.PI; scene.add(rpS); roomPlaques.push(rpS); }",
    "room plaques 22 new")
# East wing: remove walls, hide floors (keep meshes but visible=false, and remove wall entries by not adding them)
rep("addWall(55,-15,30,0.6); addWall(55,15,30,0.6); addWall(40,-9,0.6,12); addWall(40,9,0.6,12); // V12 west wall gap z-3..3",
    "// V46 east wing removed: old hospital is only 114x46m, no east wing",
    "east wing walls removed")
rep("addWall(36,-3,8,0.6); addWall(36,3,8,0.6); // corridor sides",
    "// V46 east corridor removed",
    "east corridor removed")
rep("addWall(70,-8.5,0.6,13); addWall(70,8.5,0.6,13); // east wall, gap z-2..2 for new exit",
    "// V46 east exit removed",
    "east exit removed")
# Room props: replace V44 room props loop
rep("""// V44 ROOM PROPS: one furniture piece per room, different per room type, visual only (props do not collide).
for(let i=0;i<ROOM_CENTRES.length;i++){
  const dc=ROOM_CENTRES[i];
  const col=[0x8a8f8a,0x9aa0a0,0x5a4632,0x3a4a3a,0x6a6a6a,0x4a4a4a][i%6];
  addProp(dc,-13.5,2.2,1.1,0.7,col,'roomprop');
  addProp(dc,13.5,2.2,1.1,0.7,col,'roomprop');
}""",
    """// V46 ROOM PROPS: old hospital furniture per room, visual only. Real hospital beds are loaded separately (hospital-bed.glb, see below).
for(let i=0;i<NORTH_CENTRES.length;i++){
  const dc=NORTH_CENTRES[i];
  const col=[0x6a6a6a,0x5a4632,0x3a4a3a,0x8a8f8a,0x4a4a4a,0x9aa0a0][i%6];
  addProp(dc,-16,2.2,1.1,0.7,col,'roomprop');
}
for(let i=0;i<SOUTH_CENTRES.length;i++){
  const dc=SOUTH_CENTRES[i];
  const col=[0x5a4632,0x6a6a6a,0x8a8f8a,0x3a4a3a,0x4a4a4a,0x9aa0a0][i%6];
  addProp(dc,16,2.2,1.1,0.7,col,'roomprop');
}
for(const [dx,dz] of [[-30,0],[0,0],[30,0],[-5,-13],[55,13]]){ addProp(dx,dz,1.5,0.8,0.4,0x1a1a1a,'debris'); }""",
    "room props new")
# Real hospital bed loader: insert before lockers
rep("// lockers = hiding spots",
    """// V46 REAL HOSPITAL BED (Zaw-sent hospital_bed_6_swgg.glb, 4.3MB, cm units -> scale 0.01, base ~0m, top ~1.4m, estimate not phone-verified).
if(typeof loader!=='undefined'){
  loader.load('hospital-bed.glb', gltf=>{
    const tpl=gltf.scene; tpl.scale.set(0.01,0.01,0.01);
    for(const dc of NORTH_CENTRES){ const b=tpl.clone(true); b.position.set(dc+2,-0, -16); b.rotation.y=0; scene.add(b); }
    for(const dc of SOUTH_CENTRES){ const b=tpl.clone(true); b.position.set(dc-2,0,16); b.rotation.y=Math.PI; scene.add(b); }
  }, undefined, ()=>{});
}
// lockers = hiding spots""",
    "real bed loader")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V46 part1 applied')
