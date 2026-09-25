MEU PLAYER OFFLINE

1. Coloque seus MP3 na pasta "musicas".
2. Edite o arquivo script.js e cadastre cada música no array "songs".
3. Se quiser capas, coloque-as em "capas" e informe o caminho no campo "cover".

IMPORTANTE:
O Service Worker não funciona corretamente abrindo index.html diretamente com duplo clique.
Para testar o modo offline, o projeto precisa ser servido por HTTP/HTTPS.

Exemplo com Python:
  py -m http.server 8000

Depois abra:
  http://localhost:8000

Para usar como PWA publicado na internet, hospede o projeto em GitHub Pages, por exemplo.
Depois do primeiro acesso, o navegador poderá armazenar os arquivos do site para uso offline.

Se você adicionar ou alterar arquivos do site, aumente a versão CACHE_NAME em service-worker.js:
  meu-player-v2
