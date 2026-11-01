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

# Version label
rep("V38 • ပရိဘောဂ မတိုက် + HIDE ရွေး + အလောင်းကောင် မြင် — အကုန်",
    "V39 • HIDE အရင်လို ရပ် + Compass လမ်းကြောင်း + ယူ ခလုတ် ပြင် — အကုန်",
    "version")
# Start hint back to simple HIDE
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း + နှေးနှေး သွား (Pause မှာ ရပ် လို့ ပြောင်းလို့ ရသည်)</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်)</p>",
    "start hint")
# HIDE revert: stationary, original behaviour
rep("  const moving=il>0.08 && (!S.hidden || S.hideSneak!==false);",
    "  const moving=il>0.08 && !S.hidden;",
    "hide stationary move")
rep("  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il))*(S.hidden && S.hideSneak!==false?0.5:1);",
    "  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il));",
    "hide speed revert")
rep("  $('hideTag').style.display=S.hidden?'block':'none'; if(S.hidden && $('hideTag')) $('hideTag').textContent=S.hideSneak!==false?'🫥 ပုန်းနေသည် (နှေးနှေး သွား)':'🫥 ပုန်းနေသည် (ရပ်)';",
    "  $('hideTag').style.display=S.hidden?'block':'none';",
    "hideTag revert")
rep("\n    <button class=\"btn ghost\" id=\"hideModeBtn\">🫥 HIDE: နှေးနှေး သွား</button>",
    "",
    "hide mode button remove")
rep("\nif($('hideModeBtn')){ $('hideModeBtn').addEventListener('click',()=>{ S.hideSneak=!S.hideSneak; $('hideModeBtn').textContent=S.hideSneak?'🫥 HIDE: နှေးနှေး သွား':'🫥 HIDE: ရပ်'; }); }",
    "",
    "hide mode wiring remove")
# actBtn: click -> pointerdown, with double-fire guard in doInteract
rep("$('actBtn').addEventListener('click',doInteract);",
    "$('actBtn').addEventListener('pointerdown',e=>{ e.preventDefault(); doInteract(); });",
    "actBtn pointerdown")
rep("function doInteract(){\n  if(!S.playing||S.paused||!S.interactTarget)return;\n  const t=S.interactTarget;",
    "function doInteract(){\n  if(!S.playing||S.paused||!S.interactTarget)return;\n  const t=S.interactTarget;\n  if(t.type==='key' && t.km.taken) return;\n  if(t.type==='item' && t.im.taken) return;",
    "doInteract guard")
# Compass BFS path: insert helper before compass ang calculation, and use step for arrow
rep("  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.visible=false;\n  const ang=Math.atan2(tx-playerPos.x,tz-playerPos.z);",
    "  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.visible=false;\n  let cTx=tx, cTz=tz;\n  if(typeof lineBlocked==='function' && lineBlocked(playerPos.x,playerPos.z,tx,tz)){\n    const step=compassStep(playerPos.x,playerPos.z,tx,tz);\n    if(step){ cTx=step[0]; cTz=step[1]; }\n  }\n  const ang=Math.atan2(cTx-playerPos.x,cTz-playerPos.z);",
    "compass step use")
# Helper function: place before lineBlocked definition
rep("function lineBlocked(x1,z1,x2,z2){",
    "function compassStep(px,pz,tx,tz){\n  const step=2, x0=-31, x1=69, z0=-23, z1=23;\n  const gw=Math.round((x1-x0)/step)+1, gh=Math.round((z1-z0)/step)+1;\n  const toCx=x=>Math.max(0,Math.min(gw-1,Math.round((x-x0)/step)));\n  const toCz=z=>Math.max(0,Math.min(gh-1,Math.round((z-z0)/step)));\n  const blocked=(cx,cz)=>{ const wx=x0+cx*step, wz=z0+cz*step; for(const w of walls){ if(Math.abs(wx-w.x)<w.w/2+0.6 && Math.abs(wz-w.z)<w.d/2+0.6) return true; } return false; };\n  const sx=toCx(px), sz=toCz(pz), gx=toCx(tx), gz=toCz(tz);\n  if(sx===gx && sz===gz) return [tx,tz];\n  const key=(a,b)=>a+','+b;\n  const prev=new Map(); const seen=new Set([key(sx,sz)]); const q=[[sx,sz]];\n  while(q.length){\n    const cur=q.shift();\n    if(cur[0]===gx && cur[1]===gz){\n      let node=cur;\n      while(prev.has(key(node[0],node[1]))){\n        const pr=prev.get(key(node[0],node[1]));\n        if(pr[0]===sx && pr[1]===sz) return [x0+node[0]*step, z0+node[1]*step];\n        node=pr;\n      }\n      return [tx,tz];\n    }\n    const dirs=[[1,0],[-1,0],[0,1],[0,-1]];\n    for(const d of dirs){\n      const nx=cur[0]+d[0], nz=cur[1]+d[1];\n      if(nx<0||nz<0||nx>=gw||nz>=gh) continue;\n      if(seen.has(key(nx,nz))) continue;\n      if(blocked(nx,nz)) continue;\n      seen.add(key(nx,nz)); prev.set(key(nx,nz),cur); q.push([nx,nz]);\n    }\n  }\n  return null;\n}\nfunction lineBlocked(x1,z1,x2,z2){",
    "compassStep helper")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V39 patch applied')
