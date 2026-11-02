import pathlib, re
v64 = pathlib.Path('/tmp/v64.html').read_text()
start = v64.index("/* ============ GAME FLOW ============")
end = v64.index("try{ window.__nhCP='CP9 GAMEFLOW done'")
slice_text = v64[start:end]
# Extract resetGame: from 'function resetGame(){' to just before 'function saveProgress(){'
rs = slice_text.index("function resetGame(){")
se = slice_text.index("function saveProgress(){")
reset_text = slice_text[rs:se]
print('resetGame len', len(reset_text))
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V65 • GAME FLOW စမ်းသပ် — အကုန်" in t
t = t.replace("V65 • GAME FLOW စမ်းသပ် — အကုန်", "V66 • resetGame ပြန်ထည့် — အကုန်", 1)
assert "function resetGame(){ S.playing=true; }" in t
t = t.replace("function resetGame(){ S.playing=true; }", reset_text.rstrip(), 1)
p.write_text(t, encoding='utf-8')
print('V66 applied, resetGame restored')
