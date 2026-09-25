const titles = [
"01 - David Guetta - Titanium (Lyrics) ft. Sia",
"02 - Maroon 5 - Animals (Lyrics)",
"03 - Aaron Smith - Dancin (KRONO Remix) - Lyrics",
"04 - Tears for Fears - Everybody Wants To Rule The World ｜ Tear for Fears ft. Dafuq!？Boom! ｜",
"05 - Blinding Lights",
"06 - Rod Stewart - Young Turks (Official HD Remaster)",
"07 - Thunderstruck",
"08 - Teddy Swims - The Door (Official Music Video)",
"09 - Lighthouse Family - Lovin' Every Minute (Official Music Video)",
"10 - Michael Jackson - Billie Jean (Official Video)",
"11 - Michael Jackson - Bad (Shortened Version)",
"12 - Michael Jackson - Smooth Criminal (Official Video - Shortened Version)",
"13 - Michael Jackson - Beat It (Official 4K Video)",
"14 - Post Malone, Swae Lee - Sunflower (Spider-Man： Into the Spider-Verse)",
"15 - Mirage Machine",
"16 - Subnautica： Below Zero - Die Peacefully (Without AL-AN)",
"17 - Divide Music - Survive",
"18 - Miracle of Sound - Deep Blue",
"19 - Nerd Out - Diving in too deep",
"20 - Rockit Gaming - Subnautic Stimulus",
"21 - JT Music - Take the Dive",
"22 - JT Music - Dont hold your breath",
"23 - TryHardNinja - Deep Dive feat  Zach Boucher",
"24 - Into the Unknown",
"25 - Tropical Eden",
"26 - Abandon Ship",
"27 - Ben Prunty-Below Zero (Subnautica： Below Zero OST)",
"28 - Minecraft Soundtrack - Calm4.ogg (Restored + No ＂Mojang Specifications＂)",
"29 - Aaron Grooves - Jazzy Note Blocks",
"30 - AVM 16 Soundtrack： Green's Blues",
"31 - AVM 16 Soundtrack： Note Block Rock Symphony",
"32 - Elektronomia - Sky High ｜ Progressive House ｜ NCS - Copyright Free Music",
"33 - Cartoon, Jéja - On & On (feat. Daniel Levi) ｜ Electronic Pop ｜ NCS - Copyright Free Music",
"34 - TheFatRat - Unity",
"35 - PSYCHOMANIA [Ver. Megalovania]",
"36 - Monsters Inc theme (full)",
"37 - transformers soundtrack camaro scene - kill bill",
"38 - C418 - Minecraft - Minecraft Volume Alpha",
"39 - C418 - Subwoofer Lullaby - Minecraft Volume Alpha",
"40 - C418 - Living Mice - Minecraft Volume Alpha",
"41 - C418 - Haggstrom - Minecraft Volume Alpha",
"42 - C418 - Oxygène - Minecraft Volume Alpha",
"43 - C418 - Mice on Venus - Minecraft Volume Alpha",
"44 - C418 - Wet Hands - Minecraft Volume Alpha",
"45 - C418  - Sweden - Minecraft Volume Alpha",
"46 - C418 - Moog City 2 (Minecraft Volume Beta)",
"47 - C418 - Mutation (Minecraft Volume Beta)",
"48 - C418 - Blind Spots (Minecraft Volume Beta)",
"49 - C418 - Aria Math (Minecraft Volume Beta)",
"50 - Echo in the Wind",
"51 - A Familiar Room",
"52 - Cat - Minecraft Music Disc - C418",
"53 - Blocks - Minecraft Music Disc - C418",
"54 - Mall - Minecraft Music Disc - C418",
"55 - Chirp - Minecraft Music Disc - C418",
"56 - Far - Minecraft Music Disc - C418",
"57 - Pigstep -  Minecraft Music Disc - Lena Raine",
"58 - Stal- Minecraft Music Disc - C418",
"59 - Strad - Minecraft Music Disc - C418",
"60 - Wait - Minecraft Music Disc - C418",
"61 - Precipice - Minecraft Music Disc - Aaron Cherof",
"62 - Breeze - Fan Made Minecraft 1.21 Music Disc",
"63 - Guardian - Fan Made Minecraft Music Disc",
"64 - The Wither - Fan Made Minecraft Music Disc",
"65 - Diamond Cave - Fan Made Minecraft Music Disc",
"66 - Phantom - ChillCrafter / Minecraft Fan made Disc Concept",
"67 - Sky War",
"68 - Void - [Custom Minecraft fan made disc]",
"69 - Moon Festival 2023 Menu Background (Animated) ｜ Brawl Stars OST",
"70 - Brawl Stars OST - Holiday Getaway - Snowtel - Main Menu",
"71 - Brawl Stars OST ｜ Season 21 ｜ Warrior's Journey ｜ Menu Music",
"72 - Brawl Stars OST ｜ Season 36 ｜ ＊NEW＊ Brawler Finx ｜ Menu Music",
"73 - Brawl Stars OST ｜ Season 38 & 52 ｜ Kaze & Nori ｜ Menu Music",
"74 - Brawl Stars OST ｜ Season 39 ｜ Crush The Kaiju ｜ New Menu Music",
"75 - Brawl Stars OST ｜ Season 39 ｜ New Brawler Jae-Yong ｜ Menu Music",
"76 - Dance of the Wind",
"77 - The Way You Look Tonight",
"78 - Blox Fruits OST - Maximum Strength (Tiki Outpost)",
"79 - Grasswalk - Plants vs. Zombies Soundtrack (Official)",
"80 - Ultimate Battle",
"81 - Crazy Dave (In-Game)",
"82 - Time Paradox - Chlorophied",
"83 - finale for the bonely one",
"84 - Survivor - Eye Of The Tiger (Lyrics)",
"85 - My Way (2008 Remastered)",
"86 - Bad Boys (Theme from Cops)",
"87 - The Last Breath",
"88 - Tally Hall - Hidden in the Sand",
"89 - Street Corner Renaissance - Life Could Be A Dream",
"90 - Luther Vandross - Never Too Much (Official HD Video)",
"91 - 50 Cent - In Da Club (Official Music Video)",
"92 - DJ Shadow - Six Days (Remix) (feat. Mos Def)",
"93 - DOORS Roblox OST： Dawn of the Doors",
"94 - DOORS Roblox OST： Jeff's Jingle",
"95 - Doom Eternal OST - The Only Thing They Fear Is You (Mick Gordon) [Doom Eternal Theme]",
"96 - Ricky Martin - María (Official Video)",
"97 - clubbed to death - Matrix soundtrack",
"98 - Coolio - Gangsta's Paradise (Lyrics) ft. L.V.",
"99 - Metallica： Enter Sandman (Official Music Video)",
"100 - Haddaway - What Is Love (Official 4K Video)",
"101 - Coolio - Gangsta's Paradise (feat. L.V.) [Official Music Video]",
"102 - I'm Still Standing",
"103 - 01 - Boutique Hotel",
"104 - 02 - Jazz At The Cocktail Lounge",
"105 - 03 - Romantic Comedy",
"106 - 04 - Terrace Swing",
"107 - 05 - Stroll About Swing",
"108 - 06 - Rainy Day Jazz",
"109 - 07 - Leisure Class",
"110 - 08 - Summer Getaway",
"111 - 09 - Piano Bar",
"112 - 10 - Cabaret Electro Swing",
"113 - 11 - Touch Of Jazz",
"114 - 12 - Blend Beat",
"115 - 13 - Fusion Tunes",
"116 - 14 - Harmony Mix",
"117 - 15 - Rhythm Splice",
"118 - 16 - Note Fusion",
"119 - 17 - Track Twine",
"120 - AMONG US SONG (Ambush) LYRIC VIDEO - DAGames",
];

const audio = document.getElementById("audio");
audio.volume = 1;
const playBtn = document.getElementById("play");
const progress = document.getElementById("progress");
const title = document.getElementById("music-title");
const currentTime = document.getElementById("current-time");
const duration = document.getElementById("duration");
const list = document.getElementById("song-list");
const shuffleBtn = document.getElementById("shuffle");
const repeatBtn = document.getElementById("repeat");

let current = 0;
let shuffle = true;
let repeat = false;
let playedSongs = [];

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return "0:00";
  const min = Math.floor(seconds / 60);
  const sec = Math.floor(seconds % 60).toString().padStart(2, "0");
  return `${min}:${sec}`;
}

function renderList() {
  list.innerHTML = "";

  if (!titles.length) {
    list.innerHTML = '<div class="empty">Nenhuma música cadastrada.</div>';
    return;
  }

  titles.forEach((titleName, index) => {
    const item = document.createElement("div");

    item.className = "song" + (index === current ? " active" : "");

    item.innerHTML = `
      <span class="song-number">${index + 1}</span>
      <span class="song-name">${titleName.replace(/^\d+\s*-\s*/, "")}</span>
    `;

    item.addEventListener("click", () => {
      loadSong(index);
      audio.play();
    });

    list.appendChild(item);
  });
}

function loadSong(index) {
  current = index;

  audio.src = `Musicas/${titles[current]}.mp3`;
  title.textContent = titles[current].replace(/^\d+\s*-\s*/, "");
  document.title = titles[current].replace(/^\d+\s*-\s*/, "");

  progress.value = 0;

  renderList();
}

function playPause() {
  if (!audio.src) loadSong(current);

  if (audio.paused) audio.play();
  else audio.pause();
}

function nextSong() {
  if (shuffle) {
    let available = titles
      .map((_, index) => index)
      .filter(index => !playedSongs.includes(index));

    // Se todas já foram tocadas, começa um novo ciclo
    if (available.length === 0) {
      playedSongs = [];
      available = titles.map((_, index) => index);
    }

    // Evita escolher a música atual
    available = available.filter(index => index !== current);

    const next = available[Math.floor(Math.random() * available.length)];

    current = next;
    playedSongs.push(current);
  } else {
    current = (current + 1) % titles.length;
  }

  loadSong(current);
  audio.play();
}

function previousSong() {
  current = (current - 1 + titles.length) % titles.length;

  loadSong(current);
  audio.play();
}

playBtn.addEventListener("click", playPause);
document.getElementById("next").addEventListener("click", nextSong);
document.getElementById("prev").addEventListener("click", previousSong);

document.addEventListener("keydown", (event) => {
  if (event.key === "MediaTrackNext") {
    nextSong();
  }

  if (event.key === "MediaTrackPrevious") {
    previousSong();
  }

  if (event.key === "MediaPlayPause") {
    playPause();
  }
});

audio.addEventListener("play", () => playBtn.textContent = "⏸");
audio.addEventListener("pause", () => playBtn.textContent = "▶");

audio.addEventListener("loadedmetadata", () => {
  duration.textContent = formatTime(audio.duration);
});

audio.addEventListener("timeupdate", () => {
  if (audio.duration) progress.value = (audio.currentTime / audio.duration) * 100;
  currentTime.textContent = formatTime(audio.currentTime);
});

progress.addEventListener("input", () => {
  if (audio.duration) audio.currentTime = (progress.value / 100) * audio.duration;
});

audio.addEventListener("ended", () => {
  if (repeat) {
    audio.currentTime = 0;
    audio.play();
  } else {
    nextSong();
  }
});

shuffleBtn.addEventListener("click", () => {
  shuffle = !shuffle;
  shuffleBtn.textContent = `🔀 Aleatório: ${shuffle ? "ON" : "OFF"}`;
});

repeatBtn.addEventListener("click", () => {
  repeat = !repeat;
  repeatBtn.textContent = `🔁 Repetir: ${repeat ? "ON" : "OFF"}`;
});

const randomStart = Math.floor(Math.random() * titles.length);

current = randomStart;
playedSongs.push(current);

loadSong(current);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("service-worker.js")
      .catch(error => console.error("Falha ao registrar Service Worker:", error));
  });
}