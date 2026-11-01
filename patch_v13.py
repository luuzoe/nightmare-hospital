import re, sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global t
    if old not in t:
        print("MISSING:",old[:200]); sys.exit(1)
    t=t.replace(old,new,cnt)

# --- HTML banner + CSS ---
rep("<!-- HUD -->",
"""<div id="floorBanner"></div>
<!-- HUD -->""")
rep("#stairScreen{position:fixed;",
"#floorBanner{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%);font-size:42px;font-weight:900;color:#ffd166;text-shadow:0 0 20px #ff0000,2px 2px 0 #000;z-index:45;display:none;text-align:center}#floorBanner.on{display:block}\n#stairScreen{position:fixed;")

# --- S fields ---
rep("dead:false, won:false};",
"dead:false, won:false, doorOpen:false, entranceOpen:false, entranceTimer:0, doorAnim:0, entranceAnim:0, inStair:false, distance:0, whisperTimer:0};")

# --- Missions distinct ---
rep("  5:{ep:11,type:'order',label:'ဆေး',need:7},",
"  5:{ep:11,type:'rooms',label:'အခန်း',need:4},")
rep("  4:{ep:12,type:'survive',label:'ရှင်သန်',need:90,timer:90},",
"  4:{ep:12,type:'distance',label:'လမ်းလျှောက်',need:180},")
rep("  3:{ep:13,type:'lockers',label:'Locker',need:5,dwell:3},",
"  3:{ep:13,type:'darklockers',label:'မှောင် Locker',need:5,dwell:3},")
rep("  2:{ep:14,type:'timed',label:'အချိန်မီ ပစ္စည်း',need:8,timer:75},",
"  2:{ep:14,type:'timedorder',label:'အချိန်မီ အစဉ်',need:8,timer:75},")

# missionComplete
rep("""  if(fm.type==='survive'||fm.type==='lockers'||fm.type==='lure'||fm.type==='hide') return S.missionDone;""",
"""  if(fm.type==='survive'||fm.type==='lockers'||fm.type==='lure'||fm.type==='hide'||fm.type==='distance'||fm.type==='darklockers') return S.missionDone;
  if(fm.type==='rooms') return S.visited.length>=fm.need;
  if(fm.type==='timedorder') return S.items>=fm.need;""")
# missionProgressText
rep("""  if(fm.type==='lockers') return S.visited.length+'/'+fm.need;""",
"""  if(fm.type==='lockers'||fm.type==='darklockers'||fm.type==='rooms') return S.visited.length+'/'+fm.need;
  if(fm.type==='distance') return Math.floor(S.distance)+'/'+fm.need+'m';
  if(fm.type==='timedorder') return S.items+'/'+fm.need;""")
# startFloorMission: reset distance, dark/darklockers, items, objectives, plaques/layout
rep("  S.missionDone=false; S.missionTimer=fm.timer||0; S.hideTotal=0; S.switchIdx=0; S.corpseIdx=0; S.dwell=0; S.visited=[]; S.switchOn=false;",
"  S.missionDone=false; S.missionTimer=fm.timer||0; S.hideTotal=0; S.switchIdx=0; S.corpseIdx=0; S.dwell=0; S.visited=[]; S.switchOn=false; S.distance=0;")
rep("  if(typeof flash!=='undefined' && flash){ flash.angle=fm.type==='dark'?0.30:0.45; }\n  if(scene.fog) scene.fog.density=0.09+(15-S.floor)*0.003+(fm.type==='dark'?0.04:0);",
"  if(typeof flash!=='undefined' && flash){ flash.angle=(fm.type==='dark'||fm.type==='darklockers')?0.30:0.45; }\n  if(scene.fog) scene.fog.density=0.09+(15-S.floor)*0.003+((fm.type==='dark'||fm.type==='darklockers')?0.04:0);\n  if(typeof applyFloorLayout==='function') applyFloorLayout();\n  if(typeof updatePlaques==='function') updatePlaques();\n  if(typeof setActiveGhosts==='function') setActiveGhosts();")
rep("  } else if(fm.type==='order'||fm.type==='dark'||fm.type==='timed'||fm.type==='final'){",
"  } else if(fm.type==='order'||fm.type==='dark'||fm.type==='timed'||fm.type==='final'||fm.type==='timedorder'){")
rep("""  else if(fm.type==='corpse') obj='Ep'+fm.ep+' • လူသေကောင် '+fm.need+' ကောင် အစဉ်လိုက် ထိပါ';""",
"""  else if(fm.type==='corpse') obj='Ep'+fm.ep+' • လူသေကောင် '+fm.need+' ကောင် အစဉ်လိုက် ထိပါ';
  else if(fm.type==='rooms') obj='Ep'+fm.ep+' • အခန်း ၄ ခု လုံး သွားပါ (NW/NE/SW/SE)';
  else if(fm.type==='distance') obj='Ep'+fm.ep+' • စုစုပေါင်း '+fm.need+'m လမ်းလျှောက်ပါ';
  else if(fm.type==='darklockers') obj='Ep'+fm.ep+' • မှောင်ထဲမှာ Locker '+fm.need+' ခု မှာ ၃ စက္ကန့်စီ ရပ်ပါ';
  else if(fm.type==='timedorder') obj='Ep'+fm.ep+' • '+fm.timer+' စက္ကန့်အတွင်း အစဉ်လိုက် ပစ္စည်း '+fm.need+' ခု ယူပါ!';""")

# --- Themes, rooms, plaques, layout, active ghosts (insert before $ helper) ---
rep("const $ = id => document.getElementById(id);",
"""// V13: rooms differ per floor (labels + furniture + light + tint), ghosts differ per floor
const ROOM_ZONES=[{x:-20,z:-12},{x:20,z:-12},{x:-20,z:12},{x:20,z:12}];
const ROOM_SETS=[
 ['လူနာဆောင်','ခွဲစိတ်ခန်း','ဧည့်ခန်း','ဆေးဆိုင်'],
 ['ICU','အော်ပရေး ခန်း','လော်ဘီ','ဓာတ်ခွဲခန်း'],
 ['အရေးပေါ်','X-Ray','စောင့်ခန်း','ပစ္စည်းသိုလှောင်'],
 ['ကလေးဆောင်','မီးဖွားဆောင်','ရုံးခန်း','ဆေးဆိုင်'],
 ['သီးသန့်ဆောင်','ကျောက်ကပ်ဆောင်','စားသောက်ခန်း','သေဆုံးခန်း'],
];
const FLOOR_LIGHTS=[0xffd9a0,0xa0ffd9,0xffa0a0,0xa0c8ff,0xffe080];
function makePlaque(){
  const cv=document.createElement('canvas'); cv.width=512; cv.height=128;
  const ctx=cv.getContext('2d'); const tex=new THREE.CanvasTexture(cv); tex.colorSpace=THREE.SRGBColorSpace;
  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(3.4,0.85), new THREE.MeshBasicMaterial({map:tex,side:THREE.DoubleSide}));
  mesh.userData.set=(txt)=>{ ctx.fillStyle='#1a0505'; ctx.fillRect(0,0,512,128); ctx.strokeStyle='#ff2222'; ctx.lineWidth=8; ctx.strokeRect(4,4,504,120); ctx.fillStyle='#ffd166'; ctx.font='bold 44px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(txt,256,64); tex.needsUpdate=true; };
  return mesh;
}
let entrancePlaque=null, exitPlaque=null, roomPlaques=[];
function updatePlaques(){
  if(entrancePlaque) entrancePlaque.userData.set('အထပ် '+S.floor+' • ဝင်ပေါက်');
  if(exitPlaque) exitPlaque.userData.set('အထပ် '+S.floor+' • ထွက်ပေါက် ↓');
  const set=ROOM_SETS[S.floor%5];
  roomPlaques.forEach((pl,i)=>{ if(pl) pl.userData.set('အထပ် '+S.floor+' • '+set[i]); });
}
function applyFloorLayout(){
  const fd=15-S.floor;
  const dx=((fd%3)-1)*3, dz=((fd%3)-1)*1.5;
  let pi=0;
  const partSlots=[[-20,-18],[20,-18],[-20,18],[20,18]];
  const partSlots2=[[-14,-12],[14,-12],[-14,12],[14,12]];
  for(const pr of props){
    if(!pr.mesh) continue;
    if(pr.label==='partition'){
      const slot=(pi%2===0)?partSlots[fd%4]:partSlots2[fd%4]; pi++;
      pr.x=slot[0]; pr.z=slot[1]; pr.mesh.position.x=slot[0]; pr.mesh.position.z=slot[1];
    } else if(['bed','surgery','cabinet','desk','shelf','slab','bed2','cabinet2','desk2','shelf2'].includes(pr.label)){
      pr.x=pr.ox+dx; pr.z=pr.oz+dz; pr.mesh.position.x=pr.x; pr.mesh.position.z=pr.z;
    }
  }
  const lc=FLOOR_LIGHTS[fd%5];
  for(let i=0;i<5 && i<lights.length;i++){ try{ lights[i].color.set(lc); }catch(e){} }
}
function setActiveGhosts(){
  if(!wanderingGhosts.length) return;
  const fd=15-S.floor; const n=wanderingGhosts.length;
  const active=[wanderingGhosts[fd%n].def.name, wanderingGhosts[(fd+2)%n].def.name, wanderingGhosts[(fd+4)%n].def.name];
  for(const wg of wanderingGhosts){
    if(active.includes(wg.def.name)){ wg.state='patrol'; wg.cooldown=0; wg.outer.visible=true; const wp=wg.def.wps[0]; if(wp) wg.outer.position.set(wp[0],0,wp[1]); }
    else { wg.state='patrol'; wg.cooldown=9999; wg.outer.visible=false; }
  }
}
function showFloorBanner(txt){ const fb=$('floorBanner'); if(!fb) return; fb.textContent=txt; fb.classList.add('on'); setTimeout(()=>fb.classList.remove('on'),3000); }
function stairY(z){ if(z<25) return 0; if(z>=37.6) return -3.08; const idx=Math.min(11,Math.floor((z-25)/1.05)); return -idx*0.28; }
let exitBlock=null, entranceBlock=null;
function closeExitDoor(){ S.doorOpen=false; if(exitBlock && !walls.includes(exitBlock)) walls.push(exitBlock); }
function closeEntranceDoor(){ S.entranceOpen=false; if(entranceBlock && !walls.includes(entranceBlock)) walls.push(entranceBlock); }
function openEntranceDoor(){ S.entranceOpen=true; S.entranceTimer=2.5; if(entranceBlock){ const i=walls.indexOf(entranceBlock); if(i>=0) walls.splice(i,1); } doorSound(); }
const $ = id => document.getElementById(id);""")

# --- addProp store mesh ---
rep("""function addProp(cx,cz,w,d,h,color,label){
  const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), new THREE.MeshStandardMaterial({color,roughness:.9}));
  m.position.set(cx,h/2,cz); scene.add(m); props.push({x:cx,z:cz,w,d,label}); return m;
}""",
"""function addProp(cx,cz,w,d,h,color,label){
  const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), new THREE.MeshStandardMaterial({color,roughness:.9}));
  m.position.set(cx,h/2,cz); scene.add(m); props.push({x:cx,z:cz,w,d,label,mesh:m,ox:cx,oz:cz}); return m;
}""")
# partitions after east wing props
rep("addProp(62,5,1,4,2.0,0x3a4a3a,'shelf2');",
"addProp(62,5,1,4,2.0,0x3a4a3a,'shelf2');\naddProp(-20,-18,5,0.6,2.2,0x3a3a3a,'partition'); addProp(-14,-12,0.6,5,2.2,0x3a3a3a,'partition'); addProp(20,18,5,0.6,2.2,0x3a3a3a,'partition');")

# --- South wall split for entrance gap + doors + stairwell ---
rep("addWall(-17,24,30,0.6); addWall(17,24,30,0.6);",
"addWall(-27,24,10,0.6); addWall(-9,24,14,0.6); addWall(17,24,30,0.6);")
rep("""const exitGlow=new THREE.Mesh(new THREE.PlaneGeometry(3.6,1), new THREE.MeshBasicMaterial({color:0xff2222}));
exitGlow.position.set(0,2.6,23.7); exitGlow.rotation.y=Math.PI; scene.add(exitGlow);""",
"""const exitGlow=new THREE.Mesh(new THREE.PlaneGeometry(3.6,1), new THREE.MeshBasicMaterial({color:0xff2222}));
exitGlow.position.set(0,2.6,23.7); exitGlow.rotation.y=Math.PI; scene.add(exitGlow);
// V13 entrance door (south, x=-19 gap) + plaques + walkable stairwell
const entranceDoor=new THREE.Mesh(new THREE.BoxGeometry(6,3.2,0.4), new THREE.MeshStandardMaterial({color:0x1a5a2a,roughness:.8,emissive:0x003300}));
entranceDoor.position.set(-19,1.6,24); scene.add(entranceDoor);
const entranceGlow=new THREE.Mesh(new THREE.PlaneGeometry(3.6,1), new THREE.MeshBasicMaterial({color:0x22ff88}));
entranceGlow.position.set(-19,2.6,23.7); entranceGlow.rotation.y=Math.PI; scene.add(entranceGlow);
exitBlock={x:0,z:24,w:4,d:0.6}; walls.push(exitBlock);
entranceBlock={x:-19,z:24,w:6,d:0.6}; walls.push(entranceBlock);
entrancePlaque=makePlaque(); entrancePlaque.position.set(-19,3.9,23.7); scene.add(entrancePlaque);
exitPlaque=makePlaque(); exitPlaque.position.set(0,3.9,23.7); scene.add(exitPlaque);
for(const [rx,rz] of [[-20,-12],[20,-12],[-20,12],[20,12]]){ const rp=makePlaque(); rp.position.set(rx,3.6,rz); scene.add(rp); roomPlaques.push(rp); }
updatePlaques();
// stairwell: side walls (collision + tall visuals), top landing, 12 steps down, landing floor + landing door
walls.push({x:-2.3,z:31.5,w:0.6,d:15}); walls.push({x:2.3,z:31.5,w:0.6,d:15}); walls.push({x:0,z:39.3,w:5.2,d:0.6});
for(const sx of [-2.3,2.3]){ const sw=new THREE.Mesh(new THREE.BoxGeometry(0.6,6.5,15), new THREE.MeshStandardMaterial({map:wallTex,roughness:.95})); sw.position.set(sx,-0.6,31.5); scene.add(sw); }
const stairTop=new THREE.Mesh(new THREE.PlaneGeometry(4,1), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9})); stairTop.rotation.x=-Math.PI/2; stairTop.position.set(0,0,24.5); scene.add(stairTop);
for(let i=0;i<12;i++){ const st=new THREE.Mesh(new THREE.BoxGeometry(4,0.28,1.05), new THREE.MeshStandardMaterial({color:0x444444,roughness:.9})); st.position.set(0,-i*0.28-0.14,25.5+i*1.05); scene.add(st); }
const landFloor=new THREE.Mesh(new THREE.PlaneGeometry(5,2.5), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9})); landFloor.rotation.x=-Math.PI/2; landFloor.position.set(0,-3.08,38.3); scene.add(landFloor);
const landDoor=new THREE.Mesh(new THREE.BoxGeometry(4,3.2,0.4), new THREE.MeshStandardMaterial({color:0x7a1010,roughness:.8,emissive:0x330000})); landDoor.position.set(0,-1.48,39); scene.add(landDoor);""")

# --- collide with stair flag ---
rep("""function collide(x,z,r){
  for(const w of walls.concat(props)){""",
"""function collide(x,z,r,allowStair){
  for(const w of walls.concat(props)){""")
rep("  x=Math.max(-31,x); x=Math.min(69,x); z=Math.max(-23,z); z=Math.min(23,z); // V12 overall: old map + corridor + east wing (was 31, blocked east wing)",
"  if(allowStair && x>=-2.3 && x<=2.3 && z>24){ x=Math.max(-2,x); x=Math.min(2,x); z=Math.max(-23,z); z=Math.min(38.5,z); } else { x=Math.max(-31,x); x=Math.min(69,x); z=Math.max(-23,z); z=Math.min(23,z); }")

# --- Ghost defs: 6 types ---
rep("""  const defs=[
    {name:'Ghost Girl', scale:0.80, color:0xe8e8e8, opacity:0.85, eye:0x000000, pos:[-18,-12], wps:[[-18,-12],[-24,-6],[0,0],[-16,0]], speed:2.5, radius:10},
    {name:'Child Ghost', scale:0.45, color:0x333333, opacity:0.9, eye:0xff0000, pos:[-24,16], wps:[[-24,16],[-16,12],[0,0],[-10,12]], speed:3.5, radius:8},
  ];""",
"""  const defs=[
    {name:'Ghost Girl', scale:0.80, color:0xe8e8e8, opacity:0.85, eye:0x000000, pos:[-18,-12], wps:[[-18,-12],[-24,-6],[0,0],[-16,0]], speed:2.5, radius:10, floatY:0.3, chaseTime:4.5, sound:'scream'},
    {name:'Child Ghost', scale:0.45, color:0x333333, opacity:0.9, eye:0xff0000, pos:[-24,16], wps:[[-24,16],[-16,12],[0,0],[-10,12]], speed:3.5, radius:8, floatY:0.1, chaseTime:3.5, sound:'giggle'},
    {name:'Nurse Ghost', scale:0.75, color:0xdddddd, opacity:0.9, eye:0x000000, pos:[24,-12], wps:[[24,-12],[16,-6],[0,0],[20,0]], speed:2.8, radius:11, floatY:0.25, chaseTime:5, sound:'whisper', cap:true},
    {name:'Shadow Ghost', scale:1.10, color:0x111111, opacity:0.95, eye:0xff0000, pos:[24,12], wps:[[24,12],[16,12],[0,0],[20,12]], speed:2.0, radius:12, floatY:0.4, chaseTime:6, sound:'growl'},
    {name:'Crawl Ghost', scale:0.50, color:0x8a7a68, opacity:0.9, eye:0xffff00, pos:[0,12], wps:[[0,12],[10,12],[-10,12],[0,0]], speed:4.0, radius:9, floatY:0.05, chaseTime:3, sound:'growl', crawl:true},
    {name:'Old Ghost', scale:0.85, color:0x999999, opacity:0.85, eye:0x000000, pos:[-28,20], wps:[[-28,20],[-20,12],[0,0],[-16,0]], speed:2.2, radius:11, floatY:0.1, chaseTime:5, sound:'moan', cane:true},
  ];""")
rep("      if(def.name==='Ghost Girl'){ for(const hx of [-0.26,0.26]){ const hair=new THREE.Mesh(new THREE.BoxGeometry(0.13,1.0,0.09),new THREE.MeshBasicMaterial({color:0x000000})); hair.position.set(hx,eyeY2-0.3,0.15); outer.add(hair); } const sheetW=new THREE.Mesh(new THREE.ConeGeometry(0.6,1.2,16,1,true), new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.35,side:THREE.DoubleSide})); sheetW.position.set(0,0.6,0); outer.add(sheetW); }",
"      if(def.name==='Ghost Girl'){ for(const hx of [-0.26,0.26]){ const hair=new THREE.Mesh(new THREE.BoxGeometry(0.13,1.0,0.09),new THREE.MeshBasicMaterial({color:0x000000})); hair.position.set(hx,eyeY2-0.3,0.15); outer.add(hair); } const sheetW=new THREE.Mesh(new THREE.ConeGeometry(0.6,1.2,16,1,true), new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.35,side:THREE.DoubleSide})); sheetW.position.set(0,0.6,0); outer.add(sheetW); }\n      if(def.cap){ const cap=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.12,0.4),new THREE.MeshBasicMaterial({color:0xffffff})); cap.position.set(0,eyeY2+0.35,0); outer.add(cap); const cross=new THREE.Mesh(new THREE.BoxGeometry(0.2,0.2,0.05),new THREE.MeshBasicMaterial({color:0xff0000})); cross.position.set(0,eyeY2+0.35,0.22); outer.add(cross); }\n      if(def.cane){ const cane=new THREE.Mesh(new THREE.BoxGeometry(0.07,1.4,0.07),new THREE.MeshBasicMaterial({color:0x5a4632})); cane.position.set(0.4,0.7,0.3); outer.add(cane); }\n      if(def.crawl){ outer.rotation.x=0.7; }")
# after loadWanderingGhosts loop, set active ghosts
rep("    if(g) wanderingGhosts.push(g);\n  }\n}",
"    if(g) wanderingGhosts.push(g);\n  }\n  if(typeof setActiveGhosts==='function') setActiveGhosts();\n}")

# --- doInteract exit: open door, not teleport ---
rep("""  } else if(t.type==='exit'){
    if(!missionComplete()){
      const fmE=floorMission();
      toast('🔒 တံခါးပိတ်နေသည် — လုပ်စရာ ကျန်သေးသည်: '+missionProgressText()+' (လိုအပ်: '+fmE.need+')');
    } else if(S.floor===1){ S.escapeDoorX=0; S.escapeDoorZ=24; startEscape(); }
    else { goToNextFloor(); }
  }""",
"""  } else if(t.type==='exit'){
    if(!missionComplete()){
      const fmE=floorMission();
      toast('🔒 တံခါးပိတ်နေသည် — လုပ်စရာ ကျန်သေးသည်: '+missionProgressText()+' (လိုအပ်: '+fmE.need+')');
    } else if(S.floor===1){ S.escapeDoorX=0; S.escapeDoorZ=24; startEscape(); }
    else if(S.doorOpen){ toast('🚪 တံခါး ပွင့်နေပြီ! လှေကားကနေ တစ်ထစ်ချင်း ဆင်းပါ'); }
    else { S.doorOpen=true; if(exitBlock){ const i=walls.indexOf(exitBlock); if(i>=0) walls.splice(i,1); } doorSound(); toast('🚪 တံခါး ပွင့်ပြီ! လှေကားကနေ တစ်ထစ်ချင်း ဆင်းပါ'); }
  }""")
# item order check includes timedorder
rep("    if((fmO.type==='order'||fmO.type==='final')){",
"    if((fmO.type==='order'||fmO.type==='final'||fmO.type==='timedorder')){")
# resetGame doors closed + entrance spawn handling (keep original spawn, close doors)
rep("  playerPos.set(-18,0,12); monsterPos.set(20,0,20); monsterState='patrol'; patrolIdx=0; S.blackout=0; S.blackoutTimer=30;",
"  playerPos.set(-18,0,12); monsterPos.set(20,0,20); monsterState='patrol'; patrolIdx=0; S.blackout=0; S.blackoutTimer=30; S.doorOpen=false; S.entranceOpen=false; S.doorAnim=0; S.entranceAnim=0; if(typeof closeExitDoor==='function') closeExitDoor(); if(typeof closeEntranceDoor==='function') closeEntranceDoor();")
# doFloorChange: entrance spawn, entrance door open, banner, close exit
rep("""  S.floor--; S.stage=1; S.switchOn=false; S.escaping=false; S.escapeProgress=0;
  playerPos.set(-18,0,12); S.yaw=Math.PI; monsterPos.set(20,0,20); monsterState='patrol'; patrolIdx=0; S.chase=false; S.scare=false; S.hidden=false; S.hideTimer=0; S.stamina=100; S.invuln=3; $('hideBtn').classList.remove('active');""",
"""  S.floor--; S.stage=1; S.switchOn=false; S.escaping=false; S.escapeProgress=0; S._landing=false;
  playerPos.set(-19,0,20); playerPos.y=0; S.yaw=Math.PI; monsterPos.set(20,0,20); monsterState='patrol'; patrolIdx=0; S.chase=false; S.scare=false; S.hidden=false; S.hideTimer=0; S.stamina=100; S.invuln=3; $('hideBtn').classList.remove('active');
  S.doorOpen=false; S.doorAnim=0; if(typeof closeExitDoor==='function') closeExitDoor(); if(typeof openEntranceDoor==='function') openEntranceDoor();""")
rep("  toast('⬇️ Ep'+fm.ep+' • အထပ် '+S.floor+' သို့ ဆင်းပြီ! '+fm.label+' '+fm.need+' ခု'+(fm.switch?' + Switch':'')+' လုပ်ပါ');",
"  toast('⬇️ Ep'+fm.ep+' • အထပ် '+S.floor+' သို့ ဆင်းပြီ! '+fm.label+' '+fm.need+' ခု'+(fm.switch?' + Switch':'')+' လုပ်ပါ');\n  if(typeof showFloorBanner==='function') showFloorBanner('🏢 အထပ် '+S.floor+' • Ep'+fm.ep);")
# goToNextFloor: keep for legacy but landing now uses it? Replace its body to be landing fade only (called from landing trigger)
rep("function goToNextFloor(){\n  if(S.floor<=1) return;",
"function goToNextFloor(){\n  if(S.floor<=1) return;\n  if(S._landingFade) return; S._landingFade=true;\n  S.paused=true; const ss=$('stairScreen'); if(ss) ss.classList.add('on'); const st=$('stairText'); if(st) st.textContent='အထပ် '+(S.floor-1)+' သို့ ဝင်နေသည်…'; const sub=$('stairSub'); if(sub) sub.textContent='Ep'+(16-S.floor)+' → Ep'+(17-S.floor);\n  setTimeout(()=>{ if(ss) ss.classList.remove('on'); S._landingFade=false; S.paused=false; doFloorChange(); },900); return;")

open(p,'w',encoding='utf-8').write(t)
print("PATCH PART1 OK")
