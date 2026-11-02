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

rep("V56 • main thread လွတ် — Start မစခင် render ရပ် — အကုန်",
    "V57 • tap မြင်စေ + fallback — အကုန်",
    "version v57")
# bootStatus line under version line, so tap/JS state is visible without console
rep('<p style="font-size:11px;color:#666;margin-top:8px">V57 • tap မြင်စေ + fallback — အကုန်</p>',
    '<p style="font-size:11px;color:#666;margin-top:8px">V57 • tap မြင်စေ + fallback — အကုန်</p>\n  <p id="bootStatus" style="font-size:11px;color:#888;margin-top:2px">JS loading…</p>',
    "bootstatus element")
# Inline fallback: if module handlers never registered, tapping Start at least shows a visible message instead of nothing.
# If module handlers did register, guard prevents double start.
rep('<button class="btn" id="startBtn">▶ စဆော့မယ်</button>',
    '<button class="btn" id="startBtn" onclick="window.__nhStart?window.__nhStart(event):(document.getElementById(\'startError\').textContent=\'⚠️ JS handler မရှိဘူး\',document.getElementById(\'startError\').style.display=\'block\')">▶ စဆော့မယ်</button>',
    "inline fallback")
# Expose handleStart globally and mark listeners ready, and mark tap immediately in handleStart
rep("""$('startBtn').addEventListener('touchstart',handleStart,{passive:false});
$('startBtn').addEventListener('pointerdown',handleStart);
$('startBtn').addEventListener('click',handleStart);""",
    """window.__nhStart=handleStart;
$('startBtn').addEventListener('touchstart',handleStart,{passive:false});
$('startBtn').addEventListener('pointerdown',handleStart);
$('startBtn').addEventListener('click',handleStart);
try{ const bs=$('bootStatus'); if(bs) bs.textContent='JS OK • listeners ready'; }catch(e){}""",
    "expose + js ok")
# handleStart: mark tap immediately, before any startGame work, so a silent startGame hang still shows tap arrived
rep("function handleStart(e){ if(e) e.preventDefault(); if(_starting) return;",
    "function handleStart(e){ try{ const bs=$('bootStatus'); if(bs) bs.textContent='Start tapped!'; }catch(err){} if(e) e.preventDefault(); if(_starting) return;",
    "tap marker")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V57 applied')
