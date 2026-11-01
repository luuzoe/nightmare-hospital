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

# Difficulty: monster speed, grace, hide, fog, blackout
rep("    mSpeed=6.4+(S.floor===15?S.keys*0.2:S.items*0.05)+(15-S.floor)*0.08; if(S.escaping) mSpeed+=1.0; if(mSpeed>7.8) mSpeed=7.8; // V12 harder down: floor bonus + progress",
    "    mSpeed=6.4+(S.floor===15?S.keys*0.2:S.items*0.05)+(15-S.floor)*0.15; if(S.escaping) mSpeed+=1.0; if(mSpeed>8.5) mSpeed=8.5; // V47 harder: +0.15/floor, cap 8.5",
    "monster speed v47")
rep("    if(S.catchTimer>Math.max(0.45,0.65-(15-S.floor)*0.015)){ S.catchTimer=0; loseHeart(); } // V12 harder down: grace shrinks to 0.45s at bottom",
    "    if(S.catchTimer>Math.max(0.40,0.65-(15-S.floor)*0.02)){ S.catchTimer=0; loseHeart(); } // V47 harder: grace to 0.40s at bottom",
    "grace v47")
rep("    const loseAfter=(S.hideLocker?2.5:5.0)+(15-S.floor)*0.2; // V12 harder down: monster stays even longer",
    "    const loseAfter=(S.hideLocker?3.0:6.0)+(15-S.floor)*0.3; // V47 harder: monster stays longer",
    "hide lose v47")
rep("  if(scene.fog) scene.fog.density=0.09+(15-S.floor)*0.003+((fm.type==='dark'||fm.type==='darklockers')?0.04:0);",
    "  if(scene.fog) scene.fog.density=0.10+(15-S.floor)*0.005+((fm.type==='dark'||fm.type==='darklockers')?0.04:0);",
    "fog v47")
rep("    else { S.blackoutTimer-=dt; if(S.blackoutTimer<=0){ S.blackout=2.5; S.blackoutTimer=Math.max(15,28-(15-S.floor))+Math.random()*8; screamSound(); toast('⚡ မီး ပျက်သွားပြီ!'); } }",
    "    else { S.blackoutTimer-=dt; if(S.blackoutTimer<=0){ S.blackout=4.0; S.blackoutTimer=Math.max(12,22-(15-S.floor))+Math.random()*6; thump(0.4); toast('⚡ မီး ပျက်သွားပြီ! တိတ်တိတ် နေ!'); } }",
    "blackout v47")
# Ghost count
rep("  const pickCount=4+(Math.random()<0.5?1:0);",
    "  const pickCount=S.floor>=15?5:(S.floor>=10?6:7); // V47: more ghosts down, all 7 at bottom",
    "ghost count v47")
# Ep1 wake-up: monster canSee
rep("  const canSee=!S.hidden && S.floor!==15 && monsterState!=='scare' && mDist<24 && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V43 Ep1: monster never chases, tutorial floor",
    "  const canSee=!S.hidden && (S.floor!==15 || S.keys>=1) && monsterState!=='scare' && mDist<24 && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V47 Ep1 wakes up after Key1",
    "monster canSee v47")
# Wandering chase Ep1 wake-up
rep("      if(!S.hidden && S.floor!==15 && S.invuln<=0 && (S.escaping || (wd<((wg.def.radius+(wg.def.radiusBoost||0))) && !lineBlocked(wg.outer.position.x,wg.outer.position.z,playerPos.x,playerPos.z)))){",
    "      if(!S.hidden && (S.floor!==15 || S.keys>=1) && S.invuln<=0 && (S.escaping || (wd<((wg.def.radius+(wg.def.radiusBoost||0))) && !lineBlocked(wg.outer.position.x,wg.outer.position.z,playerPos.x,playerPos.z)))){",
    "wandering chase v47")
# Front jumpscare Ep1 wake-up + interval
rep("  if(S.playing && !S.paused && S.floor!==15 && !S.hidden && S.invuln<=0){\n    S.frontScareTimer-=dt;\n    if(S.frontScareTimer<=0){\n      S.frontScareTimer=45+Math.random()*30; // V25 scarier, more frequent front jumpscare",
    "  if(S.playing && !S.paused && (S.floor!==15 || S.keys>=2) && !S.hidden && S.invuln<=0){\n    S.frontScareTimer-=dt;\n    if(S.frontScareTimer<=0){\n      S.frontScareTimer=90+Math.random()*60; // V47 quiet: front scare rarer, but loud when it happens",
    "front jumpscare v47")
# Sound quieting
rep("function growlSound(){ if(playReal('growl',0.8)) return;",
    "function growlSound(){ if(playReal('growl',0.5)) return;",
    "growl vol v47")
rep("function moanSound(){ if(playReal('moan',0.5)) return;",
    "function moanSound(){ if(playReal('moan',0.25)) return;",
    "moan vol v47")
rep("function wanderingScream(){ if(S.time-lastWanderScream<20) return;",
    "function wanderingScream(){ if(S.time-lastWanderScream<60) return;",
    "wander scream gate v47")
rep("  if(S.playing && !S.paused){ S.moanTimer-=dt; if(S.moanTimer<=0){ moanSound(); S.moanTimer=40+Math.random()*40; } } // V10 moan more often",
    "  if(S.playing && !S.paused){ S.moanTimer-=dt; if(S.moanTimer<=0){ moanSound(); S.moanTimer=120+Math.random()*60; } } // V47 quiet: moan every 2-3 min, silence is scarier",
    "moan timer v47")
rep("  if(mDist<12 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>9){ growlAcc=0; growlSound(); } } else growlAcc=0;",
    "  if(mDist<12 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>20){ growlAcc=0; growlSound(); } } else growlAcc=0;",
    "growl timer v47")
rep("  if(S.playing && !S.paused){ S.whisperTimer-=dt; if(S.whisperTimer<=0){ let nd=1e9; for(const wg of wanderingGhosts){ if(wg.outer && wg.outer.visible){ const d=Math.hypot(wg.outer.position.x-playerPos.x,wg.outer.position.z-playerPos.z); if(d<nd) nd=d; } } if(nd<6 && !S.hidden && Math.random()<0.3){ whisperSound(); } S.whisperTimer=20; } }",
    "  if(S.playing && !S.paused){ S.whisperTimer-=dt; if(S.whisperTimer<=0){ let nd=1e9; for(const wg of wanderingGhosts){ if(wg.outer && wg.outer.visible){ const d=Math.hypot(wg.outer.position.x-playerPos.x,wg.outer.position.z-playerPos.z); if(d<nd) nd=d; } } if(nd<6 && !S.hidden && Math.random()<0.3){ whisperSound(); } S.whisperTimer=40; } }",
    "whisper timer v47")
rep("    if(S.randScareTimer<=0){ S.randScareTimer=45+Math.random()*45; if(Math.random()<0.6) screamSound(); else growlSound(); }",
    "    if(S.randScareTimer<=0){ S.randScareTimer=120+Math.random()*60; if(Math.random()<0.3) screamSound(); else moanSound(); } // V47 quiet random",
    "rand scare v47")
rep("      if(wg.blinkTimer<=0){ wg.blinkTimer=10+Math.random()*8; const bdx=playerPos.x-wg.outer.position.x, bdz=playerPos.z-wg.outer.position.z; const bl=Math.hypot(bdx,bdz)||1; const nmB=collide(wg.outer.position.x+bdx/bl*4, wg.outer.position.z+bdz/bl*4, 1.0); wg.outer.position.x=nmB[0]; wg.outer.position.z=nmB[1]; screamSound(); toast('👻 '+wg.def.name+' ရုတ်တရက် နီးလာပြီ!'); }",
    "      if(wg.blinkTimer<=0){ wg.blinkTimer=14+Math.random()*10; const bdx=playerPos.x-wg.outer.position.x, bdz=playerPos.z-wg.outer.position.z; const bl=Math.hypot(bdx,bdz)||1; const nmB=collide(wg.outer.position.x+bdx/bl*4, wg.outer.position.z+bdz/bl*4, 1.0); wg.outer.position.x=nmB[0]; wg.outer.position.z=nmB[1]; if(Math.random()<0.3) whisperSound(); toast('👻 '+wg.def.name+' ရုတ်တရက် နီးလာပြီ!'); }",
    "blink quiet v47")
rep("    S.corpseIdx++; pickupSound(); screamSound();",
    "    S.corpseIdx++; pickupSound(); whisperSound();",
    "corpse sound v47")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part5 applied')
