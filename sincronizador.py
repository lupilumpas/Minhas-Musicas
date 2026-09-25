import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES — ALTERE SOMENTE O NECESSÁRIO AQUI
# ============================================================

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLsxjijFMfKSEsKchvK6xMvi1I2t7v_bwr"

PROJECT_PATH = Path(r"C:\Users\sonho\Pictures\Minhas-Musicas")

SCRIPT_FILE = "script.js"

# None = descobrir automaticamente pelo script.js
# No seu projeto atual, isso será detectado como "Musicas".
MUSIC_FOLDER = None

COMMIT_MESSAGE = "Adiciona novas músicas"


# Arquivo de estado fica FORA do projeto.
# Ele guarda IDs do YouTube para aumentar a segurança contra duplicatas.
LOCAL_STATE_DIR = Path(
    os.environ.get("LOCALAPPDATA", str(Path.home()))
) / "Minhas-Musicas-Sincronizador"

STATE_FILE = LOCAL_STATE_DIR / "youtube_ids.json"


# ============================================================
# CORES / MENSAGENS
# ============================================================

def print_header():
    print()
    print("=" * 60)
    print("       SINCRONIZADOR MINHAS-MUSICAS")
    print("=" * 60)
    print()


def fail(message):
    print()
    print("[ERRO]")
    print(message)
    print()
    sys.exit(1)


def run_command(command, cwd=None, capture=True):
    """
    Executa um comando e retorna CompletedProcess.
    """

    try:
        return subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=capture,
            check=False
        )

    except FileNotFoundError:
        raise


def command_exists(command):
    return shutil.which(command) is not None


# ============================================================
# VERIFICAÇÕES
# ============================================================

def check_configuration():
    if not PLAYLIST_URL or "COLOQUE_A_URL" in PLAYLIST_URL:
        fail(
            "Você ainda não configurou PLAYLIST_URL no início do programa."
        )

    if not PROJECT_PATH.exists():
        fail(
            f"A pasta do projeto não existe:\n{PROJECT_PATH}"
        )

    if not PROJECT_PATH.is_dir():
        fail(
            f"O caminho configurado não é uma pasta:\n{PROJECT_PATH}"
        )


def check_required_commands():
    print("[1/5] Verificando programas necessários...")

    if not command_exists("git"):
        fail(
            "Git não foi encontrado no PATH.\n"
            "Teste no CMD com:\n"
            "git --version"
        )

    if not command_exists("yt-dlp"):
        fail(
            "yt-dlp não foi encontrado no PATH.\n"
            "Teste no CMD com:\n"
            "yt-dlp --version"
        )

    # yt-dlp precisa do FFmpeg para converter para MP3.
    if not command_exists("ffmpeg"):
        fail(
            "FFmpeg não foi encontrado no PATH.\n\n"
            "O yt-dlp está instalado, mas a conversão para MP3 "
            "precisa do FFmpeg.\n\n"
            "Teste no CMD com:\n"
            "ffmpeg -version"
        )

    print("OK - Git encontrado.")
    print("OK - yt-dlp encontrado.")
    print("OK - FFmpeg encontrado.")
    print()


def check_git_repository():
    result = run_command(
        ["git", "status", "--porcelain"],
        cwd=PROJECT_PATH
    )

    if result.returncode != 0:
        error = result.stderr.strip() or result.stdout.strip()

        fail(
            "A pasta não parece ser um repositório Git válido.\n\n"
            f"Detalhes:\n{error}"
        )

    # IMPORTANTE:
    # Se já houver alterações, não mexemos em nada.
    if result.stdout.strip():
        print("O repositório possui alterações pendentes:")
        print()
        print(result.stdout.rstrip())
        print()
        fail(
            "Sincronização cancelada para não sobrescrever "
            "alterações feitas manualmente.\n\n"
            "Faça commit/stash dessas alterações e execute novamente."
        )

    print("OK - Repositório Git limpo.")
    print()


# ============================================================
# SCRIPT.JS
# ============================================================

def get_script_path():
    script_path = PROJECT_PATH / SCRIPT_FILE

    if not script_path.exists():
        fail(
            f"O arquivo {SCRIPT_FILE} não foi encontrado em:\n"
            f"{script_path}"
        )

    return script_path


def remove_number_prefix(title):
    """
    Remove:
        01 -
        1 -
        119 -

    do começo do título.
    """

    title = title.strip()

    return re.sub(
        r"^\s*\d+\s*-\s*",
        "",
        title
    ).strip()


def normalize_title(title):
    """
    Normalização usada SOMENTE para comparação.

    Não altera o título real salvo no script.js.
    """

    title = remove_number_prefix(title)

    title = unicodedata.normalize("NFKC", title)

    title = re.sub(r"\s+", " ", title)

    return title.strip().casefold()


def extract_titles_from_script(content):
    """
    Encontra:

        const titles = [
            ...
        ];

    sem tentar interpretar o restante do JavaScript.
    """

    match = re.search(
        r"\bconst\s+titles\s*=\s*\[",
        content
    )

    if not match:
        fail(
            "Não encontrei 'const titles = [' no script.js."
        )

    array_start = content.find("[", match.start())

    if array_start == -1:
        fail(
            "Não foi possível localizar o início do array titles."
        )

    array_end = find_matching_bracket(content, array_start)

    if array_end == -1:
        fail(
            "Não foi possível localizar o fechamento do array titles."
        )

    array_content = content[array_start + 1:array_end]

    titles = []

    # Aceita strings JavaScript com aspas duplas ou simples.
    pattern = re.compile(
        r"""(["'])(.*?)(?<!\\)\1""",
        re.DOTALL
    )

    for match in pattern.finditer(array_content):
        value = match.group(2)

        # Desfaz apenas escapes básicos usados em JS.
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        value = value.replace("\\\\", "\\")

        titles.append(value)

    return titles, array_start, array_end


def find_matching_bracket(text, opening_position):
    """
    Encontra o ] correspondente ao [ do array,
    ignorando strings e comentários JavaScript.
    """

    depth = 0
    quote = None
    escaped = False
    in_line_comment = False
    in_block_comment = False

    i = opening_position

    while i < len(text):
        char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False

            i += 1
            continue

        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                i += 2
                continue

            i += 1
            continue

        if quote is not None:
            if escaped:
                escaped = False

            elif char == "\\":
                escaped = True

            elif char == quote:
                quote = None

            i += 1
            continue

        if char == "/" and next_char == "/":
            in_line_comment = True
            i += 2
            continue

        if char == "/" and next_char == "*":
            in_block_comment = True
            i += 2
            continue

        if char in ('"', "'", "`"):
            quote = char
            i += 1
            continue

        if char == "[":
            depth += 1

        elif char == "]":
            depth -= 1

            if depth == 0:
                return i

        i += 1

    return -1


def get_next_number(titles, mp3_files):
    """
    Descobre o maior número existente tanto no script.js
    quanto nos arquivos MP3.

    A próxima música será maior que todos eles.
    """

    highest = 0

    for title in titles:
        match = re.match(
            r"^\s*(\d+)\s*-",
            title
        )

        if match:
            highest = max(
                highest,
                int(match.group(1))
            )

    for file in mp3_files:
        match = re.match(
            r"^\s*(\d+)\s*-",
            file.stem
        )

        if match:
            highest = max(
                highest,
                int(match.group(1))
            )

    return highest + 1


def escape_js_string(value):
    """
    Prepara o título para ser colocado dentro de:
        "Título"
    """

    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    value = value.replace("\r", " ")
    value = value.replace("\n", " ")

    return value


def update_titles_in_script(script_path, new_titles):
    """
    Modifica SOMENTE o conteúdo do array titles.
    Todo o restante do script.js permanece exatamente como estava.
    """

    content = script_path.read_text(
        encoding="utf-8-sig"
    )

    titles, array_start, array_end = extract_titles_from_script(content)

    if not new_titles:
        return False

    # Detecta a indentação usada nas entradas existentes.
    lines = content[array_start:array_end].splitlines()

    indentation = "    "

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('"') or stripped.startswith("'"):
            indentation = line[:len(line) - len(line.lstrip())]
            break

    # Mantém a estrutura original do array.
    array_body = content[array_start + 1:array_end]

    # Se já houver conteúdo, adiciona uma nova linha antes do fechamento.
    insertion = ""

    if array_body and not array_body.endswith("\n"):
        insertion += "\n"

    for title in new_titles:
        insertion += (
            f'{indentation}"{escape_js_string(title)}",\n'
        )

    new_content = (
        content[:array_end]
        + insertion
        + content[array_end:]
    )

    # Segurança adicional.
    if new_content == content:
        return False

    script_path.write_text(
        new_content,
        encoding="utf-8"
    )

    return True


# ============================================================
# DESCOBERTA DA PASTA DE MÚSICAS
# ============================================================

def discover_music_folder(script_path):
    """
    Tenta descobrir automaticamente a pasta usada pelo player.

    No seu script atual existe:

        audio.src = `Musicas/${titles[current]}.mp3`;

    Portanto será detectada a pasta Musicas.
    """

    content = script_path.read_text(
        encoding="utf-8-sig"
    )

    # Procura algo como:
    #
    # audio.src = `Musicas/${titles[current]}.mp3`;
    #
    pattern = re.compile(
        r"(?:audio\.src|src)\s*=\s*[`'\"]"
        r"([^`'\"]*?)"
        r"\$\{\s*titles\b",
        re.IGNORECASE
    )

    match = pattern.search(content)

    if match:
        prefix = match.group(1).replace("\\", "/").strip()

        if prefix:
            prefix = prefix.rstrip("/")

            folder = PROJECT_PATH / prefix

            if folder.exists() and folder.is_dir():
                return folder

            # Mesmo se ainda não existir, podemos criá-la.
            return folder

    # Se não foi possível descobrir pelo JS,
    # procura automaticamente onde estão os MP3.
    candidates = {}

    for mp3 in PROJECT_PATH.rglob("*.mp3"):
        if ".git" in mp3.parts:
            continue

        folder = mp3.parent
        candidates[folder] = candidates.get(folder, 0) + 1

    if candidates:
        return max(
            candidates,
            key=candidates.get
        )

    # Se não há MP3 ainda, usa a configuração explícita.
    if MUSIC_FOLDER:
        return PROJECT_PATH / MUSIC_FOLDER

    # Último fallback.
    return PROJECT_PATH / "Musicas"


# ============================================================
# MP3 EXISTENTES
# ============================================================

def get_existing_mp3_files():
    files = []

    for file in PROJECT_PATH.rglob("*.mp3"):
        if ".git" in file.parts:
            continue

        files.append(file)

    return files


def build_existing_title_set(titles, mp3_files):
    existing = set()

    for title in titles:
        existing.add(
            normalize_title(title)
        )

    for file in mp3_files:
        existing.add(
            normalize_title(file.stem)
        )

    return existing


# ============================================================
# ESTADO DOS IDS DO YOUTUBE
# ============================================================

def load_state():
    LOCAL_STATE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not STATE_FILE.exists():
        return set()

    try:
        data = json.loads(
            STATE_FILE.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, list):
            return set()

        return set(
            str(item)
            for item in data
            if item
        )

    except Exception:
        print(
            "Aviso: o arquivo de estado dos IDs não pôde ser lido."
        )
        print(
            "A comparação por título continuará funcionando."
        )
        return set()


def save_state(video_ids):
    LOCAL_STATE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    STATE_FILE.write_text(
        json.dumps(
            sorted(video_ids),
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


# ============================================================
# YOUTUBE / YT-DLP
# ============================================================

def get_playlist():
    print("[2/5] Consultando playlist do YouTube...")

    command = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-single-json",
        "--no-warnings",
        PLAYLIST_URL
    ]

    try:
        result = run_command(command)

    except FileNotFoundError:
        fail(
            "yt-dlp não foi encontrado."
        )

    if result.returncode != 0:
        error = (
            result.stderr.strip()
            or result.stdout.strip()
            or "Erro desconhecido."
        )

        fail(
            "Não foi possível acessar a playlist.\n\n"
            "Verifique se:\n"
            "- a URL está correta;\n"
            "- a playlist existe;\n"
            "- a playlist está acessível;\n"
            "- sua conexão está funcionando.\n\n"
            f"Erro retornado pelo yt-dlp:\n{error}"
        )

    try:
        data = json.loads(result.stdout)

    except json.JSONDecodeError:
        fail(
            "O yt-dlp não retornou um JSON válido ao consultar "
            "a playlist."
        )

    entries = data.get("entries") or []

    songs = []

    for entry in entries:
        if not entry:
            continue

        video_id = entry.get("id")
        title = entry.get("title")

        if not video_id or not title:
            continue

        webpage_url = entry.get("webpage_url")

        if not webpage_url:
            webpage_url = (
                f"https://www.youtube.com/watch?v={video_id}"
            )

        songs.append({
            "id": str(video_id),
            "title": str(title).strip(),
            "url": webpage_url
        })

    if not songs:
        fail(
            "A playlist foi acessada, mas nenhuma música válida "
            "foi encontrada."
        )

    print(
        f"OK - {len(songs)} músicas encontradas na playlist."
    )
    print()

    return songs


# ============================================================
# DESCOBRIR NOVAS MÚSICAS
# ============================================================

def find_new_songs(playlist, existing_titles, known_ids, start_number):
    new_songs = []

    next_number = start_number

    seen_ids = set(known_ids)
    seen_titles = set(existing_titles)

    for song in playlist:
        video_id = song["id"]
        original_title = song["title"]

        normalized = normalize_title(
            original_title
        )

        # ID conhecido = já sincronizado.
        if video_id in seen_ids:
            continue

        # Título já existente = provavelmente música já cadastrada.
        if normalized in seen_titles:
            continue

        display_title = (
            f"{next_number:02d} - {original_title}"
        )

        new_songs.append({
            "id": video_id,
            "original_title": original_title,
            "display_title": display_title,
            "url": song["url"]
        })

        seen_ids.add(video_id)
        seen_titles.add(normalized)

        next_number += 1

    return new_songs


# ============================================================
# NOME DE ARQUIVO
# ============================================================

def sanitize_filename(name, max_length=180):
    """
    Remove caracteres inválidos para Windows.
    """

    # Caracteres proibidos no Windows.
    name = re.sub(
        r'[<>:"/\\|?*]',
        "",
        name
    )

    # Remove caracteres de controle.
    name = "".join(
        char
        for char in name
        if ord(char) >= 32
    )

    # Windows não gosta de ponto/espaço no final.
    name = name.rstrip(" .")

    if not name:
        name = "musica"

    # Evita nomes reservados do Windows.
    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }

    stem_upper = name.upper()

    if stem_upper in reserved:
        name = f"_{name}"

    return name[:max_length].rstrip(" .")


# ============================================================
# DOWNLOAD
# ============================================================

def download_song(song, temp_dir):
    """
    Baixa uma única música para uma pasta temporária.

    O nome temporário usa o ID do YouTube.
    """

    video_id = song["id"]
    url = song["url"]

    output_template = str(
        Path(temp_dir) / f"{video_id}.%(ext)s"
    )

    command = [
        "yt-dlp",
        "--no-playlist",
        "--no-warnings",
        "--no-progress",
        "-f",
        "bestaudio/best",
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "-o",
        output_template,
        url
    ]

    result = run_command(command)

    if result.returncode != 0:
        error = (
            result.stderr.strip()
            or result.stdout.strip()
            or "Erro desconhecido."
        )

        raise RuntimeError(
            f"yt-dlp falhou:\n{error}"
        )

    # O arquivo final deve ser MP3.
    mp3_files = list(
        Path(temp_dir).glob(
            f"{video_id}.mp3"
        )
    )

    if not mp3_files:
        # Fallback: procura qualquer arquivo com o ID.
        candidates = list(
            Path(temp_dir).glob(
                f"{video_id}.*"
            )
        )

        mp3_files = [
            file
            for file in candidates
            if file.suffix.lower() == ".mp3"
        ]

    if not mp3_files:
        raise RuntimeError(
            "O yt-dlp terminou sem erro, mas o arquivo MP3 "
            "não foi encontrado."
        )

    return mp3_files[0]


# ============================================================
# SINCRONIZAÇÃO
# ============================================================

def perform_sync():
    print_header()

    # --------------------------------------------------------
    # 1. CONFIGURAÇÕES
    # --------------------------------------------------------

    check_configuration()
    check_required_commands()
    check_git_repository()

    script_path = get_script_path()

    # --------------------------------------------------------
    # 2. LER PROJETO
    # --------------------------------------------------------

    script_content = script_path.read_text(
        encoding="utf-8-sig"
    )

    titles, _, _ = extract_titles_from_script(
        script_content
    )

    music_folder = discover_music_folder(
        script_path
    )

    mp3_files = get_existing_mp3_files()

    existing_titles = build_existing_title_set(
        titles,
        mp3_files
    )

    known_ids = load_state()

    next_number = get_next_number(
        titles,
        mp3_files
    )

    print(
        f"Pasta de músicas detectada: {music_folder}"
    )

    print(
        f"Músicas cadastradas no script.js: {len(titles)}"
    )

    print(
        f"Arquivos MP3 encontrados: {len(mp3_files)}"
    )

    print()

    # --------------------------------------------------------
    # 3. PLAYLIST
    # --------------------------------------------------------

    playlist = get_playlist()

    new_songs = find_new_songs(
        playlist,
        existing_titles,
        known_ids,
        next_number
    )

    print("[3/5] Procurando músicas novas...")
    print()

    if not new_songs:
        print("Nenhuma música nova encontrada.")
        print()
        print("=" * 60)
        print("Nada para sincronizar.")
        print("=" * 60)
        print()
        return

    print(
        f"Encontradas {len(new_songs)} música(s) nova(s):"
    )
    print()

    for song in new_songs:
        print(
            f"  {song['display_title']}"
        )

    print()

    # --------------------------------------------------------
    # 4. DOWNLOADS
    # --------------------------------------------------------

    print("[4/5] Baixando músicas...")
    print()

    music_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # Todas as músicas são baixadas primeiro para uma pasta
    # temporária. Só depois são colocadas no projeto.
    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="minhas-musicas-sync-"
        )
    )

    downloaded = []

    try:
        for index, song in enumerate(new_songs, start=1):
            print(
                f"[{index}/{len(new_songs)}] "
                f"Baixando: {song['original_title']}"
            )

            try:
                temp_file = download_song(
                    song,
                    temp_dir
                )

                safe_name = sanitize_filename(
                    song["display_title"]
                )

                target = music_folder / (
                    safe_name + ".mp3"
                )

                # Verificação extra contra colisões.
                if target.exists():
                    print(
                        "  Já existe. Música não será duplicada."
                    )
                    print()
                    continue

                downloaded.append({
                    "song": song,
                    "temp_file": temp_file,
                    "target": target
                })

                print("  OK")
                print()

            except Exception as exc:
                # Se qualquer download falhar, cancelamos toda a
                # sincronização antes de alterar script.js.
                raise RuntimeError(
                    f"Falha ao baixar:\n"
                    f"{song['original_title']}\n\n"
                    f"{exc}"
                )

        if not downloaded:
            print(
                "Nenhum arquivo novo precisou ser adicionado."
            )
            return

        # ----------------------------------------------------
        # 5. MOVER MP3S
        # ----------------------------------------------------

        print("[5/5] Atualizando projeto...")
        print()

        for item in downloaded:
            shutil.move(
                str(item["temp_file"]),
                str(item["target"])
            )

            print(
                f"MP3 salvo: {item['target'].name}"
            )

        # ----------------------------------------------------
        # ATUALIZAR SCRIPT.JS
        # ----------------------------------------------------

        titles_to_add = [
            item["song"]["display_title"]
            for item in downloaded
        ]

        changed = update_titles_in_script(
            script_path,
            titles_to_add
        )

        if not changed:
            raise RuntimeError(
                "Não foi possível atualizar o array titles "
                "do script.js."
            )

        print()
        print("script.js atualizado.")
        print()

        # ----------------------------------------------------
        # ATUALIZAR IDS
        # ----------------------------------------------------

        new_ids = {
            item["song"]["id"]
            for item in downloaded
        }

        save_state(
            known_ids | new_ids
        )

        # ----------------------------------------------------
        # GIT ADD
        # ----------------------------------------------------

        print("Executando git add . ...")

        result = run_command(
            ["git", "add", "."],
            cwd=PROJECT_PATH
        )

        if result.returncode != 0:
            error = (
                result.stderr.strip()
                or result.stdout.strip()
            )

            raise RuntimeError(
                "git add falhou:\n"
                + error
            )

        print("OK - git add concluído.")
        print()

        # ----------------------------------------------------
        # VERIFICAR SE EXISTEM ALTERAÇÕES PARA COMMIT
        # ----------------------------------------------------

        result = run_command(
            ["git", "diff", "--cached", "--quiet"],
            cwd=PROJECT_PATH
        )

        if result.returncode == 0:
            raise RuntimeError(
                "O Git não detectou alterações preparadas para commit."
            )

        # ----------------------------------------------------
        # GIT COMMIT
        # ----------------------------------------------------

        print("Criando commit...")

        result = run_command(
            [
                "git",
                "commit",
                "-m",
                COMMIT_MESSAGE
            ],
            cwd=PROJECT_PATH
        )

        if result.returncode != 0:
            error = (
                result.stderr.strip()
                or result.stdout.strip()
            )

            raise RuntimeError(
                "git commit falhou:\n"
                + error
            )

        print("OK - commit criado.")
        print()

        # ----------------------------------------------------
        # GIT PUSH
        # ----------------------------------------------------

        print("Enviando para o GitHub...")

        result = run_command(
            ["git", "push"],
            cwd=PROJECT_PATH
        )

        if result.returncode != 0:
            error = (
                result.stderr.strip()
                or result.stdout.strip()
            )

            raise RuntimeError(
                "git push falhou:\n"
                + error
            )

        print("OK - git push realizado.")
        print()

        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        print("=" * 60)
        print("       SINCRONIZAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print()

        print(
            f"{len(downloaded)} música(s) adicionada(s)."
        )

        print()

        for item in downloaded:
            print(
                f"  {item['song']['display_title']}"
            )

        print()

    except Exception:
        # O script.js pode já ter sido alterado caso o erro
        # aconteça depois da atualização.
        #
        # Não escondemos o erro.
        raise

    finally:
        # Remove a pasta temporária.
        try:
            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )
        except Exception:
            pass


# ============================================================
# MAIN
# ============================================================

def main():
    try:
        perform_sync()

    except KeyboardInterrupt:
        print()
        print("Operação cancelada pelo usuário.")
        sys.exit(1)

    except Exception as exc:
        print()
        print("=" * 60)
        print("SINCRONIZAÇÃO INTERROMPIDA")
        print("=" * 60)
        print()
        print(str(exc))
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()