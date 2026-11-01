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

rep("V47 • ဆေးရုံအသစ် 15x25m, တံခါး 2.5m, လျှောက်လမ်း 10m, လှေကားအစစ် 3D, Story + ပိုကြောက်စရာ — အကုန်",
    "V48 • လှေကားစည်းကမ်း: Mission မပြီးဘဲ အောက်ဆုံးရောက်ရင် သရဲက ဂုတ်ချိုး တခါထဲ သေ — အကုန်",
    "version v48")
# neckSnapKill function, inserted before endGame
rep("function endGame(win){",
    """// V48 NECK SNAP: mission not done + staircase bottom = instant death, no respawn, no hearts left.
function neckSnapKill(){
  if(S._neckSnap) return; S._neckSnap=true; S.hearts=0; updateHUD();
  scareSound(); screamSound(); if(navigator.vibrate) navigator.vibrate([500,100,500]);
  const d=$('damage'); if(d) d.style.opacity=1;
  // ghost teleports right in front of the player (hall descent faces north, so front = -z)
  monsterPos.set(playerPos.x,0,playerPos.z-2); if(typeof monster!=='undefined' && monster){ monster.position.set(monsterPos.x,playerPos.y+1.6,monsterPos.z); monster.rotation.y=Math.PI; }
  toast('💀 သရဲက ဂုတ်ချိုးသတ်လိုက်ပြီ!');
  S.paused=true;
  setTimeout(()=>{ S.paused=false; endGame(false); },900);
}
function endGame(win){""",
    "neckSnapKill")
# endGame neckSnap text
rep("  $('endTitle').textContent=win?'🎉 လွတ်မြောက်ပြီ!':'👹 ဖမ်းခံရပြီ…';",
    "  $('endTitle').textContent=win?'🎉 လွတ်မြောက်ပြီ!':(S.neckSnap?'💀 ဂုတ်ချိုးခံရပြီ…':'👹 ဖမ်းခံရပြီ…');",
    "endTitle neckSnap")
rep("  $('endText').textContent=win?('မေသူ၏ ဒိုင်ယာရီကို ရပြီ! 15 ထပ် ဆေးရုံကနေ လွတ်မြောက်သွားပြီ! အချိန်: '+Math.floor(S.time)+' စက္ကန့် — ဒါပေမယ့် ဆေးရုံက မင်းနောက်ကို လိုက်နေတုန်းပဲ…')\n    :('အသက် ကုန်သွားပြီ။ နောက်တစ်ပွဲ ထပ်ကြိုးစားပါ — ဒီတစ်ခါ ပိုတိတ်တိတ်နဲ့ ပိုမြန်မြန် ရှာပါ။');",
    "  $('endText').textContent=win?('မေသူ၏ ဒိုင်ယာရီကို ရပြီ! 15 ထပ် ဆေးရုံကနေ လွတ်မြောက်သွားပြီ! အချိန်: '+Math.floor(S.time)+' စက္ကန့် — ဒါပေမယ့် ဆေးရုံက မင်းနောက်ကို လိုက်နေတုန်းပဲ…')\n    :(S.neckSnap?'Mission မပြီးဘဲ လှေကားအောက်ဆုံးထိ ဆင်းလို့ သရဲက ဂုတ်ချိုးသတ်လိုက်ပြီ! လှေကားမဆင်းခင် mission အရင် ပြီးအောင် လုပ်ပါ။':'အသက် ကုန်သွားပြီ။ နောက်တစ်ပွဲ ထပ်ကြိုးစားပါ — ဒီတစ်ခါ ပိုတိတ်တိတ်နဲ့ ပိုမြန်မြန် ရှာပါ။');",
    "endText neckSnap")
# reset neckSnap in resetGame
rep("S.dead=false; S.won=false; S.yaw=Math.PI/2;",
    "S.dead=false; S.won=false; S.neckSnap=false; S._neckSnap=false; S._hallWarn2=false; S.yaw=Math.PI/2;",
    "reset neckSnap")
# staircase bottom rule: replace V47 warn-only with neckSnap + halfway warning
rep("  // V47 STAIRCASE BOTTOM: mission complete + walk all the way down to z <= -21 in hall -> descend. If not complete, warn once and walk back up.\n  if(S.floor>1 && !S._landing && playerPos.x>=-9.5 && playerPos.x<=-5.5 && playerPos.z<=-21){ if(missionComplete()){ S._landing=true; toast('⬇️ လှေကားအောက်ရောက်ပြီ! အောက်ထပ် ဆင်းမယ်!'); goToNextFloor(); } else if(!S._hallWarn){ S._hallWarn=true; toast('🔒 လှေကားအောက်ရောက်ပြီ၊ ဒါပေမယ့် လုပ်စရာ ကျန်သေးသည် — ပြန်တက်ပါ'); } }\n  if(playerPos.z>-5) S._hallWarn=false;",
    """  // V48 STAIRCASE RULE: mission complete -> descend as before. Mission NOT complete + bottom (z <= -21) -> ghost neck-snaps, instant death, no respawn.
  // Halfway warning (z <= -12) gives a fair chance to turn back before the bottom.
  if(playerPos.x>=-9.5 && playerPos.x<=-5.5 && playerPos.z>=-30 && playerPos.z<=-5){
    if(!missionComplete() && !S.escaping && playerPos.z<=-12 && !S._hallWarn2){ S._hallWarn2=true; toast('⚠️ Mission မပြီးဘဲ လှေကားဆင်းနေပြီ! အောက်ဆုံးရောက်ရင် သရဲက ဂုတ်ချိုးသတ်မယ်! ပြန်တက်ပါ!'); }
    if(S.floor>1 && !S._landing && playerPos.z<=-21){ if(missionComplete()){ S._landing=true; toast('⬇️ လှေကားအောက်ရောက်ပြီ! အောက်ထပ် ဆင်းမယ်!'); goToNextFloor(); } else if(!S.escaping){ neckSnapKill(); } }
    if(!S.escaping && S.floor===1 && !missionComplete() && playerPos.z<=-21){ neckSnapKill(); }
  }
  if(playerPos.z>-5){ S._hallWarn=false; S._hallWarn2=false; }""",
    "staircase rule v48")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V48 applied')
