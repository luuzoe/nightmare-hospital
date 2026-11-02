import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V80[^<]{0,80}", t)
assert m, "V80 label not found"
t = t.replace(m.group(0), "V81 PLACEHOLDER", 1)

# --- Add 3 new wandering ghost defs, after Lethal, before the closing comment ---
rep("    {name:'Lethal Ghost Girl', src:'ghost-lethal.glb', real:true, scale:0.02, yOffset:0, pos:[-26,-12], wps:[[-26,-12],[-16,-12],[0,0],[-20,0]], speed:4.0, radius:12, floatY:0.2, chaseTime:7, sound:'scream'},",
    """    {name:'Lethal Ghost Girl', src:'ghost-lethal.glb', real:true, scale:0.02, yOffset:0, pos:[-26,-12], wps:[[-26,-12],[-16,-12],[0,0],[-20,0]], speed:4.0, radius:12, floatY:0.2, chaseTime:7, sound:'scream'},
    {name:'Cloth Ghost', src:'cloth-ghost.glb', real:true, scale:0.01, yOffset:1.15, pos:[-30,12], wps:[[-30,12],[-20,12],[0,0],[-30,0]], speed:3.5, radius:13, floatY:0.2, chaseTime:8, sound:'moan'},
    {name:'A-Pose Ghost Woman', src:'ghost-woman-apose.glb', real:true, scale:0.8, yOffset:0.95, pos:[30,-12], wps:[[30,-12],[20,-12],[0,0],[30,0]], speed:3.7, radius:12, floatY:0.2, chaseTime:8, sound:'scream'},
    {name:'Scary Halloween Ghost', src:'scary-halloween-ghost.glb', real:true, scale:0.6, yOffset:1.0, pos:[-40,0], wps:[[-40,0],[-20,0],[0,0],[-40,0]], speed:3.9, radius:13, floatY:0.2, chaseTime:8, sound:'growl'},""")

# --- setActiveGhosts: new 3 always active, old ghosts fill remaining slots ---
rep("""  const shuffled=shuffleArr(wanderingGhosts.slice());
  const pickCount=S.floor>=15?5:(S.floor>=10?6:7); // V47: more ghosts down, all 7 at bottom
  const activeSet=new Set(shuffled.slice(0,pickCount).map(wg=>wg.def.name));
  S.activeGhostCount=activeSet.size;
  S.activeGhostNames=shuffled.slice(0,pickCount).map(wg=>wg.def.name);""",
    """  const newNames=['Cloth Ghost','A-Pose Ghost Woman','Scary Halloween Ghost'];
  const newPresent=wanderingGhosts.filter(wg=>newNames.includes(wg.def.name)).map(wg=>wg.def.name);
  const oldShuffled=shuffleArr(wanderingGhosts.filter(wg=>!newNames.includes(wg.def.name)));
  const pickCount=S.floor>=15?5:(S.floor>=10?6:7); // V47: more ghosts down, all 7 at bottom
  const fillCount=Math.max(0,pickCount-newPresent.length);
  const activeSet=new Set([...newPresent, ...oldShuffled.slice(0,fillCount).map(wg=>wg.def.name)]);
  S.activeGhostCount=activeSet.size;
  S.activeGhostNames=Array.from(activeSet);""")

p.write_text(t, encoding='utf-8')
print('V81 patch applied')
