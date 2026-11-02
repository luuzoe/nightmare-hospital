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

rep("V49 • ဆေးရုံအစုတ် အစစ် + ကြောက်စရာ/စိတ်ခြောက်ခြားစရာ: မီးတင်, 3D အပျက်အစီး, ထပ်နိမ့်လေ ပိုစုတ်, shadow glimpse, hunt — အကုန်",
    "V50 • အကုန်: unseen haunting + dynamic tension + risky chase + story events + jumpscare variety — error မရှိ — အကုန်",
    "version v50")
# Reset timers
rep("S.glimpseTimer=60; S.glimpseUntil=0; S.huntTimer=150; S.yaw=Math.PI/2;",
    "S.glimpseTimer=60; S.glimpseUntil=0; S.huntTimer=150; S.hauntTimer=45; S.storyTimer=40; S.storyDoneFloor=0; S.yaw=Math.PI/2;",
    "reset timers v50")
# Story diary + per-floor story reset in startFloorMission
rep("const STORY_HINTS={15:'Ep1 • မေသူ၏ ပထမဆုံး ဒိုင်ယာရီ — “ဒီဆေးရုံက မပိတ်သေးဘူး”'",
    """const STORY_DIARY={15:'📖 မေသူ: “ဒီဆေးရုံက မပိတ်သေးဘူး။ ညက တစ်စုံတစ်ခု ငါ့နာမည်ခေါ်တယ်။”',14:'📖 မေသူ: “ညဆိုင်း သူနာပြုတွေ တစ်ယောက်ပြီး တစ်ယောက် ပျောက်နေပြီ။”',13:'📖 မေသူ: “ဒေါက်တာက စမ်းသပ်ခန်းကို သော့ခတ်ထားတယ်။ အထဲမှာ ဘာရှိလဲ မသိဘူး။”',12:'📖 မေသူ: “လူနာတွေ ညက အော်တယ်။ မနက်ကျတော့ ဘယ်သူမှ မရှိတော့ဘူး။”',11:'📖 မေသူ: “Locker ထဲမှာ စာတစ်စောင် ဝှက်ထားခဲ့တယ်။ ဖတ်မိရင် ပြန်မလာနဲ့။”',10:'📖 မေသူ: “သူ့ကို Surgery စားပွဲဆီ ဆွဲခေါ်ရမယ်။ အဲဒါမှ သူ ရပ်မယ်။”',9:'📖 မေသူ: “မှောင်ထဲမှာ ငါ့နာမည် ရေးထားတယ်။ ငါ မရေးခဲ့ဘူး။”',8:'📖 မေသူ: “အချိန်မီ ပြေးရမယ်။ သူက အချိန်ကို စောင့်နေတယ်။”',7:'📖 မေသူ: “ပုန်းနေရင်း ခြေသံ ကြားရတယ်။ ငါ့ဘေး ရပ်နေတယ်။”',6:'📖 မေသူ: “အလောင်းတွေက စကားပြောတယ်။ သူတို့က ငါ့ကို သိတယ်။”',5:'📖 မေသူ: “အခန်း ၄ ခန်းမှာ တစ်ခုစီ ရှိတယ်။ စုမှ အမှန်သိမယ်။”',4:'📖 မေသူ: “180m လမ်းလျှောက်ရင်း အရိပ် တစ်ခု ငါ့နောက် လိုက်လာတယ်။”',3:'📖 မေသူ: “မှောင် Locker ထဲမှာ ဒိုင်ယာရီ တစ်ပိုင်း ကျန်ခဲ့တယ်။”',2:'📖 မေသူ: “အစဉ်လိုက် သော့တွေ — နောက်ဆုံး အဆင့်။ ပြန်လှည့်လို့ မရတော့ဘူး။”',1:'📖 မေသူ: “အမှန်တရား ဒီမှာ ရှိတယ်။ မင်း ဒါကို ဖတ်နေရင် ငါ မရှိတော့ဘူး။”'};
const STORY_HINTS={15:'Ep1 • မေသူ၏ ပထမဆုံး ဒိုင်ယာရီ — “ဒီဆေးရုံက မပိတ်သေးဘူး”'""",
    "story diary v50")
rep("  if(typeof decayGroup2!=='undefined'){ decayGroup2.visible=S.floor<=10; decayGroup3.visible=S.floor<=5; } // V49: lower floors more ruined",
    "  if(typeof decayGroup2!=='undefined'){ decayGroup2.visible=S.floor<=10; decayGroup3.visible=S.floor<=5; } // V49: lower floors more ruined\n  S.storyTimer=40; S.storyDoneFloor=0; // V50: one story event per floor",
    "story reset v50")
# Risky chase: longer hide lose, no immediate lose when far, hide break when monster very close
rep("    const loseAfter=(S.hideLocker?3.0:6.0)+(15-S.floor)*0.3; // V47 harder: monster stays longer",
    "    const loseAfter=(S.hideLocker?5.0:9.0)+(15-S.floor)*0.3; // V50 risky: monster searches longer",
    "hide lose longer v50")
rep("    if(S.hidden && mDist>3){ monsterState='patrol'; S.chase=false; }",
    "    if(S.hidden && mDist>28){ monsterState='patrol'; S.chase=false; } // V50: hiding far away no longer ends chase instantly; hideTimer must expire",
    "no immediate hide lose v50")
# Hide break: insert into hideTimer block, after loseAfter check
rep("    if(S.hideTimer>=loseAfter){ monsterState='patrol'; S.chase=false; lastSeen=null; S.hideTimer=0; toast('👹 Monster ဖြတ်သွားပြီ — တိတ်တိတ် ထွက်ပါ'); }",
    """    if(S.hideTimer>=loseAfter){ monsterState='patrol'; S.chase=false; lastSeen=null; S.hideTimer=0; toast('👹 Monster ဖြတ်သွားပြီ — တိတ်တိတ် ထွက်ပါ'); }
    // V50 hide search: monster reaches your hide spot (within 2.5m) = hide breaks, you must run (catch still needs 1.4m + grace, so it is fair, not instant)
    if(S.hidden && monsterState==='chase' && mDist<2.5){ S.hidden=false; S.hideTimer=0; $('hideBtn').classList.remove('active'); lastSeen=playerPos.clone(); scareSound(); toast('👹 ပုန်းနေတာ တွေ့သွားပြီ! ပြေးပါ!'); }""",
    "hide break v50")
# Heartbeat danger includes hidden + very close monster (tension while hiding)
rep("  const danger=mDist<10 && !S.hidden;",
    "  const danger=(mDist<10 && !S.hidden) || (S.hidden && mDist<5); // V50: hiding near monster still feels dangerous",
    "danger hidden v50")
# Jumpscare variety: front or behind
rep("      const fx=playerPos.x+Math.sin(S.yaw)*2.5, fz=playerPos.z+Math.cos(S.yaw)*2.5;",
    "      const behind=Math.random()<0.4; const fx=playerPos.x+(behind?-1:1)*Math.sin(S.yaw)*2.5, fz=playerPos.z+(behind?-1:1)*Math.cos(S.yaw)*2.5; // V50: 40% behind scare",
    "behind scare pos v50")
rep("        S.ghostFaceUntil=S.time+1.0; screamSound(); scareSound(); if(navigator.vibrate) navigator.vibrate(200); toast('👻 သရဲ ရှေ့တည့်တည့် ပေါ်လာပြီ!');",
    "        S.ghostFaceUntil=S.time+1.0; screamSound(); scareSound(); if(navigator.vibrate) navigator.vibrate(200); toast(behind?'👻 နောက်မှာ တစ်စုံတစ်ခု ရှိနေတယ်! လှည့်ကြည့်ပါ!':'👻 သရဲ ရှေ့တည့်တည့် ပေါ်လာပြီ!');",
    "behind scare toast v50")
# Haunt + story events, after randScare line
rep("    if(S.randScareTimer<=0){ S.randScareTimer=90+Math.random()*30; if(Math.random()<0.3) screamSound(); else moanSound(); } // V49 rand scare",
    """    if(S.randScareTimer<=0){ S.randScareTimer=90+Math.random()*30; if(Math.random()<0.3) screamSound(); else moanSound(); } // V49 rand scare
    // V50 UNSEEN HAUNTING: distant footsteps, door slams by itself, light flicker (short blackout, flashlight stays) — no catch, pure dread.
    if(S.playing && !S.paused && !S.chase && !S.escaping){
      if(typeof S.hauntTimer!=='number') S.hauntTimer=45;
      S.hauntTimer-=dt;
      if(S.hauntTimer<=0){
        S.hauntTimer=45+Math.random()*45;
        const ht=Math.random();
        if(ht<0.35){ footstepSound(); whisperSound(); toast('👣 အဝေးက ခြေသံ…'); }
        else if(ht<0.65 && typeof doorWalls!=='undefined' && doorWalls.length){
          const nearDoors=doorWalls.filter(dw=>Math.hypot(dw.x-playerPos.x,dw.z-playerPos.z)<20);
          const dw=nearDoors.length?nearDoors[Math.floor(Math.random()*nearDoors.length)]:doorWalls[0];
          if(dw){ dw.doorOpen=false; doorSound(); toast('🚪 တံခါး ကိုယ်တိုင် ပိတ်သွားပြီ!'); }
        } else { S.blackout=Math.max(S.blackout,1.0); whisperSound(); toast('💡 မီး မှိတ်တုတ်မှိတ်တုတ် ဖြစ်သွားပြီ…'); }
      }
    }
    // V50 STORY EVENT: once per floor, diary line + whisper + brief flicker. No new interact, so it cannot break missions.
    if(S.playing && !S.paused && !S.chase && S.storyDoneFloor!==S.floor){
      if(typeof S.storyTimer!=='number') S.storyTimer=40;
      S.storyTimer-=dt;
      if(S.storyTimer<=0){
        S.storyDoneFloor=S.floor; S.blackout=Math.max(S.blackout,1.0); whisperSound();
        toast(typeof STORY_DIARY!=='undefined' && STORY_DIARY[S.floor] ? STORY_DIARY[S.floor] : '📖 မေသူ၏ ဒိုင်ယာရီ…');
      }
    }""",
    "haunt + story v50")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V50 applied')
