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

rep("V36 • အနီ စာ သေး + အပေါ် + Minimap ကြီး — အကုန်",
    "V37 • Morgue သော့ လွတ်တဲ့ နေရာ + လက် ပြန်မြင် + ခလုတ် သေး — အကုန်",
    "version")
# Morgue key: slab was exactly on key (20,20), narrow 0.5m corridor only. Move to open area south of slab.
rep("  {id:3,x:20,z:20,room:'Morgue',label:'Morgue သော့'},",
    "  {id:3,x:20,z:22,room:'Morgue',label:'Morgue သော့'},",
    "morgue key move")
# Hands back into view: revert inner rotation, position up, scale 1.15
rep("const handL=new THREE.Group(); handL.position.set(-0.20,-0.26,-0.40); handL.rotation.set(0,0.15,0); handsGroup.add(handL);\nconst handR=new THREE.Group(); handR.position.set(0.20,-0.26,-0.40); handR.rotation.set(0,-0.15,0); handsGroup.add(handR);",
    "const handL=new THREE.Group(); handL.position.set(-0.20,-0.22,-0.45); handL.rotation.set(0.1,0.15,0); handsGroup.add(handL);\nconst handR=new THREE.Group(); handR.position.set(0.20,-0.22,-0.45); handR.rotation.set(0.1,-0.15,0); handsGroup.add(handR);",
    "hand position back")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1.0,1.0,1.0); inner.rotation.x=-Math.PI/2; inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});",
    "handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1.15,1.15,1.15); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});",
    "handR rotate revert")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1.0,1.0,1.0); inner.rotation.x=-Math.PI/2; inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{});",
    "handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1.15,1.15,1.15); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{});",
    "handL rotate revert")
# Buttons smaller on landscape phones: add to media query block
rep("  #topbar{padding:6px}\n}",
    "  #topbar{padding:6px}\n  .btn{padding:10px 20px;font-size:16px}\n  .iconbtn{width:42px;height:42px;font-size:18px}\n}",
    "buttons smaller landscape")
# HUD buttons slightly smaller globally: abtn 72 -> 64, big 68 -> 60
rep(".abtn{width:72px;height:72px;",
    ".abtn{width:64px;height:64px;",
    "abtn smaller")
rep(".abtn.big{width:68px;height:68px;",
    ".abtn.big{width:60px;height:60px;",
    "abtn big smaller")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V37 patch applied')
