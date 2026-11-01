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

rep("V34 • Minimap + လက်ထဲ ဓာတ်မီး + Settings + Save တိုးတက်မှု — အကုန်",
    "V35 • HIDE ပုန်းပြီး လမ်းလျှောက် + သရဲမ အသံ ရှား + လက် လှည့် — အကုန်",
    "version")

# Girl whisper cooldown 60 -> 120
rep("function whisperSound(){ if(S.time-lastGirlTime<60) return;",
    "function whisperSound(){ if(S.time-lastGirlTime<120) return;",
    "whisper cooldown 120")

# Wandering scream cooldown helper, after lastGirlTime declaration
rep("let lastGirlTime=-999;",
    "let lastGirlTime=-999;\nlet lastWanderScream=-999;\nfunction wanderingScream(){ if(S.time-lastWanderScream<20) return; lastWanderScream=S.time; screamSound(); }",
    "wandering scream helper")

# Wandering scare scream -> gated
rep("wanderingScare=true; screamSound(); if(navigator.vibrate) navigator.vibrate(150);",
    "wanderingScare=true; wanderingScream(); if(navigator.vibrate) navigator.vibrate(150);",
    "wandering scare scream gated")

# Wandering chase entry scream -> gated, only the else branch in chase entry
# The chase entry line: if(wg.def.sound==='giggle') giggleSound(); else if(wg.def.sound==='whisper') whisperSound(); else if(wg.def.sound==='growl') growlSound(); else if(wg.def.sound==='moan') moanSound(); else screamSound();
rep("else if(wg.def.sound==='moan') moanSound(); else screamSound(); toast('👻 '+wg.def.name+' လိုက်လာပြီ! ပြေး!');",
    "else if(wg.def.sound==='moan') moanSound(); else wanderingScream(); toast('👻 '+wg.def.name+' လိုက်လာပြီ! ပြေး!');",
    "wandering chase scream gated")

# HIDE sneak movement: moving allows hidden, speed half, no run while hidden
rep("  const moving=il>0.08 && !S.hidden;",
    "  const moving=il>0.08;",
    "hide move allow")
rep("  const running=moving && S.run && S.stamina>0;",
    "  const running=moving && S.run && S.stamina>0 && !S.hidden;",
    "hide no run")
rep("  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il));",
    "  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il))*(S.hidden?0.5:1);",
    "hide speed half")

# Hand orientation: rotate inner hand so fingers go forward, palm up for torch grip, group tilt small, torch visible to side
rep("const handL=new THREE.Group(); handL.position.set(-0.18,-0.28,-0.42); handL.rotation.set(0.25,0.20,-0.10); handsGroup.add(handL);\nconst handR=new THREE.Group(); handR.position.set(0.18,-0.24,-0.38); handR.rotation.set(0.25,-0.20,0.10); handsGroup.add(handR);\nconst flashMeshGroup=new THREE.Group(); flashMeshGroup.position.set(0,-0.02,-0.06); handR.add(flashMeshGroup);",
    "const handL=new THREE.Group(); handL.position.set(-0.20,-0.26,-0.40); handL.rotation.set(0,0.15,0); handsGroup.add(handL);\nconst handR=new THREE.Group(); handR.position.set(0.20,-0.26,-0.40); handR.rotation.set(0,-0.15,0); handsGroup.add(handR);\nconst flashMeshGroup=new THREE.Group(); flashMeshGroup.position.set(0.07,-0.03,-0.08); flashMeshGroup.rotation.set(0,0.4,0); handR.add(flashMeshGroup);",
    "hand group + torch side")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1.15,1.15,1.15); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});",
    "handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(1.0,1.0,1.0); inner.rotation.x=-Math.PI/2; inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});",
    "handR rotate")
rep("handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1.15,1.15,1.15); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{});",
    "handLoader.load('hand-real.glb', g=>{ const inner=g.scene; inner.scale.set(-1.0,1.0,1.0); inner.rotation.x=-Math.PI/2; inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{});",
    "handL rotate")

# Timer reset also resets wandering scream
rep("S.time=0; lastGirlTime=-999; nextTwitch=25;",
    "S.time=0; lastGirlTime=-999; lastWanderScream=-999; nextTwitch=25;",
    "timer reset wander scream")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V35 patch applied')
