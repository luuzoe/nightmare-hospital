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

rep("V37 • Morgue သော့ လွတ်တဲ့ နေရာ + လက် ပြန်မြင် + ခလုတ် သေး — အကုန်",
    "V38 • ပရိဘောဂ မတိုက် + HIDE ရွေး + အလောင်းကောင် မြင် — အကုန်",
    "version")
# S hideSneak default true
rep("showMap:true, showHands:true, camSpeed:1, volume:1, lowQuality:false};",
    "showMap:true, showHands:true, camSpeed:1, volume:1, lowQuality:false, hideSneak:true};",
    "S hideSneak")
# Props no collision: only walls collide, furniture visual only
rep("function collide(x,z,r,allowStair){\n  for(const w of walls.concat(props)){",
    "function collide(x,z,r,allowStair){\n  for(const w of walls){",
    "props no collision")
# HIDE moving logic: allow walk only if hideSneak, else stationary (original)
rep("  const moving=il>0.08;",
    "  const moving=il>0.08 && (!S.hidden || S.hideSneak!==false);",
    "hide move mode")
rep("  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il))*(S.hidden?0.5:1);",
    "  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il))*(S.hidden && S.hideSneak!==false?0.5:1);",
    "hide speed mode")
# hideTag text based on mode, in updateHUD where hideTag display is set
rep("  $('hideTag').style.display=S.hidden?'block':'none';",
    "  $('hideTag').style.display=S.hidden?'block':'none'; if(S.hidden && $('hideTag')) $('hideTag').textContent=S.hideSneak!==false?'🫥 ပုန်းနေသည် (နှေးနှေး သွား)':'🫥 ပုန်းနေသည် (ရပ်)';",
    "hideTag mode text")
# Pause hide mode button, after handToggleBtn row
rep('    <button class="btn ghost" id="mapToggleBtn">🗺️ မြေပုံ: ဖွင့်</button>\n    <button class="btn ghost" id="handToggleBtn">✋ လက်: ဖွင့်</button>',
    '    <button class="btn ghost" id="mapToggleBtn">🗺️ မြေပုံ: ဖွင့်</button>\n    <button class="btn ghost" id="handToggleBtn">✋ လက်: ဖွင့်</button>\n    <button class="btn ghost" id="hideModeBtn">🫥 HIDE: နှေးနှေး သွား</button>',
    "hide mode button html")
# Hide mode wiring, after handToggle wiring
rep("if($('handToggleBtn')){ $('handToggleBtn').addEventListener('click',()=>{ S.showHands=!S.showHands; $('handToggleBtn').textContent=S.showHands?'✋ လက်: ဖွင့်':'✋ လက်: ပိတ်'; }); }",
    "if($('handToggleBtn')){ $('handToggleBtn').addEventListener('click',()=>{ S.showHands=!S.showHands; $('handToggleBtn').textContent=S.showHands?'✋ လက်: ဖွင့်':'✋ လက်: ပိတ်'; }); }\nif($('hideModeBtn')){ $('hideModeBtn').addEventListener('click',()=>{ S.hideSneak=!S.hideSneak; $('hideModeBtn').textContent=S.hideSneak?'🫥 HIDE: နှေးနှေး သွား':'🫥 HIDE: ရပ်'; }); }",
    "hide mode wiring")
# Start screen hint about HIDE sneak
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း + နှေးနှေး သွား (Pause မှာ ရပ် လို့ ပြောင်းလို့ ရသည်)</p>",
    "start hint hide")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V38 patch applied')
