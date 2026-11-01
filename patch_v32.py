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

# V32 helper: shuffle
rep(
"function floorMission(){ return FLOOR_MISSIONS[S.floor]||FLOOR_MISSIONS[15]; }",
"function floorMission(){ return FLOOR_MISSIONS[S.floor]||FLOOR_MISSIONS[15]; }\nfunction shuffleArr(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const tmp=a[i]; a[i]=a[j]; a[j]=tmp; } return a; }",
"shuffle helper")

# Start screen: V32 label, Continue button, sound credit
rep(
"  <p style=\"font-size:11px;color:#666;margin-top:8px\">V31 • အမိုး မီးသီးလုံး + မီးဖျက် — ဆေးရုံ မှောင်, ဓာတ်မီး + အနီရောင် ဘဲ</p>",
"  <p style=\"font-size:11px;color:#666;margin-top:8px\">V32 • Random သရဲ + Random ပစ္စည်း + အသံအစစ် + Save — ထပ်တိုင်း မတူတော့ဘူး</p>\n  <p style=\"font-size:11px;color:#666;margin-top:4px\">အသံ: SoundBible (လူအစစ် သရဲ အသံ)</p>",
"version label")
rep(
"    <button class=\"btn\" id=\"startBtn\">▶ စဆော့မယ်</button>",
"    <button class=\"btn\" id=\"startBtn\">▶ စဆော့မယ်</button>\n    <button class=\"btn ghost\" id=\"continueBtn\" style=\"display:none\">↻ ဆက်ဆော့မယ်</button>",
"continue button")

# Real sounds: loader block before growlSound
rep(
"function growlSound(){ playTone(60,35,1.5,'sawtooth',0.50,9); playNoise(1.5,'lowpass',180,1,0.35,9); playTone(40,28,1.5,'sine',0.40,0); } // V29 scarier: deeper, louder, longer + rumble",
"let realSounds={};\nlet realLoaded={};\nfunction loadRealSound(name,file){ try{ const a=new Audio(file); a.preload='auto'; a.addEventListener('canplaythrough',()=>{ realLoaded[name]=true; }); a.addEventListener('error',()=>{ realLoaded[name]=false; }); realSounds[name]=a; }catch(e){} }\nfunction playReal(name,vol){ if(!S.sound) return false; const a=realSounds[name]; if(!a || !realLoaded[name]) return false; try{ const c=a.cloneNode(); c.volume=vol||0.8; const pr=c.play(); if(pr && pr.catch) pr.catch(()=>{}); return true; }catch(e){ return false; } }\nloadRealSound('scream','ghost-scream.mp3');\nloadRealSound('moan','ghost-moan.mp3');\nloadRealSound('growl','ghost-growl.mp3');\nloadRealSound('roar','ghost-roar.mp3');\nloadRealSound('girl','ghost-girl.mp3');\nfunction growlSound(){ if(playReal('growl',0.8)) return; playTone(60,35,1.5,'sawtooth',0.50,9); playNoise(1.5,'lowpass',180,1,0.35,9); playTone(40,28,1.5,'sine',0.40,0); }",
"real sounds loader + growl")
rep(
"function moanSound(){ playTone(240,120,3.0,'sine',0.35,5); playNoise(3.0,'bandpass',400,2,0.25,3); playTone(120,80,3.0,'sawtooth',0.20,4); } // V29 scarier: lower, longer",
"function moanSound(){ if(playReal('moan',0.7)) return; playTone(240,120,3.0,'sine',0.35,5); playNoise(3.0,'bandpass',400,2,0.25,3); playTone(120,80,3.0,'sawtooth',0.20,4); }",
"moan real")
rep(
"function scareSound(){ playTone(110,35,1.4,'sawtooth',0.60,0); playNoise(1.4,'lowpass',300,1,0.45,0); thump(0.7); playTone(50,30,1.4,'sine',0.45,0); } // V29 scarier",
"function scareSound(){ if(playReal('roar',0.9)) { thump(0.7); return; } playTone(110,35,1.4,'sawtooth',0.60,0); playNoise(1.4,'lowpass',300,1,0.45,0); thump(0.7); playTone(50,30,1.4,'sine',0.45,0); }",
"scare real")
rep(
"function whisperSound(){ playNoise(1.6,'bandpass',1100,1.5,0.45,7); playNoise(1.4,'bandpass',750,2,0.35,11); playTone(200,130,1.6,'sine',0.22,6); playNoise(1.2,'bandpass',1600,3,0.20,13); } // V29 scarier: louder, longer, extra hiss",
"function whisperSound(){ if(playReal('girl',0.5)) return; playNoise(1.6,'bandpass',1100,1.5,0.45,7); playNoise(1.4,'bandpass',750,2,0.35,11); playTone(200,130,1.6,'sine',0.22,6); playNoise(1.2,'bandpass',1600,3,0.20,13); }",
"whisper real")
rep(
"function screamSound(){ playNoise(1.4,'highpass',900,1,0.65,0); playTone(950,200,1.4,'sawtooth',0.55,0); setTimeout(()=>playTone(1300,350,0.8,'sawtooth',0.45,0),150); setTimeout(()=>playTone(850,180,0.9,'sawtooth',0.35,0),400); setTimeout(()=>playTone(1100,300,0.7,'sawtooth',0.25,0),800); playTone(55,30,1.4,'sine',0.45,0); } // V29 scarier: louder, longer, echo + rumble",
"function screamSound(){ if(playReal('scream',0.9)) return; playNoise(1.4,'highpass',900,1,0.65,0); playTone(950,200,1.4,'sawtooth',0.55,0); setTimeout(()=>playTone(1300,350,0.8,'sawtooth',0.45,0),150); setTimeout(()=>playTone(850,180,0.9,'sawtooth',0.35,0),400); setTimeout(()=>playTone(1100,300,0.7,'sawtooth',0.25,0),800); playTone(55,30,1.4,'sine',0.45,0); }",
"scream real")

# applyFloorLayout: random partitions, pools, writings, light colour
rep(
"  const fd=15-S.floor;\n  const dx=((fd%3)-1)*3, dz=((fd%3)-1)*1.5;\n  let pi=0;\n  const partSlots=[[-22,-18],[20,-18],[-20,18],[20,18]];\n  const partSlots2=[[-14,-12],[14,-12],[-14,12],[14,12]];\n  const partSlots3=[[-24,-8],[24,-8],[-24,8],[24,8]];\n  const allSlots=[partSlots,partSlots2,partSlots3];\n  for(const pr of props){\n    if(!pr.mesh) continue;\n    if(pr.label==='partition'){\n      const slot=allSlots[pi%3][fd%4]; pi++;",
"  const fd=15-S.floor;\n  const dx=((fd%3)-1)*3, dz=((fd%3)-1)*1.5;\n  let pi=0;\n  const partSlots=[[-22,-18],[20,-18],[-20,18],[20,18]];\n  const partSlots2=[[-14,-12],[14,-12],[-14,12],[14,12]];\n  const partSlots3=[[-24,-8],[24,-8],[-24,8],[24,8]];\n  const allFlat=shuffleArr(partSlots.concat(partSlots2,partSlots3));\n  for(const pr of props){\n    if(!pr.mesh) continue;\n    if(pr.label==='partition'){\n      const slot=allFlat[pi%allFlat.length]; pi++;",
"random partitions")
rep(
"  if(typeof extraPools!=='undefined'){ extraPools.forEach((pm,i)=>{ const sl=extraPoolSlots[(fd*3+i*2)%extraPoolSlots.length]; pm.position.x=sl[0]; pm.position.z=sl[1]; }); }\n  if(typeof dynamicWritings!=='undefined'){ dynamicWritings.forEach((dw,i)=>{ dw.userData.set(SCARY_TEXTS[(fd+i*3)%SCARY_TEXTS.length]); }); }\n  const lc=FLOOR_LIGHTS[fd%5];",
"  if(typeof extraPools!=='undefined'){ const poolSlots=shuffleArr(extraPoolSlots.slice()); extraPools.forEach((pm,i)=>{ const sl=poolSlots[i%poolSlots.length]; pm.position.x=sl[0]; pm.position.z=sl[1]; }); }\n  if(typeof dynamicWritings!=='undefined'){ dynamicWritings.forEach((dw,i)=>{ dw.userData.set(SCARY_TEXTS[Math.floor(Math.random()*SCARY_TEXTS.length)]); }); }\n  const lc=FLOOR_LIGHTS[Math.floor(Math.random()*FLOOR_LIGHTS.length)];",
"random pools writings light")

# setActiveGhosts: random 4-5 ghosts, distinct spawns
rep(
"function setActiveGhosts(){\n  if(!wanderingGhosts.length) return;\n  const active=wanderingGhosts.map(wg=>wg.def.name); S.activeGhostCount=active.length;\n  for(const wg of wanderingGhosts){\n    if(active.includes(wg.def.name)){ wg.state='patrol'; wg.cooldown=0; wg.outer.visible=true; const wp=wg.def.wps[0]; if(wp) wg.outer.position.set(wp[0],0,wp[1]); }\n    else { wg.state='patrol'; wg.cooldown=9999; wg.outer.visible=false; }\n  }\n}",
"function setActiveGhosts(){\n  if(!wanderingGhosts.length) return;\n  const shuffled=shuffleArr(wanderingGhosts.slice());\n  const pickCount=4+(Math.random()<0.5?1:0);\n  const activeSet=new Set(shuffled.slice(0,pickCount).map(wg=>wg.def.name));\n  S.activeGhostCount=activeSet.size;\n  S.activeGhostNames=shuffled.slice(0,pickCount).map(wg=>wg.def.name);\n  const spawnPool=shuffleArr(wanderingGhosts.map(wg=>({pos:wg.def.pos, wps:(wg.def.origWps||wg.def.wps).slice()})));\n  let si=0;\n  for(const wg of wanderingGhosts){\n    if(activeSet.has(wg.def.name)){\n      wg.active=true;\n      wg.state='patrol';\n      wg.cooldown=0;\n      wg.outer.visible=true;\n      const sp=spawnPool[si%spawnPool.length]; si++;\n      wg.def.wps=sp.wps.slice();\n      wg.def.pos=sp.pos;\n      wg.outer.position.set(sp.pos[0],0,sp.pos[1]);\n    } else {\n      wg.active=false;\n      wg.state='patrol';\n      wg.cooldown=9999;\n      wg.outer.visible=false;\n    }\n  }\n}",
"random ghosts")

# startFloorMission: reset corpseTouched, any-order objective texts
rep(
"  S.missionDone=false; S.missionTimer=fm.timer||0; S.hideTotal=0; S.switchIdx=0; S.corpseIdx=0; S.dwell=0; S.visited=[]; S.switchOn=false; S.distance=0;",
"  S.missionDone=false; S.missionTimer=fm.timer||0; S.hideTotal=0; S.switchIdx=0; S.corpseIdx=0; S.corpseTouched=[]; S.dwell=0; S.visited=[]; S.switchOn=false; S.distance=0;",
"corpseTouched reset")
rep(
"  else if(fm.type==='lockers') obj='Ep'+fm.ep+' • Locker '+fm.need+' ခု မှာ ၂ စက္ကန့်စီ ရပ်ပါ';",
"  else if(fm.type==='lockers') obj='Ep'+fm.ep+' • Locker '+fm.need+' ခု မှာ ၂ စက္ကန့်စီ ရပ်ပါ (ဘယ် Locker ဖြစ်ဖြစ် ရသည်)';",
"lockers text")
rep(
"  else if(fm.type==='corpse') obj='Ep'+fm.ep+' • လူသေကောင် '+fm.need+' ကောင် အစဉ်လိုက် ထိပါ';",
"  else if(fm.type==='corpse') obj='Ep'+fm.ep+' • လူသေကောင် '+fm.need+' ကောင် ထိပါ (ဘယ်ကောင် ဖြစ်ဖြစ် ရသည်)';",
"corpse text")
rep(
"  else if(fm.type==='rooms') obj='Ep'+fm.ep+' • အခန်း ၄ ခု လုံး သွားပါ (NW/NE/SW/SE)';",
"  else if(fm.type==='rooms') obj='Ep'+fm.ep+' • အခန်း ၄ ခု လုံး သွားပါ (ဘယ် အစဉ်ဖြစ်ဖြစ် ရသည်)';",
"rooms text")

# setupFloorItems: shuffle spawns instead of rotation
rep(
"  // rotate spawn list by floor so each floor items are in different places\n  const rot=(15-S.floor)%ITEM_SPAWNS.length;\n  const spawns=[]; for(let i=0;i<ITEM_SPAWNS.length;i++) spawns.push(ITEM_SPAWNS[(rot+i)%ITEM_SPAWNS.length]);",
"  const spawns=shuffleArr(ITEM_SPAWNS.slice());",
"random item spawns")

# East wing ceilings, after floorCorr
rep(
"const floorCorr=new THREE.Mesh(new THREE.PlaneGeometry(8,6), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9})); floorCorr.rotation.x=-Math.PI/2; floorCorr.position.set(36,0,0); scene.add(floorCorr);",
"const floorCorr=new THREE.Mesh(new THREE.PlaneGeometry(8,6), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9})); floorCorr.rotation.x=-Math.PI/2; floorCorr.position.set(36,0,0); scene.add(floorCorr);\nconst ceilEast=new THREE.Mesh(new THREE.PlaneGeometry(30,30), new THREE.MeshStandardMaterial({map:ceilTex,roughness:1})); ceilEast.rotation.x=Math.PI/2; ceilEast.position.set(55,3.4,0); scene.add(ceilEast);\nconst ceilCorr=new THREE.Mesh(new THREE.PlaneGeometry(8,6), new THREE.MeshStandardMaterial({map:ceilTex,roughness:1})); ceilCorr.rotation.x=Math.PI/2; ceilCorr.position.set(36,3.4,0); scene.add(ceilCorr);",
"east ceilings")

# Corpse interact: any corpse, not order
rep(
"    if(!S.interactTarget && fmI.type==='corpse'){\n      const cd=corpseDefs[S.corpseIdx];\n      if(cd && Math.hypot(cd.x-playerPos.x,cd.z-playerPos.z)<2.5) S.interactTarget={type:'corpse',label:'💀 လူသေကောင်'};\n    }",
"    if(!S.interactTarget && fmI.type==='corpse'){\n      for(let ci=0;ci<corpseDefs.length;ci++){\n        const cd2=corpseDefs[ci];\n        if(!(S.corpseTouched||[]).includes(ci) && Math.hypot(cd2.x-playerPos.x,cd2.z-playerPos.z)<2.5){ S.interactTarget={type:'corpse',cdIdx:ci,label:'💀 လူသေကောင်'}; break; }\n      }\n    }",
"corpse interact any")
rep(
"  } else if(t.type==='corpse'){\n    const cd=corpseDefs[S.corpseIdx];\n    if(!cd){ toast('လူသေကောင် စုံပြီ!'); return; }\n    S.corpseIdx++; pickupSound(); screamSound();\n    toast('💀 လူသေကောင် ထိပြီ! ('+S.corpseIdx+'/'+floorMission().need+')');\n    if(S.corpseIdx<floorMission().need){ const nx=corpseDefs[S.corpseIdx]; setObjective('နောက် လူသေကောင်: ('+nx.x+','+nx.z+') သွား'); }\n    else { setObjective('လူသေကောင် စုံပြီ! တောင်တံခါး သွား'); toast('🎉 လူသေကောင် စုံပြီ! တောင်တံခါးကို သွားပါ'); }",
"  } else if(t.type==='corpse'){\n    const cidx=(typeof t.cdIdx==='number')?t.cdIdx:corpseDefs.findIndex((cd2,ci)=>!(S.corpseTouched||[]).includes(ci));\n    if(cidx<0){ toast('လူသေကောင် စုံပြီ!'); return; }\n    if(!S.corpseTouched) S.corpseTouched=[];\n    S.corpseTouched.push(cidx);\n    S.corpseIdx++; pickupSound(); screamSound();\n    toast('💀 လူသေကောင် ထိပြီ! ('+S.corpseIdx+'/'+floorMission().need+')');\n    if(S.corpseIdx<floorMission().need){ const rem=corpseDefs.filter((cd2,ci)=>!S.corpseTouched.includes(ci)); const nx=rem[0]; if(nx) setObjective('နောက် လူသေကောင်: ('+nx.x+','+nx.z+') သွား'); }\n    else { setObjective('လူသေကောင် စုံပြီ! တောင်တံခါး သွား'); toast('🎉 လူသေကောင် စုံပြီ! တောင်တံခါးကို သွားပါ'); }",
"corpse handler any")

# Compass: corpse nearest untouched, rooms nearest unvisited, lockers nearest unvisited
rep(
"  } else if(fmC.type==='corpse'){\n    const cd=corpseDefs[S.corpseIdx];\n    if(cd){ tx=cd.x; tz=cd.z; tlabel='လူသေကောင်'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }",
"  } else if(fmC.type==='corpse'){\n    const remC=corpseDefs.filter((cd2,ci)=>!(S.corpseTouched||[]).includes(ci));\n    let bestC=null; let bestD=1e9;\n    for(const cd2 of remC){ const d2=Math.hypot(cd2.x-playerPos.x,cd2.z-playerPos.z); if(d2<bestD){ bestD=d2; bestC=cd2; } }\n    if(bestC){ tx=bestC.x; tz=bestC.z; tlabel='လူသေကောင်'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }",
"compass corpse")
rep(
"  } else if(fmC.type==='rooms'){\n    const rz=ROOM_ZONES[S.visited.length];\n    if(rz){ tx=rz.x; tz=rz.z; tlabel='နောက်အခန်း'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }",
"  } else if(fmC.type==='rooms'){\n    const remR=ROOM_ZONES.filter(z=>!S.visited.includes(z));\n    let bestR=null; let bestD=1e9;\n    for(const rz2 of remR){ const d2=Math.hypot(rz2.x-playerPos.x,rz2.z-playerPos.z); if(d2<bestD){ bestD=d2; bestR=rz2; } }\n    if(bestR){ tx=bestR.x; tz=bestR.z; tlabel='နောက်အခန်း'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }",
"compass rooms")
rep(
"  } else if(fmC.type==='lockers'||fmC.type==='darklockers'){\n    const lk=hideSpots[S.visited.length];\n    if(lk){ tx=lk.x; tz=lk.z; tlabel='Locker'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }",
"  } else if(fmC.type==='lockers'||fmC.type==='darklockers'){\n    const remL=hideSpots.filter(h=>!S.visited.includes(h));\n    let bestL=null; let bestD=1e9;\n    for(const lk2 of remL){ const d2=Math.hypot(lk2.x-playerPos.x,lk2.z-playerPos.z); if(d2<bestD){ bestD=d2; bestL=lk2; } }\n    if(bestL){ tx=bestL.x; tz=bestL.z; tlabel='Locker'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }",
"compass lockers")

# Monster move clearance 0.5 -> 1.0
rep(
"    if(dl>0.1){ const nm=collide(monsterPos.x+dx/dl*mSpeed*dt, monsterPos.z+dz/dl*mSpeed*dt, 0.5); monsterPos.x=nm[0]; monsterPos.z=nm[1]; monsterAngle=Math.atan2(dx/dl,dz/dl); }",
"    if(dl>0.1){ const nm=collide(monsterPos.x+dx/dl*mSpeed*dt, monsterPos.z+dz/dl*mSpeed*dt, 1.0); monsterPos.x=nm[0]; monsterPos.z=nm[1]; monsterAngle=Math.atan2(dx/dl,dz/dl); }",
"monster clearance")

# Ghost update: skip inactive ghosts
rep(
"  for(const wg of wanderingGhosts){\n    if(!wg.outer) continue;",
"  for(const wg of wanderingGhosts){\n    if(!wg.outer) continue;\n    if(wg.active===false){ wg.outer.visible=false; continue; }",
"ghost skip inactive")

# Poltergeist: hold if player close, destination prop + player check
rep(
"    if(polterAnim){\n      polterAnim.t+=dt; const k=Math.min(1,polterAnim.t/polterAnim.dur); const e=k<0.5?2*k*k:1-Math.pow(-2*k+2,2)/2;\n      polterAnim.item.position.x=polterAnim.fx+(polterAnim.tx-polterAnim.fx)*e; polterAnim.item.position.z=polterAnim.fz+(polterAnim.tz-polterAnim.fz)*e; polterAnim.item.rotation.y=polterAnim.fry+(polterAnim.try-polterAnim.fry)*e;\n      if(k>=1){ polterAnim=null; polterTimer=20+Math.random()*20; }",
"    if(polterAnim){\n      const pd=Math.hypot(polterAnim.item.position.x-playerPos.x,polterAnim.item.position.z-playerPos.z);\n      if(pd>=0.8){\n        polterAnim.t+=dt; const k=Math.min(1,polterAnim.t/polterAnim.dur); const e=k<0.5?2*k*k:1-Math.pow(-2*k+2,2)/2;\n        polterAnim.item.position.x=polterAnim.fx+(polterAnim.tx-polterAnim.fx)*e; polterAnim.item.position.z=polterAnim.fz+(polterAnim.tz-polterAnim.fz)*e; polterAnim.item.rotation.y=polterAnim.fry+(polterAnim.try-polterAnim.fry)*e;\n        if(k>=1){ polterAnim=null; polterTimer=20+Math.random()*20; }\n      }",
"polter hold")
rep(
"          let blocked=false; for(const w of walls){ if(Math.abs(tx-w.x)<w.w/2+0.6 && Math.abs(tz-w.z)<w.d/2+0.6){ blocked=true; break; } }",
"          let blocked=false; for(const w of walls){ if(Math.abs(tx-w.x)<w.w/2+0.6 && Math.abs(tz-w.z)<w.d/2+0.6){ blocked=true; break; } }\n          if(!blocked){ for(const pr of props){ if(Math.abs(tx-pr.x)<pr.w/2+0.6 && Math.abs(tz-pr.z)<pr.d/2+0.6){ blocked=true; break; } } }\n          if(!blocked && Math.hypot(tx-playerPos.x,tz-playerPos.z)<1.2){ blocked=true; }",
"polter dest check")

# Timed mission safe teleport
rep(
"      if(S.missionTimer<=0){ setupFloorItems(); S.missionTimer=fmP.timer; screamSound(); toast('⏰ အချိန်ကုန်ပြီ! ပစ္စည်း ပြန်စ!'); monsterPos.set(playerPos.x+9,0,playerPos.z); }",
"      if(S.missionTimer<=0){ setupFloorItems(); S.missionTimer=fmP.timer; screamSound(); toast('⏰ အချိန်ကုန်ပြီ! ပစ္စည်း ပြန်စ!'); let placedSafe=false; for(let at=0;at<8 && !placedSafe;at++){ const a2=at*Math.PI/4; const cx2=playerPos.x+Math.sin(a2)*9; const cz2=playerPos.z+Math.cos(a2)*9; const cc=collide(cx2,cz2,0.5); if(Math.hypot(cc[0]-cx2,cc[1]-cz2)<1.0 && Math.hypot(cc[0]-playerPos.x,cc[1]-playerPos.z)>5){ monsterPos.set(cc[0],0,cc[1]); placedSafe=true; } } }",
"timed safe teleport")

# Rooms progress any-order
rep(
"    } else if(fmP.type==='rooms' && !S.missionDone){\n      const rz=ROOM_ZONES[S.visited.length];\n      if(rz && Math.hypot(rz.x-playerPos.x,rz.z-playerPos.z)<5){ S.visited.push(rz); pickupSound(); toast('🏥 အခန်း '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective('အခန်းစုံပြီ! တောင်တံခါး သွား'); } }",
"    } else if(fmP.type==='rooms' && !S.missionDone){\n      const rz=ROOM_ZONES.find(z=>!S.visited.includes(z) && Math.hypot(z.x-playerPos.x,z.z-playerPos.z)<5);\n      if(rz){ S.visited.push(rz); pickupSound(); toast('🏥 အခန်း '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective('အခန်းစုံပြီ! တောင်တံခါး သွား'); } }",
"rooms any")
# Lockers progress any-order
rep(
"    } else if((fmP.type==='lockers'||fmP.type==='darklockers') && !S.missionDone){\n      const lk=hideSpots[S.visited.length];\n      if(lk){\n        const ld=Math.hypot(lk.x-playerPos.x,lk.z-playerPos.z);\n        if(ld<2.0){ S.dwell+=dt; if(S.dwell>=(fmP.dwell||2)){ S.visited.push(lk); S.dwell=0; pickupSound(); toast('🔒 Locker '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective(fmP.type==='darklockers'?'မှောင် Locker စုံပြီ! တောင်တံခါး သွား':'Locker စုံပြီ! တောင်တံခါး သွား'); } } }\n        else S.dwell=0;\n      }",
"    } else if((fmP.type==='lockers'||fmP.type==='darklockers') && !S.missionDone){\n      const lk=hideSpots.find(h=>!S.visited.includes(h) && Math.hypot(h.x-playerPos.x,h.z-playerPos.z)<2.0);\n      if(lk){\n        S.dwell+=dt; if(S.dwell>=(fmP.dwell||2)){ S.visited.push(lk); S.dwell=0; pickupSound(); toast('🔒 Locker '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective(fmP.type==='darklockers'?'မှောင် Locker စုံပြီ! တောင်တံခါး သွား':'Locker စုံပြီ! တောင်တံခါး သွား'); } }\n      } else S.dwell=0;",
"lockers any")

# Hide mission any ghost
rep(
"    } else if(fmP.type==='hide' && !S.missionDone){\n      if(S.hidden && Math.hypot(monsterPos.x-playerPos.x,monsterPos.z-playerPos.z)<15){ S.hideTotal+=dt;",
"    } else if(fmP.type==='hide' && !S.missionDone){\n      let nearGhost=Math.hypot(monsterPos.x-playerPos.x,monsterPos.z-playerPos.z);\n      for(const wg2 of wanderingGhosts){ if(wg2.outer && wg2.outer.visible){ const d2=Math.hypot(wg2.outer.position.x-playerPos.x,wg2.outer.position.z-playerPos.z); if(d2<nearGhost) nearGhost=d2; } }\n      if(S.hidden && nearGhost<15){ S.hideTotal+=dt;",
"hide any ghost")

# doFloorChange: re-apply random ghosts after reset loop, save progress
rep(
"  // wandering ghosts reset to old map patrol, faster + wider detection on lower floors\n  const floorDown=15-S.floor;\n  for(const wg of wanderingGhosts){ if(wg.def.origWps) wg.def.wps=wg.def.origWps; wg.wpIdx=0; wg.state='patrol'; wg.cooldown=0; wg.chaseTimer=0; const wp=wg.def.wps[0]; wg.outer.position.set(wp[0],0,wp[1]); wg.outer.visible=true; wg.def.speedBoost=floorDown*0.1; wg.def.radiusBoost=floorDown*0.5; }",
"  const floorDown=15-S.floor;\n  for(const wg of wanderingGhosts){ if(wg.def.origWps) wg.def.wps=wg.def.origWps; wg.wpIdx=0; wg.state='patrol'; wg.cooldown=0; wg.chaseTimer=0; const wp=wg.def.wps[0]; wg.outer.position.set(wp[0],0,wp[1]); wg.outer.visible=true; wg.def.speedBoost=floorDown*0.1; wg.def.radiusBoost=floorDown*0.5; }\n  if(typeof setActiveGhosts==='function') setActiveGhosts();\n  try{ localStorage.setItem('nh_save', JSON.stringify({floor:S.floor, hearts:S.hearts, time:Math.floor(S.time)})); }catch(e){}",
"floor change random + save")

# Save helpers + Continue, near startGame
rep(
"function startGame(){",
"function saveProgress(){ try{ if(S.playing) localStorage.setItem('nh_save', JSON.stringify({floor:S.floor, hearts:S.hearts, time:Math.floor(S.time)})); }catch(e){} }\nwindow.addEventListener('beforeunload', saveProgress);\nfunction continueGame(){ let sv=null; try{ sv=JSON.parse(localStorage.getItem('nh_save')||'null'); }catch(e){} startGame(); if(sv && sv.floor>=1 && sv.floor<15){ S.floor=sv.floor; S.hearts=sv.hearts||3; playerPos.set(-19,0,20); playerPos.y=0; S.yaw=Math.PI; monsterPos.set(20,0,16); monsterState='patrol'; startFloorMission(); updateHUD(); toast('💾 သိမ်းထားတဲ့ အထပ် '+sv.floor+' ကနေ ဆက်ဆော့သည်'); } }\nfunction startGame(){",
"save continue funcs")
rep(
"$('startBtn').addEventListener('click',startGame);",
"$('startBtn').addEventListener('click',()=>{ try{ localStorage.removeItem('nh_save'); }catch(e){} startGame(); });\nif($('continueBtn')){ $('continueBtn').addEventListener('click', continueGame); try{ const sv0=JSON.parse(localStorage.getItem('nh_save')||'null'); if(sv0 && sv0.floor>=1 && sv0.floor<15){ $('continueBtn').style.display='block'; $('continueBtn').textContent='↻ အထပ် '+sv0.floor+' ကနေ ဆက်ဆော့မယ်'; } }catch(e){} }",
"continue wiring")
# endGame clears save
rep(
"function endGame(win){\n  S.playing=false; S.won=win;",
"function endGame(win){\n  try{ localStorage.removeItem('nh_save'); }catch(e){}\n  S.playing=false; S.won=win;",
"end clears save")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V32 patch applied, misses=0')
