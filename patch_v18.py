import sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# 1. FPP state + HUD ghost count + Pause FPP toggle button
rep("  <div id=\"objective\">🎯 Ward သော့ ရှာပါ</div>",
"  <div id=\"objective\">🎯 Ward သော့ ရှာပါ</div>\n      <div id=\"ghostCount\">👻 သရဲ —</div>")
rep("""  <div class="row">
    <button class="btn ghost" id="sizeDownBtn">👤− Character သေး</button>
    <button class="btn ghost" id="sizeUpBtn">👤+ Character ကြီး</button>
  </div>""",
"""  <div class="row">
    <button class="btn ghost" id="sizeDownBtn">👤− Character သေး</button>
    <button class="btn ghost" id="sizeUpBtn">👤+ Character ကြီး</button>
  </div>
  <div class="row">
    <button class="btn ghost" id="fppBtn">👁️ FPP (အခု) — TPP ပြောင်း</button>
  </div>""")
rep("  <p style=\"font-size:11px;color:#666;margin-top:8px\">V17 • Dead Body အစစ် + သွေးအစစ်</p>",
"  <p style=\"font-size:11px;color:#666;margin-top:8px\">V18 • FPP + သရဲရှေ့တည့်တည့် ပေါ်လာ + ကွင်းဖျောက် + သော့လမ်းကြောင်း</p>")
# S.fpp default true
rep("const S = {playing:false, paused:false,",
"const S = {fpp:true, frontScareTimer:30, ghostFaceUntil:0, pathTimer:0, lastPathTX:0, lastPathTZ:0, activeGhostCount:0, playing:false, paused:false,")

# 2. Hide rings at creation + in update
rep("const playerRing=new THREE.Mesh(new THREE.RingGeometry(0.5,0.65,24), new THREE.MeshBasicMaterial({color:0x00ff88,transparent:true,opacity:0.7,side:THREE.DoubleSide})); playerRing.rotation.x=-Math.PI/2; scene.add(playerRing);",
"const playerRing=new THREE.Mesh(new THREE.RingGeometry(0.5,0.65,24), new THREE.MeshBasicMaterial({color:0x00ff88,transparent:true,opacity:0.7,side:THREE.DoubleSide})); playerRing.rotation.x=-Math.PI/2; playerRing.visible=false; scene.add(playerRing);")
rep("const monsterRing=new THREE.Mesh(new THREE.RingGeometry(1.0,1.2,24), new THREE.MeshBasicMaterial({color:0xff2222,transparent:true,opacity:0.8,side:THREE.DoubleSide})); monsterRing.rotation.x=-Math.PI/2; scene.add(monsterRing);",
"const monsterRing=new THREE.Mesh(new THREE.RingGeometry(1.0,1.2,24), new THREE.MeshBasicMaterial({color:0xff2222,transparent:true,opacity:0.8,side:THREE.DoubleSide})); monsterRing.rotation.x=-Math.PI/2; monsterRing.visible=false; scene.add(monsterRing);")

# 3. Gap frames (green glowing door frames at all gaps) - insert after beacon creation
rep("""const beacon=new THREE.Mesh(new THREE.CylinderGeometry(0.25,0.25,7,12), new THREE.MeshBasicMaterial({color:0xffd700,transparent:true,opacity:0.6,depthTest:false,fog:false}));
beacon.renderOrder=999; beacon.position.set(0,3.5,24); scene.add(beacon);""",
"""const beacon=new THREE.Mesh(new THREE.CylinderGeometry(0.25,0.25,7,12), new THREE.MeshBasicMaterial({color:0xffd700,transparent:true,opacity:0.6,depthTest:false,fog:false}));
beacon.renderOrder=999; beacon.position.set(0,3.5,24); scene.add(beacon);
// V18 gap frames: green glowing door frames so gaps are obvious, not hidden dark holes
function makeGapFrame(cx,cz,alongX){
  const mat=new THREE.MeshBasicMaterial({color:0x00ff88,transparent:true,opacity:0.85});
  const len=alongX?8:6, th=0.35;
  for(const s of [-1,1]){
    const pil=new THREE.Mesh(new THREE.BoxGeometry(alongX?th:th,3.4,alongX?th:th),mat);
    if(alongX) pil.position.set(cx+s*len/2,1.7,cz); else pil.position.set(cx,1.7,cz+s*len/2);
    scene.add(pil);
  }
  const beam=new THREE.Mesh(new THREE.BoxGeometry(alongX?len+0.4:th,0.3,alongX?th:len+0.4),mat);
  beam.position.set(cx,3.3,cz); scene.add(beam);
}
for(const gx of [-16,0,16]){ makeGapFrame(gx,-3,true); makeGapFrame(gx,3,true); }
makeGapFrame(-4,0,false); makeGapFrame(4,0,false);
// V18 gold path dots pool (BFS route to objective, visible through walls)
const pathDots=[];
for(let i=0;i<30;i++){
  const d=new THREE.Mesh(new THREE.CircleGeometry(0.35,12), new THREE.MeshBasicMaterial({color:0xffd700,transparent:true,opacity:0.9,depthTest:false,fog:false}));
  d.rotation.x=-Math.PI/2; d.renderOrder=998; d.visible=false; scene.add(d); pathDots.push(d);
}
function computePathDots(tx,tz){
  // BFS on 1m grid, walkable = collide() does not push out
  const sx=Math.round(playerPos.x), sz=Math.round(playerPos.z), ex=Math.round(tx), ez=Math.round(tz);
  const key=(x,z)=>x+','+z; const q=[[sx,sz]]; const parent={}; parent[key(sx,sz)]=null; const seen=new Set([key(sx,sz)]);
  let found=null;
  while(q.length){
    const [x,z]=q.shift();
    if(Math.abs(x-ex)<=1 && Math.abs(z-ez)<=1){ found=[x,z]; break; }
    for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
      const nx=x+dx, nz=z+dz; if(seen.has(key(nx,nz))) continue;
      if(nx<-31||nx>69||nz<-23||nz>23) continue;
      const cp=collide(nx,nz,0.45); if(Math.abs(cp[0]-nx)>0.01||Math.abs(cp[1]-nz)>0.01) continue;
      seen.add(key(nx,nz)); parent[key(nx,nz)]=[x,z]; q.push([nx,nz]);
    }
  }
  if(!found) return;
  const path=[]; let cur=found;
  while(cur){ path.push(cur); cur=parent[key(cur[0],cur[1])]; }
  path.reverse();
  let di=0;
  for(let i=2;i<path.length && di<pathDots.length;i+=2){ const [px,pz]=path[i]; pathDots[di].position.set(px,0.12,pz); pathDots[di].visible=true; di++; }
  for(let j=di;j<pathDots.length;j++) pathDots[j].visible=false;
}""")

# 4. setActiveGhosts: store count
rep("  const active=[wanderingGhosts[fd%n].def.name, wanderingGhosts[(fd+1)%n].def.name, wanderingGhosts[(fd+2)%n].def.name, wanderingGhosts[(fd+3)%n].def.name, wanderingGhosts[(fd+4)%n].def.name];",
"  const active=[wanderingGhosts[fd%n].def.name, wanderingGhosts[(fd+1)%n].def.name, wanderingGhosts[(fd+2)%n].def.name, wanderingGhosts[(fd+3)%n].def.name, wanderingGhosts[(fd+4)%n].def.name]; S.activeGhostCount=active.length;")

# 5. Ghost emissive (visible in dark) - loadOne real branch + wandering build
rep("      if(opts.real){ /* real ghost texture kept as-is, no pale recolor */ }",
"      if(opts.real){ inner.traverse(o=>{ if(o.isMesh && o.material && o.material.emissive){ o.material.emissive.set(0x440000); } }); }")
rep("      if(def.real && useReal){ /* keep original ghost texture */ }",
"      if(def.real && useReal){ inner.traverse(o=>{ if(o.isMesh && o.material && o.material.emissive){ o.material.emissive.set(0x330000); } }); }")

# 6. Wandering cooldown shorter (ghosts alive, not dead)
rep("      if(wg.scareTimer<=0){ wg.state='patrol'; wg.cooldown=12+Math.random()*6; wg.outer.visible=false; toast('👻 '+wg.def.name+' ပျောက်သွားပြီ…'); }",
"      if(wg.scareTimer<=0){ wg.state='patrol'; wg.cooldown=3+Math.random()*3; wg.outer.visible=false; toast('👻 '+wg.def.name+' ပျောက်သွားပြီ… (ခဏနေ ပြန်ပေါ်မယ်)'); }")

# 7. Player visible + rings in update, FPP camera
rep("  if(player){ player.position.copy(playerPos); player.rotation.y=playerAngle; player.visible=!S.hidden; }\n  playerRing.visible=!S.hidden; // V9: ring also hid, otherwise user sees green ring and thinks hide failed",
"  if(player){ player.position.copy(playerPos); player.rotation.y=playerAngle; player.visible=S.fpp?false:!S.hidden; }\n  playerRing.visible=false; monsterRing.visible=false; // V18 user: hide bottom rings")
rep("""  // camera: behind player, pulled in if a wall would block the view (V3 FIX:
  // old camera went through/ outside walls, hiding the player behind a wall)
  const camDist=4.5, camH=playerPos.y+1.9;
  const cx=playerPos.x - Math.sin(S.yaw)*camDist, cz=playerPos.z - Math.cos(S.yaw)*camDist;
  let useX=cx, useZ=cz, found=false;
  for(let tt=1; tt>=0.3; tt-=0.1){
    const px=playerPos.x+(cx-playerPos.x)*tt, pz=playerPos.z+(cz-playerPos.z)*tt;
    let blocked=false;
    for(const w of walls){ if(Math.abs(px-w.x)<w.w/2+0.3 && Math.abs(pz-w.z)<w.d/2+0.3){ blocked=true; break; } }
    if(!blocked){ useX=px; useZ=pz; found=true; break; }
  }
  if(!found){ useX=playerPos.x+(cx-playerPos.x)*0.3; useZ=playerPos.z+(cz-playerPos.z)*0.3; }
  useX=Math.max(-31,Math.min(69,useX)); useZ=Math.max(-23,Math.min(S.inStair?38.5:23,useZ));
  camera.position.set(useX,camH,useZ);
  if(S.chase||S.scare||wanderingScare||S.escaping||S.blackout>0){ const sh=S.scare?0.45:(S.chase||S.escaping?0.25:(S.blackout>0?0.20:0.35)); camera.position.x+=(Math.random()-0.5)*sh; camera.position.y+=(Math.random()-0.5)*sh*0.7; } // V12 stronger shake
  camera.lookAt(playerPos.x,playerPos.y+1.35,playerPos.z);""",
"""  // V18 FPP default: camera at eye, no TPP pull-in, camera cannot go through walls (it is at player)
  if(S.fpp){
    camera.position.set(playerPos.x+Math.sin(S.yaw)*0.2, playerPos.y+1.65, playerPos.z+Math.cos(S.yaw)*0.2);
    if(S.chase||S.scare||wanderingScare||S.escaping||S.blackout>0){ const sh=S.scare?0.45:(S.chase||S.escaping?0.25:(S.blackout>0?0.20:0.35)); camera.position.x+=(Math.random()-0.5)*sh; camera.position.y+=(Math.random()-0.5)*sh*0.7; }
    camera.lookAt(playerPos.x+Math.sin(S.yaw)*10, playerPos.y+1.55, playerPos.z+Math.cos(S.yaw)*10);
  } else {
    const camDist=4.5, camH=playerPos.y+1.9;
    const cx=playerPos.x - Math.sin(S.yaw)*camDist, cz=playerPos.z - Math.cos(S.yaw)*camDist;
    let useX=cx, useZ=cz, found=false;
    for(let tt=1; tt>=0.3; tt-=0.1){
      const px=playerPos.x+(cx-playerPos.x)*tt, pz=playerPos.z+(cz-playerPos.z)*tt;
      let blocked=false;
      for(const w of walls){ if(Math.abs(px-w.x)<w.w/2+0.3 && Math.abs(pz-w.z)<w.d/2+0.3){ blocked=true; break; } }
      if(!blocked){ useX=px; useZ=pz; found=true; break; }
    }
    if(!found){ useX=playerPos.x+(cx-playerPos.x)*0.3; useZ=playerPos.z+(cz-playerPos.z)*0.3; }
    useX=Math.max(-31,Math.min(69,useX)); useZ=Math.max(-23,Math.min(S.inStair?38.5:23,useZ));
    camera.position.set(useX,camH,useZ);
    if(S.chase||S.scare||wanderingScare||S.escaping||S.blackout>0){ const sh=S.scare?0.45:(S.chase||S.escaping?0.25:(S.blackout>0?0.20:0.35)); camera.position.x+=(Math.random()-0.5)*sh; camera.position.y+=(Math.random()-0.5)*sh*0.7; }
    camera.lookAt(playerPos.x,playerPos.y+1.35,playerPos.z);
  }""")
# flashlight height in FPP
rep("  flash.position.set(playerPos.x,playerPos.y+2.2,playerPos.z);",
"  flash.position.set(playerPos.x,playerPos.y+(S.fpp?1.65:2.2),playerPos.z);")

# 8. HUD ghost count
rep("  $('hideTag').style.display=S.hidden?'block':'none';",
"  $('hideTag').style.display=S.hidden?'block':'none';\n  const gc=$('ghostCount'); if(gc) gc.textContent='👻 သရဲ '+((S.activeGhostCount||5)+1)+' ကောင် + Monster လှည့်နေ';")

# 9. Front jumpscare + path dots update + ghostFace during front scare - insert before V14 anti-stuck block
rep("  // V14 anti-stuck:",
"""  // V18 front jumpscare: ghost appears suddenly 2.5m in front of player, in your face (FPP = fills screen)
  if(S.playing && !S.paused && !S.hidden && S.invuln<=0){
    S.frontScareTimer-=dt;
    if(S.frontScareTimer<=0){
      S.frontScareTimer=35+Math.random()*20;
      const fx=playerPos.x+Math.sin(S.yaw)*2.5, fz=playerPos.z+Math.cos(S.yaw)*2.5;
      const fp=collide(fx,fz,0.5);
      if(Math.hypot(fp[0]-playerPos.x,fp[1]-playerPos.z)>1.2 && !lineBlocked(playerPos.x,playerPos.z,fp[0],fp[1])){
        if(monsterState!=='chase'){
          monsterPos.set(fp[0],0,fp[1]); monsterAngle=Math.atan2(playerPos.x-fp[0],playerPos.z-fp[1]); monsterState='scare'; S.scare=true; S.scareTimer=1.5;
        } else {
          const actWg=wanderingGhosts.find(wg=>wg.outer && wg.outer.visible && wg.state==='patrol');
          if(actWg){ actWg.outer.position.set(fp[0],0,fp[1]); actWg.outer.rotation.y=Math.atan2(playerPos.x-fp[0],playerPos.z-fp[1]); actWg.state='scare'; actWg.scareTimer=1.5; wanderingScare=true; }
        }
        S.ghostFaceUntil=S.time+1.0; screamSound(); scareSound(); if(navigator.vibrate) navigator.vibrate(200); toast('👻 သရဲ ရှေ့တည့်တည့် ပေါ်လာပြီ!');
      }
    }
  }
  const gf=$('ghostFace'); if(gf) gf.style.display=(S.time<S.ghostFaceUntil || (S.chase && Math.hypot(monsterPos.x-playerPos.x,monsterPos.z-playerPos.z)<3))?'block':'none';
  // V18 path dots: recompute every 1s to beacon target
  S.pathTimer-=dt;
  if(S.pathTimer<=0){ S.pathTimer=1.0; if(typeof computePathDots==='function' && (S.beaconX!==S.lastPathTX || S.beaconZ!==S.lastPathTZ)){ S.lastPathTX=S.beaconX; S.lastPathTZ=S.beaconZ; try{ computePathDots(S.beaconX,S.beaconZ); }catch(e){} } }
  // V14 anti-stuck:""")

# 10. FPP toggle button handler - after size buttons
rep("$('sizeUpBtn').addEventListener('click',()=>setCharSize(charScaleFactor+0.1));",
"""$('sizeUpBtn').addEventListener('click',()=>setCharSize(charScaleFactor+0.1));
$('fppBtn').addEventListener('click',()=>{ S.fpp=!S.fpp; $('fppBtn').textContent=S.fpp?'👁️ FPP (အခု) — TPP ပြောင်း':'👁️ TPP (အခု) — FPP ပြောင်း'; });""")

open(p,'w',encoding='utf-8').write(t)
print("V18 PATCH OK")
