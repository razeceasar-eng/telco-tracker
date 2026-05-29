const CACHE_NAME = 'xfinity-tracker-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

// Install Lifecycle Event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

// Fetch Network Requests (Allows the app to load instantly)
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
