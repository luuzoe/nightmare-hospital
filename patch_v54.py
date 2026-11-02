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

rep("V53 • အကုန် ခက်အောင် + smooth + ပြတင်းပေါက် — အကုန်",
    "V54 • Start ပြင် + start screen သန့် — အကုန်",
    "version v54")
# Start screen: smaller title, smaller buttons, less text
rep(".screen h1{font-size:52px;",
    ".screen h1{font-size:36px;",
    "h1 smaller v54")
rep(".btn{margin-top:16px;padding:18px 38px;font-size:20px;",
    ".btn{margin-top:12px;padding:12px 24px;font-size:17px;",
    "btn smaller v54")
rep("<p style=\"font-size:14px;color:#ffcccc;line-height:1.5\">📖 ဇာတ်လမ်း: သူနာပြု မေသူ ဒီစွန့်ပစ်ဆေးရုံထဲ ပျောက်သွားတာ ၃ နှစ်ရှိပြီ။ သူ့အစ်ကို မင်းက သူ့ဒိုင်ယာရီ စာမျက်နှာတွေကို တစ်ထပ်ပြီး တစ်ထပ် လိုက်ရှာရမယ်။ အပေါ်ဆုံး 15 ထပ်က စ၊ အောက်ဆုံး 1 ထပ်မှာ အမှန်တရား ရှိတယ်။ ဆေးရုံက မင်းကို စောင့်နေတယ် — တိတ်တိတ် သွား၊ အသံ မဆူပါနဲ့၊ သူ ကြားလိမ့်မယ်။</p>",
    "<p style=\"font-size:14px;color:#ffcccc;line-height:1.5\">📖 သူနာပြု မေသူ ဒီဆေးရုံထဲ ပျောက်သွားတာ ၃ နှစ်ရှိပြီ — သူ့ဒိုင်ယာရီကို တစ်ထပ်ပြီး တစ်ထပ် ရှာပါ။</p>",
    "story shorter v54")
rep("<p class=\"small\">🕹️ လမ်း • 👆 Camera • 🏃 RUN ပြေး • 🫥 HIDE ပုန်း (ရပ်) • စွန့်ပစ်ဆေးရုံ: အခန်း 15x25m, တံခါး 2.5m, လျှောက်လမ်း 10m, လှေကားအစစ်, အပေါ်ဆုံး 15 ထပ်က စ</p>",
    "<p class=\"small\">🕹️ Joystick = လမ်း • ညာဘက် ဆွဲ = Camera • RUN • HIDE</p>",
    "controls shorter v54")
rep("  <p style=\"font-size:11px;color:#666;margin-top:4px\">အသံ: SoundBible (လူအစစ် သရဲ အသံ)</p>\n",
    "",
    "sound credit removed v54")
# Error line on start screen, so a failed Start shows a reason instead of nothing
rep("""    <button class="btn ghost" id="soundBtn">🔊 အသံ: ဖွင့်</button>
  </div>""",
    """    <button class="btn ghost" id="soundBtn">🔊 အသံ: ဖွင့်</button>
  </div>
  <p id="startError" style="color:#ff6666;font-size:13px;display:none"></p>""",
    "startError element v54")
# Robust Start: pointerdown + click, guard against double, visible error on failure, restore start screen
rep("""$('startBtn').addEventListener('click',()=>{ try{ localStorage.removeItem('nh_save'); }catch(e){} startGame(); });""",
    """let _starting=false;
function handleStart(e){ if(e) e.preventDefault(); if(_starting) return; _starting=true; const errEl=$('startError'); if(errEl) errEl.style.display='none'; try{ localStorage.removeItem('nh_save'); }catch(err){} try{ startGame(); }catch(err){ _starting=false; S.playing=false; $('startScreen').classList.remove('hidden'); $('hud').classList.remove('on'); if(errEl){ errEl.textContent='⚠️ စမရဘူး: '+(err&&err.message?err.message:err); errEl.style.display='block'; } } }
$('startBtn').addEventListener('pointerdown',handleStart);
$('startBtn').addEventListener('click',handleStart);""",
    "robust start v54")
# Continue: same visible-error handling, so a failed Continue also shows a reason
rep("""if($('continueBtn')){ $('continueBtn').addEventListener('click', continueGame);""",
    """if($('continueBtn')){ $('continueBtn').addEventListener('pointerdown',(e)=>{ e.preventDefault(); try{ continueGame(); }catch(err){ const errEl=$('startError'); if(errEl){ errEl.textContent='⚠️ ဆက်ဆော့မရဘူး: '+(err&&err.message?err.message:err); errEl.style.display='block'; } } }); $('continueBtn').addEventListener('click', continueGame);""",
    "robust continue v54")
# Stop competing fullscreen requests on every pointerdown (Start already requests fullscreen itself)
rep("document.addEventListener('pointerdown',()=>{ ac(); tryAutoLandscape(); }, {passive:true});",
    "document.addEventListener('pointerdown',()=>{ ac(); }, {passive:true});",
    "no competing fullscreen v54")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V54 applied')
