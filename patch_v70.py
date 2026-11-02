import pathlib, re
v64 = pathlib.Path('/tmp/v64.html').read_text()
start = v64.index("/* ============ GAME FLOW ============")
end = v64.index("try{ window.__nhCP='CP9 GAMEFLOW done'")
slice_text = v64[start:end]
def extract(name, next_name=None):
    rs = slice_text.index(f"function {name}(")
    if next_name:
        se = slice_text.index(f"function {next_name}(")
        return slice_text[rs:se].rstrip()
    # loseHeart is last: up to end of slice
    return slice_text[rs:].rstrip()
funcs = [
    ("startEscape", "cancelEscape"),
    ("cancelEscape", "loseHeart"),
    ("loseHeart", None),
]
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
t = p.read_text(encoding='utf-8')
assert "V69 • လွှာပြောင်း ပြန်ထည့် — အကုန်" in t
t = t.replace("V69 • လွှာပြောင်း ပြန်ထည့် — အကုန်", "V70 • GAME FLOW အပြည့် ပြန်ထည့် — အကုန်", 1)
for name, nxt in funcs:
    orig = extract(name, nxt)
    print(name, len(orig))
    pat = re.compile(r"function " + name + r"\([^)]*\)\{\}")
    m = pat.search(t)
    assert m, f"stub {name} not found"
    t = t.replace(m.group(0), orig, 1)
p.write_text(t, encoding='utf-8')
print('V70 applied')
