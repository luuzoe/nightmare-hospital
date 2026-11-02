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

rep("V54 • Start ပြင် + start screen သန့် — အကုန်",
    "V55 • Start ချက်ချင်း စစေ + error မြင်စေ — အကုန်",
    "version v55")
# Classic error trap BEFORE the module script, so even a module load failure shows on the start screen
rep("<script type=\"module\">",
    """<script>
window.addEventListener('error',function(e){ try{ var ld=document.getElementById('load'); if(ld) ld.style.display='none'; var el=document.getElementById('startError'); if(el){ el.textContent='⚠️ JS Error: '+(e.message||'unknown'); el.style.display='block'; } }catch(err){} });
</script>
<script type="module">""",
    "js error trap v55")
# StartGame: show game FIRST, then reset, then audio/fullscreen best-effort (never block Start)
rep("""function startGame(){
  try{ localStorage.removeItem('nh_save'); }catch(e){}
  ac(); tryAutoLandscape(); setTimeout(()=>tryAutoLandscape(),500); startAmbient(); beep(440,.15); setTimeout(()=>beep(660,.2),150);
  resetGame(); S.playing=true; S.paused=false;
  $('startScreen').classList.add('hidden'); $('pauseScreen').classList.add('hidden'); $('endScreen').classList.add('hidden');
  $('hud').classList.add('on'); $('load').style.display='none';
  if(typeof checkOrientation==='function')checkOrientation();
  setTimeout(()=>{ const h=$('hint'); if(h) h.style.display='none'; },6000);
  toast('👹 Monster က Morgue ဘက်မှာ ရှိနေသည် — တိတ်တိတ်ရှာပါ');
}""",
    """function startGame(){
  try{ localStorage.removeItem('nh_save'); }catch(e){}
  $('startScreen').classList.add('hidden'); $('pauseScreen').classList.add('hidden'); $('endScreen').classList.add('hidden');
  $('hud').classList.add('on'); $('load').style.display='none';
  S.playing=true; S.paused=false;
  resetGame();
  try{ ac(); }catch(e){}
  try{ tryAutoLandscape(); }catch(e){}
  setTimeout(()=>{ try{ tryAutoLandscape(); }catch(e){} },500);
  try{ startAmbient(); beep(440,.15); setTimeout(()=>beep(660,.2),150); }catch(e){}
  if(typeof checkOrientation==='function')checkOrientation();
  setTimeout(()=>{ const h=$('hint'); if(h) h.style.display='none'; },6000);
  toast('👹 Monster က Morgue ဘက်မှာ ရှိနေသည် — တိတ်တိတ်ရှာပါ');
}""",
    "startgame reorder v55")
# Touchstart as well as pointerdown/click, so Android tap reaches Start even if one event type is swallowed
rep("""$('startBtn').addEventListener('pointerdown',handleStart);
$('startBtn').addEventListener('click',handleStart);""",
    """$('startBtn').addEventListener('touchstart',handleStart,{passive:false});
$('startBtn').addEventListener('pointerdown',handleStart);
$('startBtn').addEventListener('click',handleStart);""",
    "touchstart v55")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V55 applied')
