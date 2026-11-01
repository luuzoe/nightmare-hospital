import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
miss = []
def rep(old, new, name):
    global t
    if old not in t:
        miss.append(name)
        print('MISS:', name)
    else:
        t = t.replace(old, new, 1)
        print('OK:', name)

rep("V33 • တိတ်ဆိတ် + ရုတ်တရက် ကြောက် — သရဲမ အသံ ရှားရှား, အသံ နည်းနည်း",
    "V34 • Minimap + လက်ထဲ ဓာတ်မီး + Settings + Save တိုးတက်မှု — အကုန်",
    "version")

# Timer reset bug + toast wording
rep("S.time=0; S.shadowScare=false;",
    "S.time=0; lastGirlTime=-999; nextTwitch=25; S.frontScareTimer=50; S.randScareTimer=50; S.whisperTimer=0; S.shadowScare=false;",
    "timer reset")
rep("toast('👻 '+wg.def.name+' မိတော့မယ်!');",
    "toast('👻 '+wg.def.name+' ကြောက်စရာ!');",
    "toast wording")

# S settings fields
rep("randScareTimer:50};",
    "randScareTimer:50, showMap:true, showHands:true, camSpeed:1, volume:1, lowQuality:false};",
    "S settings")

# Minimap HTML + topbar button
rep('<div id="toast"></div>',
    '<div id="toast"></div>\n  <canvas id="minimap" width="150" height="75" style="position:fixed;top:64px;right:10px;z-index:20;pointer-events:none;background:rgba(0,0,0,0.6);border:1px solid #444;border-radius:6px"></canvas>',
    "minimap canvas")
rep('<button class="iconbtn" id="muteBtn" title="အသံ">🔊</button>',
    '<button class="iconbtn" id="muteBtn" title="အသံ">🔊</button>\n      <button class="iconbtn" id="mapBtn" title="မြေပုံ">🗺️</button>',
    "map button")

# Pause settings rows
rep('    <button class="btn ghost" id="fppBtn">👁️ FPP (အခု) — TPP ပြောင်း</button>\n  </div>',
    '    <button class="btn ghost" id="fppBtn">👁️ FPP (အခု) — TPP ပြောင်း</button>\n  </div>\n  <div class="row">\n    <button class="btn ghost" id="mapToggleBtn">🗺️ မြေပုံ: ဖွင့်</button>\n    <button class="btn ghost" id="handToggleBtn">✋ လက်: ဖွင့်</button>\n  </div>\n  <div class="row">\n    <button class="btn ghost" id="camSpeedBtn">📷 ကင်မရာ: ပုံမှန်</button>\n    <button class="btn ghost" id="volBtn">🔊 အသံ: ပုံမှန်</button>\n    <button class="btn ghost" id="qualityBtn">🖥️ အရည်အသွေး: မြင့်</button>\n  </div>',
    "pause settings")

# Minimap draw function, after shuffle helper
rep("function shuffleArr(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const tmp=a[i]; a[i]=a[j]; a[j]=tmp; } return a; }",
    "function shuffleArr(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const tmp=a[i]; a[i]=a[j]; a[j]=tmp; } return a; }\nlet lastMapDraw=0;\nfunction drawMinimap(){\n  const cv=$('minimap');\n  if(!cv) return;\n  const g=cv.getContext('2d');\n  if(!g) return;\n  g.clearRect(0,0,cv.width,cv.height);\n  g.fillStyle='#111111';\n  g.fillRect(0,0,cv.width,cv.height);\n  const sc=1.4;\n  g.fillStyle='#888888';\n  for(const w of walls){\n    const x=(w.x-w.w/2+32)*sc;\n    const y=(w.z-w.d/2+24)*sc;\n    g.fillRect(x,y,w.w*sc,w.d*sc);\n  }\n  if(typeof S.beaconX==='number'){\n    const bx=(S.beaconX+32)*sc;\n    const by=(S.beaconZ+24)*sc;\n    g.fillStyle='#ffcc00';\n    g.beginPath();\n    g.arc(Math.max(2,Math.min(cv.width-2,bx)),Math.max(2,Math.min(cv.height-2,by)),3,0,Math.PI*2);\n    g.fill();\n  }\n  const px=(playerPos.x+32)*sc;\n  const py=(playerPos.z+24)*sc;\n  g.fillStyle='#22ff88';\n  g.beginPath();\n  g.arc(Math.max(2,Math.min(cv.width-2,px)),Math.max(2,Math.min(cv.height-2,py)),3.5,0,Math.PI*2);\n  g.fill();\n  g.strokeStyle='#22ff88';\n  g.beginPath();\n  g.moveTo(Math.max(2,Math.min(cv.width-2,px)),Math.max(2,Math.min(cv.height-2,py)));\n  g.lineTo(Math.max(2,Math.min(cv.width-2,px+Math.sin(S.yaw)*10)),Math.max(2,Math.min(cv.height-2,py+Math.cos(S.yaw)*10)));\n  g.stroke();\n}",
    "minimap draw")

# Hand groups: closer, tilted, scale, flashlight mesh, hand light
rep("const handL=new THREE.Group(); handL.position.set(-0.20,-0.22,-0.45); handL.rotation.set(0.1,0.15,0); handsGroup.add(handL);\nconst handR=new THREE.Group(); handR.position.set(0.20,-0.22,-0.45); handR.rotation.set(0.1,-0.15,0); handsGroup.add(handR);",
    "const handL=new THREE.Group(); handL.position.set(-0.18,-0.28,-0.42); handL.rotation.set(0.25,0.20,-0.10); handsGroup.add(handL);\nconst handR=new THREE.Group(); handR.position.set(0.18,-0.24,-0.38); handR.rotation.set(0.25,-0.20,0.10); handsGroup.add(handR);\nconst flashMeshGroup=new THREE.Group(); flashMeshGroup.position.set(0,-0.02,-0.06); handR.add(flashMeshGroup);\nconst flashBody=new THREE.Mesh(new THREE.CylinderGeometry(0.022,0.026,0.14,12), new THREE.MeshStandardMaterial({color:0x1a1a1a,roughness:0.4,metalness:0.3})); flashBody.rotation.x=Math.PI/2; flashMeshGroup.add(flashBody);\nconst flashLens=new THREE.Mesh(new THREE.CircleGeometry(0.02,12), new THREE.MeshBasicMaterial({color:0xfff2cc})); flashLens.position.set(0,0,-0.075); flashLens.rotation.y=Math.PI; flashMeshGroup.add(flashLens);\nconst handLight=new THREE.PointLight(0xffe0b3,0.6,1.2,1); handLight.position.set(0,-0.1,-0.3); camera.add(handLight);",
    "hand flashlight mesh")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1,1,1); handR.add(inner); }, undefined, ()=>{});",
    "handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1.15,1.15,1.15); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});",
    "handR material")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1,1,1); inner.traverse(o=>{ if(o.isMesh){ o.material.side=THREE.DoubleSide; } }); handL.add(inner); }, undefined, ()=>{});",
    "handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1.15,1.15,1.15); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{});",
    "handL material")

# Flash origin to hand in FPP, hand light visibility, hands visibility with setting
rep("  handsGroup.visible = !!S.fpp && S.playing && !S.paused;",
    "  handsGroup.visible = !!S.fpp && S.playing && !S.paused && S.showHands!==false;\n  if(typeof handLight!=='undefined') handLight.visible=handsGroup.visible;",
    "hands visibility setting")
rep("  flash.position.set(playerPos.x,playerPos.y+(S.fpp?1.65:2.2),playerPos.z);\n  flash.target.position.set(playerPos.x+Math.sin(S.yaw)*5,playerPos.y+1.3,playerPos.z+Math.cos(S.yaw)*5);",
    "  if(S.fpp){\n    camera.updateMatrixWorld();\n    handR.getWorldPosition(handWorldVec);\n    flash.position.copy(handWorldVec);\n    flash.target.position.set(handWorldVec.x+Math.sin(S.yaw)*5,handWorldVec.y-0.15,handWorldVec.z+Math.cos(S.yaw)*5);\n  } else {\n    flash.position.set(playerPos.x,playerPos.y+2.2,playerPos.z);\n    flash.target.position.set(playerPos.x+Math.sin(S.yaw)*5,playerPos.y+1.3,playerPos.z+Math.cos(S.yaw)*5);\n  }\n  if(S.showMap!==false && $('minimap')){ if(performance.now()-lastMapDraw>100){ lastMapDraw=performance.now(); drawMinimap(); } }",
    "flash from hand + minimap update")

# handWorldVec definition after flash
rep("const flash=new THREE.SpotLight(0xfff2cc,90,18,0.45,0.35,1);",
    "const flash=new THREE.SpotLight(0xfff2cc,90,18,0.45,0.35,1);\nconst handWorldVec=new THREE.Vector3();",
    "handWorldVec")

# Volume multiplier in playReal
rep("const c=a.cloneNode(); c.volume=vol||0.8;",
    "const c=a.cloneNode(); c.volume=Math.min(1,(vol||0.8)*(S.volume||1));",
    "volume multiplier")

# Camera speed
rep("S.yaw-=(e.clientX-lastCamX)*0.005;",
    "S.yaw-=(e.clientX-lastCamX)*0.005*(S.camSpeed||1);",
    "cam speed")

# Save progress expanded
rep("function saveProgress(){ try{ if(S.playing) localStorage.setItem('nh_save', JSON.stringify({floor:S.floor, hearts:S.hearts, time:Math.floor(S.time)})); }catch(e){} }",
    "function saveProgress(){ try{ if(!S.playing) return; const fmS=floorMission(); const data={floor:S.floor, hearts:S.hearts, time:Math.floor(S.time), missionType:fmS.type, items:S.items, keys:S.keys, switchIdx:S.switchIdx, corpseTouched:(S.corpseTouched||[]).slice(), visitedRooms:ROOM_ZONES.map((z,i)=>S.visited.includes(z)?i:-1).filter(i=>i>=0), visitedLockers:hideSpots.map((h,i)=>S.visited.includes(h)?i:-1).filter(i=>i>=0), missionDone:S.missionDone, hideTotal:S.hideTotal, distance:S.distance, missionTimer:S.missionTimer, switchOn:S.switchOn, keysTaken:keyMeshes.filter(km=>km.taken && km.def.id<=KEYS_NEEDED).map(km=>km.def.id)}; localStorage.setItem('nh_save', JSON.stringify(data)); }catch(e){} }",
    "save expanded")

# doFloorChange save via saveProgress instead of direct setItem
rep("  try{ localStorage.setItem('nh_save', JSON.stringify({floor:S.floor, hearts:S.hearts, time:Math.floor(S.time)})); }catch(e){}",
    "  if(typeof saveProgress==='function') saveProgress();",
    "floor save via saveProgress")

# Continue restore mission progress + allow floor 15
rep("function continueGame(){ let sv=null; try{ sv=JSON.parse(localStorage.getItem('nh_save')||'null'); }catch(e){} startGame(); if(sv && sv.floor>=1 && sv.floor<15){ S.floor=sv.floor; S.hearts=sv.hearts||3; playerPos.set(-19,0,20); playerPos.y=0; S.yaw=Math.PI; monsterPos.set(20,0,16); monsterState='patrol'; startFloorMission(); updateHUD(); toast('💾 သိမ်းထားတဲ့ အထပ် '+sv.floor+' ကနေ ဆက်ဆော့သည်'); } }",
    "function continueGame(){ let sv=null; try{ sv=JSON.parse(localStorage.getItem('nh_save')||'null'); }catch(e){} startGame(); if(sv && sv.floor>=1 && sv.floor<=15){ S.floor=sv.floor; S.hearts=sv.hearts||3; playerPos.set(-19,0,20); playerPos.y=0; S.yaw=Math.PI; monsterPos.set(20,0,16); monsterState='patrol'; startFloorMission(); const fm2=floorMission(); if(fm2.type==='keys' && sv.keysTaken){ S.keys=0; for(const km of keyMeshes){ if(km.def.id<=KEYS_NEEDED){ if(sv.keysTaken.includes(km.def.id)){ km.taken=true; km.mesh.visible=false; S.keys++; } else { km.taken=false; km.mesh.visible=true; } } } } else if((fm2.type==='order'||fm2.type==='dark'||fm2.type==='timed'||fm2.type==='final'||fm2.type==='timedorder') && typeof sv.items==='number' && sv.items>0){ const n=Math.min(sv.items,fm2.need); S.items=0; itemMeshes.forEach((im,idx)=>{ if(idx<n){ im.taken=true; im.mesh.visible=false; S.items++; } }); } if(typeof sv.switchIdx==='number') S.switchIdx=sv.switchIdx; if(Array.isArray(sv.corpseTouched)){ S.corpseTouched=sv.corpseTouched.slice(); S.corpseIdx=S.corpseTouched.length; } if(fm2.type==='rooms' && Array.isArray(sv.visitedRooms)){ S.visited=sv.visitedRooms.map(i=>ROOM_ZONES[i]).filter(Boolean); } if((fm2.type==='lockers'||fm2.type==='darklockers') && Array.isArray(sv.visitedLockers)){ S.visited=sv.visitedLockers.map(i=>hideSpots[i]).filter(Boolean); } if(typeof sv.hideTotal==='number') S.hideTotal=sv.hideTotal; if(typeof sv.distance==='number') S.distance=sv.distance; if(typeof sv.missionTimer==='number') S.missionTimer=sv.missionTimer; if(typeof sv.switchOn==='boolean') S.switchOn=sv.switchOn; if(typeof sv.missionDone==='boolean') S.missionDone=sv.missionDone; if(missionComplete()){ setObjective('တိုးတက်မှု ပြန်ရပြီ! တောင်တံခါး သွား'); } updateHUD(); toast('💾 သိမ်းထားတဲ့ အထပ် '+sv.floor+' ကနေ ဆက်ဆော့သည်, တိုးတက်မှု ပြန်ရပြီ'); } }",
    "continue restore")
rep("if(sv0 && sv0.floor>=1 && sv0.floor<15){ $('continueBtn').style.display='block';",
    "if(sv0 && sv0.floor>=1 && sv0.floor<=15){ $('continueBtn').style.display='block';",
    "continue button floor15")

# doInteract save at end
rep("    else { S.doorOpen=true; if(exitBlock){ const i=walls.indexOf(exitBlock); if(i>=0) walls.splice(i,1); } doorSound(); toast('🚪 တံခါး ပွင့်ပြီ! လှေကားကနေ တစ်ထစ်ချင်း ဆင်းပါ'); }\n  }\n}",
    "    else { S.doorOpen=true; if(exitBlock){ const i=walls.indexOf(exitBlock); if(i>=0) walls.splice(i,1); } doorSound(); toast('🚪 တံခါး ပွင့်ပြီ! လှေကားကနေ တစ်ထစ်ချင်း ဆင်းပါ'); }\n  }\n  if(typeof saveProgress==='function') saveProgress();\n}",
    "interact save")

# Settings wiring, after soundBtn listeners
rep("$('soundBtn').addEventListener('click',toggleSound); $('muteBtn').addEventListener('click',toggleSound);",
    "$('soundBtn').addEventListener('click',toggleSound); $('muteBtn').addEventListener('click',toggleSound);\nif($('mapBtn')){ $('mapBtn').addEventListener('click',()=>{ S.showMap=!S.showMap; const mm=$('minimap'); if(mm) mm.style.display=S.showMap?'block':'none'; if($('mapToggleBtn')) $('mapToggleBtn').textContent=S.showMap?'🗺️ မြေပုံ: ဖွင့်':'🗺️ မြေပုံ: ပိတ်'; }); }\nif($('mapToggleBtn')){ $('mapToggleBtn').addEventListener('click',()=>{ S.showMap=!S.showMap; const mm=$('minimap'); if(mm) mm.style.display=S.showMap?'block':'none'; $('mapToggleBtn').textContent=S.showMap?'🗺️ မြေပုံ: ဖွင့်':'🗺️ မြေပုံ: ပိတ်'; }); }\nif($('handToggleBtn')){ $('handToggleBtn').addEventListener('click',()=>{ S.showHands=!S.showHands; $('handToggleBtn').textContent=S.showHands?'✋ လက်: ဖွင့်':'✋ လက်: ပိတ်'; }); }\nif($('camSpeedBtn')){ $('camSpeedBtn').addEventListener('click',()=>{ S.camSpeed=(S.camSpeed===1)?1.5:((S.camSpeed===1.5)?0.7:1); $('camSpeedBtn').textContent=S.camSpeed===1.5?'📷 ကင်မရာ: မြန်':(S.camSpeed===0.7?'📷 ကင်မရာ: နှေး':'📷 ကင်မရာ: ပုံမှန်'); }); }\nif($('volBtn')){ $('volBtn').addEventListener('click',()=>{ S.volume=(S.volume===1)?1.2:((S.volume===1.2)?0.4:1); $('volBtn').textContent=S.volume===1.2?'🔊 အသံ: ကျယ်':(S.volume===0.4?'🔊 အသံ: တိုး':'🔊 အသံ: ပုံမှန်'); }); }\nif($('qualityBtn')){ $('qualityBtn').addEventListener('click',()=>{ S.lowQuality=!S.lowQuality; try{ renderer.setPixelRatio(S.lowQuality?1:Math.min(devicePixelRatio,1.75)); }catch(e){} $('qualityBtn').textContent=S.lowQuality?'🖥️ အရည်အသွေး: နိမ့်':'🖥️ အရည်အသွေး: မြင့်'; }); }",
    "settings wiring")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V34 patch applied, misses=0')
