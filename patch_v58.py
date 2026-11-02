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

rep("V57 • tap မြင်စေ + fallback — အကုန်",
    "V58 • import ပျက်လား init ပျက်လား — အကုန်",
    "version v58")
# New bootError element, separate from startError so inline fallback never overwrites it
rep('<p id="bootStatus" style="font-size:11px;color:#888;margin-top:2px">JS loading…</p>',
    '<p id="bootStatus" style="font-size:11px;color:#888;margin-top:2px">JS loading…</p>\n  <p id="bootError" style="color:#ff6666;font-size:12px;display:none"></p>',
    "booterror element")
# Classic-script watchdog: runs even if module JS never runs. Captures errors, and after 8s reports import vs init.
rep("""<script>
window.addEventListener('error',function(e){ try{ var ld=document.getElementById('load'); if(ld) ld.style.display='none'; var el=document.getElementById('startError'); if(el){ el.textContent='⚠️ JS Error: '+(e.message||'unknown'); el.style.display='block'; } }catch(err){} });
</script>""",
    """<script>
window.__nhBootErrors=[];
window.addEventListener('error',function(e){ try{ window.__nhBootErrors.push(e.message||'unknown error'); var ld=document.getElementById('load'); if(ld) ld.style.display='none'; var el=document.getElementById('startError'); if(el){ el.textContent='⚠️ JS Error: '+(e.message||'unknown'); el.style.display='block'; } }catch(err){} });
window.addEventListener('unhandledrejection',function(e){ try{ window.__nhBootErrors.push('promise: '+(e.reason&&e.reason.message?e.reason.message:e.reason)); }catch(err){} });
setTimeout(function(){
  try{
    if(window.__nhStart) return;
    var be=document.getElementById('bootError'); if(!be) return;
    var errs=window.__nhBootErrors.length?window.__nhBootErrors.join(' | '):'no error event captured';
    var kind=window.__nhModuleStarted?'Module started but init failed before listeners':'Module never started (import/CDN failed or hung)';
    be.textContent='⚠️ Boot failed: '+kind+'. Errors: '+errs;
    be.style.display='block';
  }catch(err){}
},8000);
</script>""",
    "watchdog classic")
# Module top marker: first statement after imports, so import failure vs init throw can be distinguished
rep("""import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';""",
    """import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
try{ window.__nhModuleStarted=true; const bs0=document.getElementById('bootStatus'); if(bs0) bs0.textContent='Module started…'; }catch(e){}""",
    "module started marker")
if miss:
    print('MISSES:', miss); raise SystemExit(1)
p.write_text(t, encoding='utf-8')
print('V58 applied')
