// Ghost Hospital service worker — cache the app shell + assets, network-first for HTML.
const CACHE = 'ghost-hospital-v16';
const CORE = [
  './', 'index.html', 'manifest.json', 'icon-192.png', 'icon-512.png',
  'hospital/modular-kit.glb', 'hospital/abandoned-hospital.glb',
  'ghosts/samara.glb', 'ghosts/bubble-head-nurse.glb', 'ghosts/scary-doll.glb', 'ghosts/spider-witch.glb',
  'sounds/thevoicejournals__devil-beast.mp3', 'sounds/daandraait__slow-heartbeat.mp3',
  'sounds/kyles__gate-big-rusty-metal-door-garage-open-heavy-creak-rattle.mp3',
  'sounds/kkenny101__loopable-filtered-rain-resonance-drone.mp3', 'sounds/ienba__footsteps-on-tile.mp3'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  const isHTML = url.pathname.endsWith('index.html') || url.pathname.endsWith('/');
  if (isHTML) {
    e.respondWith(fetch(e.request).then(r => {
      const c = r.clone();
      caches.open(CACHE).then(cc => cc.put(e.request, c));
      return r;
    }).catch(() => caches.match(e.request)));
  } else {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(nr => {
      const c = nr.clone();
      caches.open(CACHE).then(cc => cc.put(e.request, c));
      return nr;
    })));
  }
});
