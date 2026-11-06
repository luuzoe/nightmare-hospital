import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V90[^<]{0,80}", t)
assert m, "V90 label not found"
t = t.replace(m.group(0), "V91 PLACEHOLDER", 1)

# 1. Black load screen gone: hidden from the start, menu shows at once
rep('<div id="load">ဆေးရုံဟောင်း ဖွင့်နေသည်…',
    '<div id="load" style="display:none">ဆေးရုံဟောင်း ဖွင့်နေသည်…')

# 2. Download bar at the bottom of the start screen (left to right, MB left)
rep('  <p style="font-size:11px;color:#666;margin-top:8px">V91 PLACEHOLDER</p>',
    '  <div id="loadBarWrap" style="position:absolute;bottom:16px;left:50%;transform:translateX(-50%);width:min(520px,86vw)"><div style="height:14px;background:#1a1a1a;border:2px solid #ff2222;border-radius:8px;overflow:hidden"><div id="loadBarFill" style="height:100%;width:0%;background:linear-gradient(90deg,#7a0000,#ff2222);transition:width .2s"></div></div><p id="loadBarText" style="font-size:12px;color:#ffd166;margin:4px 0 0;text-align:center">ဒေါင်းလုတ် 0 / 72.1 MB</p></div>\n  <p style="font-size:11px;color:#666;margin-top:8px">V91 PLACEHOLDER</p>')

# 3. Compact landscape menu
rep("  .iconbtn{width:42px;height:42px;font-size:18px}\n}\n</style>",
    "  .iconbtn{width:42px;height:42px;font-size:18px}\n}\n@media (orientation:landscape){ .screen{padding:12px 20px} .screen h1{font-size:30px;margin:2px 0} .screen p{font-size:14px;margin:4px 0;line-height:1.5} .btn{padding:10px 20px} #loadBarWrap{bottom:10px} }\n</style>")

# 4. Real byte progress tracker: wraps the shared GLTFLoader, seeded with exact core file sizes
rep("const loader=new GLTFLoader();",
    "const loader=new GLTFLoader();\nlet loadProgBytes={}, loadProgTotal={'cesium-man.glb':490956,'ghost-blood.glb':7322628,'dead1.glb':1611768,'dead2.glb':4085192,'dead3.glb':2630916,'dead4.glb':2731052,'dead-body-real.glb':1619896,'bodybags.glb':5625464,'ghost-dark.glb':8644964,'ghost-woman.glb':2276024,'ghost-saori.glb':1694048,'ghost-inktober.glb':16490652,'ghost-lowpoly.glb':2018120,'ghost-pig.glb':6615648,'ghost-lethal.glb':1535248,'cloth-ghost.glb':2205000,'ghost-woman-apose.glb':2276024,'scary-halloween-ghost.glb':4106484,'shazia-ghost.glb':2655560};\nfunction updLoadBar(){ try{ let l=0,tt=0; for(const k in loadProgTotal){ l+=loadProgBytes[k]||0; tt+=loadProgTotal[k]; } const pct=tt>0?Math.min(100,Math.round(l/tt*100)):0; const bar=$('loadBarFill'); if(bar) bar.style.width=pct+'%'; const tx=$('loadBarText'); if(tx) tx.textContent='ဒေါင်းလုတ် '+(l/1048576).toFixed(1)+' / '+(tt/1048576).toFixed(1)+' MB — '+Math.max(0,(tt-l)/1048576).toFixed(1)+' MB ကျန်သေးတယ်'; }catch(e){} }\nconst _origLoaderLoad=loader.load.bind(loader);\nloader.load=function(url,onLoad,onProgress,onError){ return _origLoaderLoad(url, gltf=>{ if(loadProgTotal[url]) loadProgBytes[url]=loadProgTotal[url]; updLoadBar(); if(onLoad) onLoad(gltf); }, ev=>{ if(ev && ev.total>0 && loadProgTotal[url]){ loadProgTotal[url]=ev.total; loadProgBytes[url]=ev.loaded; updLoadBar(); } if(onProgress) onProgress(ev); }, onError); };\nupdLoadBar();")

# 5. Parallel downloads: character (2 files at once)
rep("  let p=await loadOne('cesium-man.glb',PLAYER_BASE,1.8,false);\n  if(!p)p=await loadOne(CDN,PLAYER_BASE,1.8,false);\n  let m=await loadOne('ghost-blood.glb',2.8,2.8,false,{real:true,yOffset:1.4,rotX:-Math.PI/2});",
    "  let [p,m]=await Promise.all([loadOne('cesium-man.glb',PLAYER_BASE,1.8,false), loadOne('ghost-blood.glb',2.8,2.8,false,{real:true,yOffset:1.4,rotX:-Math.PI/2})]);\n  if(!p)p=await loadOne(CDN,PLAYER_BASE,1.8,false);")

# 6. Parallel downloads: corpses (13 files at once, placed in order)
rep("  for(let ci=0; ci<corpseDefs.length; ci++){\n    const c=corpseDefs[ci]; const cs=corpseSrcs[ci]||corpseSrcs[5];\n    let outer=await loadCorpse(cs.src,cs.scale,cs);",
    "  const corpseOuters=await Promise.all(corpseSrcs.map(cs=>loadCorpse(cs.src,cs.scale,cs)));\n  for(let ci=0; ci<corpseDefs.length; ci++){\n    const c=corpseDefs[ci]; const cs=corpseSrcs[ci]||corpseSrcs[5];\n    let outer=corpseOuters[ci];")

# 7. Parallel downloads: wandering ghosts (11 files at once, built in order)
rep("  for(const def of defs){\n    const build=(gltf,useReal)=>{",
    "  const ghostLoads=defs.map(def=>new Promise(res=>{ loader.load(def.src, gltf=>res({def,gltf}), undefined, ()=>res({def,gltf:null})); }));\n  for(const {def,gltf} of await Promise.all(ghostLoads)){ if(!gltf) continue;\n    const build=(gltf,useReal)=>{")
rep("    let g=null;\n    if(def.src){ g=await new Promise(res=>{ loader.load(def.src, gltf=>res(build(gltf,true)), undefined, ()=>res(null)); }); }\n    if(g) wanderingGhosts.push(g); // V22: no CesiumMan fallback - sent ghosts only",
    "    const g=build(gltf,true);\n    if(g) wanderingGhosts.push(g);")

# 8. When ready, force the bar to 100% + ready text
rep("  window.__nhCoreReady=true;\n  setCoreStatus('✅ အားလုံး အဆင်သင့် — စဆော့လို့ရပြီ');",
    "  window.__nhCoreReady=true;\n  try{ for(const k in loadProgTotal) loadProgBytes[k]=loadProgTotal[k]; updLoadBar(); const tx=$('loadBarText'); if(tx) tx.textContent='✅ အဆင်သင့် — စဆော့လို့ရပြီ'; }catch(e){}\n  setCoreStatus('✅ အားလုံး အဆင်သင့် — စဆော့လို့ရပြီ');")

p.write_text(t, encoding='utf-8')
print('V91 patch applied')
