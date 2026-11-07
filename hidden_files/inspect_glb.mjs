import fs from 'fs';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import * as THREE from 'three';
const files = process.argv.slice(2);
const loader = new GLTFLoader();
for (const f of files) {
  const buf = fs.readFileSync(f);
  const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  try {
    const gltf = await loader.parseAsync(ab, '');
    let meshes = 0, tris = 0, mats = new Set(), texs = new Set(), skins = 0, anims = gltf.animations.length;
    const box = new THREE.Box3();
    gltf.scene.traverse(o => {
      if (o.isMesh) {
        meshes++;
        const g = o.geometry;
        if (g.index) tris += g.index.count / 3; else if (g.attributes.position) tris += g.attributes.position.count / 3;
        if (o.material) { const ms = Array.isArray(o.material) ? o.material : [o.material]; for (const m of ms) { mats.add(m.name || m.type); for (const k of ['map','normalMap','roughnessMap','metalnessMap','emissiveMap']) if (m[k] && m[k].image) texs.add((m[k].image.src || 'embedded').slice(0, 40)); } }
        if (o.skeleton || o.isSkinnedMesh) skins++;
      }
    });
    box.setFromObject(gltf.scene);
    const s = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
    console.log(`${f.split('/').pop()}: ${(buf.length/1048576).toFixed(2)}MB meshes=${meshes} tris=${Math.round(tris)} mats=${mats.size} texs=${texs.size} skins=${skins} anims=${anims} bbox=${s.x.toFixed(1)}x${s.y.toFixed(1)}x${s.z.toFixed(1)} center=(${c.x.toFixed(1)},${c.y.toFixed(1)},${c.z.toFixed(1)})`);
  } catch (e) { console.log(`${f.split('/').pop()}: PARSE FAILED — ${e.message}`); }
}
