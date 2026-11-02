import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V70 • GAME FLOW အပြည့် ပြန်ထည့် — အကုန်" in t
t = t.replace("V70 • GAME FLOW အပြည့် ပြန်ထည့် — အကုန်", "V71 • Joystick+ကင်မရာ မြန်အောင် — အကုန်", 1)
# 1. Camera drag 0.005 -> 0.008 rad/px (60% faster turn)
old_cam = "S.yaw-=(e.clientX-lastCamX)*0.005*(S.camSpeed||1)"
assert old_cam in t
t = t.replace(old_cam, "S.yaw-=(e.clientX-lastCamX)*0.008*(S.camSpeed||1)", 1)
# 2. Joystick speed scaling: partial tilt faster, max unchanged (walk 3.4, run 6.0)
old_speed = "const speed=(running?6.0:3.4)*(0.45+0.55*Math.min(1,il));"
assert old_speed in t
t = t.replace(old_speed, "const speed=(running?6.0:3.4)*(0.65+0.35*Math.min(1,il));", 1)
# 3. Velocity lerp faster: dt*10 -> dt*18 (quicker acceleration, less sluggish start)
old_vk = "const vk=Math.min(1,dt*10);"
assert old_vk in t
t = t.replace(old_vk, "const vk=Math.min(1,dt*18);", 1)
p.write_text(t, encoding='utf-8')
print('V71 applied: camera 0.005->0.008, speed scale 0.45+0.55->0.65+0.35, vk dt*10->dt*18')
