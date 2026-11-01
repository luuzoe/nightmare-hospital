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

# Walls + doors + staircase: replace V46 block
rep("""// V46 OLD HOSPITAL REBUILD, exact Zaw spec, all 15 floors same:
// Floor 114m (x -57..57) x 46m (z -23..23). Corridor z-3..3 (6m, east-west).
// North (left, facing east) 11 rooms, each 10m wide x 20m deep (z -23..-3), door 2m at room centre.
// Between north room 5 (-17..-7) and room 6 (-3..7) is the staircase hall x -7..-3 (4m wide), z -23..-3, open to corridor, steps down north.
// South (right) 11 rooms in a row, each 10m x 20m (z 3..23), door 2m, plus 4m landing x 53..57 open to corridor (so total length matches north 114m).
addWall(0,-23,114.6,0.6);
addWall(0,23,114.6,0.6);
addWall(-57,-13,0.6,20); addWall(-57,13,0.6,20);
addWall(57,-13,0.6,20); addWall(57,13,0.6,20);""",
    """// V47 REBUILD, Zaw new spec, all 15 floors same:
// Floor 169m (x -84.5..84.5) x 60m (z -30..30). Corridor z-5..5 (10m wide, east-west).
// North (left) 11 rooms, each 15m wide x 25m deep (z -30..-5), door 2.5m at room centre.
// Between north room 5 (-24.5..-9.5) and room 6 (-5.5..9.5) is staircase hall x -9.5..-5.5 (4m), z -30..-5, open to corridor, REAL 3D steps down north.
// South (right) 11 rooms in a row, each 15m x 25m (z 5..30), door 2.5m, plus 4m landing x 80.5..84.5 open to corridor (total length matches north 169m).
addWall(0,-30,169.6,0.6);
addWall(0,30,169.6,0.6);
addWall(-84.5,-17.5,0.6,25); addWall(-84.5,17.5,0.6,25);
addWall(84.5,-17.5,0.6,25); addWall(84.5,17.5,0.6,25);""",
    "outer walls v47")
rep("""// V46 FIX: north rooms are NOT NORTH_BOUNDS[i]..[i+1] after the staircase gap (bounds 5-6 is the hall, not a room).
const NORTH_ROOMS=[[-57,-47],[-47,-37],[-37,-27],[-27,-17],[-17,-7],[-3,7],[7,17],[17,27],[27,37],[37,47],[47,57]];
for(let i=0;i<NORTH_CENTRES.length;i++){
  const dc=NORTH_CENTRES[i];
  const left=NORTH_ROOMS[i][0], right=NORTH_ROOMS[i][1];
  if(dc-1>left) addWall((left+dc-1)/2,-3,dc-1-left,0.6);
  if(dc+1<right) addWall((dc+1+right)/2,-3,right-dc-1,0.6);
}""",
    """// V47: north rooms explicit (staircase gap is bounds 5-6, not a room).
const NORTH_ROOMS=[[-84.5,-69.5],[-69.5,-54.5],[-54.5,-39.5],[-39.5,-24.5],[-24.5,-9.5],[-5.5,9.5],[9.5,24.5],[24.5,39.5],[39.5,54.5],[54.5,69.5],[69.5,84.5]];
for(let i=0;i<NORTH_CENTRES.length;i++){
  const dc=NORTH_CENTRES[i];
  const left=NORTH_ROOMS[i][0], right=NORTH_ROOMS[i][1];
  if(dc-1.25>left) addWall((left+dc-1.25)/2,-5,dc-1.25-left,0.6);
  if(dc+1.25<right) addWall((dc+1.25+right)/2,-5,right-dc-1.25,0.6);
}""",
    "north corridor v47")
rep("""for(let i=0;i<SOUTH_CENTRES.length;i++){
  const dc=SOUTH_CENTRES[i];
  const left=SOUTH_BOUNDS[i], right=SOUTH_BOUNDS[i+1];
  if(dc-1>left) addWall((left+dc-1)/2,3,dc-1-left,0.6);
  if(dc+1<right) addWall((dc+1+right)/2,3,right-dc-1,0.6);
}
for(let i=1;i<NORTH_BOUNDS.length-1;i++){ const bx=NORTH_BOUNDS[i]; addWall(bx,-13,0.6,20); }
for(let i=1;i<SOUTH_BOUNDS.length-1;i++){ const bx=SOUTH_BOUNDS[i]; addWall(bx,13,0.6,20); }""",
    """for(let i=0;i<SOUTH_CENTRES.length;i++){
  const dc=SOUTH_CENTRES[i];
  const left=SOUTH_BOUNDS[i], right=SOUTH_BOUNDS[i+1];
  if(dc-1.25>left) addWall((left+dc-1.25)/2,5,dc-1.25-left,0.6);
  if(dc+1.25<right) addWall((dc+1.25+right)/2,5,right-dc-1.25,0.6);
}
for(let i=1;i<NORTH_BOUNDS.length-1;i++){ const bx=NORTH_BOUNDS[i]; addWall(bx,-17.5,0.6,25); }
for(let i=1;i<SOUTH_BOUNDS.length-1;i++){ const bx=SOUTH_BOUNDS[i]; addWall(bx,17.5,0.6,25); }""",
    "south corridor + dividers v47")
rep("""function addRoomDoor(dc,z){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(2,3.2,0.3), new THREE.MeshStandardMaterial({color:0x4a1515,roughness:.85,emissive:0x220000}));
  for(const fx of [dc-1,dc+1]){ const fr=new THREE.Mesh(new THREE.BoxGeometry(0.3,3.2,0.5), new THREE.MeshBasicMaterial({color:0xffcc00})); fr.position.set(fx,1.6,z); scene.add(fr); }
  mesh.position.set(dc,1.6,z); scene.add(mesh);
  const w={x:dc,z,w:2,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};
  walls.push(w); doorWalls.push(w);
}
for(const dc of NORTH_CENTRES) addRoomDoor(dc,-3);
for(const dc of SOUTH_CENTRES) addRoomDoor(dc,3);""",
    """function addRoomDoor(dc,z){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(2.5,3.2,0.3), new THREE.MeshStandardMaterial({color:0x4a1515,roughness:.85,emissive:0x220000}));
  for(const fx of [dc-1.25,dc+1.25]){ const fr=new THREE.Mesh(new THREE.BoxGeometry(0.3,3.2,0.5), new THREE.MeshBasicMaterial({color:0xffcc00})); fr.position.set(fx,1.6,z); scene.add(fr); }
  mesh.position.set(dc,1.6,z); scene.add(mesh);
  const w={x:dc,z,w:2.5,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};
  walls.push(w); doorWalls.push(w);
}
for(const dc of NORTH_CENTRES) addRoomDoor(dc,-5);
for(const dc of SOUTH_CENTRES) addRoomDoor(dc,5);""",
    "doors 2.5 v47")
rep("""// V46 STAIRCASE HALL: x -7..-3 (4m), z -23..-3, steps down north, sign at corridor entrance.
for(let i=0;i<12;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(4,0.28,1.5), new THREE.MeshStandardMaterial({color:0x3a3a3a,roughness:.95})); st.position.set(-5,-i*0.25-0.14,-4.5-i*1.5); scene.add(st); }
const stairSign=makePlaque(); stairSign.position.set(-5,3.6,-2.6); stairSign.rotation.y=Math.PI; scene.add(stairSign); stairSign.userData.set('⬇️ အောက်ထပ် လှေကား');""",
    """// V47 REAL 3D STAIRCASE HALL: x -9.5..-5.5 (4m), z -30..-5 (25m), floor hole above, steps visible.
// Landing south z -5..-6.5 at y=0, then 15 steps 1.5m deep x 0.2m down, north landing z -29..-30 at y=-3.
for(let i=0;i<15;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(4,0.28,1.5), new THREE.MeshStandardMaterial({color:0x3a3a3a,roughness:.95})); st.position.set(-7.5,-i*0.2-0.14,-7.25-i*1.5); scene.add(st); const edge=new THREE.Mesh(new THREE.BoxGeometry(4,0.06,0.12), new THREE.MeshBasicMaterial({color:0xffcc00})); edge.position.set(-7.5,-i*0.2+0.02,-6.5-i*1.5); scene.add(edge); }
for(const rx of [-9.3,-5.7]){ const rail=new THREE.Mesh(new THREE.BoxGeometry(0.12,0.12,25), new THREE.MeshStandardMaterial({color:0x8a8a8a,roughness:.6,metalness:.4})); rail.position.set(rx,-0.5,-17.5); rail.rotation.x=Math.atan2(3,25); scene.add(rail); }
const stairSign=makePlaque(); stairSign.position.set(-7.5,3.6,-4.6); stairSign.rotation.y=Math.PI; scene.add(stairSign); stairSign.userData.set('⬇️ အောက်ထပ် လှေကား');""",
    "staircase real v47")
# entrance / exit / plaques positions
rep("const entranceDoor=new THREE.Mesh(new THREE.BoxGeometry(0.4,3.2,6), new THREE.MeshStandardMaterial({color:0x1a5a2a,roughness:.8,emissive:0x003300}));\nentranceDoor.position.set(-57,1.6,0); scene.add(entranceDoor);",
    "const entranceDoor=new THREE.Mesh(new THREE.BoxGeometry(0.4,3.2,10), new THREE.MeshStandardMaterial({color:0x1a5a2a,roughness:.8,emissive:0x003300}));\nentranceDoor.position.set(-84.5,1.6,0); scene.add(entranceDoor);",
    "entrance door v47")
rep("entranceGlow.position.set(-56.7,3.15,0); entranceGlow.rotation.y=Math.PI/2; scene.add(entranceGlow);",
    "entranceGlow.position.set(-84.2,3.15,0); entranceGlow.rotation.y=Math.PI/2; scene.add(entranceGlow);",
    "entrance glow v47")
rep("entranceBlock={x:-57,z:0,w:0.6,d:6}; walls.push(entranceBlock);",
    "entranceBlock={x:-84.5,z:0,w:0.6,d:10}; walls.push(entranceBlock);",
    "entrance block v47")
rep("entrancePlaque=makePlaque(); entrancePlaque.position.set(-56.7,3.6,0); entrancePlaque.rotation.y=Math.PI/2; scene.add(entrancePlaque);",
    "entrancePlaque=makePlaque(); entrancePlaque.position.set(-84.2,3.6,0); entrancePlaque.rotation.y=Math.PI/2; scene.add(entrancePlaque);",
    "entrance plaque v47")
rep("exitPlaque=makePlaque(); exitPlaque.position.set(-5,3.6,-2.6); exitPlaque.rotation.y=Math.PI; scene.add(exitPlaque);",
    "exitPlaque=makePlaque(); exitPlaque.position.set(-7.5,3.6,-4.6); exitPlaque.rotation.y=Math.PI; scene.add(exitPlaque);",
    "exit plaque v47")
rep("for(const dc of NORTH_CENTRES){ const rpN=makePlaque(); rpN.position.set(dc,3.6,-3.4); scene.add(rpN); roomPlaques.push(rpN); }\nfor(const dc of SOUTH_CENTRES){ const rpS=makePlaque(); rpS.position.set(dc,3.6,3.4); rpS.rotation.y=Math.PI; scene.add(rpS); roomPlaques.push(rpS); }",
    "for(const dc of NORTH_CENTRES){ const rpN=makePlaque(); rpN.position.set(dc,3.6,-5.4); scene.add(rpN); roomPlaques.push(rpN); }\nfor(const dc of SOUTH_CENTRES){ const rpS=makePlaque(); rpS.position.set(dc,3.6,5.4); rpS.rotation.y=Math.PI; scene.add(rpS); roomPlaques.push(rpS); }",
    "room plaques v47")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part2 applied')
