// יומן מתאמן: offline cache. App shell is precached; exercise images are cached in the background.
const VER = "__VER__", SHELL = "shell-" + VER, IMG = "img-v1";
const SHELL_FILES = __SHELL__, IMGS = __IMGS__;
self.addEventListener("install", e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k.startsWith("shell-") && k !== SHELL) await caches.delete(k);
  await self.clients.claim();
  const c = await caches.open(IMG); const have = new Set((await c.keys()).map(r => new URL(r.url).pathname));
  for (const p of IMGS) { const u = new URL(p, self.registration.scope); if (!have.has(u.pathname)) { try { const r = await fetch(u); if (r.ok) await c.put(u, r); } catch {} } }
})()); });
self.addEventListener("fetch", e => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url); if (url.origin !== location.origin) return;
  if (req.mode === "navigate" || url.pathname.endsWith("/index.html")) { // network first (3 s), then cache: fresh when online, works offline
    e.respondWith((async () => { const c = await caches.open(SHELL);
      try { const r = await Promise.race([fetch(req), new Promise((_, rej) => setTimeout(rej, 3000))]); if (r.ok) c.put("index.html", r.clone()); return r; }
      catch { return (await c.match("index.html")) || (await caches.match(req)) || Response.error(); } })());
    return;
  }
  e.respondWith((async () => { const hit = await caches.match(req, { ignoreSearch: true }); if (hit) return hit;
    const r = await fetch(req); if (r.ok && /\/(ex|ek)\//.test(url.pathname)) (await caches.open(IMG)).put(req, r.clone()); return r; })());
});
