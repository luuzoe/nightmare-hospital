import sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# --- REAL BLOOD: replace canvas blood texture with real PNG splatter textures ---
rep("""let bloodTex=null;
function getBloodTex(){
  if(bloodTex) return bloodTex;
  const cv=document.createElement('canvas'); cv.width=cv.height=256; const g=cv.getContext('2d');
  g.clearRect(0,0,256,256);
  for(let i=0;i<50;i++){ const x=60+Math.random()*136, y=60+Math.random()*136, r=5+Math.random()*28; g.fillStyle=Math.random()<0.5?'rgba(90,5,5,0.9)':'rgba(150,15,15,0.85)'; g.beginPath(); g.arc(x,y,r,0,7); g.fill(); }
  for(let i=0;i<20;i++){ g.fillStyle='rgba(120,10,10,0.8)'; g.beginPath(); g.arc(Math.random()*256,Math.random()*256,2+Math.random()*5,0,7); g.fill(); }
  bloodTex=new THREE.CanvasTexture(cv); bloodTex.colorSpace=THREE.SRGBColorSpace; return bloodTex;
}
function makeBloodPool(x,z,r){
  const shape=new THREE.Shape(); const N=14;
  for(let i=0;i<=N;i++){ const a=i/N*Math.PI*2; const rr=r*(0.7+Math.random()*0.6); const px=Math.cos(a)*rr, py=Math.sin(a)*rr; if(i===0) shape.moveTo(px,py); else shape.lineTo(px,py); }
  const m=new THREE.Mesh(new THREE.ShapeGeometry(shape), new THREE.MeshStandardMaterial({map:getBloodTex(),transparent:true,roughness:0.25}));
  m.rotation.x=-Math.PI/2; m.position.set(x,0.02,z); scene.add(m); return m;
}""",
"""let bloodTex=null;
const bloodTexLoader=new THREE.TextureLoader();
const bloodTextures=['blood-splatter.png','blood2.png','blood3.png','blood4.png','blood5.png'].map(f=>{ const tx=bloodTexLoader.load(f); tx.colorSpace=THREE.SRGBColorSpace; return tx; });
function getBloodTex(){ return bloodTextures[Math.floor(Math.random()*bloodTextures.length)]; }
function makeBloodPool(x,z,r){
  const tex=getBloodTex();
  const m=new THREE.Mesh(new THREE.PlaneGeometry(r*2,r*2), new THREE.MeshStandardMaterial({map:tex,transparent:true,roughness:0.25,depthWrite:false}));
  m.rotation.x=-Math.PI/2; m.rotation.z=Math.random()*Math.PI*2; m.position.set(x,0.02,z); scene.add(m); return m;
}
function makeWallBlood(x,y,z,ry,w,h){
  const tex=getBloodTex();
  const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h), new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:0.95,depthWrite:false}));
  m.position.set(x,y,z); m.rotation.y=ry; scene.add(m); return m;
}
// V17 real blood on walls everywhere
makeWallBlood(-31.6,1.5,-8,Math.PI/2,2.5,1.8); makeWallBlood(31.6,1.5,-8,-Math.PI/2,2.5,1.8); makeWallBlood(-31.6,1.5,12,Math.PI/2,3,2); makeWallBlood(31.6,1.5,12,-Math.PI/2,3,2); makeWallBlood(0,1.5,-23.6,0,3,2); makeWallBlood(0,1.5,23.6,Math.PI,3,2); makeWallBlood(-20,1.5,-2.69,0,2,1.5); makeWallBlood(20,1.5,2.69,Math.PI,2,1.5); makeWallBlood(55,1.5,0,-Math.PI/2,2.5,1.8); makeWallBlood(45,1.5,-14.69,0,2,1.5);""")

# --- DEAD BODIES: loadCorpse with real model support ---
rep("""function loadCorpse(src,scale){
  return new Promise(res=>{
    loader.load(src, gltf=>{
      const inner=gltf.scene; normalizeGroup(inner,scale);
      const outer=new THREE.Group(); outer.add(inner);
      inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.color.set(0x8a7a68); o.material.roughness=0.9; } }); // V8 pale corpse skin (was black shadow 0x2a1515)
      res(outer);
    }, undefined, ()=>res(null));
  });
}""",
"""function loadCorpse(src,scale,opts){
  opts=opts||{};
  return new Promise(res=>{
    loader.load(src, gltf=>{
      const inner=gltf.scene; normalizeGroup(inner,scale,opts.oy||0,opts.rotX||0);
      if(opts.ox||opts.oz) inner.position.set(opts.ox||0,opts.oy||0,opts.oz||0);
      const outer=new THREE.Group(); outer.add(inner);
      if(!opts.real) inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.color.set(0x8a7a68); o.material.roughness=0.9; } });
      res(outer);
    }, undefined, ()=>res(null));
  });
}""")
# loadCorpses loop: assign real bodies per corpse, last stays CesiumMan
rep("""async function loadCorpses(){
  for(const c of corpseDefs){
    let outer=await loadCorpse('cesium-man.glb',PLAYER_BASE);
    if(!outer) outer=await loadCorpse('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/CesiumMan/glTF-Binary/CesiumMan.glb',PLAYER_BASE);
    if(!outer) continue;
    const wrap=new THREE.Group(); wrap.position.set(c.x,0,c.z); wrap.rotation.y=c.yaw;
    outer.rotation.x=-Math.PI/2; if(corpseWrappers.length===2) outer.rotation.z=0.5; // surgery corpse lies twisted on its side
    outer.position.set(0,0.25,0.9); wrap.add(outer);""",
"""async function loadCorpses(){
  const corpseSrcs=[
    {src:'dead1.glb',scale:1.0,ox:0,oy:0.4,oz:0,real:true},
    {src:'dead2.glb',scale:0.01,ox:0.45,oy:0,oz:1.17,real:true},
    {src:'dead3.glb',scale:0.3048,ox:0.68,oy:0.32,oz:0,real:true},
    {src:'dead4.glb',scale:1.0,ox:-0.165,oy:0,oz:0,rotX:-Math.PI/2,real:true},
    {src:'dead2.glb',scale:0.01,ox:0.45,oy:0,oz:1.17,real:true},
    {src:'cesium-man.glb',scale:PLAYER_BASE,real:false},
  ];
  for(let ci=0; ci<corpseDefs.length; ci++){
    const c=corpseDefs[ci]; const cs=corpseSrcs[ci]||corpseSrcs[5];
    let outer=await loadCorpse(cs.src,cs.scale,cs);
    if(!outer && cs.real) outer=await loadCorpse('cesium-man.glb',PLAYER_BASE,{});
    if(!outer) outer=await loadCorpse('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/CesiumMan/glTF-Binary/CesiumMan.glb',PLAYER_BASE,{});
    if(!outer) continue;
    const wrap=new THREE.Group(); wrap.position.set(c.x,0,c.z); wrap.rotation.y=c.yaw;
    if(!cs.real){ outer.rotation.x=-Math.PI/2; if(corpseWrappers.length===2) outer.rotation.z=0.5; outer.position.set(0,0.25,0.9); }
    wrap.add(outer);""")
# body bags prop in Morgue after corpses loop (inside loadCorpses, before closing brace - find the scene.add(wrap) line)
rep("""    scene.add(wrap); corpseWrappers.push(wrap);
  }
}""",
"""    scene.add(wrap); corpseWrappers.push(wrap);
  }
  // V17 body bags pile in Morgue (visual only, not a mission corpse)
  loader.load('bodybags.glb', gltf=>{
    const inner=gltf.scene; normalizeGroup(inner,0.005,0,0); inner.position.set(1.33,-0.41,-0.20);
    const outer=new THREE.Group(); outer.position.set(28,0,20); outer.rotation.y=0.5; outer.add(inner); scene.add(outer);
  }, undefined, ()=>{});
}""")

rep("V16 • သရဲ အစစ် ၄ မျိုး - Blood / Woman / Darkness / Girl Animated",
"V17 • Dead Body အစစ် + သွေးအစစ်")

open(p,'w',encoding='utf-8').write(t)
print("V17 PATCH OK")
