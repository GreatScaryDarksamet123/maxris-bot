import os
import discord
import requests
from discord.ext import commands

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
FALIX_API_KEY = os.environ.get("FALIX_API_KEY")
SERVER_ID = os.environ.get("SERVER_ID")

FALIX_URL = "https://client.falixnodes.net"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

headers = {
    "Authorization": f"Bearer {FALIX_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı, bot aktif!')

@bot.command(name="start")
async def start_server(ctx):
    status_url = f"{FALIX_URL}/api/client/servers/{SERVER_ID}/resources"
    try:
        res = requests.get(status_url, headers=headers)
        if res.status_code == 200:
            state = res.json()['attributes']['current_state']
            if state in ['running', 'starting']:
                await ctx.send("🟢 **MAXRIS SMP** zaten açık veya başlatılıyor!")
                return
    except Exception:
        pass

    start_url = f"{FALIX_URL}/api/client/servers/{SERVER_ID}/power"
    payload = {"signal": "start"}
    
    response = requests.post(start_url, json=payload, headers=headers)
    
    if response.status_code in [204, 200]:
        await ctx.send("🚀 **MAXRIS SMP** sunucusu başlatılıyor! Lütfen 1-2 dakika bekleyin.")
    else:
        await ctx.send(f"❌ Sunucu başlatılamadı. Hata Kodu: {response.status_code}")

bot.run(DISCORD_TOKEN)
