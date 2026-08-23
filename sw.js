/* Service worker minimo de mytbe.
   Existe por dos motivos: sin el, Android agrega la app como acceso directo
   con barra de navegador en vez de app con icono propio; y ademas deja que
   la app abra sin conexion para ver las carpetas guardadas.

   Estrategia: red primero, cache como respaldo. Asi cada push a Pages se ve
   enseguida, y si no hay senal igual abre lo ultimo que se descargo. */

var CACHE = 'mytbe-v2';
var SHELL = ['./', './index.html', './manifest.json', './icon-192.png', './favicon-32.png'];

self.addEventListener('install', function(e){
  e.waitUntil(
    caches.open(CACHE)
      .then(function(c){ return c.addAll(SHELL); })
      .then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e){
  e.waitUntil(
    caches.keys()
      .then(function(ks){
        return Promise.all(ks.filter(function(k){ return k !== CACHE; })
                             .map(function(k){ return caches.delete(k); }));
      })
      .then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function(e){
  var req = e.request;
  if(req.method !== 'GET') return;

  /* La API de YouTube y las miniaturas van derecho a la red: no tiene sentido
     cachear resultados de busqueda ni avatares en el shell de la app. */
  if(new URL(req.url).origin !== location.origin) return;

  e.respondWith(
    fetch(req)
      .then(function(res){
        var copia = res.clone();
        caches.open(CACHE).then(function(c){ c.put(req, copia); });
        return res;
      })
      .catch(function(){
        return caches.match(req).then(function(r){
          return r || caches.match('./index.html');
        });
      })
  );
});
