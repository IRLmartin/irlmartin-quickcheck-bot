import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()                     # Sync slash commands
    await bot.load_extension("timer")         # Load your timer command from timer.py
    print(f"✅ Logged in as {bot.user}")

# Secure token usage (reads from Railway or .env)
bot.run(os.environ["DISCORD_TOKEN"])
