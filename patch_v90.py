import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V89[^<]{0,80}", t)
assert m, "V89 label not found"
t = t.replace(m.group(0), "V90 PLACEHOLDER", 1)

# Load screen: show that slow internet can take minutes, and give the stage span an id
rep('<div id="load">ဆေးရုံဟောင်း ဖွင့်နေသည်…<br><span style="font-size:13px;color:#aaa">Character (website က ရတဲ့ တကယ့် 3D လူ) ကို ဆွဲနေသည်</span></div>',
    '<div id="load">ဆေးရုံဟောင်း ဖွင့်နေသည်…<br><span id="loadStage" style="font-size:13px;color:#aaa">Character (website က ရတဲ့ တကယ့် 3D လူ) ကို ဆွဲနေသည်</span><br><span style="font-size:12px;color:#888">internet နှေးရင် 2-4 မိနစ် ကြာနိုင်တယ် — ခဏစောင့်ပေးပါ</span></div>')

# Stage updates also reach the load screen while it is still visible
rep("function setCoreStatus(txt){ try{ const el=document.getElementById('coreStatus'); if(el) el.textContent=txt; }catch(e){} }",
    "function setCoreStatus(txt){ try{ const el=document.getElementById('coreStatus'); if(el) el.textContent=txt; const ls=document.getElementById('loadStage'); if(ls) ls.textContent=txt; }catch(e){} }")

# 90s slow-internet fallback must also hide the black load screen
rep("setTimeout(()=>{ if(window.__nhCoreReady!==true){ window.__nhCoreReady=true; setCoreStatus('⚠️ internet နှေးနေတယ် — စဆော့လို့ရပြီ, တချို့ သရဲ နောက်မှ ပေါ်လာနိုင်တယ်'); } },90000);",
    "setTimeout(()=>{ if(window.__nhCoreReady!==true){ window.__nhCoreReady=true; try{ document.getElementById('load').style.display='none'; }catch(e){} setCoreStatus('⚠️ internet နှေးနေတယ် — စဆော့လို့ရပြီ, တချို့ သရဲ နောက်မှ ပေါ်လာနိုင်တယ်'); } },90000);")

# Hands + flashlight (24 MB) no longer compete with the first load: load them after the start screen appears
rep("const handLoader=new GLTFLoader();\nhandLoader.load('hand-woman.glb', g=>{ const inner=g.scene; inner.scale.set(0.008,0.008,0.008); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});\nhandLoader.load('hand-woman.glb', g=>{ const inner=g.scene; inner.scale.set(-0.008,0.008,0.008); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{});",
    "function loadHandsAndFlash(){ const handLoader=new GLTFLoader();\nhandLoader.load('hand-woman.glb', g=>{ const inner=g.scene; inner.scale.set(0.008,0.008,0.008); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handR.add(inner); }, undefined, ()=>{});\nhandLoader.load('hand-woman.glb', g=>{ const inner=g.scene; inner.scale.set(-0.008,0.008,0.008); inner.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.side=THREE.DoubleSide; o.material.roughness=0.6; o.material.color.setRGB(0.68,0.48,0.34); } }); handL.add(inner); }, undefined, ()=>{}); const flashLoader=new GLTFLoader(); flashLoader.load('flashlight-real.glb', g=>{ const inner=g.scene; inner.scale.set(0.000125,0.000125,0.000125); flashMeshGroup.add(inner); }, undefined, ()=>{}); }")
rep("const flashLoader=new GLTFLoader(); flashLoader.load('flashlight-real.glb', g=>{ const inner=g.scene; inner.scale.set(0.000125,0.000125,0.000125); flashMeshGroup.add(inner); }, undefined, ()=>{});\n",
    "")

# Start hands/flashlight loading right after the start screen appears
rep("loadCharacter().then(async ok=>{\n  $('load').style.display='none';",
    "loadCharacter().then(async ok=>{\n  $('load').style.display='none';\n  try{ loadHandsAndFlash(); }catch(e){}")

p.write_text(t, encoding='utf-8')
print('V90 patch applied')
