========================================
  FPSBOOST BOT - RAILWAY
  Dziala dla wielu osob naraz!
========================================

--- CZY KILKA OSOB MOZE NARAZ? ---

TAK! Kazdy gracz dostaje wlasny kanal na Discordzie.
Bot obsluguje wielu graczy jednoczesnie.

--- JAK WRZUCIC NA RAILWAY ---

1. Wejdz na https://railway.com/
2. Zaloguj sie przez GitHub
3. Stworz nowy projekt: "New Project" -> "Deploy from GitHub repo"
4. Wybierz repo z botem (wrzuc bot.py i requirements.txt na GitHub)
5. Kliknij "Add Variables":
   - TOKEN = twoj_token_bota_discord
   - GUILD_ID = id_twojego_serwera
6. Railway sam wykryje Procfile i uruchomi bota
7. Skopiuj URL (np. https://fpsboost-bot.up.railway.app)

--- JAKI URL WPISAC W MODA ---

W pliku FpsBoostMod.java zmien:
  private static final String API_URL = "https://fpsboost-bot.up.railway.app";

--- KOLEGA ROBIC TYLKO: ---
1. Pobiera fpsboost-1.0.0.jar
2. Wrzuca do .minecraft/mods/
3. Koniec. Gra. Zero configu.

========================================
