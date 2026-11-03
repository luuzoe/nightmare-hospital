import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V83[^<]{0,80}", t)
assert m, "V83 label not found"
t = t.replace(m.group(0), "V84 PLACEHOLDER", 1)

# Footsteps were almost inaudible on a phone speaker: 0.09s, 300Hz
# lowpass, volume 0.12, every 2.4m of travel. Make them clearly audible
# without rivalling the ghost sounds (moan 0.6, growl 0.8).
rep("function footstepSound(){ playNoise(0.09,'lowpass',300,1,0.12,0); }",
    "function footstepSound(){ playNoise(0.15,'lowpass',500,1,0.35,0); }")
rep("if(moving){ stepAcc+=dt*speed; if(stepAcc>2.4){ stepAcc=0; footstepSound(); } } else stepAcc=0;",
    "if(moving){ stepAcc+=dt*speed; if(stepAcc>2.0){ stepAcc=0; footstepSound(); } } else stepAcc=0;")

p.write_text(t, encoding='utf-8')
print('V84 patch applied')
