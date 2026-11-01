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

rep("V44 • အခန်း 22 ခန်း + တံခါးပေါက် + အလယ်လျှောက်လမ်း + အလယ်လှေကား — အကုန်",
    "V45 • တံခါး 1.5m + တံခါး ရွှေဘောင် + compass တံခါးဘက် အရင် ညွှန် — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • အခန်း 22 ခန်း, တံခါးနား သွားရင် တံခါးပွင့်, အလယ်လှေကား ဆင်း</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • အခန်း 5.8x21m, တံခါး 1.5m ရွှေဘောင်, compass တံခါးဘက် အရင် ညွှန်</p>",
    "start hint")
# Door gap 3m -> 1.5m
rep("// Door gap = centre +-1.5 (3m wide, so BFS 1m grid + 0.6 margin always finds a cell through the door). Room dividing walls at each boundary, north z-24..-3, south z3..24.",
    "// Door gap = centre +-0.75 (1.5m wide, Zaw ordered). Room dividing walls at each boundary, north z-24..-3, south z3..24.",
    "door gap comment")
rep("""    if(dc-1.5>left) addWall((left+dc-1.5)/2,z,dc-1.5-left,0.6);
    if(dc+1.5<right) addWall((dc+1.5+right)/2,z,right-dc-1.5,0.6);""",
    """    if(dc-0.75>left) addWall((left+dc-0.75)/2,z,dc-0.75-left,0.6);
    if(dc+0.75<right) addWall((dc+0.75+right)/2,z,right-dc-0.75,0.6);""",
    "door gap 1.5m")
rep("    const mesh=new THREE.Mesh(new THREE.BoxGeometry(3,3.2,0.3), new THREE.MeshStandardMaterial({color:0x5a1a1a,roughness:.8,emissive:0x220000}));",
    "    const mesh=new THREE.Mesh(new THREE.BoxGeometry(1.5,3.2,0.3), new THREE.MeshStandardMaterial({color:0x5a1a1a,roughness:.8,emissive:0x220000}));\n    for(const fx of [dc-0.75,dc+0.75]){ const fr=new THREE.Mesh(new THREE.BoxGeometry(0.25,3.2,0.5), new THREE.MeshBasicMaterial({color:0xffcc00})); fr.position.set(fx,1.6,z); scene.add(fr); }",
    "door mesh 1.5m + gold frame")
rep("    const w={x:dc,z,w:3,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};",
    "    const w={x:dc,z,w:1.5,d:0.6,isDoor:true,doorOpen:false,anim:0,mesh,closedX:dc};",
    "door wall 1.5m")
rep("      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*3.0;",
    "      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*1.5;",
    "door slide 1.5m")
# Door open logic: rectangle distance, not centre distance
rep("""  // V44 ROOM DOORS: open if player or monster within 3.5m, close beyond 5m, slide sideways along wall.
  if(typeof doorWalls!=='undefined'){
    for(const dw of doorWalls){
      const dp=Math.hypot(dw.x-playerPos.x,dw.z-playerPos.z);
      const dm=Math.hypot(dw.x-monsterPos.x,dw.z-monsterPos.z);
      const near=Math.min(dp,dm);
      if(!dw.doorOpen && near<3.5){ dw.doorOpen=true; doorSound(); }
      else if(dw.doorOpen && near>5){ dw.doorOpen=false; }""",
    """  // V45 ROOM DOORS: open by distance to door RECTANGLE (not centre, so approaching the door edge also opens it), open <4m, close >6m.
  if(typeof doorWalls!=='undefined'){
    for(const dw of doorWalls){
      const dp=Math.hypot(Math.max(Math.abs(playerPos.x-dw.x)-dw.w/2,0),Math.abs(playerPos.z-dw.z));
      const dm=Math.hypot(Math.max(Math.abs(monsterPos.x-dw.x)-dw.w/2,0),Math.abs(monsterPos.z-dw.z));
      const near=Math.min(dp,dm);
      if(!dw.doorOpen && near<4){ dw.doorOpen=true; doorSound(); }
      else if(dw.doorOpen && near>6){ dw.doorOpen=false; }""",
    "door rect distance")
# Compass waypoint: room-aware, door first
rep("""function compassWaypoint(px,pz,tx,tz){
  if(!lineBlockedFine(px,pz,tx,tz)) return [tx,tz];
  const path=compassPath(px,pz,tx,tz);""",
    """function roomDoorFor(px,pz){
  if(typeof ROOM_CENTRES==='undefined' || typeof ROOM_BOUNDS==='undefined') return null;
  if(pz<-3 || pz>3){
    for(let i=0;i<ROOM_CENTRES.length;i++){
      if(px>=ROOM_BOUNDS[i] && px<ROOM_BOUNDS[i+1]) return [ROOM_CENTRES[i], pz<-3?-3:3];
    }
  }
  return null;
}
function compassWaypoint(px,pz,tx,tz){
  if(!lineBlockedFine(px,pz,tx,tz)) return [tx,tz];
  const pDoor=roomDoorFor(px,pz), tDoor=roomDoorFor(tx,tz);
  if(pDoor && (!tDoor || pDoor[0]!==tDoor[0] || pDoor[1]!==tDoor[1])) return pDoor;
  if(tDoor) return tDoor;
  if(px>32 && tx<=32) return [32,0];
  if(px<=32 && tx>32) return [32,0];
  const path=compassPath(px,pz,tx,tz);""",
    "compass room aware")
# Stuck toast: mention gold door frame
rep("      if(moved<0.3 && S.time-S.stuckWarn>5){ S.stuckWarn=S.time; toast('⛔ နံရံ ပိတ်နေသည်! ကင်မရာလှည့်ပြီး compass ဘက် သွားပါ'); if(navigator.vibrate) navigator.vibrate(100); }",
    "      if(moved<0.3 && S.time-S.stuckWarn>5){ S.stuckWarn=S.time; toast('⛔ နံရံ ပိတ်နေတယ်! တံခါးပေါက် (ရွှေဘောင်) ဘက် သွား, compass ဘက် သွား'); if(navigator.vibrate) navigator.vibrate(100); }",
    "stuck toast")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V45 patch applied')
