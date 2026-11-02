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

rep("V52 • ထပ်တိုင်း မြေပုံ မတူ — အခန်းထဲ အတွင်းနံရံ + corridor နံရံ ထပ်တိုင်း ကွဲ — အကုန်",
    "V53 • အကုန် ခက်အောင် + smooth + ပြတင်းပေါက် — အကုန်",
    "version v53")
# --- Harder: monster ---
rep("  let mSpeed=3.8+S.keys*0.2, target=null; // V49: patrol faster, monster feels present",
    "  let mSpeed=4.2+S.keys*0.2, target=null; // V53 harder: patrol faster",
    "monster patrol v53")
rep("    mSpeed=6.4+(S.floor===15?S.keys*0.2:S.items*0.05)+(15-S.floor)*0.15; if(S.escaping) mSpeed+=1.0; if(mSpeed>8.5) mSpeed=8.5; // V47 harder: +0.15/floor, cap 8.5",
    "    mSpeed=7.2+(S.floor===15?S.keys*0.2:S.items*0.05)+(15-S.floor)*0.2; if(S.escaping) mSpeed+=1.0; if(mSpeed>9.2) mSpeed=9.2; // V53 harder: +0.2/floor, cap 9.2",
    "monster chase speed v53")
rep("  const canSee=!S.hidden && (S.floor!==15 || S.keys>=1) && monsterState!=='scare' && mDist<24 && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V47 Ep1 wakes up after Key1",
    "  const canSee=!S.hidden && (S.floor!==15 || S.keys>=1) && monsterState!=='scare' && mDist<28 && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V53 harder: detection 28m",
    "monster detection v53")
rep("    if(S.catchTimer>Math.max(0.40,0.65-(15-S.floor)*0.02)){ S.catchTimer=0; loseHeart(); } // V47 harder: grace to 0.40s at bottom",
    "    if(S.catchTimer>Math.max(0.30,0.55-(15-S.floor)*0.02)){ S.catchTimer=0; loseHeart(); } // V53 harder: grace to 0.30s at bottom",
    "catch grace v53")
rep("S.glimpseTimer=60; S.glimpseUntil=0; S.huntTimer=150;",
    "S.glimpseTimer=60; S.glimpseUntil=0; S.huntTimer=90;",
    "hunt initial v53")
rep("      if(typeof S.huntTimer!=='number') S.huntTimer=150;",
    "      if(typeof S.huntTimer!=='number') S.huntTimer=90;",
    "hunt guard v53")
rep("        S.huntTimer=180+Math.random()*60;",
    "        S.huntTimer=120+Math.random()*60; // V53 harder: hunts more often",
    "hunt interval v53")
rep("      S.frontScareTimer=60+Math.random()*30; // V49: front scare every 60-90s",
    "      S.frontScareTimer=45+Math.random()*30; // V53 harder: front/behind scare every 45-75s",
    "front scare interval v53")
# --- Harder: stamina ---
rep("  if(running)S.stamina=Math.max(0,S.stamina-(30+(15-S.floor)*1)*dt); else S.stamina=Math.min(100,S.stamina+12*dt); // V12 harder down: drain +1/floor",
    "  if(running)S.stamina=Math.max(0,S.stamina-(38+(15-S.floor)*1.5)*dt); else if(!moving) S.stamina=Math.min(100,S.stamina+10*dt); // V53 harder: drain faster, regen only when standing still (walking does not regen)",
    "stamina v53")
# --- Harder: compass limit on lower floors ---
rep("  $('compass').textContent='🧭 '+dirs[((idx%8)+8)%8]+' '+Math.round(Math.hypot(tx-playerPos.x,tz-playerPos.z))+'m';",
    "  const compDist=S.floor<=10?'':(' '+Math.round(Math.hypot(tx-playerPos.x,tz-playerPos.z))+'m'); $('compass').textContent='🧭 '+dirs[((idx%8)+8)%8]+compDist; // V53 harder: lower floors show direction only, no exact metres",
    "compass limit v53")
# --- Harder: medkit rarer ---
rep("  // medkit respawns each floor (survival across 15 floors needs it)\n  medkitTaken=false; if(typeof medkitMesh!=='undefined' && medkitMesh) medkitMesh.visible=true;",
    "  // V53 harder: medkit only every 3rd floor (15,12,9,6,3), not every floor\n  if(S.floor%3===0){ medkitTaken=false; if(typeof medkitMesh!=='undefined' && medkitMesh) medkitMesh.visible=true; } else { medkitTaken=true; if(typeof medkitMesh!=='undefined' && medkitMesh) medkitMesh.visible=false; }",
    "medkit rarer v53")
# --- Harder: escape hold 8 -> 10s ---
rep("      S.escapeProgress+=dt/8;",
    "      S.escapeProgress+=dt/10; // V53 harder: Final Escape hold 10s (was 8s)",
    "escape hold v53")
rep("  toast('🚨 တံခါး ဖွင့်နေသည်! သရဲတွေ အားလုံး လာနေပြီ! တံခါးနား ၈ စက္ကန့် ခံပါ!');",
    "  toast('🚨 တံခါး ဖွင့်နေသည်! သရဲတွေ အားလုံး လာနေပြီ! တံခါးနား ၁၀ စက္ကန့် ခံပါ!');",
    "escape toast v53")
# --- Harder: wandering ghosts also catch (chase state only, fair grace) ---
rep("  // V9 distant moan every ~18-30s so the hospital never feels silent",
    """  // V53 wandering ghosts also dangerous: chase-state ghost within 1.4m for 0.5s = heart loss. Scare teleport does NOT catch (fair: chase is visible, run/hide works).
  if(!S.won && S.invuln<=0 && !S.hidden){
    let wgCatch=null;
    for(const wg of wanderingGhosts){ if(wg.active!==false && wg.outer && wg.outer.visible && wg.state==='chase' && Math.hypot(wg.outer.position.x-playerPos.x,wg.outer.position.z-playerPos.z)<1.4){ wgCatch=wg; break; } }
    if(wgCatch){ if(typeof S.wanderCatchTimer!=='number') S.wanderCatchTimer=0; S.wanderCatchTimer+=dt; if(S.wanderCatchTimer>0.5){ S.wanderCatchTimer=0; wgCatch.state='scare'; wgCatch.scareTimer=2.0; loseHeart(); } } else S.wanderCatchTimer=0;
  } else S.wanderCatchTimer=0;
  // V9 distant moan every ~18-30s so the hospital never feels silent""",
    "wandering catch v53")
# --- Harder: catch drops a key/item ---
rep("""function loseHeart(){
  S.hearts--; S.invuln=3; scareSound(); screamSound(); if(navigator.vibrate) navigator.vibrate([200,100,200]);
  const js=$('jumpscare'); if(js){ js.style.display='none'; }
  const d=$('damage'); d.style.opacity=1; setTimeout(()=>d.style.opacity=0,400);
  toast('💔 ဖမ်းခံရပြီ! အသက် '+S.hearts+' ခု ကျန်သည်');""",
    """function loseHeart(){
  S.hearts--; S.invuln=3; scareSound(); screamSound(); if(navigator.vibrate) navigator.vibrate([200,100,200]);
  const js=$('jumpscare'); if(js){ js.style.display='none'; }
  const d=$('damage'); d.style.opacity=1; setTimeout(()=>d.style.opacity=0,400);
  // V53 catch cost: drop one key/item (must re-collect), not just a heart
  let dropped='';
  if(S.keys>0){ const takenKeys=keyMeshes.filter(km=>km.taken && km.def.id<=KEYS_NEEDED); const dk=takenKeys[takenKeys.length-1]; if(dk){ dk.taken=false; dk.mesh.visible=true; S.keys--; dropped=' 🔑 '+dk.def.label+' ကျသွားပြီ! ပြန်ကောက်ပါ'; } }
  else if(S.items>0){ const fmD=floorMission(); const takenItems=itemMeshes.filter((im,idx)=>im.taken && idx<fmD.need); const di=takenItems[takenItems.length-1]; if(di){ di.taken=false; di.mesh.visible=true; S.items--; dropped=' 📦 '+di.def.label+' ကျသွားပြီ! ပြန်ကောက်ပါ'; } }
  toast('💔 ဖမ်းခံရပြီ! အသက် '+S.hearts+' ခု ကျန်သည်'+dropped);""",
    "key/item drop v53")
# --- Harder: key positions random per fresh game ---
rep("/* ============ GAME FLOW ============ */\nfunction resetGame(){",
    "/* ============ GAME FLOW ============\nlet _skipKeyShuffle=false; // V53: Continue must NOT reshuffle keys\nfunction resetGame(){",
    "key shuffle flag v53")
rep("  for(const km of keyMeshes){ km.taken=false; km.mesh.visible=true; }\n  for(const km of keyMeshes){ if(km.def.id>KEYS_NEEDED){ km.taken=true; km.mesh.visible=false; } } // V12 floor15: only 3 keys\n  startFloorMission();",
    """  for(const km of keyMeshes){ km.taken=false; km.mesh.visible=true; }
  for(const km of keyMeshes){ if(km.def.id>KEYS_NEEDED){ km.taken=true; km.mesh.visible=false; } } // V12 floor15: only 3 keys
  // V53 key positions random per fresh game (labels stay with id, compass points to new positions)
  if(!_skipKeyShuffle){
    const first3=keyMeshes.filter(km=>km.def.id<=KEYS_NEEDED);
    const pos=first3.map(km=>[km.def.x,km.def.z]);
    for(let i=pos.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const tmp=pos[i]; pos[i]=pos[j]; pos[j]=tmp; }
    first3.forEach((km,i)=>{ km.def.x=pos[i][0]; km.def.z=pos[i][1]; km.mesh.position.set(pos[i][0],1.1,pos[i][1]); });
  }
  _skipKeyShuffle=false;
  startFloorMission();""",
    "key shuffle v53")
rep("function continueGame(){ let sv=null; try{ sv=JSON.parse(localStorage.getItem('nh_save')||'null'); }catch(e){} startGame();",
    "function continueGame(){ let sv=null; try{ sv=JSON.parse(localStorage.getItem('nh_save')||'null'); }catch(e){} _skipKeyShuffle=true; startGame();",
    "continue skip shuffle v53")
# --- Smooth: velocity + angle + FOV + pixelRatio + stamina transition + HUD cache ---
rep("const clock=new THREE.Clock();\nlet heartBeatAcc=0, stepAcc=0, growlAcc=0, whisperAcc=0;",
    "const clock=new THREE.Clock();\nlet heartBeatAcc=0, stepAcc=0, growlAcc=0, whisperAcc=0;\nlet smoothVX=0, smoothVZ=0; // V53 smooth movement velocity",
    "smooth velocity vars v53")
rep("""  if(moving){
    const np=collide(playerPos.x+mx*speed*dt, playerPos.z+mz*speed*dt, 0.45, true);
    playerPos.x=np[0]; playerPos.z=np[1];
    playerAngle=Math.atan2(mx,mz);
  }""",
    """  // V53 smooth movement: velocity lerps to target, no instant start/stop snap; model angle lerps too
  const targetVX=moving?mx*speed:0, targetVZ=moving?mz*speed:0;
  const vk=Math.min(1,dt*10);
  smoothVX+=(targetVX-smoothVX)*vk; smoothVZ+=(targetVZ-smoothVZ)*vk;
  if(!moving && Math.abs(smoothVX)<0.01 && Math.abs(smoothVZ)<0.01){ smoothVX=0; smoothVZ=0; }
  if(smoothVX!==0 || smoothVZ!==0){
    const np=collide(playerPos.x+smoothVX*dt, playerPos.z+smoothVZ*dt, 0.45, true);
    playerPos.x=np[0]; playerPos.z=np[1];
    if(moving){
      const targetAngle=Math.atan2(mx,mz);
      let ad=((targetAngle-playerAngle+Math.PI*3)%(Math.PI*2))-Math.PI;
      playerAngle+=ad*Math.min(1,dt*12);
    }
  }""",
    "smooth movement v53")
rep("  if(moving && floorMission().type==='distance' && !S.missionDone){ S.distance+=speed*dt; }",
    "  if(moving && floorMission().type==='distance' && !S.missionDone){ S.distance+=Math.hypot(smoothVX,smoothVZ)*dt; } // V53: distance from actual smooth velocity",
    "distance smooth v53")
rep("  const wantFov=S.chase?75:62; if(camera.fov!==wantFov){ camera.fov=wantFov; camera.updateProjectionMatrix(); }",
    "  const wantFov=S.chase?75:62; if(Math.abs(camera.fov-wantFov)>0.01){ camera.fov+=(wantFov-camera.fov)*Math.min(1,dt*6); camera.updateProjectionMatrix(); } // V53 smooth FOV, no snap zoom",
    "smooth FOV v53")
rep("renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));",
    "renderer.setPixelRatio(Math.min(devicePixelRatio,1.5)); // V53 smooth FPS: cap 1.5 (was 1.75, heavy on phone GPU)",
    "pixelRatio v53")
rep("try{ renderer.setPixelRatio(S.lowQuality?1:Math.min(devicePixelRatio,1.75)); }catch(e){}",
    "try{ renderer.setPixelRatio(S.lowQuality?1:Math.min(devicePixelRatio,1.5)); }catch(e){}",
    "pixelRatio quality v53")
rep("#staminaFill{height:100%;width:100%;background:#ffd166}",
    "#staminaFill{height:100%;width:100%;background:#ffd166;transition:width .15s linear}",
    "stamina transition v53")
rep("""function updateHUD(){
  $('hearts').textContent='❤️'.repeat(Math.max(0,S.hearts));
  { const fmH=floorMission(); if(fmH.type==='keys') $('keys').textContent='🔑 '+S.keys+' / 3'; else if(['order','dark','timed','final','timedorder'].includes(fmH.type)) $('keys').textContent='📦 '+S.items+' / '+fmH.need; else $('keys').textContent='🎯 '+missionProgressText(); }
  const fi=$('floorInfo'); if(fi) fi.textContent='🏢 '+S.floor+' လွှာ • Ep'+floorEp()+(S.floor===1?' • FINAL':'');
  $('staminaFill').style.width=S.stamina+'%';
  $('chase').style.display=S.chase?'block':'none';
  $('hideTag').style.display=S.hidden?'block':'none';
  $('actBtn').disabled=!S.interactTarget;
  $('actBtn').textContent=S.interactTarget?((S.interactTarget.type==='exit')?'✋ လှေကား ဆင်း':((S.interactTarget.type==='exit2'||S.interactTarget.type==='switch')?'✋ ဖွင့်':'✋ ယူ')):'✋ ယူ';
}""",
    """function updateHUD(){
  // V53 smooth UI: only touch DOM when text/display actually changed (was every frame, causing phone UI jank)
  if(!S._hudCache) S._hudCache={};
  const hc=S._hudCache;
  const heartsTxt='❤️'.repeat(Math.max(0,S.hearts));
  if(hc.hearts!==heartsTxt){ $('hearts').textContent=heartsTxt; hc.hearts=heartsTxt; }
  let keysTxt; { const fmH=floorMission(); if(fmH.type==='keys') keysTxt='🔑 '+S.keys+' / 3'; else if(['order','dark','timed','final','timedorder'].includes(fmH.type)) keysTxt='📦 '+S.items+' / '+fmH.need; else keysTxt='🎯 '+missionProgressText(); }
  if(hc.keys!==keysTxt){ $('keys').textContent=keysTxt; hc.keys=keysTxt; }
  const floorTxt='🏢 '+S.floor+' လွှာ • Ep'+floorEp()+(S.floor===1?' • FINAL':'');
  if(hc.floor!==floorTxt){ const fi=$('floorInfo'); if(fi) fi.textContent=floorTxt; hc.floor=floorTxt; }
  $('staminaFill').style.width=S.stamina+'%';
  if(hc.chase!==S.chase){ $('chase').style.display=S.chase?'block':'none'; hc.chase=S.chase; }
  if(hc.hide!==S.hidden){ $('hideTag').style.display=S.hidden?'block':'none'; hc.hide=S.hidden; }
  const actDisabled=!S.interactTarget;
  const actTxt=S.interactTarget?((S.interactTarget.type==='exit')?'✋ လှေကား ဆင်း':((S.interactTarget.type==='exit2'||S.interactTarget.type==='switch')?'✋ ဖွင့်':'✋ ယူ')):'✋ ယူ';
  if(hc.actD!==actDisabled){ $('actBtn').disabled=actDisabled; hc.actD=actDisabled; }
  if(hc.actT!==actTxt){ $('actBtn').textContent=actTxt; hc.actT=actTxt; }
}""",
    "HUD cache v53")
# --- Windows on outer walls only ---
rep("addWall(84.5,-17.5,0.6,25); addWall(84.5,17.5,0.6,25);",
    """addWall(84.5,-17.5,0.6,25); addWall(84.5,17.5,0.6,25);
// V53 windows: outer walls ONLY (north z=-30, south z=30), NOT interior partitions. One shared canvas texture + geometry/material, 22 windows, visual only, no collision.
{
  const wcv=document.createElement('canvas'); wcv.width=256; wcv.height=144;
  const wg=wcv.getContext('2d');
  wg.fillStyle='#0a1420'; wg.fillRect(0,0,256,144);
  wg.fillStyle='#1a2a3a'; for(let i=0;i<20;i++){ wg.fillRect(10+Math.random()*236,10+Math.random()*124,20,12); }
  wg.fillStyle='#000000'; wg.beginPath(); wg.moveTo(30,30); wg.lineTo(80,50); wg.lineTo(50,90); wg.closePath(); wg.fill();
  wg.fillStyle='#222222'; wg.fillRect(0,0,256,10); wg.fillRect(0,134,256,10); wg.fillRect(0,0,10,144); wg.fillRect(246,0,10,144); wg.fillRect(123,0,10,144); wg.fillRect(0,67,256,10);
  const wtex=new THREE.CanvasTexture(wcv); wtex.colorSpace=THREE.SRGBColorSpace;
  const wgeo=new THREE.PlaneGeometry(3,1.8);
  const wmat=new THREE.MeshStandardMaterial({map:wtex,roughness:.4,metalness:.1});
  for(const dc of NORTH_CENTRES){ const m=new THREE.Mesh(wgeo,wmat); m.position.set(dc,1.9,-29.6); scene.add(m); }
  for(const dc of SOUTH_CENTRES){ const m=new THREE.Mesh(wgeo,wmat); m.position.set(dc,1.9,29.6); m.rotation.y=Math.PI; scene.add(m); }
}""",
    "windows v53")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V53 applied')
