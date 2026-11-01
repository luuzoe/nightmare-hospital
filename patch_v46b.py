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

# collide: new bounds 114x46, door assist 1.3m for 2m door
rep("      for(const dw of doorWalls){ if(dw.doorOpen && dw.z===w.z && Math.abs(x-dw.x)<1.0){ nearOpen=true; break; } }",
    "      for(const dw of doorWalls){ if(dw.doorOpen && dw.z===w.z && Math.abs(x-dw.x)<1.3){ nearOpen=true; break; } }",
    "door assist 1.3")
rep("  if(allowStair && x>=-2.3 && x<=2.3){ x=Math.max(-2,x); x=Math.min(2,x); z=Math.max(-23,z); z=Math.min(38.5,z); } else { x=Math.max(-31,x); x=Math.min(69,x); z=Math.max(-23,z); z=Math.min(23,z); }",
    "  x=Math.max(-56,x); x=Math.min(56,x); z=Math.max(-22,z); z=Math.min(22,z);",
    "collide bounds 114x46")
# entrance door animation: slide in z, not x
rep("  if(typeof entranceDoor!=='undefined') entranceDoor.position.x=-19+S.entranceAnim*6.0;",
    "  if(typeof entranceDoor!=='undefined') entranceDoor.position.z=S.entranceAnim*6.0;",
    "entrance anim z")
# door slide 2.0
rep("      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*1.5;",
    "      if(dw.mesh) dw.mesh.position.x=dw.closedX+dw.anim*2.0;",
    "door slide 2m")
# staircase descent trigger: hall rectangle, not (0,0)
rep("  // V44 MIDDLE STAIRCASE: mission complete + stand on centre (0,0) within 2m -> descend, same as south door.\n  if(missionComplete() && S.floor>1 && !S._landing && Math.hypot(playerPos.x,playerPos.z)<2.0){ S._landing=true; toast('⬇️ အလယ် လှေကားကနေ ဆင်းမယ်!'); goToNextFloor(); }",
    "  // V46 STAIRCASE HALL: mission complete + stand in hall x -7..-3, z -23..-3 (left N5-N6) -> descend.\n  if(missionComplete() && S.floor>1 && !S._landing && playerPos.x>=-7 && playerPos.x<=-3 && playerPos.z>=-23 && playerPos.z<=-3){ S._landing=true; toast('⬇️ လှေကားကနေ အောက်ထပ် ဆင်းမယ်!'); goToNextFloor(); }",
    "staircase descent trigger")
# actBtn text for exit
rep("  $('actBtn').textContent=S.interactTarget?((S.interactTarget.type==='exit'&&S.doorOpen)?'✋ လှေကား ဆင်း':((S.interactTarget.type==='exit'||S.interactTarget.type==='exit2'||S.interactTarget.type==='switch')?'✋ ဖွင့်':'✋ ယူ')):'✋ ယူ';",
    "  $('actBtn').textContent=S.interactTarget?((S.interactTarget.type==='exit')?'✋ လှေကား ဆင်း':((S.interactTarget.type==='exit2'||S.interactTarget.type==='switch')?'✋ ဖွင့်':'✋ ယူ')):'✋ ယူ';",
    "actBtn exit")
# exit handler: staircase, no south door opening
rep("""  } else if(t.type==='exit'){
    if(!missionComplete()){
      const fmE=floorMission();
      toast('🔒 တံခါးပိတ်နေသည် — လုပ်စရာ ကျန်သေးသည်: '+missionProgressText()+' (လိုအပ်: '+fmE.need+')');
    } else if(S.floor===1){ S.escapeDoorX=0; S.escapeDoorZ=24; startEscape(); }
    else if(S.doorOpen){ S.yaw=0; toast('⬇️ လှေကားဘက် လှည့်ပြီ! ဂျွိုင်းစတစ်ကို အပေါ်တွန်းပြီး ဆင်းပါ'); }
    else { S.doorOpen=true; if(exitBlock){ const i=walls.indexOf(exitBlock); if(i>=0) walls.splice(i,1); } doorSound(); toast('🚪 တံခါး ပွင့်ပြီ! လှေကားကနေ တစ်ထစ်ချင်း ဆင်းပါ'); }
  }""",
    """  } else if(t.type==='exit'){
    if(!missionComplete()){
      const fmE=floorMission();
      toast('🔒 လှေကားပိတ်နေသည် — လုပ်စရာ ကျန်သေးသည်: '+missionProgressText()+' (လိုအပ်: '+fmE.need+')');
    } else if(S.floor===1){ S.escapeDoorX=-5; S.escapeDoorZ=-13; startEscape(); }
    else { toast('⬇️ လှေကား ထဲ ဝင်ပါ (ဘယ်ဘက် N5-N6 ကြား, 4m လှေကား)!'); goToNextFloor(); }
  }""",
    "exit handler staircase")
# hide spots
rep("const hideSpots=[{x:-28,z:-12},{x:28,z:-12},{x:-28,z:12},{x:28,z:12},{x:-14,z:-20}];",
    "const hideSpots=[{x:-52,z:-13},{x:52,z:-13},{x:-52,z:13},{x:48,z:13},{x:-32,z:-13}];",
    "hide spots new")
# keys: north room3, south room5, north room9, south room8, south room1
rep("""const keyDefs=[
  {id:1,x:-17,z:-12,room:'လူနာဆောင်',label:'သော့ 1'},
  {id:2,x:-6,z:12,room:'ဓာတ်ခွဲခန်း',label:'သော့ 2'},
  {id:3,x:17,z:-12,room:'အော်ပရေး ခန်း',label:'သော့ 3'},
  {id:4,x:10,z:12,room:'Pharmacy',label:'Pharmacy သော့'},
  {id:5,x:-28,z:20,room:'Reception',label:'Reception သော့'},
];""",
    """const keyDefs=[
  {id:1,x:-32,z:-12,room:'လူနာဆောင်',label:'သော့ 1'},
  {id:2,x:-12,z:12,room:'ဓာတ်ခွဲခန်း',label:'သော့ 2'},
  {id:3,x:32,z:-12,room:'အော်ပရေး ခန်း',label:'သော့ 3'},
  {id:4,x:18,z:12,room:'Pharmacy',label:'Pharmacy သော့'},
  {id:5,x:-52,z:12,room:'Reception',label:'Reception သော့'},
];""",
    "keys new")
# switches: A north room2, B south room6, C corridor east
rep("const switchMesh2=makeSwitch(-23,-13); const switchMesh3=makeSwitch(0,10);",
    "const switchMesh2=makeSwitch(-42,-13); const switchMesh3=makeSwitch(-2,13);",
    "switch meshes new")
rep("const switchesList=[{x:-23,z:-13,label:'Switch A'},{x:0,z:10,label:'Switch B'},{x:68,z:5,label:'Switch C'}];",
    "const switchesList=[{x:-42,z:-13,label:'Switch A'},{x:-2,z:13,label:'Switch B'},{x:50,z:0,label:'Switch C'}];",
    "switches list new")
rep("switchMesh.position.set(68,0,5);",
    "switchMesh.position.set(50,0,0);",
    "switch mesh corridor east")
rep("medkitMesh.position.set(12,0.8,14);",
    "medkitMesh.position.set(20,0.8,0);",
    "medkit corridor east")
rep("if(Math.hypot(12-playerPos.x,14-playerPos.z)<1.8 && S.hearts<3)",
    "if(Math.hypot(20-playerPos.x,0-playerPos.z)<1.8 && S.hearts<3)",
    "medkit pickup new")
# corpses: 6 rooms new
rep("""const corpseDefs=[
  {x:-23,z:-15,yaw:Math.PI/2}, {x:0,z:-15,yaw:0.5}, {x:23,z:-15,yaw:2.2},
  {x:-23,z:15,yaw:1.0}, {x:0,z:15,yaw:2.8}, {x:23,z:15,yaw:0},
];""",
    """const corpseDefs=[
  {x:-42,z:-15,yaw:Math.PI/2}, {x:2,z:-15,yaw:0.5}, {x:42,z:-15,yaw:2.2},
  {x:-42,z:15,yaw:1.0}, {x:-2,z:15,yaw:2.8}, {x:38,z:15,yaw:0},
];""",
    "corpses new")
# patrol + path nodes new, no east wing
rep("const patrolPts=[[-28,0],[-16,0],[0,0],[16,0],[28,0],[0,-13],[0,13],[-23,-13],[23,13],[36,0],[55,0],[65,0]]; // V44 corridor + rooms + east wing",
    "const patrolPts=[[-54,0],[-30,0],[-5,0],[20,0],[50,0],[-32,-13],[32,-13],[-12,13],[28,13],[55,0]];",
    "patrol new")
rep("const pathNodes=[[0,0],[-16,0],[16,0],[-28,0],[28,0],[-29,-3],[-23,-3],[-17,-3],[-11,-3],[-5,-3],[0,-3],[6,-3],[12,-3],[17,-3],[23,-3],[29,-3],[-29,3],[-23,3],[-17,3],[-11,3],[-5,3],[0,3],[6,3],[12,3],[17,3],[23,3],[29,3],[36,0],[45,0],[55,0],[65,0]]; // V44 corridor + door centres + east wing",
    "const pathNodes=[[-54,0],[-30,0],[-5,0],[20,0],[50,0],[-52,-3],[-42,-3],[-32,-3],[-22,-3],[-12,-3],[2,-3],[12,-3],[22,-3],[32,-3],[42,-3],[52,-3],[-52,3],[-42,3],[-32,3],[-22,3],[-12,3],[-2,3],[8,3],[18,3],[28,3],[38,3],[48,3],[-5,-13],[55,13]];",
    "path nodes new")
# resetGame spawn west
rep("  playerPos.set(-28,0,0); S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; patrolIdx=0;",
    "  playerPos.set(-54,0,0); S.yaw=Math.PI/2; monsterPos.set(50,0,0); monsterState='patrol'; patrolIdx=0;",
    "reset spawn west")
# continueGame spawn: floor15 west, else staircase hall
rep("S.floor=sv.floor; S.hearts=sv.hearts||3; playerPos.set(-28,0,0); playerPos.y=0; S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; startFloorMission();",
    "S.floor=sv.floor; S.hearts=sv.hearts||3; playerPos.set(sv.floor===15?-54:-5,0,sv.floor===15?0:-13); playerPos.y=0; S.yaw=sv.floor===15?Math.PI/2:0; monsterPos.set(50,0,0); monsterState='patrol'; startFloorMission();",
    "continue spawn new")
# goToNextFloor spawn: staircase hall
rep("  playerPos.set(-28,0,0); playerPos.y=0; S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; patrolIdx=0;",
    "  playerPos.set(-5,0,-13); playerPos.y=0; S.yaw=0; monsterPos.set(50,0,0); monsterState='patrol'; patrolIdx=0;",
    "descent spawn staircase hall")
# loseHeart respawn: corridor near staircase
rep("  playerPos.set(-28,0,0); S.yaw=Math.PI/2; monsterPos.set(20,0,16); monsterState='patrol'; S.chase=false;",
    "  playerPos.set(-5,0,0); S.yaw=Math.PI/2; monsterPos.set(50,0,0); monsterState='patrol'; S.chase=false;",
    "loseheart respawn corridor")
# exit interact position -> staircase hall entrance
rep("  const ed=Math.hypot(0-playerPos.x,24-playerPos.z);\n  if(ed<2.5 && !S.interactTarget) S.interactTarget={type:'exit',label:missionComplete()?(S.floor===1?'🚪 Final Escape ဖွင့်':(S.doorOpen?'🚪 လှေကား ဆင်း':'🚪 တံခါး ဖွင့်')):'🚪 တံခါး (ပိတ်ထားသည်)'};",
    "  const ed=Math.hypot(-5-playerPos.x,-3-playerPos.z);\n  if(ed<2.5 && !S.interactTarget) S.interactTarget={type:'exit',label:missionComplete()?(S.floor===1?'🚪 Final Escape ဖွင့်':'⬇️ လှေကား ဆင်း'):'🔒 လှေကား (ပိတ်ထားသည်)'};",
    "exit interact staircase")
# final switch interact position
rep("    if(!S.interactTarget && fmI.type==='final' && S.items>=fmI.need && !S.switchOn && Math.hypot(68-playerPos.x,5-playerPos.z)<2.5) S.interactTarget={type:'switchFloor',label:'⚡ Switch'};",
    "    if(!S.interactTarget && fmI.type==='final' && S.items>=fmI.need && !S.switchOn && Math.hypot(50-playerPos.x,0-playerPos.z)<2.5) S.interactTarget={type:'switchFloor',label:'⚡ Switch'};",
    "final switch interact new")
# compass fallbacks: (0,24) -> staircase (-5,-3), (68,5) -> (50,0)
t = t.replace("let tx=0,tz=24,tlabel='အဓိက တံခါး';", "let tx=-5,tz=-3,tlabel='လှေကား';")
print('OK: compass default staircase')
t = t.replace("tx=68; tz=5; tlabel='Switch';", "tx=50; tz=0; tlabel='Switch';")
print('OK: compass switch new')
# replace all remaining compass fallbacks tx=0,tz=24 with staircase
cnt = t.count("tx=0; tz=24;")
t = t.replace("tx=0; tz=24;", "tx=-5; tz=-3;")
print('OK: compass fallbacks replaced', cnt)
t = t.replace("tlabel='အောက်ထပ် တံခါး'", "tlabel='အောက်ထပ် လှေကား'")
t = t.replace("tlabel=S.floor===1?'Final တံခါး':'အောက်ထပ် တံခါး'", "tlabel=S.floor===1?'Final လှေကား':'အောက်ထပ် လှေကား'")
# objective texts: south door -> staircase hall
t = t.replace("တောင်တံခါး သွား", "လှေကား (N5-N6 ကြား) သွား")
t = t.replace("တောင်ဘက် တံခါးကို သွားပါ", "လှေကား (N5-N6 ကြား) ကို သွားပါ")
t = t.replace("တောင်တံခါးကို သွားပါ", "လှေကား (N5-N6 ကြား) ကို သွားပါ")
t = t.replace("တိုးတက်မှု ပြန်ရပြီ! တောင်တံခါး သွား", "တိုးတက်မှု ပြန်ရပြီ! လှေကား သွား")
print('OK: objective texts staircase')

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V46 part2 applied')
