import sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:180]
    t=t.replace(old,new,1)

# normalizeGroup with offset + rotation
rep("""function normalizeGroup(grp,scale){
  grp.scale.setScalar(scale); grp.position.set(0,0,0); return grp;
}""",
"""function normalizeGroup(grp,scale,yOffset,rotX){
  grp.scale.setScalar(scale); grp.position.set(0,yOffset||0,0); if(rotX) grp.rotation.x=rotX; return grp;
}""")
# loadOne with real-model options
rep("""function loadOne(src,baseScale,targetH,dark){
  return new Promise(res=>{
    loader.load(src, gltf=>{
      const inner=gltf.scene; normalizeGroup(inner,baseScale*charScaleFactor);""",
"""function loadOne(src,baseScale,targetH,dark,opts){
  opts=opts||{};
  return new Promise(res=>{
    loader.load(src, gltf=>{
      const inner=gltf.scene; normalizeGroup(inner,baseScale*charScaleFactor,opts.yOffset||0,opts.rotX||0);
      if(opts.real){ inner.userData.baseScale=baseScale; }""")
rep("""      const outer=new THREE.Group(); outer.add(inner); scene.add(outer);
      if(dark){""",
"""      const outer=new THREE.Group(); outer.add(inner); scene.add(outer);
      if(opts.real){ /* real ghost texture kept as-is, no pale recolor */ }
      else if(dark){""")
# setCharSize: preserve real monster base scale
rep("""  if(playerInner)playerInner.scale.setScalar(PLAYER_BASE*charScaleFactor);
  if(monsterInner)monsterInner.scale.setScalar(MONSTER_BASE*charScaleFactor);""",
"""  if(playerInner)playerInner.scale.setScalar(PLAYER_BASE*charScaleFactor);
  if(monsterInner)monsterInner.scale.setScalar((monsterInner.userData.baseScale||MONSTER_BASE)*charScaleFactor);""")
# loadCharacter: main monster = blood ghost, fallback to cesium dark
rep("""  let m=await loadOne('cesium-man.glb',MONSTER_BASE,2.97,true);
  if(!m)m=await loadOne(CDN,MONSTER_BASE,2.97,true);""",
"""  let m=await loadOne('ghost-blood.glb',2.8,2.8,false,{real:true,yOffset:1.4,rotX:-Math.PI/2});
  if(!m)m=await loadOne('cesium-man.glb',MONSTER_BASE,2.97,true);
  if(!m)m=await loadOne(CDN,MONSTER_BASE,2.97,true);""")
# wandering defs: 3 new real ghosts first, then 6 old
rep("""  const defs=[
    {name:'Ghost Girl', scale:0.80, color:0xe8e8e8, opacity:0.85, eye:0x000000, pos:[-18,-12], wps:[[-18,-12],[-24,-6],[0,0],[-16,0]], speed:2.5, radius:10, floatY:0.3, chaseTime:4.5, sound:'scream'},""",
"""  const defs=[
    {name:'Ghost Woman', src:'ghost-woman.glb', real:true, scale:1.0, yOffset:0.95, pos:[20,12], wps:[[20,12],[16,12],[0,0],[20,0]], speed:2.6, radius:11, floatY:0.1, chaseTime:5, sound:'moan'},
    {name:'Darkness Ghost', src:'ghost-dark.glb', real:true, scale:0.7, yOffset:0, pos:[-20,20], wps:[[-20,20],[-16,12],[0,0],[-20,0]], speed:2.4, radius:12, floatY:0.3, chaseTime:6, sound:'growl'},
    {name:'Ghost Girl Animated', src:'ghost-girl.glb', real:true, scale:1.0, yOffset:0, pos:[28,12], wps:[[28,12],[20,12],[0,0],[24,0]], speed:3.0, radius:10, floatY:0.2, chaseTime:4.5, sound:'scream'},
    {name:'Ghost Girl', scale:0.80, color:0xe8e8e8, opacity:0.85, eye:0x000000, pos:[-18,-12], wps:[[-18,-12],[-24,-6],[0,0],[-16,0]], speed:2.5, radius:10, floatY:0.3, chaseTime:4.5, sound:'scream'},""")
# wandering build: real branch
rep("""    const build=(gltf)=>{
      const inner=gltf.scene; normalizeGroup(inner,def.scale);
      const outer=new THREE.Group(); outer.add(inner);
      inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.color.set(def.color); o.material.transparent=true; o.material.opacity=def.opacity; o.material.roughness=1; } });""",
"""    const build=(gltf,useReal)=>{
      const inner=gltf.scene; normalizeGroup(inner,def.scale,def.yOffset||0,def.rotX||0);
      const outer=new THREE.Group(); outer.add(inner);
      if(def.real && useReal){ /* keep original ghost texture */ }
      else inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.color.set(def.color); o.material.transparent=true; o.material.opacity=def.opacity; o.material.roughness=1; } });
      if(def.real && useReal){
        let mixer=null; if(gltf.animations.length){ mixer=new THREE.AnimationMixer(inner); mixer.clipAction(gltf.animations[0]).play(); }
        outer.position.set(def.pos[0],0,def.pos[1]); scene.add(outer);
        return {outer,mixer,def,wpIdx:0,scareTimer:0,chaseTimer:0,cooldown:0,state:'patrol'};
      }""")
# wandering loader: try real src first, fallback cesium
rep("""    let g=await new Promise(res=>{ loader.load('cesium-man.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });
    if(!g) g=await new Promise(res=>{ loader.load('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/CesiumMan/glTF-Binary/CesiumMan.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });""",
"""    let g=null;
    if(def.src){ g=await new Promise(res=>{ loader.load(def.src, gltf=>res(build(gltf,true)), undefined, ()=>res(null)); }); }
    if(!g) g=await new Promise(res=>{ loader.load('cesium-man.glb', gltf=>res(build(gltf,false)), undefined, ()=>res(null)); });
    if(!g) g=await new Promise(res=>{ loader.load('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/CesiumMan/glTF-Binary/CesiumMan.glb', gltf=>res(build(gltf)), undefined, ()=>res(null)); });""")

rep("V15 • Nightmare - အထပ်တိုင်း ကြောက်စရာ ပြည့် + သရဲ ၅+ ကောင်",
"V16 • သရဲ အစစ် ၄ မျိုး - Blood / Woman / Darkness / Girl Animated")

open(p,'w',encoding='utf-8').write(t)
print("V16 PATCH OK")
