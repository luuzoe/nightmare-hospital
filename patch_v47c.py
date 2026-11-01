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

# room props beds positions
rep("""for(let i=0;i<NORTH_CENTRES.length;i++){
  const dc=NORTH_CENTRES[i];
  const col=[0x6a6a6a,0x5a4632,0x3a4a3a,0x8a8f8a,0x4a4a4a,0x9aa0a0][i%6];
  addProp(dc,-16,2.2,1.1,0.7,col,'roomprop');
}
for(let i=0;i<SOUTH_CENTRES.length;i++){
  const dc=SOUTH_CENTRES[i];
  const col=[0x5a4632,0x6a6a6a,0x8a8f8a,0x3a4a3a,0x4a4a4a,0x9aa0a0][i%6];
  addProp(dc,16,2.2,1.1,0.7,col,'roomprop');
}
for(const [dx,dz] of [[-30,0],[0,0],[30,0],[-5,-13],[55,13]]){ addProp(dx,dz,1.5,0.8,0.4,0x1a1a1a,'debris'); }""",
    """for(let i=0;i<NORTH_CENTRES.length;i++){
  const dc=NORTH_CENTRES[i];
  const col=[0x6a6a6a,0x5a4632,0x3a4a3a,0x8a8f8a,0x4a4a4a,0x9aa0a0][i%6];
  addProp(dc,-22,2.2,1.1,0.7,col,'roomprop');
}
for(let i=0;i<SOUTH_CENTRES.length;i++){
  const dc=SOUTH_CENTRES[i];
  const col=[0x5a4632,0x6a6a6a,0x8a8f8a,0x3a4a3a,0x4a4a4a,0x9aa0a0][i%6];
  addProp(dc,22,2.2,1.1,0.7,col,'roomprop');
}
for(const [dx,dz] of [[-50,0],[0,0],[50,0],[-7.5,-17.5],[80,17.5]]){ addProp(dx,dz,1.5,0.8,0.4,0x1a1a1a,'debris'); }""",
    "room props v47")
# real bed positions
rep("    for(let i=0;i<NORTH_CENTRES.length;i++){ const dc=NORTH_CENTRES[i]; const b=tpl.clone(true); b.position.set(dc+2,0,-16); b.rotation.y=0; b.rotation.z=(i%4===1)?0.18:0; scene.add(b); }\n    for(let i=0;i<SOUTH_CENTRES.length;i++){ const dc=SOUTH_CENTRES[i]; const b=tpl.clone(true); b.position.set(dc-2,0,16); b.rotation.y=Math.PI; b.rotation.z=(i%4===2)?-0.15:0; scene.add(b); }",
    "    for(let i=0;i<NORTH_CENTRES.length;i++){ const dc=NORTH_CENTRES[i]; const b=tpl.clone(true); b.position.set(dc+3,0,-22); b.rotation.y=0; b.rotation.z=(i%4===1)?0.18:0; scene.add(b); }\n    for(let i=0;i<SOUTH_CENTRES.length;i++){ const dc=SOUTH_CENTRES[i]; const b=tpl.clone(true); b.position.set(dc-3,0,22); b.rotation.y=Math.PI; b.rotation.z=(i%4===2)?-0.15:0; scene.add(b); }",
    "bed positions v47")
# hide spots, keys, switches, medkit, corpses
rep("const hideSpots=[{x:-52,z:-13},{x:52,z:-13},{x:-52,z:13},{x:48,z:13},{x:-32,z:-13}];",
    "const hideSpots=[{x:-77,z:-17.5},{x:77,z:-17.5},{x:-77,z:17.5},{x:73,z:17.5},{x:-47,z:-17.5}];",
    "hide spots v47")
rep("""const keyDefs=[
  {id:1,x:-32,z:-12,room:'လူနာဆောင်',label:'သော့ 1'},
  {id:2,x:-12,z:12,room:'ဓာတ်ခွဲခန်း',label:'သော့ 2'},
  {id:3,x:32,z:-12,room:'အော်ပရေး ခန်း',label:'သော့ 3'},
  {id:4,x:18,z:12,room:'Pharmacy',label:'Pharmacy သော့'},
  {id:5,x:-52,z:12,room:'Reception',label:'Reception သော့'},
];""",
    """const keyDefs=[
  {id:1,x:-47,z:-16,room:'လူနာဆောင်',label:'သော့ 1'},
  {id:2,x:-17,z:16,room:'ဓာတ်ခွဲခန်း',label:'သော့ 2'},
  {id:3,x:47,z:-16,room:'အော်ပရေး ခန်း',label:'သော့ 3'},
  {id:4,x:28,z:16,room:'Pharmacy',label:'Pharmacy သော့'},
  {id:5,x:-77,z:16,room:'Reception',label:'Reception သော့'},
];""",
    "keys v47")
rep("const switchMesh2=makeSwitch(-42,-13); const switchMesh3=makeSwitch(-2,13);",
    "const switchMesh2=makeSwitch(-62,-17.5); const switchMesh3=makeSwitch(-2,17.5);",
    "switch meshes v47")
rep("const switchesList=[{x:-42,z:-13,label:'Switch A'},{x:-2,z:13,label:'Switch B'},{x:50,z:0,label:'Switch C'}];",
    "const switchesList=[{x:-62,z:-17.5,label:'Switch A'},{x:-2,z:17.5,label:'Switch B'},{x:80,z:0,label:'Switch C'}];",
    "switches list v47")
rep("switchMesh.position.set(50,0,0);", "switchMesh.position.set(80,0,0);", "switch mesh v47")
rep("medkitMesh.position.set(20,0.8,0);", "medkitMesh.position.set(40,0.8,0);", "medkit v47")
rep("if(Math.hypot(20-playerPos.x,0-playerPos.z)<1.8 && S.hearts<3)", "if(Math.hypot(40-playerPos.x,0-playerPos.z)<1.8 && S.hearts<3)", "medkit pickup v47")
rep("""const corpseDefs=[
  {x:-42,z:-15,yaw:Math.PI/2}, {x:2,z:-15,yaw:0.5}, {x:42,z:-15,yaw:2.2},
  {x:-42,z:15,yaw:1.0}, {x:-2,z:15,yaw:2.8}, {x:38,z:15,yaw:0},
];""",
    """const corpseDefs=[
  {x:-62,z:-20,yaw:Math.PI/2}, {x:2,z:-20,yaw:0.5}, {x:62,z:-20,yaw:2.2},
  {x:-62,z:20,yaw:1.0}, {x:-2,z:20,yaw:2.8}, {x:58,z:20,yaw:0},
];""",
    "corpses v47")
rep("const patrolPts=[[-54,0],[-30,0],[-5,0],[20,0],[50,0],[-32,-13],[32,-13],[-12,13],[28,13],[55,0]];",
    "const patrolPts=[[-81,0],[-50,0],[-7.5,0],[30,0],[80,0],[-47,-17.5],[47,-17.5],[-17,17.5],[43,17.5],[80,0]];",
    "patrol v47")
rep("const pathNodes=[[-54,0],[-30,0],[-5,0],[20,0],[50,0],[-52,-3],[-42,-3],[-32,-3],[-22,-3],[-12,-3],[2,-3],[12,-3],[22,-3],[32,-3],[42,-3],[52,-3],[-52,3],[-42,3],[-32,3],[-22,3],[-12,3],[-2,3],[8,3],[18,3],[28,3],[38,3],[48,3],[-5,-13],[55,13]];",
    "const pathNodes=[[-81,0],[-50,0],[-7.5,0],[30,0],[80,0],[-77,-5],[-62,-5],[-47,-5],[-32,-5],[-17,-5],[2,-5],[17,-5],[32,-5],[47,-5],[62,-5],[77,-5],[-77,5],[-62,5],[-47,5],[-32,5],[-17,5],[-2,5],[13,5],[28,5],[43,5],[58,5],[73,5],[-7.5,-17.5],[-7.5,-29],[82,17.5]];",
    "path nodes v47")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part3 applied')
