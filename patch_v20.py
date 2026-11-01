p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# 1. Beacon hidden (key only via compass meters, as user ordered)
rep("beacon.renderOrder=999; beacon.position.set(0,3.5,24); scene.add(beacon);",
"beacon.renderOrder=999; beacon.position.set(0,3.5,24); beacon.visible=false; scene.add(beacon);")
rep("  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.scale.x=beacon.scale.z=1+Math.sin(t*3)*0.2;",
"  S.beaconX=tx; S.beaconZ=tz; beacon.position.set(tx,3.5,tz); beacon.visible=false;")
# 2. Green gap frames hidden: remove all frame creation calls (functions stay unused, no error)
rep("for(const gx of [-16,0,16]){ makeGapFrame(gx,-3,true); makeGapFrame(gx,3,true); }\nmakeGapFrame(-4,0,false); makeGapFrame(4,0,false);",
"// V20 user: green frames hidden - gaps stay as passages, no glowing frames")
rep("makeVGapFrame(-4,-12); makeVGapFrame(4,-12); makeVGapFrame(-4,12); makeVGapFrame(4,12);",
"// V20 user: new-gap green frames hidden")
# 3. Yellow path dots hidden: never compute, hide all dots in update
rep("""  // V18 path dots: recompute every 2s to beacon target
  S.pathTimer-=dt;
  if(S.pathTimer<=0){ S.pathTimer=2.0; try{ computePathDots(S.beaconX,S.beaconZ); }catch(e){} }""",
"""  // V20 user: yellow path hidden - key only via compass meters
  for(const d of pathDots) d.visible=false;""")
# 4. Ghost glow removed: emissive red -> black
rep("if(opts.real){ inner.traverse(o=>{ if(o.isMesh && o.material && o.material.emissive){ o.material.emissive.set(0x440000); } }); }",
"if(opts.real){ inner.traverse(o=>{ if(o.isMesh && o.material && o.material.emissive){ o.material.emissive.set(0x000000); } }); }")
rep("if(def.real && useReal){ inner.traverse(o=>{ if(o.isMesh && o.material && o.material.emissive){ o.material.emissive.set(0x330000); } }); }",
"if(def.real && useReal){ inner.traverse(o=>{ if(o.isMesh && o.material && o.material.emissive){ o.material.emissive.set(0x000000); } }); }")
# 5. Monster glow weaker (was 8 idle / 18 chase, now 2 / 6 - only close/chase slightly red)
rep("const monsterGlow=new THREE.PointLight(0xff0000,6,7,1.5); scene.add(monsterGlow);",
"const monsterGlow=new THREE.PointLight(0xff0000,2,5,1.5); scene.add(monsterGlow);")
rep("monsterGlow.intensity=(S.chase||S.scare)?18:8; // V12 ghost glow stronger",
"monsterGlow.intensity=(S.chase||S.scare)?6:2; // V20 user: no ghost glow, scarier")
# 6. Darker / scarier: hemisphere 0.28 -> 0.15, flashlight 130/22 -> 90/18
rep("scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.28)); // V10 darker",
"scene.add(new THREE.HemisphereLight(0x8899aa,0x111111,0.15)); // V20 darker, scarier")
rep("const flash=new THREE.SpotLight(0xfff2cc,130,22,0.50,0.35,1); // V5 strong narrow flashlight tunnel",
"const flash=new THREE.SpotLight(0xfff2cc,90,18,0.45,0.35,1); // V20 narrower/dimmer, scarier")
# 7. Anti-stuck toast: no beacon reference, compass only
rep("toast('⛔ နံရံ ပိတ်နေသည်! ကင်မရာလှည့်ပြီး အဝါရောင် တိုင် (beacon) ဘက် သွားပါ');",
"toast('⛔ နံရံ ပိတ်နေသည်! ကင်မရာလှည့်ပြီး compass ဘက် သွားပါ');")
# Version label
rep("V19 • Room1 error တွေ ပြင် — အလောင်း/သရဲ ထပ်နေတာ + နံရံ ပေါက်အသစ်",
"V20 • ကြောက်စရာကောင်း — အစိမ်းဘောင် + အဝါလမ်း + သရဲအလင်း ဖျောက်, သော့ကို မီတာနဲ့ဘဲ")
open(p,'w',encoding='utf-8').write(t)
print("V20 PATCH OK")
