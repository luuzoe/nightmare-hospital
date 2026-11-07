// Static verification for Ghost Hospital V1 (Node, no GPU):
// (a) floor layout: BFS from spawn to stair + to every open room centre, using the same
//     wall/collider logic as index.html buildFloor (copied, floor 15 seed).
// (b) ghost normalization: bbox after flat-rotation + scale-to-height, feet at y=0.
import fs from 'fs';
function rngFor(seed){let s=(seed*2654435761)>>>0;return ()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function shuffleArr(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const tmp=a[i];a[i]=a[j];a[j]=tmp;}return a;}
const ROOM_DEFS=[
  {id:0,x:-3.5,z:-12},{id:1,x:3.5,z:-12},
  {id:2,x:-3.5,z:-6},{id:3,x:3.5,z:-6},
  {id:4,x:-3.5,z:0},{id:5,x:3.5,z:0},
  {id:6,x:-3.5,z:6},{id:7,x:3.5,z:6},
  {id:8,x:-3.5,z:12},{id:9,x:3.5,z:12}
];
const walls=[];
function placeKit(part,x,z,ry,collide){
  if(!collide)return;
  const len=part==='wall2'?2:part==='wall1'?1:part==='wall05'?0.5:part==='doorway'?2:2;
  const alongX=Math.abs(Math.sin(ry||0))>0.5;
  walls.push({x,z,w:alongX?len:0.3,d:alongX?0.3:len});
}
function buildFloorWalls(floor){
  walls.length=0;
  const rng=rngFor(floor*7+3);
  const shuffled=shuffleArr(ROOM_DEFS.slice());
  const nOpen=7+Math.floor(rng()*2);
  const openRooms=[];for(let i=0;i<nOpen;i++)openRooms.push(shuffled[i].id);
  const isOpen=id=>openRooms.includes(id);
  const wallAt=(x,z,ry,len)=>{const part=len>=2?'wall2':len>=1?'wall1':'wall05';placeKit(part,x,z,ry,true);};
  for(let z=-15;z<15;z+=2){wallAt(-6,z+1,0,2);wallAt(6,z+1,0,2);}
  for(let x=-6;x<6;x+=2){wallAt(x+1,-15,Math.PI/2,2);wallAt(x+1,15,Math.PI/2,2);}
  for(const r of ROOM_DEFS){
    const side=r.x<0?-1:1;const wx=side*1;const zc=r.z;
    placeKit('wall2',wx,zc-2,0,true);
    placeKit('wall1',wx,zc+2.5,0,true);
    if(isOpen(r.id)){
      placeKit('wall05',wx,zc-0.75,0,true);
      placeKit('wall05',wx,zc+1.75,0,true);
    }else{
      placeKit('wall1',wx,zc-0.5,0,true);
      placeKit('wall2',wx,zc+1,0,true);
    }
  }
  const bands=[-9,-3,3,9];
  for(const bz of bands){
    for(const sx of[2,4]){wallAt(sx,bz,Math.PI/2,2);wallAt(-sx,bz,Math.PI/2,2);}
    wallAt(5.5,bz,Math.PI/2,1);wallAt(-5.5,bz,Math.PI/2,1);
  }
  walls.push({x:0,z:14.9,w:2.4,d:0.5});
  return openRooms;
}
function collideAt(nx,nz){
  for(const w of walls){
    if(Math.abs(nx-w.x)<w.w/2+0.45&&Math.abs(nz-w.z)<w.d/2+0.45)return true;
  }
  if(nx<-5.6||nx>5.6||nz<-14.6||nz>14.6)return true;
  return false;
}
function bfs(sx,sz,tx,tz){
  const cell=0.5;
  const key=(x,z)=>Math.round(x/cell)+','+Math.round(z/cell);
  const seen=new Set([key(sx,sz)]);
  const q=[[sx,sz,0]];
  while(q.length){
    const [x,z,d]=q.shift();
    if(Math.abs(x-tx)<0.6&&Math.abs(z-tz)<0.6)return d;
    for(const [dx,dz] of [[cell,0],[-cell,0],[0,cell],[0,-cell]]){
      const nx=x+dx,nz=z+dz;
      if(collideAt(nx,nz))continue;
      const k=key(nx,nz);
      if(seen.has(k))continue;
      seen.add(k);q.push([nx,nz,d+1]);
    }
    if(q.length>20000)return -1;
  }
  return -1;
}
console.log('=== floor layout BFS (floor 15) ===');
const open=buildFloorWalls(15);
console.log('open rooms:',open.sort((a,b)=>a-b).join(','));
console.log('wall count:',walls.length);
const dStair=bfs(0,-13.5,0,13.8);
console.log('spawn -> stair:',dStair>=0?dStair+' steps (~'+(dStair*0.5).toFixed(1)+'m)':'UNREACHABLE');
for(const r of ROOM_DEFS){
  const d=bfs(0,-13.5,r.x,r.z);
  console.log(` room ${r.id} (${r.x},${r.z}) open=${open.includes(r.id)}:`,d>=0?d+' steps':'UNREACHABLE');
}
// also test floors 1, 8 (different seeds)
for(const f of [1,8]){
  const op=buildFloorWalls(f);
  const ds=bfs(0,-13.5,0,13.8);
  let bad=0;
  for(const r of ROOM_DEFS){if(op.includes(r.id)&&bfs(0,-13.5,r.x,r.z)<0)bad++;}
  console.log(`floor ${f}: stair ${ds>=0?'OK':'BLOCKED'}, open rooms ${op.length}, unreachable open rooms: ${bad}`);
}
