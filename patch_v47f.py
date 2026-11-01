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

# Story: start screen paragraph + story hints array + floor banner + end text
rep("  <p>🏢 15 ထပ် • Ep1-10+ • အပေါ်ကနေ အောက်ထိ ဆင်း • တစ်ထပ်ပြီး တစ်ထပ် ပိုခက်</p>",
    "  <p>🏢 15 ထပ် • Ep1-15 • အပေါ်ကနေ အောက်ထိ ဆင်း • တစ်ထပ်ပြီး တစ်ထပ် ပိုခက်</p>\n  <p style=\"font-size:14px;color:#ffcccc;line-height:1.5\">📖 ဇာတ်လမ်း: သူနာပြု မေသူ ဒီစွန့်ပစ်ဆေးရုံထဲ ပျောက်သွားတာ ၃ နှစ်ရှိပြီ။ သူ့အစ်ကို မင်းက သူ့ဒိုင်ယာရီ စာမျက်နှာတွေကို တစ်ထပ်ပြီး တစ်ထပ် လိုက်ရှာရမယ်။ အပေါ်ဆုံး 15 ထပ်က စ၊ အောက်ဆုံး 1 ထပ်မှာ အမှန်တရား ရှိတယ်။ ဆေးရုံက မင်းကို စောင့်နေတယ် — တိတ်တိတ် သွား၊ အသံ မဆူပါနဲ့၊ သူ ကြားလိမ့်မယ်။</p>",
    "start story")
# Story hints: insert after FLOOR_MISSIONS definition (find the closing of that object - use the line after it)
rep("function floorMission(){ return FLOOR_MISSIONS[S.floor]||FLOOR_MISSIONS[15]; }",
    """function floorMission(){ return FLOOR_MISSIONS[S.floor]||FLOOR_MISSIONS[15]; }
// V47 STORY: sister May Thu's diary, one hint per floor, top to bottom.
const STORY_HINTS={15:'Ep1 • မေသူ၏ ပထမဆုံး ဒိုင်ယာရီ — “ဒီဆေးရုံက မပိတ်သေးဘူး”',14:'Ep2 • ညဆိုင်း သူနာပြုတွေ ပျောက်နေပြီ',13:'Ep3 • ဒေါက်တာ၏ စမ်းသပ်ခန်း',12:'Ep4 • လူနာတွေ ညက အော်သံ',11:'Ep5 • Locker ထဲမှာ ဝှက်ထားတဲ့ စာ',10:'Ep6 • သရဲကို ဆွဲခေါ်ရမယ့် အခန်း',9:'Ep7 • မှောင်ထဲမှာ ရေးထားတဲ့ နာမည်',8:'Ep8 • အချိန်မီ ပြေးရမယ့် လူနာ',7:'Ep9 • ပုန်းနေရင်း ကြားရတဲ့ ခြေသံ',6:'Ep10 • အလောင်းတွေက စကားပြောတယ်',5:'Ep11 • အခန်း ၄ ခန်းမှာ ဘာရှိလဲ',4:'Ep12 • 180m လမ်းလျှောက်ရင်း တွေ့တဲ့ အရိပ်',3:'Ep13 • မှောင် Locker ထဲက ဒိုင်ယာရီ',2:'Ep14 • အစဉ်လိုက် သော့တွေ — နောက်ဆုံး အဆင့်',1:'Ep15 FINAL • အမှန်တရား — မေသူ ဘယ်ရောက်သွားလဲ'};""",
    "story hints")
# Floor banner in goToNextFloor: replace showFloorBanner line
rep("  if(typeof showFloorBanner==='function') showFloorBanner('🏢 အထပ် '+S.floor+' • Ep'+fm.ep);",
    "  if(typeof showFloorBanner==='function') showFloorBanner(STORY_HINTS[S.floor]||('🏢 အထပ် '+S.floor+' • Ep'+fm.ep));",
    "floor banner story")
# End text: win story
rep("  $('endText').textContent=win?('15 ထပ် ဆေးရုံကနေ လွတ်မြောက်သွားပြီ! အချိန်: '+Math.floor(S.time)+' စက္ကန့်')",
    "  $('endText').textContent=win?('မေသူ၏ ဒိုင်ယာရီကို ရပြီ! 15 ထပ် ဆေးရုံကနေ လွတ်မြောက်သွားပြီ! အချိန်: '+Math.floor(S.time)+' စက္ကန့် — ဒါပေမယ့် ဆေးရုံက မင်းနောက်ကို လိုက်နေတုန်းပဲ…')",
    "end story")
# Ghost eyes: in wandering ghost build, add red eyes to outer
rep("      const inner=gltf.scene; normalizeGroup(inner,def.scale,def.yOffset||0,def.rotX||0);\n      const outer=new THREE.Group(); outer.add(inner);",
    "      const inner=gltf.scene; normalizeGroup(inner,def.scale,def.yOffset||0,def.rotX||0);\n      const outer=new THREE.Group(); outer.add(inner);\n      for(const ex of [-0.12,0.12]){ const eye=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8), new THREE.MeshBasicMaterial({color:0xff0000})); eye.position.set(ex,1.45,0.28); outer.add(eye); } // V47 ghost red eyes, visible in dark",
    "ghost eyes")
# Blood: larger pools at corpses, wall blood to new walls
rep("for(const c of corpseDefs) makeBloodPool(c.x,c.z,1.4+Math.random()*0.4);",
    "for(const c of corpseDefs){ makeBloodPool(c.x,c.z,2.2+Math.random()*0.6); makeBloodPool(c.x+0.8,c.z+0.5,1.2); }",
    "blood pools bigger")
rep("makeWallBlood(-31.6,1.5,-8,Math.PI/2,2.5,1.8); makeWallBlood(31.6,1.5,-8,-Math.PI/2,2.5,1.8); makeWallBlood(-31.6,1.5,12,Math.PI/2,3,2); makeWallBlood(31.6,1.5,12,-Math.PI/2,3,2); makeWallBlood(0,1.5,-23.6,0,3,2); makeWallBlood(0,1.5,23.6,Math.PI,3,2); makeWallBlood(-20,1.5,-2.69,0,2,1.5); makeWallBlood(20,1.5,2.69,Math.PI,2,1.5); makeWallBlood(55,1.5,0,-Math.PI/2,2.5,1.8); makeWallBlood(45,1.5,-14.69,0,2,1.5);",
    "makeWallBlood(-84.2,1.5,-17.5,Math.PI/2,3.5,2.5); makeWallBlood(84.2,1.5,-17.5,-Math.PI/2,3.5,2.5); makeWallBlood(-84.2,1.5,17.5,Math.PI/2,3.5,2.5); makeWallBlood(84.2,1.5,17.5,-Math.PI/2,3.5,2.5); makeWallBlood(0,1.5,-29.6,0,4,2.5); makeWallBlood(0,1.5,29.6,Math.PI,4,2.5); makeWallBlood(-47,1.5,-5.3,0,3,2); makeWallBlood(47,1.5,5.3,Math.PI,3,2); makeWallBlood(80,1.5,0,-Math.PI/2,3,2);",
    "wall blood new walls")
# Flies / maggots bigger + more
rep("for(const c of corpseDefs){\n  for(let i=0;i<6;i++){\n    const grp=new THREE.Group();\n    const body=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8), new THREE.MeshBasicMaterial({color:0x111111}));",
    "for(const c of corpseDefs){\n  for(let i=0;i<10;i++){\n    const grp=new THREE.Group();\n    const body=new THREE.Mesh(new THREE.SphereGeometry(0.09,8,8), new THREE.MeshBasicMaterial({color:0x111111}));",
    "flies bigger")
rep("  for(let i=0;i<6;i++){\n    const grp=new THREE.Group();\n    const mg=new THREE.Mesh(new THREE.CapsuleGeometry(0.035,0.14,4,8), new THREE.MeshStandardMaterial({map:maggotTex,roughness:0.6}));",
    "  for(let i=0;i<10;i++){\n    const grp=new THREE.Group();\n    const mg=new THREE.Mesh(new THREE.CapsuleGeometry(0.05,0.2,4,8), new THREE.MeshStandardMaterial({map:maggotTex,roughness:0.6}));",
    "maggots bigger")
# Corpses scale up 20%
rep("    {src:'dead1.glb',scale:1.0,ox:0,oy:0.4,oz:0,real:true},\n    {src:'dead2.glb',scale:0.01,ox:0.45,oy:0,oz:1.17,real:true},\n    {src:'dead3.glb',scale:0.3048,ox:0.68,oy:0.32,oz:0,real:true},\n    {src:'dead4.glb',scale:1.0,ox:-0.165,oy:0,oz:0,rotX:-Math.PI/2,real:true},\n    {src:'dead2.glb',scale:0.01,ox:0.45,oy:0,oz:1.17,real:true},",
    "    {src:'dead1.glb',scale:1.2,ox:0,oy:0.4,oz:0,real:true},\n    {src:'dead2.glb',scale:0.012,ox:0.45,oy:0,oz:1.17,real:true},\n    {src:'dead3.glb',scale:0.36,ox:0.68,oy:0.32,oz:0,real:true},\n    {src:'dead4.glb',scale:1.2,ox:-0.165,oy:0,oz:0,rotX:-Math.PI/2,real:true},\n    {src:'dead2.glb',scale:0.012,ox:0.45,oy:0,oz:1.17,real:true},",
    "corpses scale v47")
# Hospital props: syringes / medical items as detailed props (not code boxes alone - use cylinders + needles, with labels, in rooms)
rep("// V46 ABANDONED HOSPITAL: ruined, discarded, not just old. Visual only, no collision, never on a door (doors stay 2m clear).",
    """// V47 HOSPITAL PROPS: ruined medical items, visual only, never on a door. Real GLB search is running in background; these detailed props fill rooms until real assets arrive.
function medProp(kind,x,z,ry){ const g=new THREE.Group(); if(kind==='syringe'){ const barrel=new THREE.Mesh(new THREE.CylinderGeometry(0.05,0.05,0.5,10), new THREE.MeshStandardMaterial({color:0xd0e0e0,roughness:0.2})); barrel.rotation.z=Math.PI/2; const needle=new THREE.Mesh(new THREE.CylinderGeometry(0.008,0.008,0.4,6), new THREE.MeshStandardMaterial({color:0xcccccc,metalness:0.8,roughness:0.3})); needle.rotation.z=Math.PI/2; needle.position.x=0.45; const plunger=new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.03,0.2,8), new THREE.MeshStandardMaterial({color:0x222222})); plunger.rotation.z=Math.PI/2; plunger.position.x=-0.35; g.add(barrel,needle,plunger); } else if(kind==='iv'){ const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,1.9,8), new THREE.MeshStandardMaterial({color:0x888888,metalness:0.5})); pole.position.y=0.95; const bag=new THREE.Mesh(new THREE.BoxGeometry(0.3,0.4,0.1), new THREE.MeshStandardMaterial({color:0xffe0a0,transparent:true,opacity:0.7})); bag.position.set(0.2,1.7,0); g.add(pole,bag); } else if(kind==='trolley'){ const top=new THREE.Mesh(new THREE.BoxGeometry(1.2,0.08,0.6), new THREE.MeshStandardMaterial({color:0xaaaaaa,metalness:0.4})); top.position.y=0.9; const shelf=new THREE.Mesh(new THREE.BoxGeometry(1.0,0.06,0.5), top.material); shelf.position.y=0.4; g.add(top,shelf); } g.position.set(x,0.1,z); g.rotation.y=ry||0; scene.add(g); }
for(const [kx,kz] of [[-62,-22],[2,-22],[62,-22],[-62,22],[28,22]]){ medProp('syringe',kx+1,kz,0.5); medProp('syringe',kx-1,kz+1,1.2); }
for(const [kx,kz] of [[-47,-22],[47,-22],[-17,22],[43,22]]){ medProp('iv',kx,kz,0); medProp('trolley',kx+2,kz,0.3); }
// V46 ABANDONED HOSPITAL: ruined, discarded, not just old. Visual only, no collision, never on a door (doors stay 2m clear).""",
    "hospital props v47")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part6 applied')
