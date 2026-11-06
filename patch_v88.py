import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V87[^<]{0,80}", t)
assert m, "V87 label not found"
t = t.replace(m.group(0), "V88 PLACEHOLDER", 1)

# Load the 6 new CC0 Freesound sounds (MP3, ~2.9 MB total)
rep("loadRealSound('girl','ghost-girl.mp3');",
    "loadRealSound('girl','ghost-girl.mp3');\nloadRealSound('drone','horror-drone.mp3'); loadRealSound('door','door-creak.mp3'); loadRealSound('scream2','scream-female.mp3'); loadRealSound('whisper','ghost-whisper.mp3'); loadRealSound('thunder','thunder.mp3'); loadRealSound('woodstep','footsteps-wood.mp3');")

# Real door creak instead of synth creak
rep("function doorSound(){ playTone(180,320,0.5,'sawtooth',0.07,0); playNoise(0.5,'bandpass',600,2,0.03,0); }",
    "function doorSound(){ if(playReal('door',0.8)) return; playTone(180,320,0.5,'sawtooth',0.07,0); playNoise(0.5,'bandpass',600,2,0.03,0); }")

# Real ghost whisper first, then the old girl sound
rep("function whisperSound(){ if(S.time-lastGirlTime<30) return; lastGirlTime=S.time; if(playReal('girl',0.7)) return; playNoise(1.6,'bandpass',1100,1.5,0.25,7); }",
    "function whisperSound(){ if(S.time-lastGirlTime<30) return; lastGirlTime=S.time; if(playReal('whisper',0.7)) return; if(playReal('girl',0.7)) return; playNoise(1.6,'bandpass',1100,1.5,0.25,7); }")

# Female scream as a second scream, half the time
rep("function screamSound(){ if(playReal('scream',0.9)) return;",
    "function screamSound(){ if(Math.random()<0.5 && playReal('scream2',0.9)) return; if(playReal('scream',0.9)) return;")

# Real wood footstep first; synth thud only if the file is not loaded yet
rep("function footstepSound(){ playNoise(0.18,'lowpass',220,1,0.30,0); playTone(900,250,0.22,'sawtooth',0.06,8);",
    "function footstepSound(){ if(!playReal('woodstep',0.5)) playNoise(0.18,'lowpass',220,1,0.30,0); playTone(900,250,0.22,'sawtooth',0.06,8);")

# Thunder on blackout
rep("S.blackout=6.0; S.blackoutTimer=Math.max(10,18-(15-S.floor))+Math.random()*6; thump(0.4); toast('⚡ မီး ပျက်သွားပြီ! တိတ်တိတ် နေ!');",
    "S.blackout=6.0; S.blackoutTimer=Math.max(10,18-(15-S.floor))+Math.random()*6; thump(0.4); playReal('thunder',0.6); toast('⚡ မီး ပျက်သွားပြီ! တိတ်တိတ် နေ!');")

# Horror drone loop in the ambient mix, with mute handling
rep("let ambientGain=null, ambientStarted=false;",
    "let ambientGain=null, ambientStarted=false, droneAudio=null;")
rep("function toggleSound(){\n  S.sound=!S.sound;\n  if(ambientGain)ambientGain.gain.value=S.sound?0.04:0;",
    "function toggleSound(){\n  S.sound=!S.sound;\n  if(ambientGain)ambientGain.gain.value=S.sound?0.04:0;\n  if(droneAudio){ if(S.sound) droneAudio.play().catch(()=>{}); else droneAudio.pause(); }")
# Start the drone at the end of startAmbient: hook into the wind setup block
# by adding after the ambientGain creation line inside startAmbient.
rep("    ambientGain=c.createGain(); ambientGain.gain.value=S.sound?0.04:0; // V29 scarier ambient louder ambientGain.connect(c.destination);",
    "    ambientGain=c.createGain(); ambientGain.gain.value=S.sound?0.04:0; // V29 scarier ambient louder ambientGain.connect(c.destination);\n    try{ const da=realSounds['drone']; if(da && S.sound){ da.loop=true; da.volume=0.22*(S.volume||1); da.play().catch(()=>{}); droneAudio=da; } }catch(e){}")

p.write_text(t, encoding='utf-8')
print('V88 patch applied')
