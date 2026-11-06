import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V86[^<]{0,80}", t)
assert m, "V86 label not found"
t = t.replace(m.group(0), "V87 PLACEHOLDER", 1)

# Scarier + neater title
rep(".screen h1{font-size:36px;line-height:1.1;margin:8px 0;color:#ff2d2d;text-shadow:0 0 24px rgba(255,0,0,.8),0 0 60px rgba(255,0,0,.4);letter-spacing:1px;animation:flicker 3s infinite}",
    ".screen h1{font-size:42px;line-height:1.05;margin:8px 0;color:#ff2d2d;text-shadow:0 0 24px rgba(255,0,0,.9),0 0 60px rgba(255,0,0,.5),0 4px 0 #4a0000,0 8px 18px #000;letter-spacing:4px;font-weight:900;animation:flicker 3s infinite}")
rep(".badge{display:inline-block;padding:6px 12px;border:1px solid #ff4444;border-radius:20px;color:#ffb3b3;font-size:13px;margin-bottom:10px}",
    ".badge{display:inline-block;padding:6px 14px;border:2px solid #ff2222;border-radius:20px;color:#ffdddd;font-size:13px;font-weight:800;letter-spacing:1px;margin-bottom:10px;background:rgba(120,0,0,.35);text-shadow:0 0 8px rgba(255,0,0,.8)}")
rep(".screen p{max-width:520px;line-height:1.7;color:#ddd;font-size:16px}",
    ".screen p{max-width:520px;line-height:1.7;color:#e8e8e8;font-size:16px;text-shadow:0 1px 4px #000}")

# Neater HUD panel + text
rep(".panel{background:linear-gradient(180deg,rgba(40,0,0,.85),rgba(0,0,0,.75));border:1px solid rgba(255,0,0,.6);border-radius:10px;padding:4px 7px;backdrop-filter:blur(4px);max-width:220px;box-shadow:0 0 16px rgba(255,0,0,.35)}",
    ".panel{background:linear-gradient(180deg,rgba(50,0,0,.9),rgba(5,0,0,.85));border:2px solid rgba(255,30,30,.8);border-radius:12px;padding:7px 10px;backdrop-filter:blur(4px);max-width:230px;box-shadow:0 0 18px rgba(255,0,0,.4)}")
rep("#hearts{font-size:15px;letter-spacing:1px;text-shadow:0 0 10px red}",
    "#hearts{font-size:16px;letter-spacing:2px;text-shadow:0 0 10px red}")
rep("#floorInfo{font-size:11px;color:#ffd166;font-weight:800}",
    "#floorInfo{font-size:12px;color:#ffd166;font-weight:900;letter-spacing:1px}")
rep("#objective{font-size:11px;line-height:1.3;max-width:200px;color:#ffdddd;font-weight:700}",
    "#objective{font-size:12px;line-height:1.45;max-width:205px;color:#ffd9d9;font-weight:800}")
rep("#keys{font-size:11px;margin-top:2px}",
    "#keys{font-size:12px;margin-top:3px;font-weight:800;letter-spacing:1px}")
rep("#compass{font-size:11px;color:#ffd166;margin-top:2px}",
    "#compass{font-size:12px;color:#ffd166;margin-top:3px;font-weight:800}")
# Remove duplicate #objective rule (second, plain one)
rep("#objective{font-size:11px;line-height:1.3;max-width:200px}\n", "")

# Scarier toast
rep("#toast{position:absolute;left:50%;top:10px;transform:translateX(-50%);background:rgba(0,0,0,.35);border:1px solid rgba(255,120,120,.35);color:rgba(255,220,220,.85);padding:6px 10px;border-radius:10px;font-size:13px;font-weight:600;white-space:normal;max-width:70vw;text-align:center;opacity:0;transition:opacity .25s;text-shadow:none;z-index:12}",
    "#toast{position:absolute;left:50%;top:10px;transform:translateX(-50%);background:rgba(20,0,0,.88);border:1px solid #ff2222;color:#ffe0e0;padding:7px 12px;border-radius:10px;font-size:13px;font-weight:800;letter-spacing:.5px;white-space:normal;max-width:70vw;text-align:center;opacity:0;transition:opacity .25s;text-shadow:0 0 8px rgba(255,0,0,.7);z-index:12}")

# Minimap: blood-red border, darker, glow; canvas drawing darker + softer walls
rep("<canvas id=\"minimap\" width=\"120\" height=\"60\" style=\"position:fixed;top:60px;right:8px;z-index:20;pointer-events:none;background:rgba(0,0,0,0.6);border:1px solid #444;border-radius:6px\"></canvas>",
    "<canvas id=\"minimap\" width=\"120\" height=\"60\" style=\"position:fixed;top:60px;right:8px;z-index:20;pointer-events:none;background:rgba(10,0,0,.88);border:2px solid rgba(255,30,30,.85);border-radius:10px;box-shadow:0 0 16px rgba(255,0,0,.45)\"></canvas>")
rep("  g.fillStyle='#111111';\n  g.fillRect(0,0,cv.width,cv.height);\n  const sc=0.6; // V51: minimap smaller\n  g.fillStyle='#cccccc';",
    "  g.fillStyle='#0a0000';\n  g.fillRect(0,0,cv.width,cv.height);\n  const sc=0.6; // V51: minimap smaller\n  g.fillStyle='#999999';")

# Stamina label + floor banner neater
rep("#staminaWrap label{font-size:12px;color:#ccc}",
    "#staminaWrap label{font-size:12px;color:#ffdddd;font-weight:800;letter-spacing:1px;text-shadow:0 0 8px rgba(255,0,0,.6)}")
rep("#floorBanner{position:fixed;left:50%;top:14%;transform:translate(-50%,-50%);font-size:26px;font-weight:900;color:#ffd166;text-shadow:0 0 20px #ff0000,2px 2px 0 #000;z-index:45;display:none;text-align:center}",
    "#floorBanner{position:fixed;left:50%;top:14%;transform:translate(-50%,-50%);font-size:30px;font-weight:900;letter-spacing:2px;color:#ffd166;text-shadow:0 0 24px #ff0000,2px 2px 0 #000;z-index:45;display:none;text-align:center}")

# Action buttons: cleaner blood border
rep(".abtn{width:64px;height:64px;border-radius:50%;border:2px solid rgba(255,255,255,.35);background:rgba(0,0,0,.6);color:#fff;font-size:13px;font-weight:800;cursor:pointer;touch-action:manipulation;user-select:none}",
    ".abtn{width:64px;height:64px;border-radius:50%;border:2px solid rgba(255,60,60,.65);background:rgba(10,0,0,.68);color:#fff;font-size:13px;font-weight:800;cursor:pointer;touch-action:manipulation;user-select:none;text-shadow:0 0 8px rgba(255,0,0,.7)}")

p.write_text(t, encoding='utf-8')
print('V87 patch applied')
