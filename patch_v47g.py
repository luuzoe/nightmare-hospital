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

# Broken beds: every 3rd room bed is fallen/broken, plus extra broken beds in big rooms
rep("    for(let i=0;i<NORTH_CENTRES.length;i++){ const dc=NORTH_CENTRES[i]; const b=tpl.clone(true); b.position.set(dc+3,0,-22); b.rotation.y=0; b.rotation.z=(i%4===1)?0.18:0; scene.add(b); }\n    for(let i=0;i<SOUTH_CENTRES.length;i++){ const dc=SOUTH_CENTRES[i]; const b=tpl.clone(true); b.position.set(dc-3,0,22); b.rotation.y=Math.PI; b.rotation.z=(i%4===2)?-0.15:0; scene.add(b); }",
    """    for(let i=0;i<NORTH_CENTRES.length;i++){ const dc=NORTH_CENTRES[i]; const b=tpl.clone(true); if(i%3===2){ b.position.set(dc+3,0.35,-22); b.rotation.y=0.5; b.rotation.z=0.7; } else { b.position.set(dc+3,0,-22); b.rotation.y=0; b.rotation.z=(i%4===1)?0.18:0; } scene.add(b); }
    for(let i=0;i<SOUTH_CENTRES.length;i++){ const dc=SOUTH_CENTRES[i]; const b=tpl.clone(true); if(i%3===2){ b.position.set(dc-3,0.35,22); b.rotation.y=Math.PI+0.5; b.rotation.z=-0.7; } else { b.position.set(dc-3,0,22); b.rotation.y=Math.PI; b.rotation.z=(i%4===2)?-0.15:0; } scene.add(b); }
    // V47 extra broken beds, off the door path, in big rooms + landing
    for(const [bx,bz,by] of [[-74,-22,0.4],[74,-22,0.4],[-70,22,0.4],[70,22,0.4],[82,17.5,0.4]]){ const b2=tpl.clone(true); b2.position.set(bx,by,bz); b2.rotation.z=0.8; b2.rotation.y=0.7; scene.add(b2); }""",
    "broken beds v47")
# New real assets + torn cloths, inserted after bed block
rep("""// lockers = hiding spots""",
    """// V47 REAL MEDICAL ASSETS (Google free download, no login): skeleton 1.72m, IV stand, trolley, wheelchair, crash cart, syringe.
{
  const assetLoader=new GLTFLoader();
  function placeAsset(src,scale,yOff,x,y,z,ry,rx){
    assetLoader.load(src, gltf=>{
      const wrap=new THREE.Group(); wrap.position.set(x,y,z); wrap.rotation.y=ry||0;
      const inner=gltf.scene; inner.scale.setScalar(scale); inner.position.y=yOff||0; if(rx) inner.rotation.x=rx;
      wrap.add(inner); scene.add(wrap);
    }, undefined, ()=>{});
  }
  // Skeletons: lying in N4/S4/N10, standing in N1/S10
  placeAsset('skeleton.glb',1.0,0,-32,0.15,-18,0.3,-Math.PI/2);
  placeAsset('skeleton.glb',1.0,0,-32,0.15,18,1.2,-Math.PI/2);
  placeAsset('skeleton.glb',1.0,0,62,0.15,-18,2.0,-Math.PI/2);
  placeAsset('skeleton.glb',1.0,0.11,-74,0,-18,0.8,0);
  placeAsset('skeleton.glb',1.0,0.11,61,0,18,2.5,0);
  // IV stands (model 2.56m tall, scale 0.7 -> 1.79m, base -0.7*0.7=-0.49, so yOff 0.49)
  for(const [ix,iz] of [[-49,-20],[17,-20],[62,-20],[-49,20],[13,20],[58,20]]) placeAsset('iv-stand.glb',0.7,0.49,ix,0,iz,0.4,0);
  // Medical trolleys (base -0.36, yOff 0.36)
  for(const [tx,tz] of [[-45,-20],[19,-20],[-45,20],[15,20],[73,-20],[73,20]]) placeAsset('medical-trolley.glb',1.0,0.36,tx,0,tz,0.3,0);
  // Real wheelchairs (base -0.34, yOff 0.34)
  for(const [wx,wz] of [[-50,0],[50,0],[-47,-22],[43,22]]) placeAsset('wheelchair-real.glb',1.0,0.34,wx,0,wz,0.6,0);
  // Crash carts (base -0.35, yOff 0.35)
  for(const [cx,cz] of [[32,-20],[-17,20],[80,0]]) placeAsset('crash-cart.glb',1.0,0.35,cx,0,cz,0.2,0);
  // Syringes on beds/trolleys, scale 2x for visibility (real syringe 16cm, game-visible 32cm)
  for(const [sx,sy,sz] of [[-44,1.0,-22],[18,1.0,-22],[-44,1.0,22],[14,1.0,22],[73,1.0,-20],[73,1.0,20],[-60,1.0,0],[60,1.0,0]]) placeAsset('syringe.glb',2.0,0,sx,sy,sz,0.5,0);
}
// V47 TORN CLOTHS: dirty torn sheets, floor + hanging, in every room + corridor.
function tornCloth(x,y,z,ry,hanging){
  const shape=new THREE.Shape();
  shape.moveTo(-0.6,0); shape.lineTo(0.6,0); shape.lineTo(0.6,-0.8);
  shape.lineTo(0.3,-0.6); shape.lineTo(0.1,-0.9); shape.lineTo(-0.2,-0.6); shape.lineTo(-0.4,-0.85); shape.lineTo(-0.6,-0.7); shape.lineTo(-0.6,0);
  const geo=new THREE.ShapeGeometry(shape);
  const mat=new THREE.MeshStandardMaterial({color:0xcfc8b8,roughness:1,side:THREE.DoubleSide});
  const m=new THREE.Mesh(geo,mat);
  if(hanging){ m.position.set(x,y,z); m.rotation.y=ry||0; }
  else { m.rotation.x=-Math.PI/2; m.rotation.z=ry||0; m.position.set(x,0.03,z); }
  scene.add(m);
}
for(let i=0;i<NORTH_CENTRES.length;i++){ const dc=NORTH_CENTRES[i]; tornCloth(dc-2,0,-20,0.4,false); tornCloth(dc+4,1.4,-22,0.2,true); }
for(let i=0;i<SOUTH_CENTRES.length;i++){ const dc=SOUTH_CENTRES[i]; tornCloth(dc+2,0,20,1.0,false); tornCloth(dc-4,1.4,22,2.8,true); }
for(const [cx,cz] of [[-60,0],[0,0],[60,0],[-7.5,-10],[82,0]]) tornCloth(cx,0,cz,0.7,false);
// lockers = hiding spots""",
    "real assets + torn cloths v47")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V47 part7 applied')
