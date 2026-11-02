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

rep("V60 • GAME FLOW ထဲ ဘယ် function လဲ — အကုန်",
    "V61 • listener အစောဆုံး တပ် — အကုန်",
    "version v61")
# Move _starting to top of module, so early listeners can use it without TDZ
rep("""try{ window.__nhModuleStarted=true; const bs0=document.getElementById('bootStatus'); if(bs0) bs0.textContent='Module started…'; }catch(e){}""",
    """try{ window.__nhModuleStarted=true; const bs0=document.getElementById('bootStatus'); if(bs0) bs0.textContent='Module started…'; }catch(e){}
let _starting=false;
try{ const _sb=document.getElementById('startBtn'); if(_sb){ _sb.addEventListener('touchstart',handleStart,{passive:false}); _sb.addEventListener('pointerdown',handleStart); _sb.addEventListener('click',handleStart); window.__nhStart=handleStart; const _bs=document.getElementById('bootStatus'); if(_bs) _bs.textContent='Early listeners ready'; } }catch(e){}""",
    "early listeners")
# Remove later _starting declaration to avoid duplicate let
rep("let _starting=false;\nfunction handleStart(e){",
    "function handleStart(e){",
    "remove later starting")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V61 applied')
