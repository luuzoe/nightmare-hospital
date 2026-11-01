import sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:180]
    t=t.replace(old,new,1)

# 1. FULLSCREEN: hide button via CSS, auto on any first tap + on start
rep("#floorBanner{position:fixed;",
"#landBtn{display:none!important}\n#floorBanner{position:fixed;")
rep("function startGame(){\n  ac(); tryAutoLandscape();",
"function startGame(){\n  ac(); tryAutoLandscape(); setTimeout(()=>tryAutoLandscape(),500);")
rep("document.addEventListener('pointerdown',()=>{ ac(); }, {passive:true});",
"document.addEventListener('pointerdown',()=>{ ac(); tryAutoLandscape(); }, {passive:true});")

# 2. S fields for beacon/stuck/heartbeat/random scare
rep("distance:0, whisperTimer:0};",
"distance:0, whisperTimer:0, beaconX:0, beaconZ:24, stuckTimer:0, lastPX:-18, lastPZ:12, stuckWarn:0, heartTimer:0, randScareTimer:25};")

# 3. Sounds louder + heartbeat
rep("function growlSound(){ playTone(75,55,0.9,'sawtooth',0.20,9); playNoise(0.9,'lowpass',200,1,0.15,9); }",
"function growlSound(){ playTone(75,55,0.9,'sawtooth',0.30,9); playNoise(0.9,'lowpass',200,1,0.22,9); }\nfunction heartbeatSound(){ thump(0.5); setTimeout(()=>thump(0.4),180); }")
rep("function moanSound(){ playTone(280,170,2.0,'sine',0.12,5); playNoise(2.0,'bandpass',500,2,0.08,3); }",
"function moanSound(){ playTone(280,170,2.0,'sine',0.20,5); playNoise(2.0,'bandpass',500,2,0.14,3); }")
rep("function scareSound(){ playTone(120,45,0.9,'sawtooth',0.28,0); playNoise(0.9,'lowpass',400,1,0.20,0); thump(0.4); }",
"function scareSound(){ playTone(120,45,0.9,'sawtooth',0.40,0); playNoise(0.9,'lowpass',400,1,0.30,0); thump(0.5); }")
rep("function screamSound(){ playNoise(0.8,'highpass',1000,1,0.30,0); playTone(900,250,0.8,'sawtooth',0.25,0); setTimeout(()=>playTone(1200,400,0.5,'sawtooth',0.20,0),150); setTimeout(()=>playTone(800,200,0.6,'sawtooth',0.12,0),400); } // V12 echo",
"function screamSound(){ playNoise(0.8,'highpass',1000,1,0.45,0); playTone(900,250,0.8,'sawtooth',0.38,0); setTimeout(()=>playTone(1200,400,0.5,'sawtooth',0.30,0),150); setTimeout(()=>playTone(800,200,0.6,'sawtooth',0.20,0),400); }")
rep("function whisperSound(){ playNoise(1.2,'bandpass',1200,1.5,0.20,7); playNoise(1.0,'bandpass',800,2,0.15,11); playTone(220,160,1.2,'sine',0.08,6); }",
"function whisperSound(){ playNoise(1.2,'bandpass',1200,1.5,0.30,7); playNoise(1.0,'bandpass',800,2,0.22,11); playTone(220,160,1.2,'sine',0.14,6); }")

# 4. Flashlight stronger + room light a bit brighter, ceiling visible
rep("const flash=new THREE.SpotLight(0xfff2cc,80,15,0.45,0.35,1);",
"const flash=new THREE.SpotLight(0xfff2cc,130,22,0.50,0.35,1);")
rep("scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.20));",
"scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.28));")
rep("ceil.rotation.x=Math.PI/2; ceil.position.set(0,3.4,0); scene.add(ceil); ceil.visible=false; // V5: no big ceiling plane in view",
"ceil.rotation.x=Math.PI/2; ceil.position.set(0,3.4,0); scene.add(ceil); ceil.visible=true;")

# 5. Ghost face overlay div (proximity jumpscare, separate from #jumpscare)
rep('<div id="vignette"></div><div id="damage"></div><div id="bloodScreen"></div><div id="jumpscare">👻</div>',
'<div id="vignette"></div><div id="damage"></div><div id="bloodScreen"></div><div id="jumpscare">👻</div><div id="ghostFace" style="display:none;position:fixed;inset:0;z-index:30;pointer-events:none;text-align:center;padding-top:18%;font-size:180px;text-shadow:0 0 40px #ff0000">👻</div>')

# 6. Beacon + hospital details + door frames (after stairwell block, before collision helpers)
rep("/* ============ COLLISION HELPERS ============ */",
"""// V14 objective beacon: tall gold pillar, visible through walls/fog, always points to next objective
const beacon=new THREE.Mesh(new THREE.CylinderGeometry(0.25,0.25,7,12), new THREE.MeshBasicMaterial({color:0xffd700,transparent:true,opacity:0.6,depthTest:false,fog:false}));
beacon.renderOrder=999; beacon.position.set(0,3.5,24); scene.add(beacon);
// V14 realistic details: lamps, IV stands, wheelchairs, stretchers, posters, debris, door frames (visual only, no collision)
for(const [lx,lz] of [[-18,-12],[18,-12],[-18,12],[18,12],[0,0]]){ const lamp=new THREE.Mesh(new THREE.BoxGeometry(1.4,0.12,0.7), new THREE.MeshBasicMaterial({color:0xfff2cc})); lamp.position.set(lx,3.35,lz); scene.add(lamp); }
function ivStand(x,z){ const g=new THREE.Group(); const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,1.9,8), new THREE.MeshStandardMaterial({color:0x888888})); pole.position.y=0.95; const top=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.06,0.06), pole.material); top.position.y=1.9; const bag=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.35,0.08), new THREE.MeshStandardMaterial({color:0xffe0a0})); bag.position.set(0.25,1.7,0); g.add(pole,top,bag); g.position.set(x,0,z); scene.add(g); }
ivStand(-24,-16); ivStand(22,-14); ivStand(-22,14); ivStand(58,-10);
function wheelchair(x,z,ry){ const g=new THREE.Group(); const seat=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.1,0.6), new THREE.MeshStandardMaterial({color:0x222222})); seat.position.y=0.5; const back=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.7,0.1), seat.material); back.position.set(0,0.9,-0.3); g.add(seat,back); for(const sx of [-0.35,0.35]){ const w=new THREE.Mesh(new THREE.TorusGeometry(0.32,0.04,8,16), new THREE.MeshStandardMaterial({color:0x111111})); w.position.set(sx,0.32,0); g.add(w); } g.position.set(x,0,z); g.rotation.y=ry; scene.add(g); }
wheelchair(-16,10,0.5); wheelchair(14,-8,2.0);
function stretcher(x,z,ry){ const g=new THREE.Group(); const bed=new THREE.Mesh(new THREE.BoxGeometry(1.9,0.15,0.7), new THREE.MeshStandardMaterial({color:0x3a3a3a})); bed.position.y=0.9; g.add(bed); for(const [px,pz] of [[-0.8,-0.3],[0.8,-0.3],[-0.8,0.3],[0.8,0.3]]){ const leg=new THREE.Mesh(new THREE.BoxGeometry(0.08,0.9,0.08), bed.material); leg.position.set(px,0.45,pz); g.add(leg); } g.position.set(x,0,z); g.rotation.y=ry; scene.add(g); }
stretcher(0,-8,0); stretcher(10,0,1.57);
function poster(txt,x,y,z,ry){ const cv=document.createElement('canvas'); cv.width=256; cv.height=128; const g=cv.getContext('2d'); g.fillStyle='#0a2a5a'; g.fillRect(0,0,256,128); g.fillStyle='#ffffff'; g.font='bold 36px sans-serif'; g.textAlign='center'; g.fillText(txt,128,70); const tex=new THREE.CanvasTexture(cv); tex.colorSpace=THREE.SRGBColorSpace; const m=new THREE.Mesh(new THREE.PlaneGeometry(2,1), new THREE.MeshBasicMaterial({map:tex})); m.position.set(x,y,z); m.rotation.y=ry; scene.add(m); }
poster('EMERGENCY',-31.6,2,0,Math.PI/2); poster('ICU',31.6,2,-10,-Math.PI/2); poster('PHARMACY',10,2,23.6,Math.PI); poster('X-RAY',-10,2,-23.6,0);
for(let i=0;i<20;i++){ const db=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.08,0.25), new THREE.MeshStandardMaterial({color:0x1a1a1a})); db.position.set(-30+Math.random()*95,-0+0.04,-22+Math.random()*44); if(Math.abs(db.position.x)<5 && Math.abs(db.position.z)<4) continue; scene.add(db); }
function doorFrame(cx,cz,vertical){ const mat=new THREE.MeshStandardMaterial({color:0x2a2a2a}); const w=vertical?0.25:4.4, d=vertical?4.4:0.25; const top=new THREE.Mesh(new THREE.BoxGeometry(w,0.3,d), mat); top.position.set(cx,3.25,cz); scene.add(top); const off=vertical?2:2; for(const s of [-1,1]){ const post=new THREE.Mesh(new THREE.BoxGeometry(vertical?0.25:0.25,3.4,vertical?0.25:0.25), mat); if(vertical) post.position.set(cx,1.7,cz+s*2); else post.position.set(cx+s*2,1.7,cz); scene.add(post); } }
doorFrame(-16,-3,false); doorFrame(-16,3,false); doorFrame(16,-3,false); doorFrame(16,3,false); doorFrame(0,-3,false); doorFrame(0,3,false);
makeBloodWriting('IT SEES YOU',-31.6,1.8,8,Math.PI/2); makeBloodWriting("DON'T TRUST",31.6,1.8,8,-Math.PI/2);
/* ============ COLLISION HELPERS ============ */""")

# 7. Ghost eyes/mouth bigger + stretched taller (main monster)
rep("        for(const sx of [-0.14,0.14]){ const sock=new THREE.Mesh(new THREE.SphereGeometry(0.13,8,8),blackMat); sock.position.set(sx,eyeY,0.18); outer.add(sock); const pup=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8),redMat); pup.position.set(sx,eyeY,0.28); outer.add(pup); }\n        const mouth=new THREE.Mesh(new THREE.BoxGeometry(0.22,0.14,0.05),blackMat); mouth.position.set(0,targetH*0.82,0.22); outer.add(mouth);",
"        for(const sx of [-0.14,0.14]){ const sock=new THREE.Mesh(new THREE.SphereGeometry(0.18,8,8),blackMat); sock.position.set(sx,eyeY,0.18); outer.add(sock); const pup=new THREE.Mesh(new THREE.SphereGeometry(0.08,8,8),redMat); pup.position.set(sx,eyeY,0.28); outer.add(pup); }\n        const mouth=new THREE.Mesh(new THREE.BoxGeometry(0.30,0.20,0.05),blackMat); mouth.position.set(0,targetH*0.82,0.22); outer.add(mouth);")
# wandering ghost eyes bigger
rep("      for(const sx of [-0.14,0.14]){ const e=new THREE.Mesh(new THREE.SphereGeometry(0.13,8,8),eyeMat); e.position.set(sx,eyeY2,0.18); outer.add(e); if(def.eye===0x000000){ const pup=new THREE.Mesh(new THREE.SphereGeometry(0.05,8,8),new THREE.MeshBasicMaterial({color:0xff0000})); pup.position.set(sx,eyeY2,0.27); outer.add(pup); } }\n      const mouthW=new THREE.Mesh(new THREE.BoxGeometry(0.18,0.12,0.05),eyeMat); mouthW.position.set(0,eyeY2*0.89,0.22); outer.add(mouthW);",
"      for(const sx of [-0.14,0.14]){ const e=new THREE.Mesh(new THREE.SphereGeometry(0.16,8,8),eyeMat); e.position.set(sx,eyeY2,0.18); outer.add(e); if(def.eye===0x000000){ const pup=new THREE.Mesh(new THREE.SphereGeometry(0.07,8,8),new THREE.MeshBasicMaterial({color:0xff0000})); pup.position.set(sx,eyeY2,0.27); outer.add(pup); } }\n      const mouthW=new THREE.Mesh(new THREE.BoxGeometry(0.24,0.16,0.05),eyeMat); mouthW.position.set(0,eyeY2*0.89,0.22); outer.add(mouthW);")

# 8. Beacon target + anti-stuck + heartbeat + random scare + ghost face + blink (insert before monster AI comment, and in update)
rep("  const ang=Math.atan2(tx-playerPos.x,tz-playerPos.z);",
"  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.scale.x=beacon.scale.z=1+Math.sin(t*3)*0.2;\n  const ang=Math.atan2(tx-playerPos.x,tz-playerPos.z);")
# anti-stuck + heartbeat + random scare: insert before V12 FINAL ESCAPE progress comment (second occurrence in update, after ghosts loop)
rep("  // V12 FINAL ESCAPE progress: 8s near exit door, pauses if away/hidden, win at 100%",
"""  // V14 anti-stuck: pushing joystick 2s without moving = wall, warn + point to beacon
  if(S.playing && !S.paused && S.joy.active){
    S.stuckTimer+=dt;
    if(S.stuckTimer>=2){
      const moved=Math.hypot(playerPos.x-S.lastPX,playerPos.z-S.lastPZ);
      if(moved<0.3 && S.time-S.stuckWarn>5){ S.stuckWarn=S.time; toast('⛔ နံရံ ပိတ်နေသည်! ကင်မရာလှည့်ပြီး အဝါရောင် တိုင် (beacon) ဘက် သွားပါ'); if(navigator.vibrate) navigator.vibrate(100); }
      S.stuckTimer=0; S.lastPX=playerPos.x; S.lastPZ=playerPos.z;
    }
  } else { S.stuckTimer=0; S.lastPX=playerPos.x; S.lastPZ=playerPos.z; }
  // V14 heartbeat: closer ghost/monster = faster heartbeat
  if(S.playing && !S.paused){
    let nd2=Math.hypot(monsterPos.x-playerPos.x,monsterPos.z-playerPos.z);
    for(const wg of wanderingGhosts){ if(wg.outer && wg.outer.visible){ const d=Math.hypot(wg.outer.position.x-playerPos.x,wg.outer.position.z-playerPos.z); if(d<nd2) nd2=d; } }
    S.heartTimer-=dt;
    if(nd2<12 && S.heartTimer<=0){ heartbeatSound(); S.heartTimer=Math.max(0.45,nd2*0.07); }
    S.randScareTimer-=dt;
    if(S.randScareTimer<=0){ S.randScareTimer=20+Math.random()*20; if(Math.random()<0.6) screamSound(); else if(Math.random()<0.5) whisperSound(); else growlSound(); }
    const gf=$('ghostFace'); if(gf) gf.style.display=(S.chase && nd2<3)?'block':'none';
  }
  // V12 FINAL ESCAPE progress: 8s near exit door, pauses if away/hidden, win at 100%""")
# ghost blink in patrol: insert in wandering patrol else branch, before wp movement
rep("      wg.outer.visible=true; wg.outer.position.y=(wg.def.floatY||0.1)+Math.sin(t*2.5)*0.06;",
"""      wg.outer.visible=true; wg.outer.position.y=(wg.def.floatY||0.1)+Math.sin(t*2.5)*0.06;
      if(typeof wg.blinkTimer==='undefined') wg.blinkTimer=8+Math.random()*6;
      wg.blinkTimer-=dt;
      if(wg.blinkTimer<=0){ wg.blinkTimer=10+Math.random()*8; const bdx=playerPos.x-wg.outer.position.x, bdz=playerPos.z-wg.outer.position.z; const bl=Math.hypot(bdx,bdz)||1; const nmB=collide(wg.outer.position.x+bdx/bl*4, wg.outer.position.z+bdz/bl*4, 0.5); wg.outer.position.x=nmB[0]; wg.outer.position.z=nmB[1]; screamSound(); toast('👻 '+wg.def.name+' ရုတ်တရက် နီးလာပြီ!'); }""")

rep("V13.1 • လှေကား ဝင်လို့ရပြီ + အနီအကွက် သေးသွားပြီ",
"V14 • Beacon + Auto Fullscreen + ပိုကြောက် + ပို Realistic")

open(p,'w',encoding='utf-8').write(t)
print("V14 PATCH OK")
