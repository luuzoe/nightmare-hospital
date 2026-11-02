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

rep("V62 • early error မြင်စေ — အကုန်",
    "V63 • early error သီးသန့် — အကုန်",
    "version v63")
# Separate earlyError element, never overwritten by watchdog
rep('<p id="bootError" style="color:#ff6666;font-size:12px;display:none"></p>',
    '<p id="bootError" style="color:#ff6666;font-size:12px;display:none"></p>\n  <p id="earlyError" style="color:#ffcc66;font-size:12px;display:none"></p>',
    "earlyerror element")
# Early code writes to earlyError, not bootError, and records OK status too
rep("""try{ const _sb=document.getElementById('startBtn'); if(!_sb){ const _be=document.getElementById('bootError'); if(_be){ _be.textContent='⚠️ Early: startBtn not found in DOM'; _be.style.display='block'; } } else { _sb.addEventListener('touchstart',handleStart,{passive:false}); _sb.addEventListener('pointerdown',handleStart); _sb.addEventListener('click',handleStart); window.__nhStart=handleStart; const _bs=document.getElementById('bootStatus'); if(_bs) _bs.textContent='Early listeners ready'; } }catch(e){ window.__nhEarlyError=e.message||String(e); const _be2=document.getElementById('bootError'); if(_be2){ _be2.textContent='⚠️ Early listeners failed: '+(e.message||String(e)); _be2.style.display='block'; } }""",
    """try{ const _sb=document.getElementById('startBtn'); const _ee=document.getElementById('earlyError'); if(!_sb){ if(_ee){ _ee.textContent='⚠️ Early: startBtn not found in DOM'; _ee.style.display='block'; } } else { _sb.addEventListener('touchstart',handleStart,{passive:false}); _sb.addEventListener('pointerdown',handleStart); _sb.addEventListener('click',handleStart); window.__nhStart=handleStart; window.__nhEarlyOK=true; if(_ee){ _ee.textContent='Early listeners OK'; _ee.style.display='block'; } const _bs=document.getElementById('bootStatus'); if(_bs) _bs.textContent='Early listeners ready'; } }catch(e){ window.__nhEarlyError=e.message||String(e); const _ee2=document.getElementById('earlyError'); if(_ee2){ _ee2.textContent='⚠️ Early listeners failed: '+(e.message||String(e)); _ee2.style.display='block'; } }""",
    "early to separate element")
# Watchdog includes early status in its message, so final bootError preserves it
rep("var kind=window.__nhModuleStarted?('Module started, last checkpoint: '+(window.__nhCP||'none')+', init failed before listeners'):'Module never started (import/CDN failed or hung)';",
    "var kind=window.__nhModuleStarted?('Module started, last checkpoint: '+(window.__nhCP||'none')+', early: '+(window.__nhEarlyOK?'OK':(window.__nhEarlyError||'no early error'))+', init failed before listeners'):'Module never started (import/CDN failed or hung)';",
    "watchdog early status")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V63 applied')
