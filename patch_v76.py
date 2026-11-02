import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
m = re.search(r"V75[^<]{0,80}", t)
assert m, "V75 label not found"
t = t.replace(m.group(0), "V76 PLACEHOLDER", 1)

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:120]}"
    t = t.replace(old, new, 1)

# --- Death: 5s slow countdown, not instant respawn ---
rep("function loseHeart(){\n  S.hearts--; S.invuln=3;", "function loseHeart(){\n  if(S._dying) return; S._dying=true; S.hearts--; S.invuln=3;")
rep("const d=$('damage'); d.style.opacity=1; setTimeout(()=>d.style.opacity=0,400);", "const d=$('damage'); d.style.opacity=1;")
rep("  playerPos.set(-7.5,0,0); S.yaw=Math.PI/2; monsterPos.set(80,0,0); monsterState='patrol'; S.chase=false; S.scare=false; S.catchTimer=0; S.hidden=false; S.hideTimer=0; $('hideBtn').classList.remove('active');\n  if(S.hearts<=0) endGame(false); updateHUD();",
    "  S.paused=true; let cd=5; toast('💀 သေသွားပြီ… '+cd); const cdInt=setInterval(()=>{ cd--; if(cd>0){ toast('💀 '+cd); try{ heartbeatSound(); }catch(e){} } else { clearInterval(cdInt); S._dying=false; S.paused=false; if(d) d.style.opacity=0; if(S.hearts<=0){ endGame(false); } else { playerPos.set(-7.5,0,0); S.yaw=Math.PI/2; monsterPos.set(80,0,0); monsterState='patrol'; S.chase=false; S.scare=false; S.catchTimer=0; S.hidden=false; S.hideTimer=0; $('hideBtn').classList.remove('active'); S.invuln=3; toast('👻 ပြန်ပေါ်လာပြီ! တိတ်တိတ် ရှာပါ'); } updateHUD(); } },1000); updateHUD();")
rep("function resetGame(){\n  S.hearts=3;", "function resetGame(){\n  S._dying=false; S.hearts=3;")

# --- Ghost sounds: louder, more frequent ---
rep("if(playReal('moan',0.25))", "if(playReal('moan',0.6))")
rep("if(playReal('growl',0.5))", "if(playReal('growl',0.8))")
rep("if(playReal('girl',0.35))", "if(playReal('girl',0.7))")
rep("if(S.time-lastGirlTime<120) return;", "if(S.time-lastGirlTime<30) return;")
rep("S.moanTimer=90+Math.random()*30;", "S.moanTimer=45+Math.random()*25;")
rep("if(mDist<16 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>15){", "if(mDist<20 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>10){")
rep("if(mDist<9 && !S.hidden && monsterState!=='scare'){ whisperAcc+=dt; if(whisperAcc>18){", "if(mDist<12 && !S.hidden && monsterState!=='scare'){ whisperAcc+=dt; if(whisperAcc>12){")

# --- Chair dash: alternate bed/chair, not random ---
rep("let dashTimer=40+Math.random()*30, dashAnim=null;", "let dashTimer=40+Math.random()*30, dashAnim=null, dashIdx=0;")
rep("const it=dashItems[Math.floor(Math.random()*dashItems.length)];", "const it=dashItems[dashIdx%2]; dashIdx++;")

# --- Corpses: corridor + more rooms (append only, old indices preserved) ---
rep("  {x:-62,z:20,yaw:1.0}, {x:-2,z:20,yaw:2.8}, {x:58,z:20,yaw:0},\n];",
    "  {x:-62,z:20,yaw:1.0}, {x:-2,z:20,yaw:2.8}, {x:58,z:20,yaw:0},\n  {x:-40,z:0,yaw:0.5}, {x:10,z:0,yaw:2.0}, {x:60,z:0,yaw:1.0},\n  {x:-77,z:-20,yaw:1.5}, {x:-17,z:-20,yaw:0.2}, {x:73,z:20,yaw:2.5}, {x:-32,z:20,yaw:0.8},\n];")
rep("    {src:'cesium-man.glb',scale:PLAYER_BASE,real:false},\n  ];",
    "    {src:'cesium-man.glb',scale:PLAYER_BASE,real:false},\n    {src:'dead1.glb',scale:1.2,ox:0,oy:0.4,oz:0,real:true},\n    {src:'dead2.glb',scale:0.012,ox:0.45,oy:0,oz:1.17,real:true},\n    {src:'dead3.glb',scale:0.36,ox:0.68,oy:0.32,oz:0,real:true},\n    {src:'dead4.glb',scale:1.2,ox:-0.165,oy:0,oz:0,rotX:-Math.PI/2,real:true},\n    {src:'dead1.glb',scale:1.2,ox:0,oy:0.4,oz:0,real:true},\n    {src:'dead2.glb',scale:0.012,ox:0.45,oy:0,oz:1.17,real:true},\n    {src:'dead3.glb',scale:0.36,ox:0.68,oy:0.32,oz:0,real:true},\n  ];")

# --- Blood: more floor pools + wall smears in corridor and rooms ---
rep("makeWallBlood(-47,1.5,-5.3,0,3,2); makeWallBlood(47,1.5,5.3,Math.PI,3,2); makeWallBlood(80,1.5,0,-Math.PI/2,3,2);",
    "makeWallBlood(-47,1.5,-5.3,0,3,2); makeWallBlood(47,1.5,5.3,Math.PI,3,2); makeWallBlood(80,1.5,0,-Math.PI/2,3,2);\nmakeWallBlood(-17,1.5,-5.3,0,3,2); makeWallBlood(17,1.5,-5.3,0,3,2); makeWallBlood(62,1.5,-5.3,0,3,2); makeWallBlood(-32,1.5,5.3,Math.PI,3,2); makeWallBlood(13,1.5,5.3,Math.PI,3,2); makeWallBlood(58,1.5,5.3,Math.PI,3,2); makeWallBlood(-40,1.5,-29.6,0,4,2.5); makeWallBlood(40,1.5,-29.6,0,4,2.5); makeWallBlood(-40,1.5,29.6,Math.PI,4,2.5); makeWallBlood(40,1.5,29.6,Math.PI,4,2.5);\nmakeBloodPool(-60,0,1.2); makeBloodPool(-20,0,1.0); makeBloodPool(20,0,1.3); makeBloodPool(60,0,1.1); makeBloodPool(-47,-20,1.0); makeBloodPool(32,-20,1.2); makeBloodPool(-62,20,1.0); makeBloodPool(43,20,1.2);")

p.write_text(t, encoding='utf-8')
print('V76 patch applied')
