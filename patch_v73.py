import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V72" in t
# Version label: replace V72 line generically (first occurrence of V72 label)
import re
m = re.search(r"V72[^<]{0,80}", t)
assert m, "V72 label not found"
t = t.replace(m.group(0), "V73 • ပိုကြောက်အောင် + အစုတ်အပြက် အခန်း — အကုန်", 1)

def rep(old, new, count=1):
    global t
    assert old in t, f"NOT FOUND: {old[:90]}"
    t = t.replace(old, new, count)

# --- 1. Scarier timers ---
rep("S.huntTimer=90;", "S.huntTimer=60;")
rep("S.huntTimer=120+Math.random()*60;", "S.huntTimer=80+Math.random()*40;")
rep("S.hauntTimer=45;", "S.hauntTimer=25;")
rep("S.hauntTimer=45+Math.random()*45;", "S.hauntTimer=25+Math.random()*25;")
rep("S.frontScareTimer=50; S.randScareTimer=50;", "S.frontScareTimer=35; S.randScareTimer=35;")
rep("S.nextScare=15;", "S.nextScare=12;")
rep("S.nextScare=Math.max(6,15-floorDown);", "S.nextScare=Math.max(5,12-floorDown);")
rep("S.blackoutTimer=30;", "S.blackoutTimer=20;")
rep("S.blackout=4.0; S.blackoutTimer=Math.max(12,22-(15-S.floor))+Math.random()*6;", "S.blackout=6.0; S.blackoutTimer=Math.max(10,18-(15-S.floor))+Math.random()*6;")
# --- 2. Darker fog and lights ---
rep("scene.fog=new THREE.FogExp2(0x020202,0.09);", "scene.fog=new THREE.FogExp2(0x020202,0.11);")
rep("scene.fog.density=0.07+(15-S.floor)*0.005+", "scene.fog.density=0.085+(15-S.floor)*0.005+")
rep("new THREE.HemisphereLight(0x8899aa,0x111111,0.12)", "new THREE.HemisphereLight(0x8899aa,0x111111,0.08)")
# --- 3. Heartbeat, vignette, growl, whisper closer and stronger ---
rep("const danger=(mDist<10 && !S.hidden) || (S.hidden && mDist<5);", "const danger=(mDist<15 && !S.hidden) || (S.hidden && mDist<8);")
rep("bs.style.opacity=(S.chase||danger)?0.55:0;", "bs.style.opacity=(S.chase||danger)?0.7:0;")
rep("if(mDist<12 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>20){", "if(mDist<16 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>15){")
rep("if(mDist<6 && !S.hidden && monsterState!=='scare'){ whisperAcc+=dt; if(whisperAcc>25){", "if(mDist<9 && !S.hidden && monsterState!=='scare'){ whisperAcc+=dt; if(whisperAcc>18){")
# --- 4. Monster faster and sees farther ---
rep("let mSpeed=4.2+S.keys*0.2,", "let mSpeed=4.7+S.keys*0.2,")
rep("mSpeed=7.2+(S.floor===15?S.keys*0.2:S.items*0.05)+(15-S.floor)*0.2;", "mSpeed=7.7+(S.floor===15?S.keys*0.2:S.items*0.05)+(15-S.floor)*0.2;")
rep("if(mSpeed>9.2) mSpeed=9.2;", "if(mSpeed>9.7) mSpeed=9.7;")
# detection 28 -> 32, only mDist forms
assert t.count("mDist<28") >= 1
t = t.replace("mDist<28", "mDist<32")
assert t.count("mDist>28") >= 1
t = t.replace("mDist>28", "mDist>32")
# --- 5. Wandering ghosts 15 percent bigger, scarier presence ---
rep("normalizeGroup(inner,def.scale,def.yOffset||0,def.rotX||0);", "normalizeGroup(inner,def.scale*1.15,def.yOffset||0,def.rotX||0);")
# --- 6. Haunt whispers: psychological lines, random choice ---
import re as _re
_pat = _re.compile(r"if\(ht<0\.35\)\{ footstepSound\(\); whisperSound\(\); toast\('[^']*'\); \}")
assert _pat.search(t), "haunt footstep line not found"
_new_haunt = "if(ht<0.35){ footstepSound(); whisperSound(); const wl=['👣 အဝေးက ခြေသံ…','နောက်မှာ ရှိနေတယ်…','မလှည့်နဲ့…','မင်းကို ကြည့်နေတယ်…']; toast(wl[Math.floor(Math.random()*wl.length)]); }"
t = _pat.sub(_new_haunt, t, count=1)

# --- 7. Abandoned props + ghost dash items, inserted after stretcher(20,0,1.57); ---
anchor = "stretcher(20,0,1.57);"
assert anchor in t
insert = anchor + """
// V73 abandoned hospital: broken furniture and debris, visual only, no collision
function brokenChair(x,z,ry){ const g=new THREE.Group(); const seat=new THREE.Mesh(new THREE.BoxGeometry(0.55,0.08,0.55), new THREE.MeshStandardMaterial({color:0x1a1a1a})); seat.position.y=0.25; const back=new THREE.Mesh(new THREE.BoxGeometry(0.55,0.6,0.08), seat.material); back.position.set(0,0.5,-0.25); g.add(seat,back); g.position.set(x,0.12,z); g.rotation.set(0,ry,1.35); scene.add(g); }
brokenChair(-70,-22,0.4); brokenChair(-30,22,2.1); brokenChair(55,22,1.2); brokenChair(20,-22,0.9);
function debrisPile(x,z){ const g=new THREE.Group(); for(let di=0; di<5; di++){ const d=new THREE.Mesh(new THREE.BoxGeometry(0.4+Math.random()*0.5,0.12,0.3+Math.random()*0.4), new THREE.MeshStandardMaterial({color:0x2a2520})); d.position.set((Math.random()-0.5)*1.6,0.06,(Math.random()-0.5)*1.6); d.rotation.y=Math.random()*3; g.add(d); } g.position.set(x,0,z); scene.add(g); }
debrisPile(-62,-20); debrisPile(-17,20); debrisPile(47,-20); debrisPile(0,0); debrisPile(62,20); debrisPile(-77,20);
function dirtStain(x,z,r){ const d=new THREE.Mesh(new THREE.CircleGeometry(r,16), new THREE.MeshBasicMaterial({color:0x1a1208,transparent:true,opacity:0.55})); d.rotation.x=-Math.PI/2; d.position.set(x,0.02,z); scene.add(d); }
dirtStain(-47,-16,2.2); dirtStain(-17,16,2.2); dirtStain(47,-16,2.2); dirtStain(0,0,3.0); dirtStain(-62,17,1.8);
// V73 ghost dash: a bed and a chair that zip across in front of the player, visual only
function dashBed(){ const g=new THREE.Group(); const bed=new THREE.Mesh(new THREE.BoxGeometry(1.9,0.15,0.7), new THREE.MeshStandardMaterial({color:0x3a3a3a})); bed.position.y=0.9; g.add(bed); for(const px of [-0.8,0.8]){ for(const pz of [-0.3,0.3]){ const leg=new THREE.Mesh(new THREE.BoxGeometry(0.08,0.9,0.08), bed.material); leg.position.set(px,0.45,pz); g.add(leg); } } g.visible=false; scene.add(g); return g; }
function dashChair(){ const g=new THREE.Group(); const seat=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.1,0.6), new THREE.MeshStandardMaterial({color:0x222222})); seat.position.y=0.5; const back=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.7,0.1), seat.material); back.position.set(0,0.9,-0.3); g.add(seat,back); g.visible=false; scene.add(g); return g; }
const dashItems=[dashBed(),dashChair()]; let dashTimer=40+Math.random()*30, dashAnim=null;
"""
t = t.replace(anchor, insert, 1)

# --- 8. Ghost dash update, inserted before whisperTimer block ---
anchor2 = "if(S.playing && !S.paused){ S.whisperTimer-=dt;"
assert anchor2 in t
dash_update = """if(S.playing && !S.paused){
  if(dashAnim){
    dashAnim.t+=dt; const k=Math.min(1,dashAnim.t/dashAnim.dur);
    dashAnim.item.position.x=dashAnim.fx+(dashAnim.tx-dashAnim.fx)*k;
    dashAnim.item.position.z=dashAnim.fz+(dashAnim.tz-dashAnim.fz)*k;
    if(k>=1){ dashAnim.item.visible=false; dashAnim=null; }
  } else {
    dashTimer-=dt;
    if(dashTimer<=0){
      dashTimer=45+Math.random()*35;
      const it=dashItems[Math.floor(Math.random()*dashItems.length)];
      const fx=playerPos.x+Math.sin(S.yaw)*7, fz=playerPos.z+Math.cos(S.yaw)*7;
      const px=Math.cos(S.yaw), pz=-Math.sin(S.yaw);
      const sx=Math.max(-80,Math.min(80,fx+px*10)), sz=Math.max(-26,Math.min(26,fz+pz*10));
      const ex=Math.max(-80,Math.min(80,fx-px*10)), ez=Math.max(-26,Math.min(26,fz-pz*10));
      it.position.set(sx,0,sz); it.rotation.y=Math.atan2(ex-sx,ez-sz); it.visible=true;
      dashAnim={item:it,fx:sx,fz:sz,tx:ex,tz:ez,t:0,dur:1.4};
      try{ whisperSound(); }catch(e){}
    }
  }
}
"""
t = t.replace(anchor2, dash_update + anchor2, 1)

p.write_text(t, encoding='utf-8')
print('V73 patch applied')
