import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
old1 = """  let cTx=tx, cTz=tz;
  if(typeof lineBlocked==='function' && lineBlocked(playerPos.x,playerPos.z,tx,tz)){
    const step=compassStep(playerPos.x,playerPos.z,tx,tz);
    if(step){ cTx=step[0]; cTz=step[1]; }
  }"""
new1 = """  let cTx=tx, cTz=tz;
  const step=compassStep(playerPos.x,playerPos.z,tx,tz);
  if(step){ cTx=step[0]; cTz=step[1]; }"""
assert old1 in t, "compass use not found"
t = t.replace(old1, new1, 1)
old2 = "  const step=2, x0=-31, x1=69, z0=-23, z1=23;"
new2 = "  const step=1, x0=-31, x1=69, z0=-23, z1=23;"
assert old2 in t, "step not found"
t = t.replace(old2, new2, 1)
p.write_text(t, encoding='utf-8')
print('V39b applied: compass always BFS, step 1m')
