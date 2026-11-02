import pathlib
v64 = pathlib.Path('/tmp/v64.html').read_text()
start = v64.index("/* ============ GAME FLOW ============")
end = v64.index("try{ window.__nhCP='CP9 GAMEFLOW done'")
slice_text = v64[start:end]
def extract(name, next_name):
    rs = slice_text.index(f"function {name}(")
    se = slice_text.index(f"function {next_name}(")
    return slice_text[rs:se].rstrip()
save_text = extract("saveProgress", "continueGame")
cont_text = extract("continueGame", "startGame")
start_text = extract("startGame", "pauseGame")
print('save', len(save_text), 'cont', len(cont_text), 'start', len(start_text))
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V66 • resetGame ပြန်ထည့် — အကုန်" in t
t = t.replace("V66 • resetGame ပြန်ထည့် — အကုန်", "V67 • save+continue+start ပြန်ထည့် — အကုန်", 1)
assert "function saveProgress(){}" in t
t = t.replace("function saveProgress(){}", save_text, 1)
assert "function continueGame(){}" in t
t = t.replace("function continueGame(){}", cont_text, 1)
# stub startGame in V65/V66: exact text, no regex (nested braces break [^}]*)
stub_start = "function startGame(){ try{ $('startScreen').classList.add('hidden'); $('hud').classList.add('on'); }catch(e){} S.playing=true; try{ toast('V65 stub start'); }catch(e){} }"
assert stub_start in t, "stub startGame not found"
t = t.replace(stub_start, start_text, 1)
p.write_text(t, encoding='utf-8')
print('V67 applied')
