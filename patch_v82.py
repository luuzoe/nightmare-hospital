import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V81[^<]{0,80}", t)
assert m, "V81 label not found"
t = t.replace(m.group(0), "V82 PLACEHOLDER", 1)

# GPU: default pixelRatio 1.25 -> 1.0 (about 36 percent fewer pixels)
rep("renderer.setPixelRatio(Math.min(devicePixelRatio,1.25));",
    "renderer.setPixelRatio(Math.min(devicePixelRatio,1.0));")
# Quality button: high now means 1.25 (not 1.5, which undid the V79 fix)
rep("renderer.setPixelRatio(S.lowQuality?1:Math.min(devicePixelRatio,1.5))",
    "renderer.setPixelRatio(S.lowQuality?1:Math.min(devicePixelRatio,1.25))")
# Default quality state now matches the 1.0 default
rep("lowQuality:false", "lowQuality:true")
rep('<button class="btn ghost" id="qualityBtn">🖥️ အရည်အသွေး: မြင့်</button>',
    '<button class="btn ghost" id="qualityBtn">🖥️ အရည်အသွေး: နိမ့်</button>')

# CPU: compass recompute at most every 0.5s instead of every frame.
# The compass block is self-contained between the beacon line and monster AI.
old_compass = """  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.visible=false;
  let cTx=tx, cTz=tz;
  const step=compassWaypoint(playerPos.x,playerPos.z,tx,tz);
  if(step){ cTx=step[0]; cTz=step[1]; }
  const ang=Math.atan2(cTx-playerPos.x,cTz-playerPos.z);
  const dirs=['↑','↗','→','↘','↓','↙','←','↖'];
  const idx=Math.round(((ang-S.yaw)%(Math.PI*2))/(Math.PI/4));
  const compDist=S.floor<=10?'':(' '+Math.round(Math.hypot(tx-playerPos.x,tz-playerPos.z))+'m'); $('compass').textContent='🧭 '+dirs[((idx%8)+8)%8]+compDist; // V53 harder: lower floors show direction only, no exact metres"""
new_compass = """  if(!S._compassT || S.time-S._compassT>=0.5){ S._compassT=S.time;
  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.visible=false;
  let cTx=tx, cTz=tz;
  const step=compassWaypoint(playerPos.x,playerPos.z,tx,tz);
  if(step){ cTx=step[0]; cTz=step[1]; }
  const ang=Math.atan2(cTx-playerPos.x,cTz-playerPos.z);
  const dirs=['↑','↗','→','↘','↓','↙','←','↖'];
  const idx=Math.round(((ang-S.yaw)%(Math.PI*2))/(Math.PI/4));
  const compDist=S.floor<=10?'':(' '+Math.round(Math.hypot(tx-playerPos.x,tz-playerPos.z))+'m'); $('compass').textContent='🧭 '+dirs[((idx%8)+8)%8]+compDist; // V53 harder: lower floors show direction only, no exact metres
  }"""
rep(old_compass, new_compass)

p.write_text(t, encoding='utf-8')
print('V82 patch applied')
