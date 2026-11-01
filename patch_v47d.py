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

rep("      for(const dw of doorWalls){ if(dw.doorOpen && dw.z===w.z && Math.abs(x-dw.x)<1.3){ nearOpen=true; break; } }",
    "      for(const dw of doorWalls){ if(dw.doorOpen && dw.z===w.z && Math.abs(x-dw.x)<1.5){ nearOpen=true; break; } }",
    "door assist 1.5")
rep("  x=Math.max(-56,x); x=Math.min(56,x); z=Math.max(-22,z); z=Math.min(22,z);",
    "  x=Math.max(-83,x); x=Math.min(83,x); z=Math.max(-29,z); z=Math.min(29,z);",
    "collide bounds v47")
rep("  if(typeof entranceDoor!=='undefined') entranceDoor.position.z=S.entranceAnim*6.0;",
    "  if(typeof entranceDoor!=='undefined') entranceDoor.position.z=S.entranceAnim*10.0;",
    "entrance anim v47")
rep("      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*2.0;",
    "      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*2.5;",
    "door slide 2.5")
# staircase Y + descent: replace old inStair block
rep("""  S.inStair=(playerPos.z>24 && playerPos.x>=-2.5 && playerPos.x<=2.5);
  if(S.inStair){ playerPos.y=stairY(playerPos.z); if(moving){ const sidx=Math.floor((playerPos.z-25)/1.05); if(sidx!==S._lastStep){ S._lastStep=sidx; footstepSound(); } } }
  else playerPos.y=0;""",
    """  // V47 REAL STAIRCASE: hall x -9.5..-5.5, z -30..-5, player actually descends 0 -> -3m as he walks north.
  S.inStair=(playerPos.x>=-9.5 && playerPos.x<=-5.5 && playerPos.z>=-30 && playerPos.z<=-5);
  if(S.inStair){ const hallY=Math.max(-3, Math.min(0, (playerPos.z+5)/25*3)); playerPos.y=hallY; if(moving){ const sidx=Math.floor((-6.5-playerPos.z)/1.5); if(sidx!==S._lastStep){ S._lastStep=sidx; footstepSound(); } } }
  else playerPos.y=0;""",
    "staircase Y v47")
# descent trigger: hall bottom z <= -21, not whole hall rectangle
rep("  // V46 STAIRCASE HALL: mission complete + stand in hall x -7..-3, z -23..-3 (left N5-N6) -> descend.\n  if(missionComplete() && S.floor>1 && !S._landing && playerPos.x>=-7 && playerPos.x<=-3 && playerPos.z>=-23 && playerPos.z<=-3){ S._landing=true; toast('⬇️ လှေကားကနေ အောက်ထပ် ဆင်းမယ်!'); goToNextFloor(); }",
    "  // V47 STAIRCASE BOTTOM: mission complete + walk all the way down to z <= -21 in hall -> descend. If not complete, warn once and walk back up.\n  if(S.floor>1 && !S._landing && playerPos.x>=-9.5 && playerPos.x<=-5.5 && playerPos.z<=-21){ if(missionComplete()){ S._landing=true; toast('⬇️ လှေကားအောက်ရောက်ပြီ! အောက်ထပ် ဆင်းမယ်!'); goToNextFloor(); } else if(!S._hallWarn){ S._hallWarn=true; toast('🔒 လှေကားအောက်ရောက်ပြီ၊ ဒါပေမယ့် လုပ်စရာ ကျန်သေးသည် — ပြန်တက်ပါ'); } }\n  if(playerPos.z>-5) S._hallWarn=false;",
    "descent bottom v47")
# spawn west, descent spawn, loseheart, continue
rep("  playerPos.set(-54,0,0); S.yaw=Math.PI/2; monsterPos.set(50,0,0); monsterState='patrol'; patrolIdx=0;",
    "  playerPos.set(-81,0,0); S.yaw=Math.PI/2; monsterPos.set(80,0,0); monsterState='patrol'; patrolIdx=0;",
    "reset spawn v47")
rep("  playerPos.set(-5,0,-13); playerPos.y=0; S.yaw=0; monsterPos.set(50,0,0); monsterState='patrol'; patrolIdx=0;",
    "  playerPos.set(-7.5,0,0); playerPos.y=0; S.yaw=Math.PI/2; monsterPos.set(80,0,0); monsterState='patrol'; patrolIdx=0;",
    "descent spawn v47")
rep("  playerPos.set(-5,0,0); S.yaw=Math.PI/2; monsterPos.set(50,0,0); monsterState='patrol'; S.chase=false;",
    "  playerPos.set(-7.5,0,0); S.yaw=Math.PI/2; monsterPos.set(80,0,0); monsterState='patrol'; S.chase=false;",
    "loseheart v47")
rep("playerPos.set(sv.floor===15?-54:-5,0,sv.floor===15?0:-13); playerPos.y=0; S.yaw=sv.floor===15?Math.PI/2:0; monsterPos.set(50,0,0);",
    "playerPos.set(sv.floor===15?-81:-7.5,0,0); playerPos.y=0; S.yaw=Math.PI/2; monsterPos.set(80,0,0);",
    "continue spawn v47")
# exit interact + handler escape door
rep("  const ed=Math.hypot(-5-playerPos.x,-3-playerPos.z);",
    "  const ed=Math.hypot(-7.5-playerPos.x,-5-playerPos.z);",
    "exit interact v47")
rep("    } else if(S.floor===1){ S.escapeDoorX=-5; S.escapeDoorZ=-13; startEscape(); }",
    "    } else if(S.floor===1){ S.escapeDoorX=-7.5; S.escapeDoorZ=-29; startEscape(); }",
    "exit handler v47")
# compass defaults
t = t.replace("let tx=-5,tz=-3,tlabel='လှေကား';", "let tx=-7.5,tz=-5,tlabel='လှေကား';")
print('OK: compass default v47')
t = t.replace("tx=-5; tz=-3;", "tx=-7.5; tz=-5;")
print('OK: compass fallbacks v47')
t = t.replace("tx=50; tz=0; tlabel='Switch';", "tx=80; tz=0; tlabel='Switch';")
print('OK: compass switch v47')
# roomDoorFor north/south new
rep("""  if(px>=-7 && px<=-3 && pz>=-23 && pz<=-3) return [-5,-3];
  if(pz<-3){
    const NR=[[-57,-47],[-47,-37],[-37,-27],[-27,-17],[-17,-7],[-3,7],[7,17],[17,27],[27,37],[37,47],[47,57]];
    for(let i=0;i<NORTH_CENTRES.length;i++){
      if(px>=NR[i][0] && px<NR[i][1]) return [NORTH_CENTRES[i],-3];
    }
  }
  if(pz>3){
    for(let i=0;i<SOUTH_CENTRES.length;i++){
      if(px>=SOUTH_BOUNDS[i] && px<SOUTH_BOUNDS[i+1]) return [SOUTH_CENTRES[i],3];
    }
  }""",
    """  if(px>=-9.5 && px<=-5.5 && pz>=-30 && pz<=-5) return [-7.5,-5];
  if(pz<-5){
    const NR=[[-84.5,-69.5],[-69.5,-54.5],[-54.5,-39.5],[-39.5,-24.5],[-24.5,-9.5],[-5.5,9.5],[9.5,24.5],[24.5,39.5],[39.5,54.5],[54.5,69.5],[69.5,84.5]];
    for(let i=0;i<NORTH_CENTRES.length;i++){
      if(px>=NR[i][0] && px<NR[i][1]) return [NORTH_CENTRES[i],-5];
    }
  }
  if(pz>5){
    for(let i=0;i<SOUTH_CENTRES.length;i++){
      if(px>=SOUTH_BOUNDS[i] && px<SOUTH_BOUNDS[i+1]) return [SOUTH_CENTRES[i],5];
    }
  }""",
    "roomDoorFor v47")
# compass east fallback 50 -> 80
t = t.replace("if(px>50 && tx<=50) return [50,0];", "if(px>80 && tx<=80) return [80,0];")
t = t.replace("if(px<=50 && tx>50) return [50,0];", "if(px<=80 && tx>80) return [80,0];")
print('OK: compass east v47')
# escapeDoor defaults in reset / startEscape
t = t.replace("S.escapeDoorX=-5; S.escapeDoorZ=-13; S.floor=15;", "S.escapeDoorX=-7.5; S.escapeDoorZ=-29; S.floor=15;")
t = t.replace("if(S.stage!==2){ S.escapeDoorX=-5; S.escapeDoorZ=-13; }", "if(S.stage!==2){ S.escapeDoorX=-7.5; S.escapeDoorZ=-29; }")
print('OK: escapeDoor defaults v47')
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part4 applied')
