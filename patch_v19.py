p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# Corpses: c0 centre corridor -> NW room, c3 inside desk -> SW room free spot, c5 north corridor middle -> north end
rep("""const corpseDefs=[
  {x:2,z:0,yaw:Math.PI/2}, {x:-18,z:-12,yaw:0.5}, {x:24,z:-10,yaw:2.2},
  {x:-24,z:16,yaw:1.0}, {x:26,z:16,yaw:2.8}, {x:0,z:-12,yaw:0},
];""",
"""const corpseDefs=[
  {x:-20,z:-20,yaw:Math.PI/2}, {x:-18,z:-12,yaw:0.5}, {x:24,z:-10,yaw:2.2},
  {x:-24,z:12,yaw:1.0}, {x:26,z:16,yaw:2.8}, {x:0,z:-20,yaw:0},
];""")
# Partition slot 0: bed overlap fix
rep("  const partSlots=[[-20,-18],[20,-18],[-20,18],[20,18]];",
"  const partSlots=[[-22,-18],[20,-18],[-20,18],[20,18]];")
# Vertical walls: add gaps at z=-12 and z=12 (north-centre was a dead end, now a passage)
rep("""// vertical corridor walls x=-4 and x=4, gap -3..3
for(const x of [-4,4]){
  addWall(x,-13.5,0.6,21); addWall(x,13.5,0.6,21);
}""",
"""// vertical corridor walls x=-4 and x=4, gaps -3..3 (middle), -14..-10 (north, V19), 10..14 (south, V19) - north-centre was a dead end before
for(const x of [-4,4]){
  addWall(x,-19,0.6,10); addWall(x,-6.5,0.6,7); addWall(x,6.5,0.6,7); addWall(x,19,0.6,10);
}""")
# Gap frames for new vertical gaps
rep("makeGapFrame(-4,0,false); makeGapFrame(4,0,false);",
"""makeGapFrame(-4,0,false); makeGapFrame(4,0,false);
function makeVGapFrame(x,z){ const mat=new THREE.MeshBasicMaterial({color:0x00ff88,transparent:true,opacity:0.85}); for(const s of [-2,2]){ const pil=new THREE.Mesh(new THREE.BoxGeometry(0.35,3.4,0.35),mat); pil.position.set(x,1.7,z+s); scene.add(pil); } const beam=new THREE.Mesh(new THREE.BoxGeometry(0.35,0.3,4.4),mat); beam.position.set(x,3.3,z); scene.add(beam); }
makeVGapFrame(-4,-12); makeVGapFrame(4,-12); makeVGapFrame(-4,12); makeVGapFrame(4,12);""")
# Ghost spawns: avoid corpse/key/locker exact matches
rep("pos:[28,12], wps:[[28,12],[20,12],[0,0],[24,0]]",
"pos:[24,20], wps:[[24,20],[20,12],[0,0],[24,0]]")
rep("pos:[-18,-12], wps:[[-18,-12],[-24,-6],[0,0],[-16,0]]",
"pos:[-22,-12], wps:[[-22,-12],[-24,-6],[0,0],[-16,0]]")
rep("pos:[-24,16], wps:[[-24,16],[-16,12],[0,0],[-10,12]]",
"pos:[-26,20], wps:[[-26,20],[-16,12],[0,0],[-10,12]]")
rep("pos:[24,-12], wps:[[24,-12],[16,-6],[0,0],[20,0]]",
"pos:[20,-20], wps:[[20,-20],[16,-6],[0,0],[20,0]]")
rep("pos:[-28,20], wps:[[-28,20],[-20,12],[0,0],[-16,0]]",
"pos:[-20,12], wps:[[-20,12],[-16,12],[0,0],[-16,0]]")
# Monster spawn: (20,20) was exactly Morgue key -> (20,16)
t=t.replace("monsterPos.set(20,0,20)", "monsterPos.set(20,0,16)")
t=t.replace("let playerPos=new THREE.Vector3(-18,0,12), monsterPos=new THREE.Vector3(20,0,20);",
"let playerPos=new THREE.Vector3(-18,0,12), monsterPos=new THREE.Vector3(20,0,16);")
# Ghost loading toasts (so user knows ghosts are loading, not dead)
rep("async function loadWanderingGhosts(){",
"async function loadWanderingGhosts(){ toast('👻 သရဲတွေ တင်နေသည်…');")
rep("  if(typeof setActiveGhosts==='function') setActiveGhosts();\n}",
"  if(typeof setActiveGhosts==='function') setActiveGhosts(); toast('👻 သရဲတွေ အဆင်သင့် — '+wanderingGhosts.length+' ကောင်');\n}")
# Version label
rep("V18 • FPP + သရဲရှေ့တည့်တည့် ပေါ်လာ + ကွင်းဖျောက် + သော့လမ်းကြောင်း",
"V19 • Room1 error တွေ ပြင် — အလောင်း/သရဲ ထပ်နေတာ + နံရံ ပေါက်အသစ်")
open(p,'w',encoding='utf-8').write(t)
print("V19 PATCH OK")
