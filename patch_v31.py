p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:250]
    t=t.replace(old,new,1)

# V31: lights off - hemisphere + directional almost off
rep("scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.15));",
    "scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.03));")
rep("const dir=new THREE.DirectionalLight(0xffe0b3,0.10);",
    "const dir=new THREE.DirectionalLight(0xffe0b3,0.02);")
# Warm ceiling point lights: initial intensity 12 -> 0 (off, update loop below also forces 0)
rep("  const p=new THREE.PointLight(0xffd9a0,12,16,1.8); p.position.set(x,3.2,z); scene.add(p); lights.push(p);\n  const bulb=new THREE.Mesh(new THREE.SphereGeometry(0.18,8,8), new THREE.MeshBasicMaterial({color:0xffe0a0}));",
    "  const p=new THREE.PointLight(0xffd9a0,0,16,1.8); p.position.set(x,3.2,z); scene.add(p); lights.push(p);\n  const bulb=new THREE.Mesh(new THREE.SphereGeometry(0.18,8,8), new THREE.MeshBasicMaterial({color:0x664422}));")
# Update loop: warm lights (first 5) always off, red lights (rest) dim flicker only
old_lights="  lights.forEach((L,i)=>{ if(S.blackout>0){ L.intensity=0; } else if(S.scare||S.chase||wanderingScare){ L.intensity=Math.random()<(S.scare?0.4:0.3)?0:14; } else { L.intensity=7+Math.sin(t*13+i*2)*2+(Math.random()<0.08?-6:0); } });"
new_lights="  lights.forEach((L,i)=>{ if(i<5){ L.intensity=0; } else { L.intensity = S.blackout>0 ? 0 : 2+Math.sin(t*10+i)*1; } });"
rep(old_lights,new_lights)
# Lamps (bright panels) -> dim off panels
rep("const lamp=new THREE.Mesh(new THREE.BoxGeometry(1.4,0.12,0.7), new THREE.MeshBasicMaterial({color:0xfff2cc}));",
    "const lamp=new THREE.Mesh(new THREE.BoxGeometry(1.4,0.12,0.7), new THREE.MeshBasicMaterial({color:0x333322}));")
# Emergency light separate -> dim
rep("const emergencyLight=new THREE.PointLight(0xff0000,5,20,1.5);",
    "const emergencyLight=new THREE.PointLight(0xff0000,2,20,1.5);")
# New small ceiling bulbs grid, hanging with wire, dim warm, visual only (no light)
old_bulb_block="""// V12 red emergency lights (flicker + blackout with other lights)"""
new_bulb_block="""// V31 small ceiling bulbs everywhere, hanging with wire, dim warm dots in the dark (visual only, no light)
{
  const bulbGeo=new THREE.SphereGeometry(0.12,8,8);
  const bulbMat=new THREE.MeshBasicMaterial({color:0x886644});
  const wireGeo=new THREE.CylinderGeometry(0.02,0.02,0.4,6);
  const wireMat=new THREE.MeshBasicMaterial({color:0x222222});
  const bulbPositions=[];
  for(let bx=-28; bx<=28; bx+=8){ for(let bz=-20; bz<=20; bz+=8){ bulbPositions.push([bx,bz]); } }
  for(let bx=44; bx<=68; bx+=8){ for(let bz=-12; bz<=12; bz+=12){ bulbPositions.push([bx,bz]); } }
  for(const [bx,bz] of bulbPositions){
    const b=new THREE.Mesh(bulbGeo,bulbMat); b.position.set(bx,3.2,bz); scene.add(b);
    const w=new THREE.Mesh(wireGeo,wireMat); w.position.set(bx,3.45,bz); scene.add(w);
  }
}
// V12 red emergency lights (flicker + blackout with other lights)"""
rep(old_bulb_block,new_bulb_block)
# Version label
rep("V30 • ခြေထောက် ကြီး ပြင် — သရဲ နံရံနဲ့ ဝေးဝေး + အကျယ် သရဲ သေးအောင်",
    "V31 • အမိုး မီးသီးလုံး + မီးဖျက် — ဆေးရုံ မှောင်, ဓာတ်မီး + အနီရောင် ဘဲ")
open(p,'w',encoding='utf-8').write(t)
print("V31 PATCH OK")
