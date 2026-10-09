const V='nava-16.1.0';
const A=['/','/index.html','/styles.css','/app.js','/config.js','/manifest.webmanifest','/assets/brand-logo.svg','/assets/brand-mark.svg','/version.json'];
self.addEventListener('install',e=>e.waitUntil(caches.open(V).then(c=>c.addAll(A)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(x=>Promise.all(x.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(
    fetch(e.request).then(r=>{
      const c=r.clone();
      caches.open(V).then(x=>x.put(e.request,c)).catch(()=>{});
      return r;
    }).catch(async()=>{
      const cached=await caches.match(e.request);
      return cached||new Response('Offline',{status:503,headers:{'Content-Type':'text/plain'}});
    })
  );
});
