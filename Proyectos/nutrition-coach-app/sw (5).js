const CACHE_NAME = "coach-nutricional-v1";

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  // Deja pasar todo directo a la red; no cacheamos nada crítico
  // porque la app depende de datos frescos (API de Anthropic) y de tu localStorage.
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});
