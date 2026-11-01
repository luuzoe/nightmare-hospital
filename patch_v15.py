import sys
p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:180]
    t=t.replace(old,new,1)

# 1. Active ghosts: 5 per floor instead of 3
rep("  const active=[wanderingGhosts[fd%n].def.name, wanderingGhosts[(fd+2)%n].def.name, wanderingGhosts[(fd+4)%n].def.name];",
"  const active=[wanderingGhosts[fd%n].def.name, wanderingGhosts[(fd+1)%n].def.name, wanderingGhosts[(fd+2)%n].def.name, wanderingGhosts[(fd+3)%n].def.name, wanderingGhosts[(fd+4)%n].def.name];")

# 2. Extra blood pools + dynamic writings + red pulsing lamps + apparitions (after existing blood pools line)
rep("makeBloodWriting(\"DON'T SLEEP\",3.69,1.8,12,-Math.PI/2); makeBloodWriting('HE IS HERE',55,1.8,-14.69,0); makeBloodPool(36,0,1.0); makeBloodPool(55,0,1.2); makeHandprint(39.69,1.2,0,-Math.PI/2);",
"""makeBloodWriting("DON'T SLEEP",3.69,1.8,12,-Math.PI/2); makeBloodWriting('HE IS HERE',55,1.8,-14.69,0); makeBloodPool(36,0,1.0); makeBloodPool(55,0,1.2); makeHandprint(39.69,1.2,0,-Math.PI/2);
// V15: every floor full of horror - extra pools (repositioned per floor), dynamic writings, pulsing red lamps, ghost apparitions
const extraPools=[]; const extraPoolSlots=[[-24,-16],[24,-16],[-20,12],[20,12],[0,-12],[0,12],[-16,0],[16,0],[48,-10],[62,10],[55,0],[-28,20],[10,-20],[-10,20],[36,0],[65,0],[45,-12],[45,12],[-24,0],[24,0]];
for(let i=0;i<12;i++){ const pm=makeBloodPool(extraPoolSlots[i][0],extraPoolSlots[i][1],1.0+Math.random()*0.5); extraPools.push(pm); }
function makeDynamicWriting(x,y,z,ry){
  const cv=document.createElement('canvas'); cv.width=512; cv.height=128; const ctx=cv.getContext('2d'); const tex=new THREE.CanvasTexture(cv); tex.colorSpace=THREE.SRGBColorSpace;
  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(3,0.75), new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:0.95})); mesh.position.set(x,y,z); mesh.rotation.y=ry; scene.add(mesh);
  mesh.userData.set=(txt)=>{ ctx.clearRect(0,0,512,128); ctx.fillStyle='#8a1010'; ctx.font='bold 64px sans-serif'; ctx.textAlign='center'; ctx.fillText(txt,256,80); tex.needsUpdate=true; };
  return mesh;
}
const dynamicWritings=[makeDynamicWriting(-31.6,1.8,-8,Math.PI/2), makeDynamicWriting(31.6,1.8,-8,-Math.PI/2), makeDynamicWriting(-10,1.8,23.6,Math.PI), makeDynamicWriting(10,1.8,-23.6,0)];
const SCARY_TEXTS=["BEHIND YOU","IT'S COMING","NO ESCAPE","DON'T LOOK","IT SEES YOU","RUN NOW","DEAD END","HE IS HERE","CAN'T HIDE","IT KNOWS"];
const redLamps=[];
for(const [rx,rz] of [[-20,-12],[20,-12],[-20,12],[20,12]]){ const rl=new THREE.Mesh(new THREE.SphereGeometry(0.25,10,10), new THREE.MeshBasicMaterial({color:0xff0000,transparent:true,opacity:0.8})); rl.position.set(rx,3.2,rz); scene.add(rl); redLamps.push(rl); }
const apparitions=[];
for(let i=0;i<8;i++){
  const g=new THREE.Group();
  const body=new THREE.Mesh(new THREE.ConeGeometry(0.6,1.6,12,1,true), new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.45,side:THREE.DoubleSide})); body.position.y=0.8;
  const head=new THREE.Mesh(new THREE.SphereGeometry(0.28,10,10), new THREE.MeshBasicMaterial({color:0xe8e8e8,transparent:true,opacity:0.6})); head.position.y=1.9;
  const e1=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8), new THREE.MeshBasicMaterial({color:0xff0000})); e1.position.set(-0.1,1.95,0.24);
  const e2=e1.clone(); e2.position.x=0.1;
  g.add(body,head,e1,e2); g.position.set(0,0,0); g.visible=false; scene.add(g);
  apparitions.push({mesh:g, timer:3+i*2, visible:false});
}
const apparitionSlots=[[-20,-12],[20,-12],[-20,12],[20,12],[0,-12],[0,12],[-16,0],[16,0],[48,0],[55,-10],[55,10],[36,0]];""")

# 3. Per-floor horror update in applyFloorLayout: pools + writings
rep("  const lc=FLOOR_LIGHTS[fd%5];",
"""  if(typeof extraPools!=='undefined'){ extraPools.forEach((pm,i)=>{ const sl=extraPoolSlots[(fd*3+i*2)%extraPoolSlots.length]; pm.position.x=sl[0]; pm.position.z=sl[1]; }); }
  if(typeof dynamicWritings!=='undefined'){ dynamicWritings.forEach((dw,i)=>{ dw.userData.set(SCARY_TEXTS[(fd+i*3)%SCARY_TEXTS.length]); }); }
  const lc=FLOOR_LIGHTS[fd%5];""")

# 4. Apparitions + red lamps pulse + more frequent twitch + more frequent blackout on lower floors (in update, before final escape block)
rep("  // V14 anti-stuck:",
"""  // V15 apparitions: ghost silhouettes appear/vanish in every room, whisper when near
  for(let ai=0; ai<apparitions.length; ai++){
    const ap=apparitions[ai]; ap.timer-=dt;
    if(ap.timer<=0){
      ap.visible=!ap.visible; ap.timer=ap.visible?3+Math.random()*4:5+Math.random()*8;
      if(ap.visible){ const sl=apparitionSlots[Math.floor(Math.random()*apparitionSlots.length)]; ap.mesh.position.set(sl[0],0,sl[1]); ap.mesh.visible=true; if(Math.hypot(sl[0]-playerPos.x,sl[1]-playerPos.z)<12) whisperSound(); }
      else ap.mesh.visible=false;
    }
    if(ap.visible){ ap.mesh.rotation.y=Math.atan2(playerPos.x-ap.mesh.position.x, playerPos.z-ap.mesh.position.z); ap.mesh.position.y=Math.sin(t*2+ai)*0.1; }
  }
  for(let ri=0; ri<redLamps.length; ri++){ const s=1+Math.sin(t*5+ri*1.7)*0.35; redLamps[ri].scale.set(s,s,s); redLamps[ri].material.opacity=0.5+Math.sin(t*5+ri)*0.3; }
  // V14 anti-stuck:""")
# twitch more often
rep("    if(S.time>nextTwitch){ twitchUntil=S.time+1; nextTwitch=S.time+20+Math.random()*15; whisperSound(); toast('👻 လူသေကောင် လှုပ်သွားသလား…?'); }",
"    if(S.time>nextTwitch){ twitchUntil=S.time+1; nextTwitch=S.time+10+Math.random()*10; whisperSound(); toast('👻 လူသေကောင် လှုပ်သွားသလား…?'); }")
# blackout even more frequent on lower floors: already max(20,35-fd) - make it max(15,28-fd)
rep("S.blackoutTimer=Math.max(20,35-(15-S.floor))+Math.random()*10;",
"S.blackoutTimer=Math.max(15,28-(15-S.floor))+Math.random()*8;")

# 5. Monster detection bigger + chase speed a bit higher on lower floors (in monster AI, detection section)
# Find monster chase speed line: search pattern
import re
m=re.search(r"const mSpeed[^\n]+", t)
print("mSpeed line:", m.group(0) if m else "NOT FOUND")

rep("V14 • Beacon + Auto Fullscreen + ပိုကြောက် + ပို Realistic",
"V15 • Nightmare - အထပ်တိုင်း ကြောက်စရာ ပြည့် + သရဲ ၅+ ကောင်")

open(p,'w',encoding='utf-8').write(t)
print("V15 PATCH OK")
