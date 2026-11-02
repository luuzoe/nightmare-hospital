import pathlib, re
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
# Version label
assert "V64 • handleStart အစောဆုံး — အကုန်" in t
t = t.replace("V64 • handleStart အစောဆုံး — အကုန်", "V65 • GAME FLOW စမ်းသပ် — အကုန်", 1)
# Find GAME FLOW header and CP9 marker, replace everything between with stubs
start = t.index("/* ============ GAME FLOW ============")
end = t.index("try{ window.__nhCP='CP9 GAMEFLOW done'")
slice_text = t[start:end]
print('GAME FLOW slice len', len(slice_text))
stubs = """/* ============ GAME FLOW ============ */
let _skipKeyShuffle=false;
function resetGame(){ S.playing=true; }
function saveProgress(){}
function continueGame(){}
function startGame(){ try{ $('startScreen').classList.add('hidden'); $('hud').classList.add('on'); }catch(e){} S.playing=true; try{ toast('V65 stub start'); }catch(e){} }
function pauseGame(){}
function resumeGame(){}
function neckSnapKill(){}
function endGame(win){}
function winGame(){}
function goToStage2(){}
function goToNextFloor(){}
function doFloorChange(){}
function startEscape(){}
function cancelEscape(){}
function loseHeart(){}
"""
t = t[:start] + stubs + t[end:]
p.write_text(t, encoding='utf-8')
print('V65 applied, GAME FLOW stubbed')
