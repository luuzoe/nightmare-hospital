import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V84[^<]{0,80}", t)
assert m, "V84 label not found"
t = t.replace(m.group(0), "V85 PLACEHOLDER", 1)

# Scary footsteps: deep hospital-floor thud + a quiet floorboard creak
# + an echo (empty building), and every 10th step a faint extra step
# 350ms later, as if something else is walking behind the player.
rep("function footstepSound(){ playNoise(0.15,'lowpass',500,1,0.35,0); }",
    "function footstepSound(){ playNoise(0.18,'lowpass',220,1,0.30,0); playTone(900,250,0.22,'sawtooth',0.06,8); setTimeout(()=>{ try{ playNoise(0.12,'lowpass',300,1,0.12,0); }catch(e){} },140); S._footCount=(S._footCount||0)+1; if(S._footCount%10===0){ setTimeout(()=>{ try{ playNoise(0.15,'lowpass',200,1,0.15,0); }catch(e){} },350); } }")

p.write_text(t, encoding='utf-8')
print('V85 patch applied')
