const CACHE_NAME = "meu-player-v2";

const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./style.css",
  "./script.js",
  "./manifest.json"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {

      // Arquivos principais
      await cache.addAll([
        "./",
        "./index.html",
        "./style.css",
        "./script.js",
        "./manifest.json"
      ]);

      // Lê o script.js
      const response = await fetch("./script.js");
      const script = await response.text();

      // Encontra o conteúdo de const titles = [...]
      const match = script.match(/const\s+titles\s*=\s*\[([\s\S]*?)\]/);

      if (!match) {
        throw new Error("Não foi possível encontrar a variável titles no script.js");
      }

      // Extrai todos os títulos entre aspas
      const titles = [];
      const regex = /"((?:\\.|[^"\\])*)"/g;

      let item;

      while ((item = regex.exec(match[1])) !== null) {
        titles.push(JSON.parse(`"${item[1]}"`));
      }

      console.log(`Encontradas ${titles.length} músicas.`);

      // Monta os caminhos dos MP3s
      const musicas = titles.map(title =>
        `./Musicas/${encodeURIComponent(title)}.mp3`
      );

      // Coloca TODAS as músicas no cache
      await cache.addAll(musicas);

      console.log(`Cacheadas ${musicas.length} músicas.`);
    })
  );

  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  if (event.request.url.includes("script.js")) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const copy = response.clone();

          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, copy);
          });

          return response;
        })
        .catch(() => caches.match(event.request))
    );

    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).then(response => {

        if (response.status === 200) {
          const copy = response.clone();

          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, copy);
          });
        }

        return response;
      });
    }).catch(() => caches.match("./index.html"))
  );
});
