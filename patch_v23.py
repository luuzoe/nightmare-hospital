p="/home/hatch/workspace/nightmare-hospital/index.html"
t=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global t
    assert old in t, "MISSING "+old[:200]
    t=t.replace(old,new,cnt)

# Real wandering build: store all animation actions, play walk/Stalking initially (not idle)
# This block is unique to wandering real branch (contains 'return {outer,mixer,def,wpIdx' after it)
rep("""      if(def.real && useReal){
        let mixer=null; if(gltf.animations.length){ mixer=new THREE.AnimationMixer(inner); mixer.clipAction(gltf.animations[0]).play(); }
        outer.position.set(def.pos[0],0,def.pos[1]); scene.add(outer);
        return {outer,mixer,def,wpIdx:0,scareTimer:0,chaseTimer:0,cooldown:0,state:'patrol'};
      }""",
"""      if(def.real && useReal){
        let mixer=null, actions={}, curAnim=null;
        if(gltf.animations.length){
          mixer=new THREE.AnimationMixer(inner);
          for(const clip of gltf.animations){ actions[clip.name]=mixer.clipAction(clip); }
          const init = def.name==='Ghost Girl Animated' ? 'walk' : (def.name==='Darkness Ghost' ? 'Armature|Stalking 1' : gltf.animations[0].name);
          if(actions[init]){ actions[init].play(); curAnim=init; }
          else if(gltf.animations[0]){ actions[gltf.animations[0].name].play(); curAnim=gltf.animations[0].name; }
        }
        outer.position.set(def.pos[0],0,def.pos[1]); scene.add(outer);
        return {outer,mixer,def,wpIdx:0,scareTimer:0,chaseTimer:0,cooldown:0,state:'patrol',actions,curAnim};
      }""")
# Update loop: switch animation by state before mixer.update
rep("    if(wg.mixer && wg.outer.visible) wg.mixer.update(dt*0.9);",
"""    if(wg.mixer && wg.outer.visible){
      // V23: walk/run while moving, idle while scare-facing, Chasing while chasing (sent files' real clips)
      let want=null;
      if(wg.def.name==='Ghost Girl Animated'){ want = wg.state==='chase' ? 'run' : (wg.state==='scare' ? 'idle_1' : 'walk'); }
      else if(wg.def.name==='Darkness Ghost'){ want = wg.state==='chase' ? 'Armature|Chasing' : 'Armature|Stalking 1'; }
      if(want && wg.actions && wg.actions[want] && wg.curAnim!==want){ if(wg.curAnim && wg.actions[wg.curAnim]) wg.actions[wg.curAnim].stop(); wg.actions[want].play(); wg.curAnim=want; }
      wg.mixer.update(dt*(wg.state==='chase'?1.4:0.9));
    }""")
# Version label
rep("V22 • သရဲအစစ် ဘဲ — တြိဂံအဖြူ သရဲအတု ဖျောက်, မင်းပို့တဲ့ သရဲဘဲ",
"V23 • သရဲအစစ် လမ်းလျောက် — Girl walk/run, Darkness Stalking/Chasing")
open(p,'w',encoding='utf-8').write(t)
print("V23 PATCH OK")
