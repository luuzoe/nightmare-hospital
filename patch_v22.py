p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# 1. Wandering defs: keep ONLY Zaw-sent real ghosts, remove all CesiumMan toy ghosts (Ghost Girl cone sheet, Child, Nurse, Shadow, Crawl, Old)
rep("""    {name:'Ghost Girl', scale:0.80, color:0xe8e8e8, opacity:0.85, eye:0x000000, pos:[-22,-12], wps:[[-22,-12],[-24,-6],[0,0],[-16,0]], speed:2.5, radius:10, floatY:0.3, chaseTime:4.5, sound:'scream'},
    {name:'Child Ghost', scale:0.45, color:0x333333, opacity:0.9, eye:0xff0000, pos:[-26,20], wps:[[-26,20],[-16,12],[0,0],[-10,12]], speed:3.5, radius:8, floatY:0.1, chaseTime:3.5, sound:'giggle'},
    {name:'Nurse Ghost', scale:0.75, color:0xdddddd, opacity:0.9, eye:0x000000, pos:[20,-20], wps:[[20,-20],[16,-6],[0,0],[20,0]], speed:2.8, radius:11, floatY:0.25, chaseTime:5, sound:'whisper', cap:true},
    {name:'Shadow Ghost', scale:1.10, color:0x111111, opacity:0.95, eye:0xff0000, pos:[24,12], wps:[[24,12],[16,12],[0,0],[20,12]], speed:2.0, radius:12, floatY:0.4, chaseTime:6, sound:'growl'},
    {name:'Crawl Ghost', scale:0.50, color:0x8a7a68, opacity:0.9, eye:0xffff00, pos:[0,12], wps:[[0,12],[10,12],[-10,12],[0,0]], speed:4.0, radius:9, floatY:0.05, chaseTime:3, sound:'growl', crawl:true},
    {name:'Old Ghost', scale:0.85, color:0x999999, opacity:0.85, eye:0x000000, pos:[-20,12], wps:[[-20,12],[-16,12],[0,0],[-16,0]], speed:2.2, radius:11, floatY:0.1, chaseTime:5, sound:'moan', cane:true},
""",
"    // V22 user: toy ghosts removed - only Zaw-sent real ghosts remain (Woman, Darkness, Girl Animated + main blood monster)\n")
# 2. setActiveGhosts: activate ALL real ghosts (3), not 5-of-9
rep("""function setActiveGhosts(){
  if(!wanderingGhosts.length) return;
  const fd=15-S.floor; const n=wanderingGhosts.length;
  const active=[wanderingGhosts[fd%n].def.name, wanderingGhosts[(fd+1)%n].def.name, wanderingGhosts[(fd+2)%n].def.name, wanderingGhosts[(fd+3)%n].def.name, wanderingGhosts[(fd+4)%n].def.name]; S.activeGhostCount=active.length;""",
"""function setActiveGhosts(){
  if(!wanderingGhosts.length) return;
  const active=wanderingGhosts.map(wg=>wg.def.name); S.activeGhostCount=active.length;""")
# 3. No CesiumMan fallback for wandering ghosts (real only, skip if file fails)
rep("""    let g=null;
    if(def.src){ g=await new Promise(res=>{ loader.load(def.src, gltf=>res(build(gltf,true)), undefined, ()=>res(null)); }); }
    if(!g) g=await new Promise(res=>{ loader.load('cesium-man.glb', gltf=>res(build(gltf,false)), undefined, ()=>res(null)); });
    if(!g) g=await new Promise(res=>{ loader.load('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/CesiumMan/glTF-Binary/CesiumMan.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });
    if(g) wanderingGhosts.push(g);""",
"""    let g=null;
    if(def.src){ g=await new Promise(res=>{ loader.load(def.src, gltf=>res(build(gltf,true)), undefined, ()=>res(null)); }); }
    if(g) wanderingGhosts.push(g); // V22: no CesiumMan fallback - sent ghosts only""")
# 4. Toast without count (aligns with V21 no-count order)
rep("  if(typeof setActiveGhosts==='function') setActiveGhosts(); toast('👻 သရဲတွေ အဆင်သင့် — '+wanderingGhosts.length+' ကောင်');",
"  if(typeof setActiveGhosts==='function') setActiveGhosts(); toast('👻 သရဲတွေ အဆင်သင့်');")
# 5. Shadow scare ghost: replace CesiumMan toy with real Darkness ghost (original texture, no recolor/eyes)
rep("""async function loadGhost(){
  const build=(gltf)=>{
    const inner=gltf.scene; normalizeGroup(inner,MONSTER_BASE);
    const outer=new THREE.Group(); outer.add(inner);
    inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.color.set(0xdddddd); o.material.transparent=true; o.material.opacity=0.65; o.material.roughness=1; } });
    const eyeMat=new THREE.MeshBasicMaterial({color:0x000000});
    for(const sx of [-0.14,0.14]){ const e=new THREE.Mesh(new THREE.SphereGeometry(0.14,8,8),eyeMat); e.position.set(sx,2.73,0.18); outer.add(e); const pup=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8),new THREE.MeshBasicMaterial({color:0xff0000})); pup.position.set(sx,2.73,0.28); outer.add(pup); }
    const mouth2=new THREE.Mesh(new THREE.BoxGeometry(0.22,0.14,0.05),eyeMat); mouth2.position.set(0,2.44,0.22); outer.add(mouth2);
    let mixer=null; if(gltf.animations.length){ mixer=new THREE.AnimationMixer(inner); mixer.clipAction(gltf.animations[0]).play(); }
    outer.visible=false; scene.add(outer); return {outer,mixer};
  };
  let g=await new Promise(res=>{ loader.load('cesium-man.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });
  if(!g) g=await new Promise(res=>{ loader.load('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/CesiumMan/glTF-Binary/CesiumMan.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });
  if(g){ shadowGhost=g.outer; shadowGhostMixer=g.mixer; }
}""",
"""async function loadGhost(){
  // V22: shadow scare uses Zaw-sent Darkness ghost, original texture, no toy recolor
  const build=(gltf)=>{
    const inner=gltf.scene; normalizeGroup(inner,0.7,0,0);
    const outer=new THREE.Group(); outer.add(inner);
    let mixer=null; if(gltf.animations.length){ mixer=new THREE.AnimationMixer(inner); mixer.clipAction(gltf.animations[0]).play(); }
    outer.visible=false; scene.add(outer); return {outer,mixer};
  };
  let g=await new Promise(res=>{ loader.load('ghost-dark.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });
  if(g){ shadowGhost=g.outer; shadowGhostMixer=g.mixer; }
}""")
# Version label
rep("V21 • သရဲအရေအတွက် ဖျောက် — HUD မှာ မပြတော့ဘူး",
"V22 • သရဲအစစ် ဘဲ — တြိဂံအဖြူ သရဲအတု ဖျောက်, မင်းပို့တဲ့ သရဲဘဲ")
open(p,'w',encoding='utf-8').write(t)
print("V22 PATCH OK")
