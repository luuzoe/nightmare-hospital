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

rep("V46 • ဆေးရုံအဟောင်း အသစ်: အခန်း 22 ခန်း 10x20m, တံခါး 2m, လှေကား 4m N5-N6 ကြား, အခန်း 15 ထပ် အပေါ်ဆုံးက စ — အကုန်",
    "V47 • ဆေးရုံအသစ် 15x25m, တံခါး 2.5m, လျှောက်လမ်း 10m, လှေကားအစစ် 3D, Story + ပိုကြောက်စရာ — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • ဆေးရုံအဟောင်း: အခန်း 10x20m, တံခါး 2m, လှေကား 4m, အပေါ်ဆုံး 15 ထပ်က စ</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • စွန့်ပစ်ဆေးရုံ: အခန်း 15x25m, တံခါး 2.5m, လျှောက်လမ်း 10m, လှေကားအစစ်, အပေါ်ဆုံး 15 ထပ်က စ</p>",
    "start hint")
# constants
rep("const NORTH_CENTRES=[-52,-42,-32,-22,-12,2,12,22,32,42,52];\nconst SOUTH_CENTRES=[-52,-42,-32,-22,-12,-2,8,18,28,38,48];\nconst NORTH_BOUNDS=[-57,-47,-37,-27,-17,-7,-3,7,17,27,37,47,57];\nconst SOUTH_BOUNDS=[-57,-47,-37,-27,-17,-7,3,13,23,33,43,53,57];\nconst ROOM_CENTRES=NORTH_CENTRES;",
    "const NORTH_CENTRES=[-77,-62,-47,-32,-17,2,17,32,47,62,77];\nconst SOUTH_CENTRES=[-77,-62,-47,-32,-17,-2,13,28,43,58,73];\nconst NORTH_BOUNDS=[-84.5,-69.5,-54.5,-39.5,-24.5,-9.5,-5.5,9.5,24.5,39.5,54.5,69.5,84.5];\nconst SOUTH_BOUNDS=[-84.5,-69.5,-54.5,-39.5,-24.5,-9.5,5.5,20.5,35.5,50.5,65.5,80.5,84.5];\nconst ROOM_CENTRES=NORTH_CENTRES;",
    "centres bounds v47")
rep("const ROOM_ZONES=[{x:-32,z:-13},{x:32,z:-13},{x:-32,z:13},{x:28,z:13}];",
    "const ROOM_ZONES=[{x:-47,z:-17.5},{x:47,z:-17.5},{x:-47,z:17.5},{x:43,z:17.5}];",
    "room zones v47")
rep("const ITEM_SPAWNS=[[-52,-13],[-42,-13],[-32,-13],[-22,-13],[-12,-13],[2,-13],[12,-13],[22,-13],[32,-13],[42,-13],[52,-13],[-52,13],[-42,13],[-32,13],[-22,13],[-12,13],[-5,0]];",
    "const ITEM_SPAWNS=[[-77,-17.5],[-62,-17.5],[-47,-17.5],[-32,-17.5],[-17,-17.5],[2,-17.5],[17,-17.5],[32,-17.5],[47,-17.5],[62,-17.5],[77,-17.5],[-77,17.5],[-62,17.5],[-47,17.5],[-32,17.5],[-17,17.5],[-7.5,0]];",
    "item spawns v47")
# minimap
rep("  const sc=1.6;", "  const sc=1.1;", "minimap scale v47")
rep("    const x=(w.x-w.w/2+57)*sc;\n    const y=(w.z-w.d/2+23)*sc;", "    const x=(w.x-w.w/2+84.5)*sc;\n    const y=(w.z-w.d/2+30)*sc;", "minimap walls v47")
rep("    const bx=(S.beaconX+57)*sc;\n    const by=(S.beaconZ+23)*sc;", "    const bx=(S.beaconX+84.5)*sc;\n    const by=(S.beaconZ+30)*sc;", "minimap beacon v47")
rep("  const px=(playerPos.x+57)*sc;\n  const py=(playerPos.z+23)*sc;", "  const px=(playerPos.x+84.5)*sc;\n  const py=(playerPos.z+30)*sc;", "minimap player v47")
# floor split + ceiling
rep("const floor=new THREE.Mesh(new THREE.PlaneGeometry(114,46), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9}));\nfloor.rotation.x=-Math.PI/2; floor.position.set(0,0,0); scene.add(floor);",
    """// V47 floor split: leave a real hole over the staircase hall (x -9.5..-5.5, z -30..-5) so steps are visible, not hidden under a flat floor.
function addFloorPlane(w,d,cx,cz){ const f=new THREE.Mesh(new THREE.PlaneGeometry(w,d), new THREE.MeshStandardMaterial({map:floorTex,roughness:.9})); f.rotation.x=-Math.PI/2; f.position.set(cx,0,cz); scene.add(f); return f; }
addFloorPlane(75,25,-47,-17.5); addFloorPlane(90,25,39.5,-17.5); addFloorPlane(169,10,0,0); addFloorPlane(169,25,0,17.5);
const floor=addFloorPlane(1,1,0,0); floor.visible=false;""",
    "floor split v47")
rep("const ceil=new THREE.Mesh(new THREE.PlaneGeometry(114,46), new THREE.MeshStandardMaterial({map:ceilTex,roughness:1}));",
    "const ceil=new THREE.Mesh(new THREE.PlaneGeometry(169,60), new THREE.MeshStandardMaterial({map:ceilTex,roughness:1}));",
    "ceil v47")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part1 applied')
