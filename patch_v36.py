import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
miss = []
def rep(old, new, name):
    global t
    if old not in t:
        miss.append(name)
        print('MISS:', name)
    else:
        t = t.replace(old, new, 1)
        print('OK:', name)

rep("V35 • HIDE ပုန်းပြီး လမ်းလျှောက် + သရဲမ အသံ ရှား + လက် လှည့် — အကုန်",
    "V36 • အနီ စာ သေး + အပေါ် + Minimap ကြီး — အကုန်",
    "version")
# Floor banner to top, smaller
rep("#floorBanner{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%);font-size:42px;",
    "#floorBanner{position:fixed;left:50%;top:14%;transform:translate(-50%,-50%);font-size:26px;",
    "floor banner top smaller")
# Blood writing: plane smaller, y higher, font smaller
rep("  g.fillStyle='#8a1010'; g.font='bold 72px sans-serif';",
    "  g.fillStyle='#8a1010'; g.font='bold 56px sans-serif';",
    "blood font")
rep("  const m=new THREE.Mesh(new THREE.PlaneGeometry(3,0.75), new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:0.95}));\n  m.position.set(x,y,z); m.rotation.y=ry; scene.add(m);\n}\nmakeBloodWriting('HELP',0,1.8,-2.69,0); makeBloodWriting('RUN',0,1.8,2.69,Math.PI); makeBloodWriting(\"DON'T LOOK BACK\",-3.69,1.8,-12,Math.PI/2);\nmakeBloodWriting(\"DON'T SLEEP\",3.69,1.8,12,-Math.PI/2); makeBloodWriting('HE IS HERE',55,1.8,-14.69,0);",
    "  const m=new THREE.Mesh(new THREE.PlaneGeometry(2,0.5), new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:0.95}));\n  m.position.set(x,2.7,z); m.rotation.y=ry; scene.add(m);\n}\nmakeBloodWriting('HELP',0,1.8,-2.69,0); makeBloodWriting('RUN',0,1.8,2.69,Math.PI); makeBloodWriting(\"DON'T LOOK BACK\",-3.69,1.8,-12,Math.PI/2);\nmakeBloodWriting(\"DON'T SLEEP\",3.69,1.8,12,-Math.PI/2); makeBloodWriting('HE IS HERE',55,1.8,-14.69,0);",
    "blood writing size top")
# Dynamic writing: plane smaller, y higher, font smaller
rep("  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(3,0.75), new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:0.95})); mesh.position.set(x,y,z); mesh.rotation.y=ry; scene.add(mesh);\n  mesh.userData.set=(txt)=>{ ctx.clearRect(0,0,512,128); ctx.fillStyle='#8a1010'; ctx.font='bold 64px sans-serif';",
    "  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(2,0.5), new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:0.95})); mesh.position.set(x,2.7,z); mesh.rotation.y=ry; scene.add(mesh);\n  mesh.userData.set=(txt)=>{ ctx.clearRect(0,0,512,128); ctx.fillStyle='#8a1010'; ctx.font='bold 48px sans-serif';",
    "dynamic writing size top")
# Other blood writings at 918: IT SEES YOU, DON'T TRUST - they use makeBloodWriting, so y will be forced to 2.7 by function, good, no need separate.
# Minimap larger: canvas 150x75 -> 200x100, scale 1.4 -> 1.85, walls brighter, dots larger
rep('<canvas id="minimap" width="150" height="75"',
    '<canvas id="minimap" width="200" height="100"',
    "minimap canvas size")
rep("  const sc=1.4;\n  g.fillStyle='#888888';",
    "  const sc=1.85;\n  g.fillStyle='#cccccc';",
    "minimap scale bright")
rep("    g.arc(Math.max(2,Math.min(cv.width-2,bx)),Math.max(2,Math.min(cv.height-2,by)),3,0,Math.PI*2);",
    "    g.arc(Math.max(2,Math.min(cv.width-2,bx)),Math.max(2,Math.min(cv.height-2,by)),5,0,Math.PI*2);",
    "minimap objective dot")
rep("  g.arc(Math.max(2,Math.min(cv.width-2,px)),Math.max(2,Math.min(cv.height-2,py)),3.5,0,Math.PI*2);",
    "  g.arc(Math.max(2,Math.min(cv.width-2,px)),Math.max(2,Math.min(cv.height-2,py)),5,0,Math.PI*2);",
    "minimap player dot")
rep("  g.lineTo(Math.max(2,Math.min(cv.width-2,px+Math.sin(S.yaw)*10)),Math.max(2,Math.min(cv.height-2,py+Math.cos(S.yaw)*10)));",
    "  g.lineTo(Math.max(2,Math.min(cv.width-2,px+Math.sin(S.yaw)*14)),Math.max(2,Math.min(cv.height-2,py+Math.cos(S.yaw)*14)));",
    "minimap direction line")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V36 patch applied')
