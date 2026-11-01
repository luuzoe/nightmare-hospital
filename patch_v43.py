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

rep("V42 • အဖြူ သရဲ emoji ဖြုတ် + ပေါက် frame + Ep1 သရဲ လိုက်တာ လျှော့ — အကုန်",
    "V43 • Ep1 ပြန်လုပ်: သော့ ၃ ချောင်း စတဲ့ အခန်းထဲမှာပဲ + Ep1 သရဲ မလိုက် — အကုန်",
    "version")
rep("  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • အဖြူ သရဲ emoji မရှိတော့</p>",
    "  <p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • Ep1: သော့ အခန်းထဲမှာပဲ, သရဲ မလိုက်</p>",
    "start hint")
# Floor 15 keys redo: all in spawn quadrant (south-west, x -32..-4, z 3..24), no wall crossing
rep("""const keyDefs=[
  {id:1,x:-24,z:-16,room:'Ward',label:'Ward သော့'},
  {id:2,x:24,z:-16,room:'Surgery',label:'Surgery သော့'},
  {id:3,x:20,z:22,room:'Morgue',label:'Morgue သော့'},""",
    """const keyDefs=[
  {id:1,x:-24,z:20,room:'Start',label:'သော့ 1'},
  {id:2,x:-10,z:16,room:'Start',label:'သော့ 2'},
  {id:3,x:-20,z:6,room:'Start',label:'သော့ 3'},""",
    "keys redo")
# Keys bigger and easier to see
rep("  keyMeshes.push({def:k,mesh:grp,taken:false});",
    "  grp.scale.set(1.6,1.6,1.6); keyMeshes.push({def:k,mesh:grp,taken:false});",
    "keys bigger")
# Key interact distance 1.8 -> 3.0, keys only
rep("    if(!km.taken && Math.hypot(km.def.x-playerPos.x,km.def.z-playerPos.z)<1.8){ S.interactTarget={type:'key',km,label:km.def.label}; break; }",
    "    if(!km.taken && Math.hypot(km.def.x-playerPos.x,km.def.z-playerPos.z)<3.0){ S.interactTarget={type:'key',km,label:km.def.label}; break; }",
    "key interact 3m")
# Ep1: monster never chases (canSee false on floor 15)
rep("  const canSee=!S.hidden && monsterState!=='scare' && mDist<(S.floor===15?16:24) && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V42 Ep1: 16m, later floors 24m",
    "  const canSee=!S.hidden && S.floor!==15 && monsterState!=='scare' && mDist<24 && !lineBlocked(monsterPos.x,monsterPos.z,playerPos.x,playerPos.z) && S.invuln<=0; // V43 Ep1: monster never chases, tutorial floor",
    "monster no chase Ep1")
# Ep1: wandering ghosts never start chase
rep("      if(!S.hidden && S.invuln<=0 && (S.escaping || (wd<((wg.def.radius+(wg.def.radiusBoost||0))*(S.floor===15?0.65:1)) && !lineBlocked(wg.outer.position.x,wg.outer.position.z,playerPos.x,playerPos.z)))){",
    "      if(!S.hidden && S.floor!==15 && S.invuln<=0 && (S.escaping || (wd<((wg.def.radius+(wg.def.radiusBoost||0))) && !lineBlocked(wg.outer.position.x,wg.outer.position.z,playerPos.x,playerPos.z)))){",
    "wandering no chase Ep1")
# Ep1: no monster scare teleport, no front jumpscare - find those conditions
# Monster scare: if(!S.paused && monsterState!=='scare' && !S.hidden && S.invuln<=0){ S.nextScare-=dt;
rep("  if(!S.paused && monsterState!=='scare' && monsterState!=='chase' && !S.hidden && S.invuln<=0){",
    "  if(!S.paused && S.floor!==15 && monsterState!=='scare' && monsterState!=='chase' && !S.hidden && S.invuln<=0){",
    "monster scare Ep1")
# Front jumpscare condition
rep("  if(S.playing && !S.paused && !S.hidden && S.invuln<=0){",
    "  if(S.playing && !S.paused && S.floor!==15 && !S.hidden && S.invuln<=0){",
    "front jumpscare Ep1")

if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V43 patch applied')
