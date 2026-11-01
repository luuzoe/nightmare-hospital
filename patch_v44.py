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

rep("V43 • Ep1 ပြန်လုပ်: သော့ ၃ ချောင်း စတဲ့ အခန်းထဲမှာပဲ + Ep1 သရဲ မလိုက် — အကုန်",
    "V44 • အခန်း 22 ခန်း + တံခါးပေါက် + အလယ်လျှောက်လမ်း + အလယ်လှေကား — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • Ep1: သော့ အခန်းထဲမှာပဲ, သရဲ မလိုက်</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • အခန်း 22 ခန်း, တံခါးနား သွားရင် တံခါးပွင့်, အလယ်လှေကား ဆင်း</p>",
    "start hint")

# --- ROOM TYPES + ZONES (before MAP, ROOM_ZONES is at line ~326, before MAP) ---
rep("const ROOM_ZONES=[{x:-20,z:-12},{x:20,z:-12},{x:-20,z:12},{x:20,z:12}];",
    "const ROOM_CENTRES=[-29.1,-23.3,-17.5,-11.7,-5.9,-0.1,5.7,11.5,17.3,23.1,29];\nconst ROOM_TYPES=['လူနာဆောင် 1','ICU','ခွဲစိတ်ခန်း','ကလေးဆောင်','မီးဖွားဆောင်','ဓာတ်ခွဲခန်း','X-Ray ခန်း','အရေးပေါ်','ဆေးဆိုင်','ရုံးခန်း','သေဆုံးခန်း','လူနာဆောင် 2','စောင့်ခန်း','လော်ဘီ','ပစ္စည်းသိုလှောင်','ကျောက်ကပ်ဆောင်','သီးသန့်ဆောင်','စားသောက်ခန်း','ဧည့်ခန်း','အော်ပရေး ခန်း','ဆေးဝါးခန်း','စတိုခန်း'];\nconst ROOM_ZONES=[{x:-17.5,z:-13.5},{x:17.3,z:-13.5},{x:-17.5,z:13.5},{x:17.3,z:13.5}];",
    "room types zones")
rep("const ITEM_SPAWNS=[[-24,-16],[24,-16],[20,20],[10,12],[-28,20],[48,-10],[62,-12],[55,10],[0,0],[-16,0],[16,0],[0,-12],[0,12],[-20,-20],[26,-20],[45,0],[65,0]];",
    "const ITEM_SPAWNS=[[-29,-13],[-23,-13],[-17,-13],[-11,-13],[-5,-13],[0,-13],[7,-13],[13,-13],[19,-13],[25,-13],[29,-13],[-29,13],[-23,13],[-17,13],[-11,13],[0,13],[55,0]];",
    "item spawns")

# updatePlaques: 22 plaques, room types
rep("  const set=ROOM_SETS[S.floor%5];\n  roomPlaques.forEach((pl,i)=>{ if(pl) pl.userData.set('အထပ် '+S.floor+' • '+set[i]); });",
    "  roomPlaques.forEach((pl,i)=>{ if(pl) pl.userData.set('အထပ် '+S.floor+' • '+(ROOM_TYPES[i]||('အခန်း '+(i+1)))); });",
    "update plaques")

# --- WEST WALL: gap for corridor west entrance ---
rep("addWall(-32,0,0.6,48.6);",
    "addWall(-32,-13.5,0.6,21); addWall(-32,13.5,0.6,21); // V44 west wall gap z-3..3 = corridor entrance",
    "west wall gap")

# --- INTERNAL WALLS: replace old corridor walls with 22-room walls ---
rep("""// horizontal corridor walls z=-3 and z=3, doors at -20..-12, 12..20, centre gap -4..4
for(const z of [-3,3]){
  for(const [a,b] of [[-32,-20],[-12,-4],[4,12],[20,32]]) addWall((a+b)/2,z,b-a,0.6);
}
// vertical corridor walls x=-4 and x=4, gaps -3..3 (middle), -14..-10 (north, V19), 10..14 (south, V19) - north-centre was a dead end before
for(const x of [-4,4]){
  addWall(x,-19,0.6,10); addWall(x,-6.5,0.6,7); addWall(x,6.5,0.6,7); addWall(x,19,0.6,10);
}""",
    """// V44 22 ROOMS: central corridor z-3..3 (east-west walkway), north 11 rooms + south 11 rooms.
// Corridor walls at z=-3 (north rooms, door at room centre) and z=3 (south rooms, door at room centre).
// Door gap = centre +-1 (2m wide). Room dividing walls at each boundary, north z-24..-3, south z3..24.
const ROOM_BOUNDS=[-32,-26.2,-20.4,-14.6,-8.8,-3,2.8,8.6,14.4,20.2,26,32];
for(const z of [-3,3]){
  for(let i=0;i<ROOM_CENTRES.length;i++){
    const dc=ROOM_CENTRES[i];
    const left=ROOM_BOUNDS[i], right=ROOM_BOUNDS[i+1];
    if(dc-1>left) addWall((left+dc-1)/2,z,dc-1-left,0.6);
    if(dc+1<right) addWall((dc+1+right)/2,z,right-dc-1,0.6);
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
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(2,3.2,0.3), new THREE.MeshStandardMaterial({color:0x5a1a1a,roughness:.8,emissive:0x220000}));
    mesh.position.set(dc,1.6,z); scene.add(mesh);
    const w={x:dc,z,w:2,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};
    walls.push(w); doorWalls.push(w);
  }
}
// V44 MIDDLE STAIRCASE: visual steps at corridor centre (0,0), 4x4 area, corridor still passable around it (1m gaps north/south).
for(let i=0;i<6;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(4,0.28,0.7), new THREE.MeshStandardMaterial({color:0x555555,roughness:.9})); st.position.set(0,-i*0.12+0.14,-1.4+i*0.55); scene.add(st); }
const stairSign=makePlaque(); stairSign.position.set(0,3.6,0); scene.add(stairSign); stairSign.userData.set('အလယ် လှေကား ↓');""",
    "internal walls 22 rooms")

# --- ROOM PLAQUES: 22 plaques at room doors ---
rep("for(const [rx,rz] of [[-20,-12],[20,-12],[-20,12],[20,12]]){ const rp=makePlaque(); rp.position.set(rx,3.6,rz); scene.add(rp); roomPlaques.push(rp); }",
    "for(let i=0;i<ROOM_CENTRES.length;i++){ const dc=ROOM_CENTRES[i]; const rpN=makePlaque(); rpN.position.set(dc,3.6,-3.4); scene.add(rpN); roomPlaques.push(rpN); const rpS=makePlaque(); rpS.position.set(dc,3.6,3.4); rpS.rotation.y=Math.PI; scene.add(rpS); roomPlaques.push(rpS); }",
    "room plaques 22")

# --- COLLISION / PATHFINDING: doors ---
rep("""function collide(x,z,r,allowStair){
  for(const w of walls){""",
    """function collide(x,z,r,allowStair){
  for(const w of walls){
    if(w.isDoor && w.doorOpen) continue;""",
    "collide doors")
rep("""  for(let i=1;i<n;i++){
    const x=x1+(x2-x1)*i/n, z=z1+(z2-z1)*i/n;
    for(const w of walls){ if(Math.abs(x-w.x)<w.w/2+0.2 && Math.abs(z-w.z)<w.d/2+0.2) return true; }
  }
  return false;
}""",
    """  for(let i=1;i<n;i++){
    const x=x1+(x2-x1)*i/n, z=z1+(z2-z1)*i/n;
    for(const w of walls){ if(w.isDoor) continue; if(Math.abs(x-w.x)<w.w/2+0.2 && Math.abs(z-w.z)<w.d/2+0.2) return true; }
  }
  return false;
}""",
    "lineBlockedFine doors")
rep("""  const blocked=(cx,cz)=>{ const wx=x0+cx*step, wz=z0+cz*step; for(const w of walls){ if(Math.abs(wx-w.x)<w.w/2+0.6 && Math.abs(wz-w.z)<w.d/2+0.6) return true; } return false; };""",
    """  const blocked=(cx,cz)=>{ const wx=x0+cx*step, wz=z0+cz*step; for(const w of walls){ if(w.isDoor) continue; if(Math.abs(wx-w.x)<w.w/2+0.6 && Math.abs(wz-w.z)<w.d/2+0.6) return true; } return false; };""",
    "compassPath doors")
rep("""function lineBlocked(x1,z1,x2,z2){
  for(let i=1;i<10;i++){
    const x=x1+(x2-x1)*i/10, z=z1+(z2-z1)*i/10;
    for(const w of walls){ if(Math.abs(x-w.x)<w.w/2+0.2 && Math.abs(z-w.z)<w.d/2+0.2) return true; }
  }
  return false;
}""",
    """function lineBlocked(x1,z1,x2,z2){
  for(let i=1;i<10;i++){
    const x=x1+(x2-x1)*i/10, z=z1+(z2-z1)*i/10;
    for(const w of walls){ if(w.isDoor) continue; if(Math.abs(x-w.x)<w.w/2+0.2 && Math.abs(z-w.z)<w.d/2+0.2) return true; }
  }
  return false;
}""",
    "lineBlocked doors")

# minimap: skip open doors
rep("""  for(const w of walls){
    const x=(w.x-w.w/2+32)*sc;""",
    """  for(const w of walls){
    if(w.isDoor && w.doorOpen) continue;
    const x=(w.x-w.w/2+32)*sc;""",
    "minimap doors")

# --- KEYS, CORPSES, SWITCHES, PATROL ---
rep("""const keyDefs=[
  {id:1,x:-24,z:20,room:'Start',label:'သော့ 1'},
  {id:2,x:-10,z:16,room:'Start',label:'သော့ 2'},
  {id:3,x:-20,z:6,room:'Start',label:'သော့ 3'},""",
    """const keyDefs=[
  {id:1,x:-17,z:-12,room:'လူနာဆောင်',label:'သော့ 1'},
  {id:2,x:-6,z:12,room:'ဓာတ်ခွဲခန်း',label:'သော့ 2'},
  {id:3,x:17,z:-12,room:'အော်ပရေး ခန်း',label:'သော့ 3'},""",
    "keys rooms")
rep("""const corpseDefs=[
  {x:-20,z:-20,yaw:Math.PI/2}, {x:-18,z:-12,yaw:0.5}, {x:24,z:-10,yaw:2.2},
  {x:-24,z:12,yaw:1.0}, {x:26,z:16,yaw:2.8}, {x:0,z:-20,yaw:0},
];""",
    """const corpseDefs=[
  {x:-23,z:-15,yaw:Math.PI/2}, {x:0,z:-15,yaw:0.5}, {x:23,z:-15,yaw:2.2},
  {x:-23,z:15,yaw:1.0}, {x:0,z:15,yaw:2.8}, {x:23,z:15,yaw:0},
];""",
    "corpses rooms")
rep("const switchMesh2=makeSwitch(-26,-10); const switchMesh3=makeSwitch(0,10);\nconst switchesList=[{x:-26,z:-10,label:'Switch A'},{x:0,z:10,label:'Switch B'},{x:68,z:5,label:'Switch C'}];",
    "const switchMesh2=makeSwitch(-23,-13); const switchMesh3=makeSwitch(0,10);\nconst switchesList=[{x:-23,z:-13,label:'Switch A'},{x:0,z:10,label:'Switch B'},{x:68,z:5,label:'Switch C'}];",
    "switches rooms")
rep("const patrolPts=[[20,20],[20,8],[0,0],[-20,-15],[20,-15],[-20,10],[0,0],[36,0],[55,0],[65,0]]; // V12 patrols old + east wing",
    "const patrolPts=[[-28,0],[-16,0],[0,0],[16,0],[28,0],[0,-13],[0,13],[-23,-13],[23,13],[36,0],[55,0],[65,0]]; // V44 corridor + rooms + east wing",
    "patrol")
rep("const pathNodes=[[0,0],[-16,0],[16,0],[0,-12],[0,12],[-16,-3],[16,-3],[0,-3],[-16,3],[16,3],[0,3],[-24,-12],[24,-12],[-24,12],[24,12],[36,0],[45,0],[55,0],[65,0]]; // V12 + east wing corridor nodes",
    "const pathNodes=[[0,0],[-16,0],[16,0],[-28,0],[28,0],[-29,-3],[-23,-3],[-17,-3],[-11,-3],[-5,-3],[0,-3],[6,-3],[12,-3],[17,-3],[23,-3],[29,-3],[-29,3],[-23,3],[-17,3],[-11,3],[-5,3],[0,3],[6,3],[12,3],[17,3],[23,3],[29,3],[36,0],[45,0],[55,0],[65,0]]; // V44 corridor + door centres + east wing",
    "pathNodes")

# --- SPAWN / RESPAWN: corridor west, facing east ---
rep("  playerPos.set(-18,0,12); monsterPos.set(20,0,16); monsterState='patrol'; patrolIdx=0; S.blackout=0; S.blackoutTimer=30;",
    "  playerPos.set(-28,0,0); S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; patrolIdx=0; S.blackout=0; S.blackoutTimer=30;",
    "reset spawn")
rep("  S.hearts=3; S.keys=0; S.stamina=100; S.hidden=false; S.hideTimer=0; S.hideLocker=false; S.moanTimer=40; S.invuln=0; S.chase=false; S.scare=false; S.scareTimer=0; S.catchTimer=0; S.nextScare=15; S.time=0; lastGirlTime=-999; lastWanderScream=-999; nextTwitch=25; S.frontScareTimer=50; S.randScareTimer=50; S.whisperTimer=0; S.shadowScare=false; S.escaping=false; S.escapeProgress=0; S.stage=1; S.items=0; S.switchOn=false; S.escapeDoorX=0; S.escapeDoorZ=24; S.floor=15; if(typeof shadowGhost!=='undefined' && shadowGhost) shadowGhost.visible=false; S.dead=false; S.won=false; S.yaw=Math.PI;",
    "  S.hearts=3; S.keys=0; S.stamina=100; S.hidden=false; S.hideTimer=0; S.hideLocker=false; S.moanTimer=40; S.invuln=0; S.chase=false; S.scare=false; S.scareTimer=0; S.catchTimer=0; S.nextScare=15; S.time=0; lastGirlTime=-999; lastWanderScream=-999; nextTwitch=25; S.frontScareTimer=50; S.randScareTimer=50; S.whisperTimer=0; S.shadowScare=false; S.escaping=false; S.escapeProgress=0; S.stage=1; S.items=0; S.switchOn=false; S.escapeDoorX=0; S.escapeDoorZ=24; S.floor=15; if(typeof shadowGhost!=='undefined' && shadowGhost) shadowGhost.visible=false; S.dead=false; S.won=false; S.yaw=Math.PI/2;",
    "reset yaw")
rep("playerPos.set(-19,0,20); playerPos.y=0; S.yaw=Math.PI; monsterPos.set(20,0,16); monsterState='patrol'; startFloorMission();",
    "playerPos.set(-28,0,0); playerPos.y=0; S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; startFloorMission();",
    "continue spawn")
rep("  playerPos.set(-19,0,20); playerPos.y=0; S.yaw=Math.PI; monsterPos.set(20,0,16); monsterState='patrol'; patrolIdx=0; S.chase=false;",
    "  playerPos.set(-28,0,0); playerPos.y=0; S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; patrolIdx=0; S.chase=false;",
    "floorchange spawn")
# loseHeart respawn
rep("  playerPos.set(-18,0,12); monsterPos.set(20,0,16); monsterState='patrol'; S.chase=false; S.scare=false; S.catchTimer=0;",
    "  playerPos.set(-28,0,0); S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; S.chase=false; S.scare=false; S.catchTimer=0;",
    "loseHeart spawn")

# --- DOOR UPDATE + MIDDLE STAIRCASE DESCENT: insert after entrance door animation block ---
rep("""  if(typeof entranceDoor!=='undefined') entranceDoor.position.x=-19+S.entranceAnim*6.0;
  if(S.doorOpen && S.floor>1 && !S._landing && playerPos.z>=37.5){ S._landing=true; goToNextFloor(); }""",
    """  if(typeof entranceDoor!=='undefined') entranceDoor.position.x=-19+S.entranceAnim*6.0;
  // V44 ROOM DOORS: open if player or monster within 3.5m, close beyond 5m, slide sideways along wall.
  if(typeof doorWalls!=='undefined'){
    for(const dw of doorWalls){
      const dp=Math.hypot(dw.x-playerPos.x,dw.z-playerPos.z);
      const dm=Math.hypot(dw.x-monsterPos.x,dw.z-monsterPos.z);
      const near=Math.min(dp,dm);
      if(!dw.doorOpen && near<3.5){ dw.doorOpen=true; doorSound(); }
      else if(dw.doorOpen && near>5){ dw.doorOpen=false; }
      dw.anim+=((dw.doorOpen?1:0)-dw.anim)*Math.min(1,dt*6);
      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*2.0;
    }
  }
  // V44 MIDDLE STAIRCASE: mission complete + stand on centre (0,0) within 2m -> descend, same as south door.
  if(missionComplete() && S.floor>1 && !S._landing && Math.hypot(playerPos.x,playerPos.z)<2.0){ S._landing=true; toast('⬇️ အလယ် လှေကားကနေ ဆင်းမယ်!'); goToNextFloor(); }
  if(S.doorOpen && S.floor>1 && !S._landing && playerPos.z>=37.5){ S._landing=true; goToNextFloor(); }""",
    "door update + middle stair descent")

# --- ROOM PROPS: one per room, after old props, before lockers ---
rep("// lockers = hiding spots",
    """// V44 ROOM PROPS: one furniture piece per room, different per room type, visual only (props do not collide).
for(let i=0;i<ROOM_CENTRES.length;i++){
  const dc=ROOM_CENTRES[i];
  const col=[0x8a8f8a,0x9aa0a0,0x5a4632,0x3a4a3a,0x6a6a6a,0x4a4a4a][i%6];
  addProp(dc,-13.5,2.2,1.1,0.7,col,'roomprop');
  addProp(dc,13.5,2.2,1.1,0.7,col,'roomprop');
}
// lockers = hiding spots""",
    "room props")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V44 patch applied')
