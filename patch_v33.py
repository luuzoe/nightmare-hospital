import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
miss = []
def rep(old, new, name):
    global t
    if old not in t:
        miss.append(name)
        print('MISS:', name)
    else:
        t = t.replace(old, new, 1)
        print('OK:', name)

rep(
"V32 • Random သရဲ + Random ပစ္စည်း + အသံအစစ် + Save — ထပ်တိုင်း မတူတော့ဘူး",
"V33 • တိတ်ဆိတ် + ရုတ်တရက် ကြောက် — သရဲမ အသံ ရှားရှား, အသံ နည်းနည်း",
"version label")

# Girl voice: hard cooldown 60s, quieter, silence if too soon
rep(
"function whisperSound(){ if(playReal('girl',0.5)) return; playNoise(1.6,'bandpass',1100,1.5,0.45,7); playNoise(1.4,'bandpass',750,2,0.35,11); playTone(200,130,1.6,'sine',0.22,6); playNoise(1.2,'bandpass',1600,3,0.20,13); }",
"let lastGirlTime=-999;\nfunction whisperSound(){ if(S.time-lastGirlTime<60) return; lastGirlTime=S.time; if(playReal('girl',0.35)) return; playNoise(1.6,'bandpass',1100,1.5,0.25,7); }",
"whisper cooldown quiet")

# Moan quieter and rarer (function volume)
rep(
"function moanSound(){ if(playReal('moan',0.7)) return;",
"function moanSound(){ if(playReal('moan',0.5)) return;",
"moan quieter")

# Ambient quieter
rep(
"ambientGain.gain.value=S.sound?0.07:0;",
"ambientGain.gain.value=S.sound?0.04:0;",
"ambient quieter start")
rep(
"if(ambientGain) ambientGain.gain.value=S.sound?(0.04+floorDown*0.005):0;",
"if(ambientGain) ambientGain.gain.value=S.sound?(0.03+floorDown*0.003):0;",
"ambient quieter floor")

# Initial timers in S object
rep("frontScareTimer:30", "frontScareTimer:50", "front initial")
rep("randScareTimer:25", "randScareTimer:50", "rand initial")
rep("moanTimer:12", "moanTimer:40", "moan initial S")
rep("S.moanTimer=12;", "S.moanTimer=40;", "moan reset")

# Monster close whisper: 3s -> 25s
rep(
"if(mDist<6 && !S.hidden && monsterState!=='scare'){ whisperAcc+=dt; if(whisperAcc>3){ whisperAcc=0; whisperSound(); } } else whisperAcc=0;",
"if(mDist<6 && !S.hidden && monsterState!=='scare'){ whisperAcc+=dt; if(whisperAcc>25){ whisperAcc=0; whisperSound(); } } else whisperAcc=0;",
"monster whisper rare")

# Monster near growl: 1.2s -> 9s
rep(
"if(mDist<12 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>1.2){ growlAcc=0; growlSound(); } } else growlAcc=0;",
"if(mDist<12 && !S.hidden && monsterState!=='scare'){ growlAcc+=dt; if(growlAcc>9){ growlAcc=0; growlSound(); } } else growlAcc=0;",
"monster growl rare")

# Monster scare: remove girl whisper, keep scream + scare
rep(
"monsterState='scare'; S.scare=true; S.scareTimer=2.5; whisperSound(); screamSound(); scareSound();",
"monsterState='scare'; S.scare=true; S.scareTimer=2.5; screamSound(); scareSound();",
"monster scare no girl")

# Wandering chase to scare: remove girl whisper
rep(
"wg.state='scare'; wg.scareTimer=2.0; wanderingScare=true; screamSound(); whisperSound();",
"wg.state='scare'; wg.scareTimer=2.0; wanderingScare=true; screamSound();",
"wandering scare no girl")

# Moan timer: 12-20s -> 40-80s
rep(
"if(S.playing && !S.paused){ S.moanTimer-=dt; if(S.moanTimer<=0){ moanSound(); S.moanTimer=12+Math.random()*8; } }",
"if(S.playing && !S.paused){ S.moanTimer-=dt; if(S.moanTimer<=0){ moanSound(); S.moanTimer=40+Math.random()*40; } }",
"moan timer rare")

# Front jumpscare: 25-40s -> 45-75s
rep(
"S.frontScareTimer=25+Math.random()*15;",
"S.frontScareTimer=45+Math.random()*30;",
"front jumpscare rare")

# Random scare: 20-40s -> 45-90s, no girl whisper in pool
rep(
"if(S.randScareTimer<=0){ S.randScareTimer=20+Math.random()*20; if(Math.random()<0.6) screamSound(); else if(Math.random()<0.5) whisperSound(); else growlSound(); }",
"if(S.randScareTimer<=0){ S.randScareTimer=45+Math.random()*45; if(Math.random()<0.6) screamSound(); else growlSound(); }",
"rand scare rare no girl")

# Poltergeist whisper: rare 20% only
rep(
"if(Math.hypot(tx-playerPos.x,tz-playerPos.z)<12) whisperSound();",
"if(Math.hypot(tx-playerPos.x,tz-playerPos.z)<12 && Math.random()<0.2) whisperSound();",
"polter whisper rare")

# Whisper timer loop: 3s -> 20s, 30% chance only
rep(
"if(nd<6 && !S.hidden){ whisperSound(); } S.whisperTimer=3;",
"if(nd<6 && !S.hidden && Math.random()<0.3){ whisperSound(); } S.whisperTimer=20;",
"whisper timer rare")

# Corpse twitch: 10-20s -> 60-120s, girl voice 25% only
rep(
"if(S.time>nextTwitch){ twitchUntil=S.time+1; nextTwitch=S.time+10+Math.random()*10; whisperSound(); toast('👻 လူသေကောင် လှုပ်သွားသလား…?'); }",
"if(S.time>nextTwitch){ twitchUntil=S.time+1; nextTwitch=S.time+60+Math.random()*60; if(Math.random()<0.25) whisperSound(); toast('👻 လူသေကောင် လှုပ်သွားသလား…?'); }",
"twitch rare")

if miss:
    print('MISSES:', miss)
    raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V33 patch applied, misses=0')
