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

rep("V40 • HIDE ပုန်း + နှေးနှေး သွား ပြန် + Compass ပေါက်ကို တည့်တည့် ပြ — အကုန်",
    "V41 • HIDE ဖွင့်ထားရင် မလှုပ် (အရင်လို) + Compass ပေါက် + သော့ လမ်းကြောင်း စစ်ပြီး — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း + နှေးနှေး သွား</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်)</p>",
    "start hint")
rep("  const moving=il>0.08;",
    "  const moving=il>0.08 && !S.hidden;",
    "hide stationary")
rep("  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il))*(S.hidden?0.5:1);",
    "  const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il));",
    "hide speed")
rep("  $('hideTag').style.display=S.hidden?'block':'none'; if(S.hidden && $('hideTag')) $('hideTag').textContent='🫥 ပုန်းနေသည် • နှေးနှေး သွား';",
    "  $('hideTag').style.display=S.hidden?'block':'none';",
    "hideTag")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V41 patch applied')
