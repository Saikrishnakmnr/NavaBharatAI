const V='nava-16.2.0-free-chat-1';
const A=['/','/index.html','/styles.css','/app.js','/chat.js','/chat.css','/marketplace.js','/growth.js','/config.js','/manifest.webmanifest','/assets/brand-logo.svg','/assets/brand-mark.svg'];
const STATIC=new Set(A);
self.addEventListener('install',e=>e.waitUntil(caches.open(V).then(c=>c.addAll(A)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(x=>Promise.all(x.filter(k=>k.startsWith('nava-')&&k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  const url=new URL(e.request.url);
  // Never cache AI, Supabase, maintenance, payments or third-party traffic.
  if(e.request.method!=='GET'||url.origin!==self.location.origin||!STATIC.has(url.pathname))return;
  e.respondWith(
    fetch(e.request).then(r=>{
      if(r.ok&&!/no-store/i.test(r.headers.get('Cache-Control')||'')){
        const c=r.clone();e.waitUntil(caches.open(V).then(x=>x.put(url.pathname,c)).catch(()=>{}));
      }
      return r;
    }).catch(async()=>{
      const cached=await caches.match(url.pathname);
      return cached||new Response('Offline',{status:503,headers:{'Content-Type':'text/plain'}});
    })
  );
});
