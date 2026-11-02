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

rep("V59 • ဘယ်အပိုင်းမှာ ရပ်လဲ — အကုန်",
    "V60 • GAME FLOW ထဲ ဘယ် function လဲ — အကုန်",
    "version v60")
cp("function resetGame(){", "GF1 before resetGame")
cp("function saveProgress(){", "GF2 before saveProgress")
cp("function continueGame(){", "GF3 before continueGame")
cp("function startGame(){", "GF4 before startGame")
cp("function pauseGame(){", "GF5 before pauseGame")
cp("function endGame(win){", "GF6 before endGame")
cp("function goToNextFloor(){", "GF7 before goToNextFloor")
cp("function startEscape(){", "GF8 before startEscape")
cp("function loseHeart(){", "GF9 before loseHeart")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V60 applied')
