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
def cp(anchor, label):
    global t
    marker = "try{ window.__nhCP='%s'; const _bs=document.getElementById('bootStatus'); if(_bs) _bs.textContent='%s'; }catch(e){}\n" % (label, label)
    rep(anchor, marker + anchor, 'cp ' + label)

rep("V58 • import ပျက်လား init ပျက်လား — အကုန်",
    "V59 • ဘယ်အပိုင်းမှာ ရပ်လဲ — အကုန်",
    "version v59")
cp("/* ============ AUDIO (synth, no files) ============ */", "CP1 STATE done")
cp("/* ============ THREE SETUP ============ */", "CP2 AUDIO done")
cp("/* ============ MAP ============ */", "CP3 THREE done")
cp("/* ============ KEYS ============ */", "CP4 MAP done")
cp("/* ============ COLLISION HELPERS ============ */", "CP5 KEYS+GORE done")
cp("/* ============ CHARACTERS (real GLB from website) ============ */", "CP6 COLLISION done")
cp("/* ============ CONTROLS ============ */", "CP7 CHARACTERS done")
cp("/* ============ GAME FLOW ============", "CP8 CONTROLS done")
cp("let _starting=false;", "CP9 GAMEFLOW done")
# Watchdog: report last checkpoint reached
rep("var kind=window.__nhModuleStarted?'Module started but init failed before listeners':'Module never started (import/CDN failed or hung)';",
    "var kind=window.__nhModuleStarted?('Module started, last checkpoint: '+(window.__nhCP||'none')+', init failed before listeners'):'Module never started (import/CDN failed or hung)';",
    "watchdog cp")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V59 applied')
