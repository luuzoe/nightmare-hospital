// Direct GLB JSON inspection — no three.js loader (avoids Node 'self' issue).
import fs from 'fs';
function mat4(t, r, s) {
  // compose T * R * S from nodeTRS (rotation as quaternion, may be absent)
  const [x, y, z, w] = r || [0, 0, 0, 1];
  const [sx, sy, sz] = s || [1, 1, 1];
  const [tx, ty, tz] = t || [0, 0, 0];
  const x2 = x + x, y2 = y + y, z2 = z + z;
  const xx = x * x2, xy = x * y2, xz = x * z2, yy = y * y2, yz = y * z2, zz = z * z2, wx = w * x2, wy = w * y2, wz = w * z2;
  const R = [[1 - (yy + zz), xy - wz, xz + wy], [xy + wz, 1 - (xx + zz), yz - wx], [xz - wy, yz + wx, 1 - (xx + yy)]];
  // M = T * R * S  (column-major application to [x,y,z])
  return [[R[0][0] * sx, R[0][1] * sy, R[0][2] * sz, tx], [R[1][0] * sx, R[1][1] * sy, R[1][2] * sz, ty], [R[2][0] * sx, R[2][1] * sy, R[2][2] * sz, tz]];
}
function mul(A, B) { // A * B (3x4 matrices)
  const C = [[0,0,0,0],[0,0,0,0],[0,0,0,0]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 4; j++) { let v = 0; for (let k = 0; k < 3; k++) v += A[i][k] * B[k][j]; if (j === 3) v += A[i][3]; C[i][j] = v; }
  return C;
}
function apply(M, p) { return [M[0][0]*p[0]+M[0][1]*p[1]+M[0][2]*p[2]+M[0][3], M[1][0]*p[0]+M[1][1]*p[1]+M[1][2]*p[2]+M[1][3], M[2][0]*p[0]+M[2][1]*p[1]+M[2][2]*p[2]+M[2][3]]; }
for (const f of process.argv.slice(2)) {
  const buf = fs.readFileSync(f);
  const jlen = buf.readUInt32LE(12);
  const j = JSON.parse(buf.subarray(20, 20 + jlen).toString());
  let tris = 0, prims = 0;
  const meshes = j.meshes || [];
  for (const m of meshes) for (const p of m.primitives) {
    prims++;
    const idx = p.indices !== undefined ? j.accessors[p.indices] : null;
    const pos = j.accessors[p.attributes.POSITION];
    tris += Math.round((idx ? idx.count : pos.count) / 3);
  }
  // world bbox via node tree
  const nodes = j.nodes || [];
  const parents = new Map();
  nodes.forEach((n, i) => (n.children || []).forEach(c => parents.set(c, i)));
  const roots = nodes.map((_, i) => i).filter(i => !parents.has(i));
  let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
  const walk = (ni, M) => {
    const n = nodes[ni];
    const local = n.matrix ? [[n.matrix[0], n.matrix[4], n.matrix[8], n.matrix[12]], [n.matrix[1], n.matrix[5], n.matrix[9], n.matrix[13]], [n.matrix[2], n.matrix[6], n.matrix[10], n.matrix[14]]] : mat4(n.translation, n.rotation, n.scale);
    const W = M ? mul(M, local) : local;
    if (n.mesh !== undefined) {
      for (const p of meshes[n.mesh].primitives) {
        const a = j.accessors[p.attributes.POSITION];
        if (!a.min) continue;
        for (const [x, y, z] of [[a.min[0], a.min[1], a.min[2]], [a.max[0], a.max[1], a.max[2]], [a.min[0], a.min[1], a.max[2]], [a.min[0], a.max[1], a.min[2]], [a.max[0], a.min[1], a.min[2]], [a.min[0], a.max[1], a.max[2]], [a.max[0], a.min[1], a.max[2]], [a.max[0], a.max[1], a.min[2]]]) {
          const q = apply(W, [x, y, z]);
          for (let i = 0; i < 3; i++) { mn[i] = Math.min(mn[i], q[i]); mx[i] = Math.max(mx[i], q[i]); }
        }
      }
    }
    (n.children || []).forEach(c => walk(c, W));
  };
  roots.forEach(r => walk(r, null));
  const size = mx.map((v, i) => (v - mn[i]).toFixed(1)).join('x');
  const ctr = mn.map((v, i) => ((v + mx[i]) / 2).toFixed(1)).join(',');
  const skins = (j.skins || []).length, anims = (j.animations || []).length;
  const imgs = (j.images || []).length, mats = (j.materials || []).length;
  const names = (j.nodes || []).map(n => n.name).filter(Boolean).slice(0, 12).join(', ');
  console.log(`${f.split('/').pop()}: ${(buf.length/1048576).toFixed(2)}MB meshes=${meshes.length} prims=${prims} tris=${tris} mats=${mats} images=${imgs} skins=${skins} anims=${anims} bbox=${size} center=(${ctr}) nodes=[${names}]`);
}
