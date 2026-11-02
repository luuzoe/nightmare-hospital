import pathlib
p = pathlib.Path('/home/hatch/workspace/nightmare-hospital/index.html')
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)
# Find handleStart definition line (single line, top-level function)
idx = None
for i, l in enumerate(lines):
    if l.startswith('function handleStart(e){'):
        idx = i
        break
assert idx is not None, 'handleStart not found'
handle_line = lines[idx]
print('handleStart at line', idx+1, 'len', len(handle_line))
# Remove it from original location
del lines[idx]
t = ''.join(lines)
# Insert it before early listeners try block, after _starting declaration
anchor = "let _starting=false;\n"
assert anchor in t, 'anchor not found'
t = t.replace(anchor, anchor + handle_line, 1)
# Version label
t = t.replace("V63 • early error သီးသန့် — အကုန်", "V64 • handleStart အစောဆုံး — အကုန်", 1)
p.write_text(t, encoding='utf-8')
print('V64 applied, handleStart moved to top')
