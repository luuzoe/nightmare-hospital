p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:250]
    t=t.replace(old,new,1)

# --- 1) Scarier sounds: louder, deeper, longer, echo ---
rep("function growlSound(){ playTone(75,55,0.9,'sawtooth',0.30,9); playNoise(0.9,'lowpass',200,1,0.22,9); }",
    "function growlSound(){ playTone(60,35,1.5,'sawtooth',0.50,9); playNoise(1.5,'lowpass',180,1,0.35,9); playTone(40,28,1.5,'sine',0.40,0); } // V29 scarier: deeper, louder, longer + rumble")
rep("function moanSound(){ playTone(280,170,2.0,'sine',0.20,5); playNoise(2.0,'bandpass',500,2,0.14,3); }",
    "function moanSound(){ playTone(240,120,3.0,'sine',0.35,5); playNoise(3.0,'bandpass',400,2,0.25,3); playTone(120,80,3.0,'sawtooth',0.20,4); } // V29 scarier: lower, longer")
rep("function scareSound(){ playTone(120,45,0.9,'sawtooth',0.40,0); playNoise(0.9,'lowpass',400,1,0.30,0); thump(0.5); }",
    "function scareSound(){ playTone(110,35,1.4,'sawtooth',0.60,0); playNoise(1.4,'lowpass',300,1,0.45,0); thump(0.7); playTone(50,30,1.4,'sine',0.45,0); } // V29 scarier")
rep("function whisperSound(){ playNoise(1.2,'bandpass',1200,1.5,0.30,7); playNoise(1.0,'bandpass',800,2,0.22,11); playTone(220,160,1.2,'sine',0.14,6); } // breathy shhh, louder",
    "function whisperSound(){ playNoise(1.6,'bandpass',1100,1.5,0.45,7); playNoise(1.4,'bandpass',750,2,0.35,11); playTone(200,130,1.6,'sine',0.22,6); playNoise(1.2,'bandpass',1600,3,0.20,13); } // V29 scarier: louder, longer, extra hiss")
rep("function screamSound(){ playNoise(0.8,'highpass',1000,1,0.45,0); playTone(900,250,0.8,'sawtooth',0.38,0); setTimeout(()=>playTone(1200,400,0.5,'sawtooth',0.30,0),150); setTimeout(()=>playTone(800,200,0.6,'sawtooth',0.20,0),400); }",
    "function screamSound(){ playNoise(1.4,'highpass',900,1,0.65,0); playTone(950,200,1.4,'sawtooth',0.55,0); setTimeout(()=>playTone(1300,350,0.8,'sawtooth',0.45,0),150); setTimeout(()=>playTone(850,180,0.9,'sawtooth',0.35,0),400); setTimeout(()=>playTone(1100,300,0.7,'sawtooth',0.25,0),800); playTone(55,30,1.4,'sine',0.45,0); } // V29 scarier: louder, longer, echo + rumble")
rep("ambientGain.gain.value=S.sound?0.04:0;",
    "ambientGain.gain.value=S.sound?0.07:0; // V29 scarier ambient louder")

# --- 2) New ghosts: Inktober + LowPoly (duplicates + oil-tank ghost_3 skipped) ---
old_def="{name:'Ghost Girl', src:'ghost-saori.glb', real:true, scale:0.2, yOffset:0.79, rotX:Math.PI/2, pos:[24,20], wps:[[24,20],[20,12],[0,0],[24,0]], speed:3.0, radius:12, floatY:0.2, chaseTime:4.5, sound:'scream'}, // V28: replaces lying Ghost Girl Animated with Zaw-sent Saori girl (no anim, head at -Z so rotX +PI/2 stands it up, scale 0.2 => 1.84m)"
new_def=old_def+"""
    {name:'Inktober Ghost', src:'ghost-inktober.glb', real:true, scale:1.0, yOffset:1.01, pos:[-24,-12], wps:[[-24,-12],[-16,-12],[0,0],[-20,0]], speed:2.5, radius:12, floatY:0.2, chaseTime:5, sound:'moan'},
    {name:'Low Poly Ghost', src:'ghost-lowpoly.glb', real:true, scale:0.056, yOffset:0.43, pos:[24,-20], wps:[[24,-20],[16,-12],[0,0],[20,0]], speed:2.7, radius:12, floatY:0.2, chaseTime:5, sound:'growl'},"""
rep(old_def,new_def)

# --- 3) Poltergeist: wheelchairs + stretchers move by themselves occasionally ---
rep("function wheelchair(x,z,ry){",
    "const poltergeistItems=[]; let polterTimer=20+Math.random()*15, polterAnim=null;\nfunction wheelchair(x,z,ry){")
# push in wheelchair: after g.position.set(x,0,z); g.rotation.y=ry; scene.add(g);
rep("g.position.set(x,0,z); g.rotation.y=ry; scene.add(g); }\nwheelchair(-16,10,0.5);",
    "g.position.set(x,0,z); g.rotation.y=ry; scene.add(g); poltergeistItems.push(g); }\nwheelchair(-16,10,0.5);")
rep("g.position.set(x,0,z); g.rotation.y=ry; scene.add(g); }\nstretcher(0,-8,0);",
    "g.position.set(x,0,z); g.rotation.y=ry; scene.add(g); poltergeistItems.push(g); }\nstretcher(0,-8,0);")
# update logic: insert before whisper timer block
anchor="  if(S.playing && !S.paused){ S.whisperTimer-=dt;"
polter="""  // V29 poltergeist: occasionally a wheelchair/stretcher moves by itself (visual-only, no collision, so it cannot break walls)
  if(S.playing && !S.paused){
    if(polterAnim){
      polterAnim.t+=dt; const k=Math.min(1,polterAnim.t/polterAnim.dur); const e=k<0.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
      polterAnim.item.position.x=polterAnim.fx+(polterAnim.tx-polterAnim.fx)*e; polterAnim.item.position.z=polterAnim.fz+(polterAnim.tz-polterAnim.fz)*e; polterAnim.item.rotation.y=polterAnim.fry+(polterAnim.try-polterAnim.fry)*e;
      if(k>=1){ polterAnim=null; polterTimer=20+Math.random()*20; }
    } else {
      polterTimer-=dt;
      if(polterTimer<=0){
        const near=poltergeistItems.filter(it=>Math.hypot(it.position.x-playerPos.x,it.position.z-playerPos.z)<25);
        const pool=near.length?near:poltergeistItems;
        if(pool.length){
          const it=pool[Math.floor(Math.random()*pool.length)];
          const ang=Math.random()*Math.PI*2, dist=3+Math.random()*2;
          let tx=Math.max(-30,Math.min(68,it.position.x+Math.cos(ang)*dist)), tz=Math.max(-22,Math.min(22,it.position.z+Math.sin(ang)*dist));
          let blocked=false; for(const w of walls){ if(Math.abs(tx-w.x)<w.w/2+0.6 && Math.abs(tz-w.z)<w.d/2+0.6){ blocked=true; break; } }
          if(!blocked){ polterAnim={item:it,fx:it.position.x,fz:it.position.z,tx,tz,fry:it.rotation.y,try:it.rotation.y+(Math.random()<0.5?-1:1)*(0.5+Math.random()*1.5),t:0,dur:2.0}; doorSound(); playNoise(1.5,'lowpass',300,1,0.20,0); if(Math.hypot(tx-playerPos.x,tz-playerPos.z)<12) whisperSound(); }
          else polterTimer=5;
        } else polterTimer=10;
      }
    }
  }
"""
rep(anchor, polter+anchor)

# version label
rep("V28 • Ghost Girl အသစ် (Saori) — လှဲနေတဲ့ အဟောင်း အစားထိုး",
    "V29 • သရဲ ၂ ကောင် အသစ် + ပရိဘောဂ သူ့သူ ရွှေ့ + အသံ ပိုကြောက်")
open(p,'w',encoding='utf-8').write(t)
print("V29 PATCH OK")
