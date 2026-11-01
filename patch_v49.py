import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
miss = []
def rep(old, new, name):
    global t
    if old not in t:
        miss.append(name); print('MISS:', name)
    else:
        t = t.replace(old, new, 1); print('OK:', name)

rep("V48 • လှေကားစည်းကမ်း: Mission မပြီးဘဲ အောက်ဆုံးရောက်ရင် သရဲက ဂုတ်ချိုး တခါထဲ သေ — အကုန်",
    "V49 • ဆေးရုံအစုတ် အစစ် + ကြောက်စရာ/စိတ်ခြောက်ခြားစရာ: မီးတင်, 3D အပျက်အစီး, ထပ်နိမ့်လေ ပိုစုတ်, shadow glimpse, hunt — အကုန်",
    "version v49")
# Lighting: abandoned details must be visible, not pitch black
rep("scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.03)); // V20 darker, scarier",
    "scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.12)); // V49: dim moonlight, abandoned shapes visible, still dark",
    "hemi v49")
rep("const dir=new THREE.DirectionalLight(0xffe0b3,0.02);",
    "const dir=new THREE.DirectionalLight(0xffe0b3,0.08);",
    "dir v49")
rep("  if(scene.fog) scene.fog.density=0.10+(15-S.floor)*0.005+((fm.type==='dark'||fm.type==='darklockers')?0.04:0);",
    "  if(scene.fog) scene.fog.density=0.07+(15-S.floor)*0.005+((fm.type==='dark'||fm.type==='darklockers')?0.04:0); // V49: less fog, rooms visible\n  if(typeof decayGroup2!=='undefined'){ decayGroup2.visible=S.floor<=10; decayGroup3.visible=S.floor<=5; } // V49: lower floors more ruined",
    "fog + decay visibility v49")
# Textures: brick + peeling plaster + mold, broken tiles
m = re.search(r"const floorTex=makeTex\(\(g,s\)=>\{.*?\},8,6\);", t, re.S)
if not m: miss.append("floorTex regex")
else:
    new_floor = """const floorTex=makeTex((g,s)=>{
  g.fillStyle='#2a2724'; g.fillRect(0,0,s,s);
  for(let y=0;y<4;y++)for(let x=0;x<4;x++){
    const missing=Math.random()<0.18;
    if(missing){ g.fillStyle='#141210'; g.fillRect(x*64+2,y*64+2,60,60); }
    else { g.fillStyle=(x+y)%2?'#35312d':'#2a2724'; g.fillRect(x*64+2,y*64+2,60,60); g.fillStyle='rgba(0,0,0,.35)'; g.fillRect(x*64+2,y*64+2,60,4); }
    g.fillStyle='rgba(0,0,0,.25)'; for(let i=0;i<10;i++)g.fillRect(Math.random()*256,Math.random()*256,4,3);
  }
  g.fillStyle='rgba(120,20,20,.35)'; g.beginPath(); g.ellipse(180,90,28,12,0.5,0,7); g.fill(); g.beginPath(); g.ellipse(60,180,22,10,0.2,0,7); g.fill();
  g.fillStyle='rgba(20,30,20,.4)'; for(let i=0;i<10;i++){ g.beginPath(); g.ellipse(Math.random()*256,Math.random()*256,12+Math.random()*18,8+Math.random()*10,0,0,7); g.fill(); }
  g.strokeStyle='rgba(0,0,0,.6)'; g.lineWidth=2; g.beginPath(); g.moveTo(0,100); g.lineTo(80,120); g.lineTo(140,100); g.lineTo(256,140); g.stroke(); g.beginPath(); g.moveTo(200,0); g.lineTo(190,90); g.lineTo(220,180); g.stroke();
},8,6);"""
    t = t[:m.start()] + new_floor + t[m.end():]; print('OK: floorTex v49')
m = re.search(r"const wallTex=makeTex\(\(g,s\)=>\{.*?\},6,2\);", t, re.S)
if not m: miss.append("wallTex regex")
else:
    new_wall = """const wallTex=makeTex((g,s)=>{
  g.fillStyle='#5a5a52'; g.fillRect(0,0,s,s);
  // exposed brick where plaster peeled off (abandoned look, not flat panels)
  for(let by=0;by<4;by++)for(let bx=0;bx<8;bx++){
    if(Math.random()<0.35){ g.fillStyle='#7a4a3a'; g.fillRect(bx*32+1,by*64+1,30,30); g.fillStyle='#3a3a3a'; g.fillRect(bx*32+1,by*64+31,30,2); }
  }
  for(let y=0;y<4;y++){ g.fillStyle=y<2?'#6e7266':'#4e524a'; if(Math.random()<0.6) g.fillRect(0,y*64,s,62); g.fillStyle='#383b36'; g.fillRect(0,y*64,s,2); }
  // large peeling plaster flakes (light)
  g.fillStyle='rgba(200,190,170,.35)'; for(let i=0;i<16;i++){ g.beginPath(); g.ellipse(Math.random()*256,Math.random()*256,10+Math.random()*20,6+Math.random()*12,0,0,7); g.fill(); }
  // mold / damp blotches (dark green-black)
  g.fillStyle='rgba(20,35,20,.5)'; for(let i=0;i<14;i++){ g.beginPath(); g.ellipse(Math.random()*256,120+Math.random()*130,12+Math.random()*22,10+Math.random()*16,0,0,7); g.fill(); }
  g.fillStyle='rgba(40,30,20,.35)'; for(let i=0;i<30;i++)g.fillRect(Math.random()*256,120+Math.random()*130,6,14);
  g.fillStyle='rgba(120,20,20,.4)'; g.fillRect(40,150,30,50);
  g.strokeStyle='rgba(20,20,20,.6)'; g.lineWidth=2; g.beginPath(); g.moveTo(20,0); g.lineTo(40,80); g.lineTo(30,160); g.lineTo(50,256); g.stroke();
  g.fillStyle='rgba(90,70,40,.3)'; for(let i=0;i<10;i++){ g.fillRect(100+Math.random()*80,0,4,120+Math.random()*100); }
},6,2);"""
    t = t[:m.start()] + new_wall + t[m.end():]; print('OK: wallTex v49')
# Scare frequency: V47 quiet was too rare, V49 brings real scares back more often (still quieter than original)
rep("  if(S.playing && !S.paused){ S.moanTimer-=dt; if(S.moanTimer<=0){ moanSound(); S.moanTimer=120+Math.random()*60; } } // V47 quiet: moan every 2-3 min, silence is scarier",
    "  if(S.playing && !S.paused){ S.moanTimer-=dt; if(S.moanTimer<=0){ moanSound(); S.moanTimer=90+Math.random()*30; } } // V49: moan every 90-120s, dread without noise",
    "moan v49")
rep("      S.frontScareTimer=90+Math.random()*60; // V47 quiet: front scare rarer, but loud when it happens",
    "      S.frontScareTimer=60+Math.random()*30; // V49: front scare every 60-90s",
    "front scare v49")
rep("    if(S.randScareTimer<=0){ S.randScareTimer=120+Math.random()*60; if(Math.random()<0.3) screamSound(); else moanSound(); } // V47 quiet random",
    "    if(S.randScareTimer<=0){ S.randScareTimer=90+Math.random()*30; if(Math.random()<0.3) screamSound(); else moanSound(); } // V49 rand scare",
    "rand scare v49")
rep("  let mSpeed=3.2+S.keys*0.2, target=null;",
    "  let mSpeed=3.8+S.keys*0.2, target=null; // V49: patrol faster, monster feels present",
    "patrol speed v49")
# Reset timers
rep("S.neckSnap=false; S._neckSnap=false; S._hallWarn2=false; S.yaw=Math.PI/2;",
    "S.neckSnap=false; S._neckSnap=false; S._hallWarn2=false; S.glimpseTimer=60; S.glimpseUntil=0; S.huntTimer=150; S.yaw=Math.PI/2;",
    "reset timers v49")
# Ruined props + shadow figure, inserted before lockers
rep("// lockers = hiding spots",
    """// V49 RUINED HOSPITAL 3D: visual only, never on a door path (doors at room centres, corridor centre z=0 kept clear).
const decayGroup2=new THREE.Group(); const decayGroup3=new THREE.Group(); scene.add(decayGroup2); scene.add(decayGroup3);
function ruinBox(w,h,d,x,y,z,ry,rz,mat,grp){ const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), mat||new THREE.MeshStandardMaterial({color:0x3a3a35,roughness:1})); m.position.set(x,y,z); m.rotation.y=ry||0; if(rz) m.rotation.z=rz; (grp||scene).add(m); return m; }
function ruinPipe(x,y,z,len,ry){ const m=new THREE.Mesh(new THREE.CylinderGeometry(0.09,0.09,len,8), new THREE.MeshStandardMaterial({color:0x6a3a2a,roughness:.8,metalness:.3})); m.rotation.z=Math.PI/2; m.rotation.y=ry||0; m.position.set(x,y,z); scene.add(m); }
function ruinWire(x,z){ const m=new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.02,1.2,6), new THREE.MeshBasicMaterial({color:0x111111})); m.position.set(x,2.8,z); scene.add(m); }
function ruinDebris(x,z,grp,scale){ const s=scale||1; for(let i=0;i<6;i++){ const m=new THREE.Mesh(new THREE.BoxGeometry((0.3+Math.random()*0.5)*s,(0.15+Math.random()*0.3)*s,(0.3+Math.random()*0.5)*s), new THREE.MeshStandardMaterial({color:0x4a4a44,roughness:1})); m.position.set(x+(Math.random()-0.5)*1.5,0.15,z+(Math.random()-0.5)*1.5); m.rotation.y=Math.random()*3; (grp||scene).add(m); } }
function ruinPuddle(x,z){ const m=new THREE.Mesh(new THREE.PlaneGeometry(2.2,1.4), new THREE.MeshStandardMaterial({color:0x1a2a2a,roughness:0.05,transparent:true,opacity:0.65})); m.rotation.x=-Math.PI/2; m.position.set(x,0.02,z); scene.add(m); }
function ruinMold(x,y,z,ry,grp){ const m=new THREE.Mesh(new THREE.PlaneGeometry(2.5,1.8), new THREE.MeshBasicMaterial({color:0x16281a,transparent:true,opacity:0.7})); m.position.set(x,y,z); m.rotation.y=ry||0; (grp||scene).add(m); }
// corridor: pipes along ceiling, hanging wires, debris at edges (z=+-4.2, not centre), puddles at edges
for(const px of [-70,-40,-10,20,50,75]) ruinPipe(px,3.15,4.2,18,0);
for(const [wx,wz] of [[-60,4.2],[-20,-4.2],[20,4.2],[60,-4.2],[-7.5,-4.2]]) ruinWire(wx,wz);
for(const [dx,dz] of [[-70,4.2],[-30,-4.2],[10,4.2],[40,-4.2],[70,4.2]]) ruinDebris(dx,dz,null,1);
for(const [px,pz] of [[-50,4.2],[0,-4.2],[50,4.2]]) ruinPuddle(px,pz);
// rooms: fallen beams, mattresses on floor, broken doors leaning, mold on far walls (corners, off door path)
for(let i=0;i<NORTH_CENTRES.length;i++){ const dc=NORTH_CENTRES[i]; ruinBox(5,0.25,0.25,dc-4,0.3,-24,0.4,0.2); ruinDebris(dc+4,-24,null,1); ruinMold(dc,2,-29.6,0); const mat=ruinBox(1.8,0.15,0.9,dc-4,0.1,-20,0.3,0); }
for(let i=0;i<SOUTH_CENTRES.length;i++){ const dc=SOUTH_CENTRES[i]; ruinBox(5,0.25,0.25,dc+4,0.3,24,-0.4,-0.2); ruinDebris(dc-4,24,null,1); ruinMold(dc,2,29.6,Math.PI); }
// decay layer 2 (floors 10 and below): more debris, more mold, fallen ceiling chunks
for(const [dx,dz] of [[-60,-20],[0,-20],[60,-20],[-60,20],[0,20],[60,20]]) ruinDebris(dx,dz,decayGroup2,1.5);
for(const dc of NORTH_CENTRES) ruinMold(dc-3,1.8,-29.6,0,decayGroup2);
for(const dc of SOUTH_CENTRES) ruinMold(dc+3,1.8,29.6,Math.PI,decayGroup2);
// decay layer 3 (floors 5 and below): heaviest ruin, collapsed chunks in corridor edges
for(const [dx,dz] of [[-70,-4.2],[-30,4.2],[10,-4.2],[50,4.2]]) ruinDebris(dx,dz,decayGroup3,2);
for(const [cx,cz] of [[-40,0],[40,0]]) { const ch=ruinBox(3,0.4,2,cx,0.2,cz,0.5,0.15,new THREE.MeshStandardMaterial({color:0x2a2a26,roughness:1}),decayGroup3); }
// V49 SHADOW FIGURE: a dark silhouette that appears far away for a few seconds, then vanishes. No chase, no catch — pure dread.
const shadowFigure=new THREE.Group();
{ const body=new THREE.Mesh(new THREE.CapsuleGeometry(0.35,1.1,4,8), new THREE.MeshBasicMaterial({color:0x000000})); body.position.y=0.9; const head=new THREE.Mesh(new THREE.SphereGeometry(0.28,10,10), new THREE.MeshBasicMaterial({color:0x000000})); head.position.y=1.85; shadowFigure.add(body,head); shadowFigure.visible=false; scene.add(shadowFigure); }
// lockers = hiding spots""",
    "ruined props + shadow v49")
# Hunt + glimpse logic, inserted after randScare block
rep("    if(S.randScareTimer<=0){ S.randScareTimer=90+Math.random()*30; if(Math.random()<0.3) screamSound(); else moanSound(); } // V49 rand scare",
    """    if(S.randScareTimer<=0){ S.randScareTimer=90+Math.random()*30; if(Math.random()<0.3) screamSound(); else moanSound(); } // V49 rand scare
    // V49 HAUNTING: shadow glimpse (far, brief, no chase) + periodic hunt (monster knows where you are for a while)
    if(S.playing && !S.paused && !S.chase && !S.escaping && (S.floor!==15 || S.keys>=1)){
      if(typeof S.glimpseTimer!=='number') S.glimpseTimer=60;
      S.glimpseTimer-=dt;
      if(S.glimpseTimer<=0){
        S.glimpseTimer=60+Math.random()*60;
        const farPts=[[-77,-17.5],[77,-17.5],[-77,17.5],[73,17.5],[-81,0],[80,0],[-47,-17.5],[47,-17.5]];
        const fp=farPts[Math.floor(Math.random()*farPts.length)];
        if(Math.hypot(fp[0]-playerPos.x,fp[1]-playerPos.z)>15){ shadowFigure.position.set(fp[0],0,fp[1]); shadowFigure.visible=true; S.glimpseUntil=S.time+2.5; whisperSound(); toast('👤 တစ်စုံတစ်ခု ဖြတ်သွားတယ်…'); }
      }
      if(S.glimpseUntil && S.time>S.glimpseUntil){ shadowFigure.visible=false; S.glimpseUntil=0; }
      if(typeof S.huntTimer!=='number') S.huntTimer=150;
      S.huntTimer-=dt;
      if(S.huntTimer<=0){
        S.huntTimer=180+Math.random()*60;
        monsterState='chase'; S.chase=true; lastSeen=playerPos.clone(); screamSound(); if(navigator.vibrate) navigator.vibrate(200); toast('🚨 သရဲက မင်းကို လိုက်နေပြီ! ပုန်းပါ!');
      }
    }""",
    "hunt + glimpse v49")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V49 applied')
