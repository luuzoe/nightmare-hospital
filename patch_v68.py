import pathlib
v64 = pathlib.Path('/tmp/v64.html').read_text()
start = v64.index("/* ============ GAME FLOW ============")
end = v64.index("try{ window.__nhCP='CP9 GAMEFLOW done'")
slice_text = v64[start:end]
def extract(name, next_name):
    rs = slice_text.index(f"function {name}(")
    se = slice_text.index(f"function {next_name}(")
    return slice_text[rs:se].rstrip()
funcs = [
    ("pauseGame", "resumeGame"),
    ("resumeGame", "neckSnapKill"),
    ("neckSnapKill", "endGame"),
    ("endGame", "winGame"),
    ("winGame", "goToStage2"),
]
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V67 • save+continue+start ပြန်ထည့် — အကုန်" in t
t = t.replace("V67 • save+continue+start ပြန်ထည့် — အကုန်", "V68 • pause+end+win ပြန်ထည့် — အကုန်", 1)
for name, nxt in funcs:
    orig = extract(name, nxt)
    print(name, len(orig))
    # stub forms: function name(){} or function endGame(win){}
    import re
    pat = re.compile(r"function " + name + r"\([^)]*\)\{\}")
    m = pat.search(t)
    assert m, f"stub {name} not found"
    t = t.replace(m.group(0), orig, 1)
p.write_text(t, encoding='utf-8')
print('V68 applied')
