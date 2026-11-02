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

rep("V51 • toast အပေါ်ဆုံး + မှိန် + minimap သေး — အကုန်",
    "V52 • ထပ်တိုင်း မြေပုံ မတူ — အခန်းထဲ အတွင်းနံရံ + corridor နံရံ ထပ်တိုင်း ကွဲ — အကုန်",
    "version v52")
# Layout walls registry, right after doorWalls definition
rep("const doorWalls=[];",
    "const doorWalls=[];\nconst layoutWalls=[]; // V52: per-floor interior walls, rebuilt on every floor start, removed before rebuild",
    "layoutWalls registry v52")
# Build function + hook: insert before applyFloorLayout definition
rep("function applyFloorLayout(){",
    """function buildFloorLayout(){
  // V52: clear previous floor layout walls first (idempotent, no duplicates)
  for(const w of layoutWalls){ if(w.mesh) scene.remove(w.mesh); const ix=walls.indexOf(w); if(ix>=0) walls.splice(ix,1); }
  layoutWalls.length=0;
  // Deterministic seeded RNG per floor (same floor = same layout, every time, incl. Continue)
  let seed=(S.floor*2654435761)>>>0;
  const rng=()=>{ seed=(seed*1664525+1013904223)>>>0; return seed/4294967296; };
  const shuffled=(arr)=>{ const a=arr.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(rng()*(i+1)); const tmp=a[i]; a[i]=a[j]; a[j]=tmp; } return a; };
  const addLayoutWall=(cx,cz,w,d)=>{
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,3.4,d), new THREE.MeshStandardMaterial({map:wallTex,roughness:.95}));
    mesh.position.set(cx,1.7,cz); scene.add(mesh);
    const wall={x:cx,z:cz,w,d,layout:true,mesh}; walls.push(wall); layoutWalls.push(wall);
  };
  // Rooms: north centres with z -17.5, south centres with z 17.5. Door->centre path stays clear by design:
  // H walls are at the FAR side of the room (z -24 / 24, 6.5m beyond centre), V walls are at the SIDE (x dc +/- 4).
  // Keys, switches, items and corpses are at/near room centres, so they are never behind a layout wall.
  const rooms=[];
  for(const dc of NORTH_CENTRES) rooms.push({dc,cz:-17.5,side:'N'});
  for(const dc of SOUTH_CENTRES) rooms.push({dc,cz:17.5,side:'S'});
  const picked=shuffled(rooms);
  const nWalls=5+Math.floor((15-S.floor)/3); // V52: lower floors get more interior walls (5 at Floor 15, up to 9 at Floor 1)
  for(let i=0;i<nWalls && i<picked.length;i++){
    const r=picked[i];
    if(rng()<0.5){
      const off=(rng()-0.5)*3; // +/-1.5m, gaps on both sides stay >= 3m (room 15m, wall 6m)
      addLayoutWall(r.dc+off, r.side==='N'?-24:24, 6, 0.6);
    } else {
      const sideX=r.dc+(rng()<0.5?-4:4);
      addLayoutWall(sideX, r.cz, 0.6, 6);
    }
  }
  // Corridor edge walls: 10m corridor, wall at z +/-4 (3m long) leaves >= 6m clear, never near spawn/hall/monster/switch.
  const corrX=shuffled([-60,-30,10,40,60]);
  for(let i=0;i<2;i++){
    const cx=corrX[i];
    if(Math.abs(cx+7.5)<6 || Math.abs(cx-80)<6 || Math.abs(cx+81)<6) continue;
    addLayoutWall(cx, rng()<0.5?-4:4, 3, 0.6);
  }
}
function applyFloorLayout(){""",
    "buildFloorLayout v52")
# Call build at start of applyFloorLayout (before props move, so minimap/BFS see new walls immediately)
rep("function applyFloorLayout(){\n  const fd=15-S.floor;",
    "function applyFloorLayout(){\n  if(typeof buildFloorLayout==='function') buildFloorLayout(); // V52: new wall layout per floor\n  const fd=15-S.floor;",
    "call buildFloorLayout v52")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V52 applied')
