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

rep("V61 • listener အစောဆုံး တပ် — အကုန်",
    "V62 • early error မြင်စေ — အကုန်",
    "version v62")
rep("""try{ const _sb=document.getElementById('startBtn'); if(_sb){ _sb.addEventListener('touchstart',handleStart,{passive:false}); _sb.addEventListener('pointerdown',handleStart); _sb.addEventListener('click',handleStart); window.__nhStart=handleStart; const _bs=document.getElementById('bootStatus'); if(_bs) _bs.textContent='Early listeners ready'; } }catch(e){}""",
    """try{ const _sb=document.getElementById('startBtn'); if(!_sb){ const _be=document.getElementById('bootError'); if(_be){ _be.textContent='⚠️ Early: startBtn not found in DOM'; _be.style.display='block'; } } else { _sb.addEventListener('touchstart',handleStart,{passive:false}); _sb.addEventListener('pointerdown',handleStart); _sb.addEventListener('click',handleStart); window.__nhStart=handleStart; const _bs=document.getElementById('bootStatus'); if(_bs) _bs.textContent='Early listeners ready'; } }catch(e){ window.__nhEarlyError=e.message||String(e); const _be2=document.getElementById('bootError'); if(_be2){ _be2.textContent='⚠️ Early listeners failed: '+(e.message||String(e)); _be2.style.display='block'; } }""",
    "early error visible")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V62 applied')
