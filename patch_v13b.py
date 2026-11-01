import sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global t
    if old not in t:
        print("MISSING:",old[:220]); sys.exit(1)
    t=t.replace(old,new,cnt)

# --- player movement: collide allowStair, distance, stair Y ---
rep("    const np=collide(playerPos.x+mx*speed*dt, playerPos.z+mz*speed*dt, 0.45);",
"    const np=collide(playerPos.x+mx*speed*dt, playerPos.z+mz*speed*dt, 0.45, true);")
rep("""  if(player){ player.position.copy(playerPos); player.rotation.y=playerAngle; player.visible=!S.hidden; }""",
"""  S.inStair=(playerPos.z>24 && playerPos.x>=-2.5 && playerPos.x<=2.5);
  if(S.inStair){ playerPos.y=stairY(playerPos.z); if(moving){ const sidx=Math.floor((playerPos.z-25)/1.05); if(sidx!==S._lastStep){ S._lastStep=sidx; footstepSound(); } } }
  else playerPos.y=0;
  if(moving && floorMission().type==='distance' && !S.missionDone){ S.distance+=speed*dt; }
  if(player){ player.position.copy(playerPos); player.rotation.y=playerAngle; player.visible=!S.hidden; }""")
# camera Y + clamp
rep("  const camDist=4.5, camH=1.9; // V5 close eye-level, not far top-down",
"  const camDist=4.5, camH=playerPos.y+1.9;")
rep("  useX=Math.max(-31,Math.min(69,useX)); useZ=Math.max(-23,Math.min(23,useZ)); // V12 overall bounds: old map + corridor + east wing (wall pull-in still applies)",
"  useX=Math.max(-31,Math.min(69,useX)); useZ=Math.max(-23,Math.min(S.inStair?38.5:23,useZ));")
rep("  camera.lookAt(playerPos.x,1.35,playerPos.z);",
"  camera.lookAt(playerPos.x,playerPos.y+1.35,playerPos.z);")
rep("  playerRing.position.set(playerPos.x,0.05,playerPos.z);",
"  playerRing.position.set(playerPos.x,playerPos.y+0.05,playerPos.z);")
rep("  flash.position.set(playerPos.x,2.2,playerPos.z);",
"  flash.position.set(playerPos.x,playerPos.y+2.2,playerPos.z);")
rep("  flash.target.position.set(playerPos.x+Math.sin(S.yaw)*5,1.3,playerPos.z+Math.cos(S.yaw)*5);",
"  flash.target.position.set(playerPos.x+Math.sin(S.yaw)*5,playerPos.y+1.3,playerPos.z+Math.cos(S.yaw)*5);")
# door animation + entrance timer + landing trigger (insert before interact targets comment)
rep("  // interact / hide targets",
"""  // V13 door animation + entrance auto-close + landing trigger
  if(S.doorOpen) S.doorAnim=Math.min(1,S.doorAnim+dt*2); else S.doorAnim=Math.max(0,S.doorAnim-dt*2);
  if(typeof exitDoor!=='undefined') exitDoor.position.x=S.doorAnim*4.0;
  if(S.entranceOpen){ S.entranceAnim=Math.min(1,S.entranceAnim+dt*2); S.entranceTimer-=dt; if(S.entranceTimer<=0) closeEntranceDoor(); }
  else S.entranceAnim=Math.max(0,S.entranceAnim-dt*2);
  if(typeof entranceDoor!=='undefined') entranceDoor.position.x=-19+S.entranceAnim*6.0;
  if(S.doorOpen && S.floor>1 && !S._landing && playerPos.z>=37.5){ S._landing=true; goToNextFloor(); }
  // interact / hide targets""")
# interact: items include timedorder, exit label door open
rep("    if(fmI.type==='order'||fmI.type==='dark'||fmI.type==='timed'||fmI.type==='final'){",
"    if(fmI.type==='order'||fmI.type==='dark'||fmI.type==='timed'||fmI.type==='final'||fmI.type==='timedorder'){")
rep("  if(ed<2.5 && !S.interactTarget) S.interactTarget={type:'exit',label:missionComplete()?(S.floor===1?'🚪 Final Escape ဖွင့်':'🚪 အောက်ထပ် ဆင်း'):'🚪 တံခါး (ပိတ်ထားသည်)'};",
"  if(ed<2.5 && !S.interactTarget) S.interactTarget={type:'exit',label:missionComplete()?(S.floor===1?'🚪 Final Escape ဖွင့်':(S.doorOpen?'🚪 လှေကား ဆင်း':'🚪 တံခါး ဖွင့်')):'🚪 တံခါး (ပိတ်ထားသည်)'};")
# compass: timedorder, darklockers, rooms, distance
rep("  } else if(fmC.type==='order'||fmC.type==='dark'||fmC.type==='timed'||fmC.type==='final'){",
"  } else if(fmC.type==='order'||fmC.type==='dark'||fmC.type==='timed'||fmC.type==='final'||fmC.type==='timedorder'){")
rep("  } else if(fmC.type==='lockers'){",
"  } else if(fmC.type==='rooms'){\n    const rz=ROOM_ZONES[S.visited.length];\n    if(rz){ tx=rz.x; tz=rz.z; tlabel='နောက်အခန်း'; } else { tx=0; tz=24; tlabel='အောက်ထပ် တံခါး'; }\n  } else if(fmC.type==='distance'){\n    tx=0; tz=0; tlabel='လမ်းလျှောက်';\n  } else if(fmC.type==='lockers'||fmC.type==='darklockers'){")
# HUD keys text for new missions
rep("  $('keys').textContent=S.floor===15?('🔑 '+S.keys+' / 3'):('📦 '+S.items+' / '+floorMission().need);",
"  { const fmH=floorMission(); if(fmH.type==='keys') $('keys').textContent='🔑 '+S.keys+' / 3'; else if(['order','dark','timed','final','timedorder'].includes(fmH.type)) $('keys').textContent='📦 '+S.items+' / '+fmH.need; else $('keys').textContent='🎯 '+missionProgressText(); }")
# actBtn text for exit open
rep("  $('actBtn').textContent=S.interactTarget?((S.interactTarget.type==='exit'||S.interactTarget.type==='exit2'||S.interactTarget.type==='switch')?'✋ ဖွင့်':'✋ ယူ'):'✋ ယူ';",
"  $('actBtn').textContent=S.interactTarget?((S.interactTarget.type==='exit'&&S.doorOpen)?'✋ လှေကား ဆင်း':((S.interactTarget.type==='exit'||S.interactTarget.type==='exit2'||S.interactTarget.type==='switch')?'✋ ဖွင့်':'✋ ယူ')):'✋ ယူ';")
# mission progress: timed -> timedorder, lockers -> darklockers, rooms, distance
rep("    } else if(fmP.type==='timed' && !missionComplete()){",
"    } else if((fmP.type==='timed'||fmP.type==='timedorder') && !missionComplete()){")
rep("      if(sec2!==S._lastSec){ S._lastSec=sec2; setObjective('Ep'+fmP.ep+' • '+sec2+'s အတွင်း ပစ္စည်း '+S.items+'/'+fmP.need); }",
"      if(sec2!==S._lastSec){ S._lastSec=sec2; setObjective('Ep'+fmP.ep+' • '+sec2+'s အတွင်း '+(fmP.type==='timedorder'?'အစဉ်လိုက် ':'')+'ပစ္စည်း '+S.items+'/'+fmP.need); }")
rep("    } else if(fmP.type==='lockers' && !S.missionDone){",
"    } else if((fmP.type==='lockers'||fmP.type==='darklockers') && !S.missionDone){")
rep("        if(ld<2.0){ S.dwell+=dt; if(S.dwell>=(fmP.dwell||2)){ S.visited.push(lk); S.dwell=0; pickupSound(); toast('🔒 Locker '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective('Locker စုံပြီ! တောင်တံခါး သွား'); } } }",
"        if(ld<2.0){ S.dwell+=dt; if(S.dwell>=(fmP.dwell||2)){ S.visited.push(lk); S.dwell=0; pickupSound(); toast('🔒 Locker '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective(fmP.type==='darklockers'?'မှောင် Locker စုံပြီ! တောင်တံခါး သွား':'Locker စုံပြီ! တောင်တံခါး သွား'); } } }")
rep("""    } else if(fmP.type==='hide' && !S.missionDone){""",
"""    } else if(fmP.type==='rooms' && !S.missionDone){
      const rz=ROOM_ZONES[S.visited.length];
      if(rz && Math.hypot(rz.x-playerPos.x,rz.z-playerPos.z)<5){ S.visited.push(rz); pickupSound(); toast('🏥 အခန်း '+(S.visited.length)+'/'+fmP.need); if(S.visited.length>=fmP.need){ S.missionDone=true; setObjective('အခန်းစုံပြီ! တောင်တံခါး သွား'); } }
    } else if(fmP.type==='distance' && !S.missionDone){
      const dm=Math.floor(S.distance); if(dm!==S._lastSec){ S._lastSec=dm; setObjective('Ep'+fmP.ep+' • လမ်းလျှောက်ပြီ: '+dm+'/'+fmP.need+'m'); }
      if(S.distance>=fmP.need){ S.missionDone=true; setObjective('လမ်းလျှောက်ပြီ! တောင်တံခါး သွား'); toast('🎉 '+fmP.need+'m လမ်းလျှောက်ပြီ!'); }
    } else if(fmP.type==='hide' && !S.missionDone){""")
# blackout more frequent + longer on lower floors
rep("    if(S.blackout>0){ S.blackout-=dt; }\n    else { S.blackoutTimer-=dt; if(S.blackoutTimer<=0){ S.blackout=2.0; S.blackoutTimer=30+Math.random()*15; screamSound(); toast('⚡ မီး ပျက်သွားပြီ!'); } }",
"    if(S.blackout>0){ S.blackout-=dt; }\n    else { S.blackoutTimer-=dt; if(S.blackoutTimer<=0){ S.blackout=2.5; S.blackoutTimer=Math.max(20,35-(15-S.floor))+Math.random()*10; screamSound(); toast('⚡ မီး ပျက်သွားပြီ!'); } }")
# wandering ghost Y, chase time, sound
rep("      wg.outer.visible=true; wg.outer.position.y=(wg.def.name==='Ghost Girl'?0.3:0.1)+Math.sin(t*2.5)*0.06;",
"      wg.outer.visible=true; wg.outer.position.y=(wg.def.floatY||0.1)+Math.sin(t*2.5)*0.06;")
rep("        wg.state='chase'; wg.chaseTimer=S.escaping?8:(wg.def.name==='Child Ghost'?3.5:4.5); if(wg.def.name==='Child Ghost' && typeof giggleSound==='function') giggleSound(); else screamSound(); toast('👻 '+wg.def.name+' လိုက်လာပြီ! ပြေး!');",
"        wg.state='chase'; wg.chaseTimer=S.escaping?8:(wg.def.chaseTime||4.5); if(wg.def.sound==='giggle') giggleSound(); else if(wg.def.sound==='whisper') whisperSound(); else if(wg.def.sound==='growl') growlSound(); else if(wg.def.sound==='moan') moanSound(); else screamSound(); toast('👻 '+wg.def.name+' လိုက်လာပြီ! ပြေး!');")
# proximity whisper timer for wandering ghosts (insert before wandering loop end? add after loop: simple timer in update after ghosts loop)
rep("  // V12 FINAL ESCAPE progress:",
"""  if(S.playing && !S.paused){ S.whisperTimer-=dt; if(S.whisperTimer<=0){ let nd=1e9; for(const wg of wanderingGhosts){ if(wg.outer && wg.outer.visible){ const d=Math.hypot(wg.outer.position.x-playerPos.x,wg.outer.position.z-playerPos.z); if(d<nd) nd=d; } } if(nd<6 && !S.hidden){ whisperSound(); } S.whisperTimer=3; } }
  // V12 FINAL ESCAPE progress:""")
# version label
rep("V12.1 • 15 ထပ် + လှေကားကနေ ဆင်း + Ep1-10+",
"V13 • လှေကား အစစ် + အထပ်တိုင်း မြေပုံ/မစ်ရှင်/သရဲ မတူ")

open(p,'w',encoding='utf-8').write(t)
print("PATCH PART2 OK")
