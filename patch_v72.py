import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V71 • Joystick+ကင်မရာ မြန်အောင် — အကုန်" in t
t = t.replace("V71 • Joystick+ကင်မရာ မြန်အောင် — အကုန်", "V72 • အဝါရောင် တံခါးဘောင် ဖြုတ် — အကုန်", 1)
# Remove bright yellow (0xffcc00) side posts in addRoomDoor; keep the dark door mesh itself.
old = "  for(const fx of [dc-1.25,dc+1.25]){ const fr=new THREE.Mesh(new THREE.BoxGeometry(0.3,3.2,0.5), new THREE.MeshBasicMaterial({color:0xffcc00})); fr.position.set(fx,1.6,z); scene.add(fr); }\n"
assert old in t, "yellow door posts not found"
t = t.replace(old, "", 1)
p.write_text(t, encoding='utf-8')
print('V72 applied: yellow door posts removed')
