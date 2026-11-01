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

rep("V39 • HIDE အရင်လို ရပ် + Compass လမ်းကြောင်း + ယူ ခလုတ် ပြင် — အကုန်",
    "V40 • HIDE ပုန်း + နှေးနှေး သွား ပြန် + Compass ပေါက်ကို တည့်တည့် ပြ — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်)</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း + နှေးနှေး သွား</p>",
    "start hint")
# HIDE sneak restore: hidden can walk slowly, no RUN while hidden
rep("  const moving=il>0.08 && !S.hidden;",
    "  const moving=il>0.08;",
    "hide sneak move")
rep("  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il));",
    "  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il))*(S.hidden?0.5:1);",
    "hide sneak speed")
rep("  $('hideTag').style.display=S.hidden?'block':'none';",
    "  $('hideTag').style.display=S.hidden?'block':'none'; if(S.hidden && $('hideTag')) $('hideTag').textContent='🫥 ပုန်းနေသည် • နှေးနှေး သွား';",
    "hideTag sneak text")
# Compass: use smoothed BFS path waypoint, not first grid step
rep("""  let cTx=tx, cTz=tz;
  const step=compassStep(playerPos.x,playerPos.z,tx,tz);
  if(step){ cTx=step[0]; cTz=step[1]; }""",
    """  let cTx=tx, cTz=tz;
  const step=compassWaypoint(playerPos.x,playerPos.z,tx,tz);
  if(step){ cTx=step[0]; cTz=step[1]; }""",
    "compass waypoint use")
# Replace compassStep helper with compassPath + compassWaypoint + fine line check
rep("function compassStep(px,pz,tx,tz){",
    "function lineBlockedFine(x1,z1,x2,z2){\n  const d=Math.hypot(x2-x1,z2-z1); const n=Math.max(1,Math.ceil(d/0.5));\n  for(let i=1;i<n;i++){\n    const x=x1+(x2-x1)*i/n, z=z1+(z2-z1)*i/n;\n    for(const w of walls){ if(Math.abs(x-w.x)<w.w/2+0.2 && Math.abs(z-w.z)<w.d/2+0.2) return true; }\n  }\n  return false;\n}\nfunction compassPath(px,pz,tx,tz){",
    "compassPath rename")
# Inside compassPath, change return logic: instead of returning first step, return full path
# Original compassStep returns [x0+node*step, ...] for first step, and [tx,tz] if start==target.
# We rewrite the path reconstruction block to collect full path.
rep("""  if(sx===gx && sz===gz) return [tx,tz];
  const key=(a,b)=>a+','+b;
  const prev=new Map(); const seen=new Set([key(sx,sz)]); const q=[[sx,sz]];
  while(q.length){
    const cur=q.shift();
    if(cur[0]===gx && cur[1]===gz){
      let node=cur;
      while(prev.has(key(node[0],node[1]))){
        const pr=prev.get(key(node[0],node[1]));
        if(pr[0]===sx && pr[1]===sz) return [x0+node[0]*step, z0+node[1]*step];
        node=pr;
      }
      return [tx,tz];
    }""",
    """  if(sx===gx && sz===gz) return [[tx,tz]];
  const key=(a,b)=>a+','+b;
  const prev=new Map(); const seen=new Set([key(sx,sz)]); const q=[[sx,sz]];
  while(q.length){
    const cur=q.shift();
    if(cur[0]===gx && cur[1]===gz){
      const path=[]; let node=cur;
      while(prev.has(key(node[0],node[1]))){ path.unshift([x0+node[0]*step, z0+node[1]*step]); node=prev.get(key(node[0],node[1])); }
      path.push([tx,tz]); return path;
    }""",
    "compassPath full path")
# After compassPath function, add compassWaypoint that smooths to farthest line-clear point
rep("function lineBlocked(x1,z1,x2,z2){",
    "function compassWaypoint(px,pz,tx,tz){\n  if(!lineBlockedFine(px,pz,tx,tz)) return [tx,tz];\n  const path=compassPath(px,pz,tx,tz);\n  if(!path || !path.length) return null;\n  let best=path[0];\n  for(const pt of path){ if(!lineBlockedFine(px,pz,pt[0],pt[1])) best=pt; else break; }\n  return best;\n}\nfunction lineBlocked(x1,z1,x2,z2){",
    "compassWaypoint helper")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V40 patch applied')
