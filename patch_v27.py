p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:250]
    t=t.replace(old,new,1)

# 1) Real hands: replace oval makeHand with real CC0 hand GLB (Innerscene hand-posable, MakeHuman base)
old_hands="""// V26 FPP hands: user asked why no two hands in FPP - hands attached to camera, bottom left/right, visible only in FPP
const handsGroup=new THREE.Group(); camera.add(handsGroup);
function makeHand(side){
  const g=new THREE.Group(); const skin=new THREE.MeshStandardMaterial({color:0xcccccc,roughness:0.9});
  const palm=new THREE.Mesh(new THREE.SphereGeometry(0.055,10,10),skin); palm.scale.set(0.85,1.15,0.45); g.add(palm);
  for(let i=0;i<4;i++){
    const f=new THREE.Mesh(new THREE.CapsuleGeometry(0.011,0.05,4,8),skin);
    f.position.set(-0.033+i*0.022, 0.02, -0.055); f.rotation.x=Math.PI/2-0.25; g.add(f);
  }
  const th=new THREE.Mesh(new THREE.CapsuleGeometry(0.012,0.04,4,8),skin);
  th.position.set(side*0.055, -0.01, -0.03); th.rotation.z=side*-0.7; th.rotation.x=0.4; g.add(th);
  return g;
}
const handL=makeHand(-1); handL.position.set(-0.22,-0.26,-0.55); handL.rotation.set(-0.2,0,0.15); handsGroup.add(handL);
const handR=makeHand(1); handR.position.set(0.22,-0.26,-0.55); handR.rotation.set(-0.2,0,-0.15); handsGroup.add(handR);
handsGroup.visible=false;"""
new_hands="""// V27 REAL hands: CC0 anatomical right hand (Innerscene hand-posable.glb, MakeHuman base, 18.6cm, softly curved fingers, no animation) - V26 oval hands removed, user was right they looked like eggs
const handsGroup=new THREE.Group(); camera.add(handsGroup);
const handL=new THREE.Group(); handL.position.set(-0.20,-0.22,-0.45); handL.rotation.set(0.1,0.15,0); handsGroup.add(handL);
const handR=new THREE.Group(); handR.position.set(0.20,-0.22,-0.45); handR.rotation.set(0.1,-0.15,0); handsGroup.add(handR);
handsGroup.visible=false;
const handLoader=new GLTFLoader();
handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1,1,1); handR.add(inner); }, undefined, ()=>{});
handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1,1,1); inner.traverse(o=>{ if(o.isMesh){ o.material.side=THREE.DoubleSide; } }); handL.add(inner); }, undefined, ()=>{});"""
rep(old_hands,new_hands)
# bob base y -0.26 -> -0.22 for real hands
rep("if(handsGroup.visible){ const bob = (typeof moving!=='undefined' && moving) ? Math.sin(S.time*10)*0.015 : 0; handL.position.y=-0.26+bob; handR.position.y=-0.26-bob; }",
    "if(handsGroup.visible){ const bob = (typeof moving!=='undefined' && moving) ? Math.sin(S.time*10)*0.015 : 0; handL.position.y=-0.22+bob; handR.position.y=-0.22-bob; }")

# 2) Remove cone apparitions entirely (V15 toy cone ghosts - user said they were gone, but apparitions were still in)
old_app="""const apparitions=[];
for(let i=0;i<8;i++){
  const g=new THREE.Group();
  const body=new THREE.Mesh(new THREE.ConeGeometry(0.6,1.6,12,1,true), new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.45,side:THREE.DoubleSide})); body.position.y=0.8;
  const head=new THREE.Mesh(new THREE.SphereGeometry(0.28,10,10), new THREE.MeshBasicMaterial({color:0xe8e8e8,transparent:true,opacity:0.6})); head.position.y=1.9;
  const e1=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8), new THREE.MeshBasicMaterial({color:0xff0000})); e1.position.set(-0.1,1.95,0.24);
  const e2=e1.clone(); e2.position.x=0.1;
  g.add(body,head,e1,e2); g.position.set(0,0,0); g.visible=false; scene.add(g);
  apparitions.push({mesh:g, timer:3+i*2, visible:false});
}"""
rep(old_app, "const apparitions=[]; // V27 REMOVED: cone apparitions were the toy ghost user saw in screenshot 1282 - no cone/sphere ghosts remain")

# 3) Ghost Girl Animated: walk/run animations make it lie/fly horizontal in this engine - switch to idle_1 only (standing, gliding like a ghost)
rep("if(wg.def.name==='Ghost Girl Animated'){ want = wg.state==='chase' ? 'run' : (wg.state==='scare' ? 'idle_1' : 'walk'); }",
    "if(wg.def.name==='Ghost Girl Animated'){ want = 'idle_1'; } // V27: walk/run made it lie horizontal in screenshot 1283 - idle only, standing/gliding")

# version label
rep("V26 • FPP လက်နှစ်ဖက် — ကင်မရာ အောက်မှာ လက်ဘဲ/ညာ ပေါ်မယ်",
    "V27 • လက်အစစ် + cone သရဲ ဖျက် + Ghost Girl မတ်တပ်ရပ်")
open(p,'w',encoding='utf-8').write(t)
print("V27 PATCH OK")
