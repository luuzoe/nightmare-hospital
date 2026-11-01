p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# FPP hands: two hands attached to camera, visible only in FPP, palm+fingers from capsule/sphere (same style as corpse limbs, skin colour = player)
rep("const camera=new THREE.PerspectiveCamera(62,innerWidth/innerHeight,0.1,120);",
"""const camera=new THREE.PerspectiveCamera(62,innerWidth/innerHeight,0.1,120); scene.add(camera);
// V26 FPP hands: user asked why no two hands in FPP - hands attached to camera, bottom left/right, visible only in FPP
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
handsGroup.visible=false;""")
# In update, after FPP camera block, set hands visibility + bob (insert before flashlight line, which is after camera block in both FPP/TPP paths)
rep("  flash.position.set(playerPos.x,playerPos.y+(S.fpp?1.65:2.2),playerPos.z);",
"""  handsGroup.visible = !!S.fpp && S.playing && !S.paused;
  if(handsGroup.visible){ const bob = (typeof moving!=='undefined' && moving) ? Math.sin(S.time*10)*0.015 : 0; handL.position.y=-0.26+bob; handR.position.y=-0.26-bob; }
  flash.position.set(playerPos.x,playerPos.y+(S.fpp?1.65:2.2),playerPos.z);""")
# Version label
rep("V25 • သရဲအစစ်နဲ့ ကြောက်စရာကောင်း — လိုက်တာ ပိုဝေး, ရှေ့တည့်တည့် ပိုခဏပေါ်",
"V26 • FPP လက်နှစ်ဖက် — ကင်မရာ အောက်မှာ လက်ဘဲ/ညာ ပေါ်မယ်")
open(p,'w',encoding='utf-8').write(t)
print("V26 PATCH OK")
