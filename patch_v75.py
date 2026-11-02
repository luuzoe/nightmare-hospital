import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
m = re.search(r"V74[^<]{0,80}", t)
assert m, "V74 label not found"
t = t.replace(m.group(0), "V75 \u2022 \u1000\u103c\u102d\u102f\u1000\u103a \u1001\u1000\u103a \u1014\u103e\u1004\u103a \u2014 \u1001\u1000\u103a\u1001\u1000\u103a", 1)

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:120]}"
    t = t.replace(old, new, 1)

# --- Missions harder: FLOOR_MISSIONS ---
rep("15:{ep:1,type:'keys',label:'သော့',need:3,keys:true},", "15:{ep:1,type:'keys',label:'သော့',need:4,keys:true},")
rep("14:{ep:2,type:'order',label:'ဆေး',need:3},", "14:{ep:2,type:'order',label:'ဆေး',need:4},")
rep("13:{ep:3,type:'switches',label:'Switch',need:3},", "13:{ep:3,type:'switches',label:'Switch',need:4},")
rep("12:{ep:4,type:'survive',label:'ရှင်သန်',need:60,timer:60},", "12:{ep:4,type:'survive',label:'ရှင်သန်',need:90,timer:90},")
rep("11:{ep:5,type:'lockers',label:'Locker',need:5},", "11:{ep:5,type:'lockers',label:'Locker',need:7},")
rep("9:{ep:7,type:'dark',label:'မှောင်ထဲ ပစ္စည်း',need:5},", "9:{ep:7,type:'dark',label:'မှောင်ထဲ ပစ္စည်း',need:7},")
rep("8:{ep:8,type:'timed',label:'အချိန်မီ ပစ္စည်း',need:6,timer:90},", "8:{ep:8,type:'timed',label:'အချိန်မီ ပစ္စည်း',need:7,timer:75},")
rep("7:{ep:9,type:'hide',label:'ပုန်း',need:30},", "7:{ep:9,type:'hide',label:'ပုန်း',need:45},")
rep("6:{ep:10,type:'corpse',label:'လူသေကောင်',need:3},", "6:{ep:10,type:'corpse',label:'လူသေကောင်',need:4},")
rep("5:{ep:11,type:'rooms',label:'အခန်း',need:4},", "5:{ep:11,type:'rooms',label:'အခန်း',need:6},")
rep("4:{ep:12,type:'distance',label:'လမ်းလျှောက်',need:180},", "4:{ep:12,type:'distance',label:'လမ်းလျှောက်',need:240},")
rep("3:{ep:13,type:'darklockers',label:'မှောင် Locker',need:5,dwell:3},", "3:{ep:13,type:'darklockers',label:'မှောင် Locker',need:6,dwell:4},")
rep("2:{ep:14,type:'timedorder',label:'အချိန်မီ အစဉ်',need:8,timer:75},", "2:{ep:14,type:'timedorder',label:'အချိန်မီ အစဉ်',need:9,timer:60},")
rep("1:{ep:15,type:'final',label:'ထွက်ပေါက်',need:8,switch:true},", "1:{ep:15,type:'final',label:'ထွက်ပေါက်',need:10,switch:true},")
rep("KEYS_NEEDED = 3;", "KEYS_NEEDED = 4;")
rep("setObjective('Ep1 • သော့ 3 ချောင်း ရှာပါ');", "setObjective('Ep1 • သော့ 4 ချောင်း ရှာပါ');")

# --- Wandering ghosts: faster chase, longer chase, scarier size ---
rep("{name:'Ghost Woman', src:'ghost-woman.glb', real:true, scale:1.0, yOffset:0.95, pos:[20,12], wps:[[20,12],[16,12],[0,0],[20,0]], speed:2.6, radius:13, floatY:0.1, chaseTime:5, sound:'moan'},",
    "{name:'Ghost Woman', src:'ghost-woman.glb', real:true, scale:1.0, yOffset:0.95, pos:[20,12], wps:[[20,12],[16,12],[0,0],[20,0]], speed:3.4, radius:13, floatY:0.1, chaseTime:8, sound:'moan'},")
rep("{name:'Darkness Ghost', src:'ghost-dark.glb', real:true, scale:0.6, yOffset:0, pos:[-20,20], wps:[[-20,20],[-16,12],[0,0],[-20,0]], speed:2.4, radius:14, floatY:0.3, chaseTime:6, sound:'growl'},",
    "{name:'Darkness Ghost', src:'ghost-dark.glb', real:true, scale:0.6, yOffset:0, pos:[-20,20], wps:[[-20,20],[-16,12],[0,0],[-20,0]], speed:3.2, radius:14, floatY:0.3, chaseTime:9, sound:'growl'},")
rep("speed:3.0, radius:12, floatY:0.2, chaseTime:4.5, sound:'scream'}, // V28:", "speed:3.8, radius:12, floatY:0.2, chaseTime:7, sound:'scream'}, // V28:")
rep("speed:2.5, radius:12, floatY:0.2, chaseTime:5, sound:'moan'},", "speed:3.3, radius:12, floatY:0.2, chaseTime:8, sound:'moan'},")
rep("speed:2.7, radius:12, floatY:0.2, chaseTime:5, sound:'growl'},", "speed:3.5, radius:12, floatY:0.2, chaseTime:8, sound:'growl'},")
rep("speed:2.8, radius:13, floatY:0.1, chaseTime:5, sound:'growl'},", "speed:3.6, radius:13, floatY:0.1, chaseTime:8, sound:'growl'},")
rep("speed:3.2, radius:12, floatY:0.2, chaseTime:4.5, sound:'scream'},", "speed:4.0, radius:12, floatY:0.2, chaseTime:7, sound:'scream'},")
rep("def.scale*1.15", "def.scale*1.25")
# Wandering catch grace 0.5 -> 0.4
rep("if(S.wanderCatchTimer>0.5){", "if(S.wanderCatchTimer>0.4){")

# --- Main monster: catch radius 1.4 -> 1.6, hide breaks easier, searches longer ---
rep("if(monsterState!=='scare' && mDist<1.4 && !S.hidden && S.invuln<=0 && !S.won){", "if(monsterState!=='scare' && mDist<1.6 && !S.hidden && S.invuln<=0 && !S.won){")
rep("if(S.hidden && monsterState==='chase' && mDist<2.5){", "if(S.hidden && monsterState==='chase' && mDist<3.5){")
rep("const loseAfter=(S.hideLocker?5.0:9.0)+(15-S.floor)*0.3;", "const loseAfter=(S.hideLocker?7.0:12.0)+(15-S.floor)*0.3;")

# --- Psychological lure lines in haunt whispers ---
rep("const wl=['👣 အဝေးက ခြေသံ…','နောက်မှာ ရှိနေတယ်…','မလှည့်နဲ့…','မင်းကို ကြည့်နေတယ်…'];",
    "const wl=['👣 အဝေးက ခြေသံ…','နောက်မှာ ရှိနေတယ်…','မလှည့်နဲ့…','မင်းကို ကြည့်နေတယ်…','ဒီမှာလာခဲ့…','ဆေးဒီမှာရှိတယ်… လာယူ…','ကလေးငိုသံ… အဲဒီအခန်းထဲမှာ…','တံခါးနောက်မှာ တစ်ခုခု ရှိတယ်…'];")

# --- Dash bed looks like a real hospital bed (mattress + pillow), not a flat box ---
rep("function dashBed(){ const g=new THREE.Group(); const bed=new THREE.Mesh(new THREE.BoxGeometry(1.9,0.15,0.7), new THREE.MeshStandardMaterial({color:0x3a3a3a})); bed.position.y=0.9; g.add(bed);",
    "function dashBed(){ const g=new THREE.Group(); const bed=new THREE.Mesh(new THREE.BoxGeometry(1.9,0.15,0.7), new THREE.MeshStandardMaterial({color:0x3a3a3a})); bed.position.y=0.9; g.add(bed); const mattress=new THREE.Mesh(new THREE.BoxGeometry(1.8,0.12,0.65), new THREE.MeshStandardMaterial({color:0xd8d8d0})); mattress.position.y=1.02; g.add(mattress); const pillow=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.1,0.55), new THREE.MeshStandardMaterial({color:0xeeeeee})); pillow.position.set(-0.6,1.12,0); g.add(pillow);")

# --- Poltergeist: more beds + IV stands move occasionally (visual only, not always) ---
rep("stretcher(-2,-13,0); stretcher(20,0,1.57);",
    "stretcher(-2,-13,0); stretcher(20,0,1.57); stretcher(-30,-20,0.5); stretcher(50,20,1.2); function polterIV(x,z){ const g=new THREE.Group(); const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,1.9,8), new THREE.MeshStandardMaterial({color:0x888888})); pole.position.y=0.95; const top=new THREE.Mesh(new THREE.BoxGeometry(0.6,0.06,0.06), pole.material); top.position.y=1.9; const bag=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.35,0.08), new THREE.MeshStandardMaterial({color:0xffe0a0})); bag.position.set(0.25,1.7,0); g.add(pole,top,bag); g.position.set(x,0,z); scene.add(g); poltergeistItems.push(g); } polterIV(-20,20); polterIV(30,-20); polterIV(-62,-20); polterIV(62,20);")

p.write_text(t, encoding='utf-8')
print('V75 patch applied')
