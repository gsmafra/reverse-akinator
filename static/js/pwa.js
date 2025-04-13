document.addEventListener("DOMContentLoaded", () => {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('Service Worker registered with scope:', registration.scope);
                })
                .catch(err => {
                    console.log('Service Worker registration failed:', err);
                });
        });
    }
});

self.addEventListener('install', function(event) {
    // Perform install steps if necessary, e.g., caching
    console.log('Service Worker installing.');
});

self.addEventListener('fetch', function(event) {
    // You can intercept requests here
    event.respondWith(fetch(event.request));
});
