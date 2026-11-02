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

rep("V50 • အကုန်: unseen haunting + dynamic tension + risky chase + story events + jumpscare variety — error မရှိ — အကုန်",
    "V51 • toast အပေါ်ဆုံး + မှိန် + minimap သေး — အကုန်",
    "version v51")
# Toast: topmost, faint, smaller, wrapping (no long wide red bar overlapping HUD/game view)
rep("#toast{position:absolute;left:50%;top:84px;transform:translateX(-50%);background:rgba(40,0,0,.85);border:1px solid #ff2222;color:#ffdddd;padding:10px 16px;border-radius:12px;font-size:16px;font-weight:700;white-space:nowrap;opacity:0;transition:opacity .25s;text-shadow:0 0 8px red}\n#toast.show{opacity:1}",
    "#toast{position:absolute;left:50%;top:10px;transform:translateX(-50%);background:rgba(0,0,0,.35);border:1px solid rgba(255,120,120,.35);color:rgba(255,220,220,.85);padding:6px 10px;border-radius:10px;font-size:13px;font-weight:600;white-space:normal;max-width:70vw;text-align:center;opacity:0;transition:opacity .25s;text-shadow:none;z-index:12}\n#toast.show{opacity:.75}",
    "toast top faint v51")
rep("  #toast{top:64px}",
    "  #toast{top:8px;font-size:12px}",
    "toast landscape v51")
# Minimap: 200x100 -> 120x60, scale 1.1 -> 0.6, dots 5 -> 3, direction line 14 -> 8
rep('<canvas id="minimap" width="200" height="100" style="position:fixed;top:64px;right:10px;z-index:20;pointer-events:none;background:rgba(0,0,0,0.6);border:1px solid #444;border-radius:6px"></canvas>',
    '<canvas id="minimap" width="120" height="60" style="position:fixed;top:60px;right:8px;z-index:20;pointer-events:none;background:rgba(0,0,0,0.6);border:1px solid #444;border-radius:6px"></canvas>',
    "minimap canvas v51")
rep("  const sc=1.1;",
    "  const sc=0.6; // V51: minimap smaller",
    "minimap scale v51")
rep("    g.arc(Math.max(2,Math.min(cv.width-2,bx)),Math.max(2,Math.min(cv.height-2,by)),5,0,Math.PI*2);",
    "    g.arc(Math.max(2,Math.min(cv.width-2,bx)),Math.max(2,Math.min(cv.height-2,by)),3,0,Math.PI*2);",
    "minimap beacon dot v51")
rep("  g.arc(Math.max(2,Math.min(cv.width-2,px)),Math.max(2,Math.min(cv.height-2,py)),5,0,Math.PI*2);",
    "  g.arc(Math.max(2,Math.min(cv.width-2,px)),Math.max(2,Math.min(cv.height-2,py)),3,0,Math.PI*2);",
    "minimap player dot v51")
rep("  g.lineTo(Math.max(2,Math.min(cv.width-2,px+Math.sin(S.yaw)*14)),Math.max(2,Math.min(cv.height-2,py+Math.cos(S.yaw)*14)));",
    "  g.lineTo(Math.max(2,Math.min(cv.width-2,px+Math.sin(S.yaw)*8)),Math.max(2,Math.min(cv.height-2,py+Math.cos(S.yaw)*8)));",
    "minimap direction v51")

# HUD left top texts: smaller (user: too big)
rep(".panel{background:linear-gradient(180deg,rgba(40,0,0,.85),rgba(0,0,0,.75));border:1px solid rgba(255,0,0,.6);border-radius:12px;padding:6px 10px;backdrop-filter:blur(4px);max-width:340px;box-shadow:0 0 16px rgba(255,0,0,.35)}",
    ".panel{background:linear-gradient(180deg,rgba(40,0,0,.85),rgba(0,0,0,.75));border:1px solid rgba(255,0,0,.6);border-radius:10px;padding:4px 7px;backdrop-filter:blur(4px);max-width:220px;box-shadow:0 0 16px rgba(255,0,0,.35)}",
    "panel smaller v51")
rep("#hearts{font-size:19px;letter-spacing:2px;text-shadow:0 0 10px red}",
    "#hearts{font-size:15px;letter-spacing:1px;text-shadow:0 0 10px red}",
    "hearts smaller v51")
rep("#floorInfo{font-size:13px;color:#ffd166;font-weight:800}",
    "#floorInfo{font-size:11px;color:#ffd166;font-weight:800}",
    "floorInfo smaller v51")
rep("#objective{font-size:13px;line-height:1.3;max-width:300px;color:#ffdddd;font-weight:700}",
    "#objective{font-size:11px;line-height:1.3;max-width:200px;color:#ffdddd;font-weight:700}",
    "objective smaller v51")
rep("#keys{font-size:13px;margin-top:2px}",
    "#keys{font-size:11px;margin-top:2px}",
    "keys smaller v51")
rep("#objective{font-size:13px;line-height:1.3;max-width:300px}",
    "#objective{font-size:11px;line-height:1.3;max-width:200px}",
    "objective2 smaller v51")
rep("#compass{font-size:12px;color:#ffd166;margin-top:2px}",
    "#compass{font-size:11px;color:#ffd166;margin-top:2px}",
    "compass smaller v51")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V51 applied')
