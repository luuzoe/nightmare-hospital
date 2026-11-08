// V3 diagnosis: (1) doorway mesh opening (visual hole) — where + how wide;
// (2) collider-model room entry simulation with the real collideAt + buildFloor walls.
import fs from 'fs';

const KIT = 'hospital/modular-kit.glb';
const buf = fs.readFileSync(KIT);
const jlen = buf.readUInt32LE(12);
const j = JSON.parse(buf.subarray(20, 20 + jlen).toString());
const binStart = 20 + jlen + 8;

function mat4(t, r, s) {
  const [x, y, z, w] = r || [0, 0, 0, 1];
  const [sx, sy, sz] = s || [1, 1, 1];
  const [tx, ty, tz] = t || [0, 0, 0];
  const x2 = x + x, y2 = y + y, z2 = z + z;
  const xx = x * x2, xy = x * y2, xz = x * z2, yy = y * y2, yz = y * z2, zz = z * z2, wx = w * x2, wy = w * y2, wz = w * z2;
  const R = [[1 - (yy + zz), xy - wz, xz + wy], [xy + wz, 1 - (xx + zz), yz - wx], [xz - wy, yz + wx, 1 - (xx + yy)]];
  return [[R[0][0] * sx, R[0][1] * sy, R[0][2] * sz, tx], [R[1][0] * sx, R[1][1] * sy, R[1][2] * sz, ty], [R[2][0] * sx, R[2][1] * sy, R[2][2] * sz, tz]];
}
function mul(A, B) {
  const C = [[0,0,0,0],[0,0,0,0],[0,0,0,0]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 4; j++) { let v = 0; for (let k = 0; k < 3; k++) v += A[i][k] * B[k][j]; if (j === 3) v += A[i][3]; C[i][j] = v; }
  return C;
}
function apply(M, p) { return [M[0][0]*p[0]+M[0][1]*p[1]+M[0][2]*p[2]+M[0][3], M[1][0]*p[0]+M[1][1]*p[1]+M[1][2]*p[2]+M[1][3], M[2][0]*p[0]+M[2][1]*p[1]+M[2][2]*p[2]+M[2][3]]; }
function readAccessor(ai) {
  const a = j.accessors[ai];
  const bv = j.bufferViews[a.bufferView];
  const base = binStart + (bv.byteOffset || 0) + (a.byteOffset || 0);
  const ncomp = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 }[a.type];
  const out = [];
  for (let i = 0; i < a.count; i++) {
    const o = base + i * ncomp * (a.componentType === 5126 ? 4 : a.componentType === 5123 ? 2 : 4);
    const v = [];
    for (let c = 0; c < ncomp; c++) {
      if (a.componentType === 5126) v.push(buf.readFloatLE(o + c * 4));
      else if (a.componentType === 5123) v.push(buf.readUInt16LE(o + c * 2));
      else v.push(buf.readUInt32LE(o + c * 4));
    }
    out.push(v);
  }
  return out;
}

// ---- find doorway node + its world matrix ----
const nodes = j.nodes || [];
const parents = new Map();
nodes.forEach((n, i) => (n.children || []).forEach(c => parents.set(c, i)));
const roots = nodes.map((_, i) => i).filter(i => !parents.has(i));
let doorNode = null, doorWorld = null;
const walk = (ni, M) => {
  const n = nodes[ni];
  const local = n.matrix ? [[n.matrix[0], n.matrix[4], n.matrix[8], n.matrix[12]], [n.matrix[1], n.matrix[5], n.matrix[9], n.matrix[13]], [n.matrix[2], n.matrix[6], n.matrix[10], n.matrix[14]]] : mat4(n.translation, n.rotation, n.scale);
  const W = M ? mul(M, local) : local;
  if (n.name === 'SM_Doorway_2*3_1_M_modular_0') { doorNode = n; doorWorld = W; }
  (n.children || []).forEach(c => walk(c, W));
};
roots.forEach(r => walk(r, null));
if (!doorNode) { console.log('DOORWAY NODE NOT FOUND'); process.exit(1); }
const mesh = j.meshes[doorNode.mesh];
const prim = mesh.primitives[0];
const pos = readAccessor(prim.attributes.POSITION);
const idx = prim.indices !== undefined ? readAccessor(prim.indices).map(v => v[0]) : pos.map((_, i) => i);
// bake: apply world matrix, then recenter XZ + base Y=0 (same as bakeKitPiece)
let pts = pos.map(p => apply(doorWorld, p));
let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
for (const p of pts) for (let i = 0; i < 3; i++) { mn[i] = Math.min(mn[i], p[i]); mx[i] = Math.max(mx[i], p[i]); }
const cx = (mn[0] + mx[0]) / 2, cz = (mn[2] + mx[2]) / 2;
pts = pts.map(p => [p[0] - cx, p[1] - mn[1], p[2] - cz]);
mn = [1e9, 1e9, 1e9]; mx = [-1e9, -1e9, -1e9];
for (const p of pts) for (let i = 0; i < 3; i++) { mn[i] = Math.min(mn[i], p[i]); mx[i] = Math.max(mx[i], p[i]); }
console.log('doorway baked bbox x[' + mn[0].toFixed(2) + ',' + mx[0].toFixed(2) + '] y[' + mn[1].toFixed(2) + ',' + mx[1].toFixed(2) + '] z[' + mn[2].toFixed(2) + ',' + mx[2].toFixed(2) + ']');
// length axis = the wider horizontal axis
const lenAxis = (mx[0] - mn[0]) > (mx[2] - mn[2]) ? 0 : 2;
console.log('length axis: ' + (lenAxis === 0 ? 'X' : 'Z') + ' (' + (mx[lenAxis] - mn[lenAxis]).toFixed(2) + 'm), thickness ' + (mx[2 - lenAxis] - mn[2 - lenAxis]).toFixed(2) + 'm');
// rasterize (length, y) plane, 0.05m cells; mark cells covered by any triangle
const L0 = mn[lenAxis], L1 = mx[lenAxis], Y0 = 0, Y1 = 3;
const step = 0.05;
const nL = Math.ceil((L1 - L0) / step), nY = Math.ceil((Y1 - Y0) / step);
const grid = Array.from({ length: nY }, () => new Uint8Array(nL));
const triCover = (a, b, c) => {
  const lmin = Math.min(a[lenAxis], b[lenAxis], c[lenAxis]), lmax = Math.max(a[lenAxis], b[lenAxis], c[lenAxis]);
  const ymin = Math.min(a[1], b[1], c[1]), ymax = Math.max(a[1], b[1], c[1]);
  const i0 = Math.max(0, Math.floor((lmin - L0) / step)), i1 = Math.min(nL - 1, Math.floor((lmax - L0) / step));
  const j0 = Math.max(0, Math.floor((ymin - Y0) / step)), j1 = Math.min(nY - 1, Math.floor((ymax - Y0) / step));
  for (let jj = j0; jj <= j1; jj++) for (let ii = i0; ii <= i1; ii++) grid[jj][ii] = 1;
};
for (let t = 0; t + 2 < idx.length; t += 3) triCover(pts[idx[t]], pts[idx[t + 1]], pts[idx[t + 2]]);
// ASCII map of the wall (rows y=3 top -> y=0 bottom)
console.log('wall map (rows y 3.0->0, cols length -1..+1, #=solid .=hole):');
for (let jj = nY - 1; jj >= 0; jj--) {
  let row = '';
  for (let ii = 0; ii < nL; ii++) row += grid[jj][ii] ? '#' : '.';
  if (jj % 4 === 0) console.log((jj * step).toFixed(2) + ' ' + row);
}
// opening: widest continuous empty run in the walkable band y in [0.2, 2.2]
let best = { w: 0, l0: 0, l1: 0 };
for (let jj = 0; jj < nY; jj++) {
  const y = jj * step;
  if (y < 0.2 || y > 2.2) continue;
  let run = 0, start = 0;
  for (let ii = 0; ii <= nL; ii++) {
    if (ii < nL && !grid[jj][ii]) { if (run === 0) start = ii; run++; }
    else { if (run > best.w) best = { w: run, l0: L0 + start * step, l1: L0 + (start + run) * step }; run = 0; }
  }
}
console.log('widest empty run in walkable band: ' + (best.w * step).toFixed(2) + 'm, length range [' + best.l0.toFixed(2) + ', ' + best.l1.toFixed(2) + '] (piece centre = 0)');

// ---- part 2: V3 collider entry simulation (radius 0.38, beds far wall, wheelchairs in rooms) ----
const walls = [];
function placeWall(x, z, ry, len) {
  const alongX = Math.abs(Math.sin(ry || 0)) > 0.5;
  walls.push({ x, z, w: alongX ? len : 0.3, d: alongX ? 0.3 : len });
}
function collideAt(nx, nz) {
  for (const w of walls) {
    if (Math.abs(nx - w.x) < w.w / 2 + 0.38 && Math.abs(nz - w.z) < w.d / 2 + 0.38) return true;
  }
  if (nx < -5.6 || nx > 5.6 || nz < -14.6 || nz > 14.6) return true;
  return false;
}
// room C1 (west, zc=0) open + neighbours B1/D1 open; bands at z=-3,3
for (const zc of [-6, 0, 6]) {
  const wx = -1;
  placeWall(wx, zc - 2, 0, 2); placeWall(wx, zc + 2.5, 0, 1);
  placeWall(wx, zc - 0.75, 0, 0.5); placeWall(wx, zc + 1.75, 0, 0.5);
  // doorway at (wx, zc+0.5): NO collider
}
for (const bz of [-3, 3]) {
  for (const sx of [2, 4]) { placeWall(sx, bz, Math.PI / 2, 2); placeWall(-sx, bz, Math.PI / 2, 2); }
  placeWall(5.5, bz, Math.PI / 2, 1); placeWall(-5.5, bz, Math.PI / 2, 1);
}
for (let z = -15; z < 15; z += 2) { placeWall(-6, z + 1, 0, 2); placeWall(6, z + 1, 0, 2); }
for (let x = -6; x < 6; x += 2) { placeWall(x + 1, -15, Math.PI / 2, 2); placeWall(x + 1, 15, Math.PI / 2, 2); }
// V3 props: bed at far wall (ry~PI/2 -> collider 0.9 x 1.9), wheelchair in room (0.8 x 0.8)
// worst case: bed z = zc+1.1 (nearest doorway), wheelchair z = zc-1.0
walls.push({ x: -5.05, z: 1.1, w: 0.9, d: 1.9 });   // bed C1
walls.push({ x: -4.9, z: -1.0, w: 0.8, d: 0.8 });   // wheelchair C1
walls.push({ x: -5.05, z: -6 + 1.1, w: 0.9, d: 1.9 }); // bed B1
// movePlayer collision resolution: full move, else x-only, else z-only
function stepMove(px, pz, tx, tz) {
  const dx = tx - px, dz = tz - pz, d = Math.hypot(dx, dz);
  if (d < 0.01) return [px, pz, true];
  const s = Math.min(0.05, d);
  const vx = dx / d * s, vz = dz / d * s;
  const nx = px + vx, nz = pz + vz;
  if (!collideAt(nx, pz)) px = nx;
  if (!collideAt(px, nz)) pz = nz;
  return [px, pz, false];
}
function tryEntry(name, sx, sz, tx, tz) {
  let px = sx, pz = sz, stuck = 0, lastD = 1e9;
  for (let i = 0; i < 3000; i++) {
    const d = Math.hypot(tx - px, tz - pz);
    if (d < 0.3) { console.log(name + ': REACHED in ' + i + ' steps'); return true; }
    if (Math.abs(d - lastD) < 1e-9) { if (++stuck > 40) { console.log(name + ': STUCK at (' + px.toFixed(2) + ',' + pz.toFixed(2) + ') dist to target ' + d.toFixed(2) + 'm'); return false; } }
    else stuck = 0;
    lastD = d;
    [px, pz] = stepMove(px, pz, tx, tz);
  }
  console.log(name + ': TIMEOUT at (' + px.toFixed(2) + ',' + pz.toFixed(2) + ')');
  return false;
}
console.log('--- V3 entry simulation (radius 0.38, beds far wall, wheelchairs in rooms) ---');
tryEntry('A straight (0,0.5)->room centre (-3.5,0)', 0, 0.5, -3.5, 0);
tryEntry('B angled from north (0,-2)->(-3.5,0)', 0, -2, -3.5, 0);
tryEntry('C angled from south (0,3)->(-3.5,0)', 0, 3, -3.5, 0);
tryEntry('D to far corner past bed (-4.2,0.5)', 0, 0.5, -4.2, 0.5);
tryEntry('E corridor traversal (0,-13.5)->(0,14.5)', 0, -13.5, 0, 14.5);
tryEntry('F corridor traversal south->north (0,14)->(0,-13.5)', 0, 14, 0, -13.5);
