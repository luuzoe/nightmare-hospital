import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')

def rep(old, new):
    global t
    assert old in t, f"NOT FOUND: {old[:160]}"
    t = t.replace(old, new, 1)

# Version label
m = re.search(r"V79[^<]{0,80}", t)
assert m, "V79 label not found"
t = t.replace(m.group(0), "V80 PLACEHOLDER", 1)

# --- Clean start screen: hide routine diagnostic line ---
rep('<p id="bootStatus" style="font-size:11px;color:#888;margin-top:2px">JS loading…</p>',
    '<p id="bootStatus" style="display:none">JS loading…</p>')
# Early listeners: keep text for diagnostics, but do not show it on screen
rep("if(_ee){ _ee.textContent='Early listeners OK'; _ee.style.display='block'; }",
    "if(_ee){ _ee.textContent='Early listeners OK'; }")

# --- Tutorial button on start screen ---
rep('<button class="btn ghost" id="soundBtn">🔊 အသံ: ဖွင့်</button>',
    '<button class="btn ghost" id="soundBtn">🔊 အသံ: ဖွင့်</button>\n    <button class="btn ghost" id="tutorialBtn">📖 ဘယ်လိုဆော့မလဲ</button>')

# --- Load progress line under the start row ---
rep('<p id="startError" style="color:#ff6666;font-size:13px;display:none"></p>',
    '<p id="startError" style="color:#ff6666;font-size:13px;display:none"></p>\n  <p id="coreStatus" style="font-size:12px;color:#ffcc66;margin-top:6px">⏳ သရဲတွေ တင်နေသည်…</p>')

# --- Tutorial overlay, after the start screen ---
rep('<!-- Pause -->',
    '''<div id="tutorialScreen" class="screen hidden">
  <h2>📖 ဘယ်လိုဆော့ရမလဲ</h2>
  <p style="font-size:15px;text-align:left">🕹️ <b>ဘယ် Joystick</b> = လမ်း • <b>ညာဘက် ဆွဲ</b> = Camera လှည့်<br>
  🏃 <b>RUN</b> = ပြေး (စွမ်းအင် ကုန်ရင် ရပ်ရမယ်)<br>
  🫥 <b>HIDE</b> = ပုန်း — HIDE ဖွင့်ထားရင် လမ်းမလျှောက်ရဘူး, သရဲ အလွယ်မမြင်ဘူး (အရမ်းနီးရင် တွေ့တယ်)<br>
  ✋ <b>ယူ/ဖွင့်</b> = သော့ (အနီး 3m) / ပစ္စည်း (အနီး 1.8m) ယူ<br>
  🎯 <b>Mission ပြီးမှ</b> လှေကားအောက် ဆင်း — mission မပြီးပဲ လှေကားအောက် ရောက်ရင် သရဲက ချက်ချင်း သတ်တယ် (လမ်းတစ်ဝက်မှာ သတိပေးတယ်)<br>
  💀 သရဲဖမ်းရင် နှလုံး 1 လုံး + ယူထားတဲ့ ပစ္စည်း 1 ခု ကျတယ်, သေရင် 5 စက္ကန့် ရေတွက်ပြီး ပြန်ပေါ်တယ်<br>
  💾 Save: ထပ်/နှလုံး/အချိန် သိမ်းတယ်, ဆက်ဆော့မယ် နဲ့ ပြန်ဆော့လို့ရတယ်</p>
  <div class="row"><button class="btn" id="tutorialCloseBtn">✅ နားလည်ပြီ, စဆော့မယ်</button></div>
</div>

<!-- Pause -->''')

# --- Core-ready guard in handleStart (before _starting is set) ---
rep("function handleStart(e){ try{ const bs=$('bootStatus'); if(bs) bs.textContent='Start tapped!'; }catch(err){} if(e) e.preventDefault(); if(_starting) return; _starting=true;",
    "function handleStart(e){ try{ const bs=$('bootStatus'); if(bs) bs.textContent='Start tapped!'; }catch(err){} if(e) e.preventDefault(); if(window.__nhCoreReady!==true){ const cs=$('coreStatus'); if(cs) cs.textContent='⏳ သရဲတွေ တင်နေတုန်း… ခဏစောင့်, ပြီးရင် စဆော့မယ် ထပ်နှိပ်'; return; } if(_starting) return; _starting=true;")
# --- Core-ready guard in continueGame ---
rep("function continueGame(){ let sv=null;",
    "function continueGame(){ if(window.__nhCoreReady!==true){ const cs=$('coreStatus'); if(cs) cs.textContent='⏳ သရဲတွေ တင်နေတုန်း… ခဏစောင့်, ပြီးရင် ဆက်ဆော့မယ် ထပ်နှိပ်'; return; } let sv=null;")

# --- Load progress + core-ready flag + 90s fallback ---
rep("loadCharacter().then(async ok=>{\n  $('load').style.display='none';\n  await new Promise(r=>setTimeout(r,50));\n  await loadCorpses();\n  await new Promise(r=>setTimeout(r,50));\n  await loadGhost();\n  await new Promise(r=>setTimeout(r,50));\n  await loadWanderingGhosts();",
    "function setCoreStatus(txt){ try{ const el=document.getElementById('coreStatus'); if(el) el.textContent=txt; }catch(e){} }\nsetTimeout(()=>{ if(window.__nhCoreReady!==true){ window.__nhCoreReady=true; setCoreStatus('⚠️ internet နှေးနေတယ် — စဆော့လို့ရပြီ, တချို့ သရဲ နောက်မှ ပေါ်လာနိုင်တယ်'); } },90000);\nloadCharacter().then(async ok=>{\n  $('load').style.display='none';\n  setCoreStatus('⏳ အလောင်းတွေ တင်နေသည်…');\n  await loadCorpses();\n  setCoreStatus('⏳ သရဲကြီး တင်နေသည်…');\n  await loadGhost();\n  setCoreStatus('⏳ နောက်ထပ် သရဲတွေ တင်နေသည်…');\n  await loadWanderingGhosts();\n  window.__nhCoreReady=true;\n  setCoreStatus('✅ အားလုံး အဆင်သင့် — စဆော့လို့ရပြီ');")

# --- Classic tutorial script, after the module script, before </body> ---
rep("</script>\n</body>",
    """</script>
<script>
(function(){
  var tut=document.getElementById('tutorialScreen');
  var btn=document.getElementById('tutorialBtn');
  var closeBtn=document.getElementById('tutorialCloseBtn');
  function showTut(){ if(tut) tut.classList.remove('hidden'); }
  function hideTut(){ if(tut) tut.classList.add('hidden'); try{ localStorage.setItem('nh_tutorial_seen','1'); }catch(e){} }
  if(btn) btn.addEventListener('click',showTut);
  if(closeBtn) closeBtn.addEventListener('click',hideTut);
  try{ if(!localStorage.getItem('nh_tutorial_seen')) showTut(); }catch(e){}
})();
</script>
</body>""")

p.write_text(t, encoding='utf-8')
print('V80 patch applied')
