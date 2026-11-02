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

rep("V55 • Start ချက်ချင်း စစေ + error မြင်စေ — အကုန်",
    "V56 • main thread လွတ် — Start မစခင် render ရပ် — အကုန်",
    "version v56")
# Key fix: do NOT render the invisible game canvas before Start. Start screen covers it completely,
# so rendering every frame before Start is pure waste that saturates the main thread and blocks taps.
rep("""function animate(){
  requestAnimationFrame(animate);
  const dt=Math.min(0.05,clock.getDelta());
  update(dt);
  renderer.render(scene,camera);
}""",
    """function animate(){
  requestAnimationFrame(animate);
  if(!S.playing) return; // V56: start screen covers canvas, rendering before Start only blocks taps
  const dt=Math.min(0.05,clock.getDelta());
  update(dt);
  renderer.render(scene,camera);
}""",
    "no render before start v56")
# Stagger large GLB loads after the start screen shows, with yields between groups, so taps can get through
rep("""loadCharacter().then(ok=>{
  loadCorpses(); loadGhost(); loadWanderingGhosts();
  $('load').style.display='none';""",
    """loadCharacter().then(async ok=>{
  $('load').style.display='none';
  await new Promise(r=>setTimeout(r,50));
  await loadCorpses();
  await new Promise(r=>setTimeout(r,50));
  await loadGhost();
  await new Promise(r=>setTimeout(r,50));
  await loadWanderingGhosts();""",
    "stagger glb loads v56")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V56 applied')
