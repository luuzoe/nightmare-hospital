p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,1)

# Add 2 new real wandering ghosts after Girl Animated def
rep("""    {name:'Ghost Girl Animated', src:'ghost-girl.glb', real:true, scale:1.0, yOffset:0, pos:[24,20], wps:[[24,20],[20,12],[0,0],[24,0]], speed:3.0, radius:10, floatY:0.2, chaseTime:4.5, sound:'scream'},""",
"""    {name:'Ghost Girl Animated', src:'ghost-girl.glb', real:true, scale:1.0, yOffset:0, pos:[24,20], wps:[[24,20],[20,12],[0,0],[24,0]], speed:3.0, radius:10, floatY:0.2, chaseTime:4.5, sound:'scream'},
    {name:'Ghost Pig', src:'ghost-pig.glb', real:true, scale:0.02, yOffset:-0.45, pos:[28,-12], wps:[[28,-12],[20,-12],[0,0],[24,0]], speed:2.8, radius:11, floatY:0.1, chaseTime:5, sound:'growl'},
    {name:'Lethal Ghost Girl', src:'ghost-lethal.glb', real:true, scale:0.02, yOffset:0, pos:[-26,-12], wps:[[-26,-12],[-16,-12],[0,0],[-20,0]], speed:3.2, radius:10, floatY:0.2, chaseTime:4.5, sound:'scream'},""")
# Initial animation for new ghosts
rep("""          const init = def.name==='Ghost Girl Animated' ? 'walk' : (def.name==='Darkness Ghost' ? 'Armature|Stalking 1' : gltf.animations[0].name);""",
"""          const init = def.name==='Ghost Girl Animated' ? 'walk' : def.name==='Darkness Ghost' ? 'Armature|Stalking 1' : def.name==='Ghost Pig' ? 'ghost_pig_reference_skeleton|0200' : def.name==='Lethal Ghost Girl' ? 'ghost_girl_lc_ghost_girl.dmx_skeleton|Skip' : gltf.animations[0].name;""")
# Animation switch for new ghosts
rep("""      if(wg.def.name==='Ghost Girl Animated'){ want = wg.state==='chase' ? 'run' : (wg.state==='scare' ? 'idle_1' : 'walk'); }
      else if(wg.def.name==='Darkness Ghost'){ want = wg.state==='chase' ? 'Armature|Chasing' : 'Armature|Stalking 1'; }""",
"""      if(wg.def.name==='Ghost Girl Animated'){ want = wg.state==='chase' ? 'run' : (wg.state==='scare' ? 'idle_1' : 'walk'); }
      else if(wg.def.name==='Darkness Ghost'){ want = wg.state==='chase' ? 'Armature|Chasing' : 'Armature|Stalking 1'; }
      else if(wg.def.name==='Ghost Pig'){ want = wg.state==='chase' ? 'ghost_pig_reference_skeleton|0500' : (wg.state==='scare' ? 'ghost_pig_reference_skeleton|roar' : 'ghost_pig_reference_skeleton|0200'); }
      else if(wg.def.name==='Lethal Ghost Girl'){ want = wg.state==='scare' ? 'ghost_girl_lc_ghost_girl.dmx_skeleton|idle' : 'ghost_girl_lc_ghost_girl.dmx_skeleton|Skip'; }""")
# Version label
rep("V23 • သရဲအစစ် လမ်းလျောက် — Girl walk/run, Darkness Stalking/Chasing",
"V24 • သရဲအသစ် 2 ကောင် — Ghost Pig + Lethal Ghost Girl (မင်းပို့တဲ့ ဖိုင်)")
open(p,'w',encoding='utf-8').write(t)
print("V24 PATCH OK")
