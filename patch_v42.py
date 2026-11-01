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

rep("V41 • HIDE ဖွင့်ထားရင် မလှုပ် (အရင်လို) + Compass ပေါက် + သော့ လမ်းကြောင်း စစ်ပြီး — အကုန်",
    "V42 • အဖြူ သရဲ emoji ဖြုတ် + ပေါက် frame + Ep1 သရဲ လိုက်တာ လျှော့ — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်)</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • အဖြူ သရဲ emoji မရှိတော့</p>",
    "start hint")
# Remove white cartoon ghost overlay: HTML empty, JS never shows it
rep('<div id="vignette"></div><div id="damage"></div><div id="bloodScreen"></div><div id="jumpscare">👻</div><div id="ghostFace" style="display:none;position:fixed;inset:0;z-index:30;pointer-events:none;text-align:center;padding-top:18%;font-size:180px;text-shadow:0 0 40px #ff0000">👻</div>',
    '<div id="vignette"></div><div id="damage"></div><div id="bloodScreen"></div><div id="jumpscare"></div><div id="ghostFace" style="display:none"></div>',
    "ghost emoji html")
rep("  const js=$('jumpscare'); if(js){ js.style.display='block'; setTimeout(()=>js.style.display='none',600); }",
    "  const js=$('jumpscare'); if(js){ js.style.display='none'; }",
    "jumpscare 600")
rep("      const js2=$('jumpscare'); if(js2){ js2.style.display='block'; setTimeout(()=>js2.style.display='none',250); }",
    "      const js2=$('jumpscare'); if(js2){ js2.style.display='none'; }",
    "jumpscare 250")
rep("  const gf=$('ghostFace'); if(gf) gf.style.display=(S.time<S.ghostFaceUntil || (S.chase && Math.hypot(monsterPos.x-playerPos.x,monsterPos.z-playerPos.z)<3))?'block':'none';",
    "  const gf=$('ghostFace'); if(gf) gf.style.display='none';",
    "ghostFace front")
rep("    const gf=$('ghostFace'); if(gf && S.time>=S.ghostFaceUntil) gf.style.display=(S.chase && nd2<3)?'block':'none';",
    "    const gf=$('ghostFace'); if(gf) gf.style.display='none';",
    "ghostFace chase")
# Door frames at vertical gaps, so gaps are visible in the dark
rep("doorFrame(-16,-3,false); doorFrame(-16,3,false); doorFrame(16,-3,false); doorFrame(16,3,false); doorFrame(0,-3,false); doorFrame(0,3,false);",
    "doorFrame(-16,-3,false); doorFrame(-16,3,false); doorFrame(16,-3,false); doorFrame(16,3,false); doorFrame(0,-3,false); doorFrame(0,3,false); doorFrame(-4,-12,true); doorFrame(4,-12,true); doorFrame(-4,0,true); doorFrame(4,0,true); doorFrame(-4,12,true); doorFrame(4,12,true);",
    "vertical door frames")
# Floor 15 only: monster detection 24 -> 16, so Ep1 is learnable, not constant chase
rep("  const canSee=!S.hidden && monsterState!=='scare' && mDist<24 && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V10 sees farther",
    "  const canSee=!S.hidden && monsterState!=='scare' && mDist<(S.floor===15?16:24) && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V42 Ep1: 16m, later floors 24m",
    "monster detection Ep1")
# Floor 15 only: wandering chase radius reduced via radiusBoost negative on floor 15 in setActiveGhosts? Simpler: in wandering chase check, use effective radius
rep("      if(!S.hidden && S.invuln<=0 && (S.escaping || (wd<(wg.def.radius+(wg.def.radiusBoost||0)) && !lineBlocked(wg.outer.position.x,wg.outer.position.z,playerPos.x,playerPos.z)))){",
    "      if(!S.hidden && S.invuln<=0 && (S.escaping || (wd<((wg.def.radius+(wg.def.radiusBoost||0))*(S.floor===15?0.65:1)) && !lineBlocked(wg.outer.position.x,wg.outer.position.z,playerPos.x,playerPos.z)))){",
    "wandering radius Ep1")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V42 patch applied')
