#!/usr/bin/env python3
"""Pack a Sketchfab glTF download (scene.gltf + scene.bin + textures) into a single .glb.
Usage: python3 gltf_to_glb.py <dir-with-scene.gltf> <out.glb>
- Reads scene.gltf, embeds the external .bin buffer and all image files into one BIN chunk.
- Keeps the original bufferViews (they index buffer 0); appends a bufferView per image.
- Handles KHR_materials_pbrSpecularGlossiness by warning (three.js r160 does not support it;
  use Blender or the game's material rewrite if a model comes out grey — see ASSETS.md lesson).
- Refuses Draco-compressed glTF (needs a Draco decoder; use Blender instead).
Pure stdlib. Test: run with no args to self-test on a synthetic glTF.
"""
import json, struct, sys, os

def align4(n): return (n + 3) & ~3

def pack(gltf_dir, out_path):
    gpath = os.path.join(gltf_dir, 'scene.gltf')
    if not os.path.exists(gpath):
        # allow pointing at the .gltf directly
        gpath = gltf_dir if gltf_dir.endswith('.gltf') else gpath
        gltf_dir = os.path.dirname(gpath)
    g = json.load(open(gpath, encoding='utf-8'))
    if 'extensionsUsed' in g and 'KHR_draco_mesh_compression' in g['extensionsUsed']:
        raise SystemExit('ERROR: Draco-compressed glTF — convert with Blender instead.')
    if 'extensionsUsed' in g and 'KHR_materials_pbrSpecularGlossiness' in g['extensionsUsed']:
        print('WARN: KHR_materials_pbrSpecularGlossiness present — three.js r160 ignores it; '
              'rewrite materials to pbrMetallicRoughness if the model renders grey.')
    # --- buffer 0 (the .bin) ---
    bufs = g.get('buffers', [])
    if not bufs: raise SystemExit('ERROR: no buffers in glTF')
    bin_uri = bufs[0].get('uri', '')
    if bin_uri.startswith('data:'):
        raise SystemExit('ERROR: buffer already embedded; nothing to pack.')
    bin_path = os.path.join(gltf_dir, bin_uri)
    bin_data = open(bin_path, 'rb').read()
    if len(bin_data) != bufs[0].get('byteLength', len(bin_data)):
        print(f"WARN: .bin size {len(bin_data)} != declared {bufs[0].get('byteLength')}; using actual.")
    chunks = [bin_data]
    off = len(bin_data)
    # --- images -> bufferViews ---
    for img in g.get('images', []):
        uri = img.get('uri')
        if not uri or uri.startswith('data:'):
            continue
        data = open(os.path.join(gltf_dir, uri), 'rb').read()
        pad = align4(off) - off
        if pad: chunks.append(b'\x00' * pad); off += pad
        bv = {'buffer': 0, 'byteOffset': off, 'byteLength': len(data)}
        g.setdefault('bufferViews', []).append(bv)
        img['bufferView'] = len(g['bufferViews']) - 1
        img['mimeType'] = 'image/png' if uri.lower().endswith('.png') else 'image/jpeg'
        del img['uri']
        chunks.append(data); off += len(data)
    # --- finalize ---
    g['buffers'] = [{'byteLength': align4(off)}]
    if 'bufferViews' in g:
        for bv in g['bufferViews']:
            if bv.get('buffer', 0) != 0: bv['buffer'] = 0
    j = json.dumps(g, separators=(',', ':')).encode('utf-8')
    j += b' ' * (align4(len(j)) - len(j))
    bin_total = align4(off)
    bin_blob = b''.join(chunks)
    bin_blob += b'\x00' * (bin_total - len(bin_blob))
    glb = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(j) + 8 + len(bin_blob))
    glb += struct.pack('<II', len(j), 0x4E4F534A) + j
    glb += struct.pack('<II', len(bin_blob), 0x004E4942) + bin_blob
    open(out_path, 'wb').write(glb)
    print(f'WROTE {out_path}  {len(glb)} bytes  ({len(g.get("images", []))} images embedded, '
          f'{len(g.get("meshes", []))} meshes, {len(g.get("bufferViews", []))} bufferViews)')

def selftest():
    import base64, tempfile
    d = tempfile.mkdtemp()
    # minimal glTF: 1 triangle, 1 buffer, 1 tiny PNG image
    pos = struct.pack('<9f', 0,0,0, 1,0,0, 0,1,0)
    idx = struct.pack('<3H', 0,1,2)
    bindata = pos + idx
    png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==')
    open(os.path.join(d,'scene.bin'),'wb').write(bindata)
    open(os.path.join(d,'tex.png'),'wb').write(png)
    g = {"asset":{"version":"2.0"},"scene":0,"scenes":[{"nodes":[0]}],"nodes":[{"mesh":0}],
         "meshes":[{"primitives":[{"attributes":{"POSITION":0},"indices":1,"material":0}]}],
         "materials":[{"pbrMetallicRoughness":{"baseColorTexture":{"index":0}}}],
         "textures":[{"source":0}],"images":[{"uri":"tex.png"}],
         "accessors":[{"bufferView":0,"componentType":5126,"count":3,"type":"VEC3","max":[1,1,0],"min":[0,0,0]},
                      {"bufferView":1,"componentType":5123,"count":3,"type":"SCALAR"}],
         "bufferViews":[{"buffer":0,"byteOffset":0,"byteLength":36},{"buffer":0,"byteOffset":36,"byteLength":6}],
         "buffers":[{"uri":"scene.bin","byteLength":len(bindata)}]}
    json.dump(g, open(os.path.join(d,'scene.gltf'),'w'))
    out = os.path.join(d,'test.glb')
    pack(d, out)
    print('selftest GLB OK:', os.path.getsize(out), 'bytes')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        selftest()
    elif len(sys.argv) == 3:
        pack(sys.argv[1], sys.argv[2])
    else:
        print('usage: gltf_to_glb.py <dir-with-scene.gltf> <out.glb>   (no args = self-test)')
        sys.exit(2)
