import os
import threading
import discord
from flask import Flask

# Inicjalizacja aplikacji Flask (wymagane przez Render do utrzymania usługi)
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot Discord działa poprawnie na Renderze!", 200


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


# Konfiguracja bota Discord
intents = discord.Intents.default()
intents.message_content = (
    True  # Wymagane do odczytywania treści wiadomości
)

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"Zalogowano pomyślnie jako: {client.user.name}")


@client.event
async def on_message(message):
  # Ignorowanie wiadomości od samego bota, aby uniknąć pętli
  if message.author == client.user:
    return

  if message.content.startswith("!start"):
    await message.channel.send(
        "Cześć! Jestem botem Discord uruchomionym na Renderze."
    )
  elif message.content.startswith("!ping"):
    await message.channel.send("Pong! 🏓 Bot działa stabilnie.")


TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
  if not TOKEN:
    print("BŁĄD: Brak zmiennej środowiskowej DISCORD_BOT_TOKEN!")
    exit(1)

  # Uruchomienie serwera Flask w osobnym wątku (dla Render Web Service)
  flask_thread = threading.Thread(target=run_flask)
  flask_thread.daemon = True
  flask_thread.start()

  # Uruchomienie bota Discord w głównym wątku
  client.run(TOKEN)