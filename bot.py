import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands
    await bot.load_extension("timer")  # Load the timer command from timer.py
    print(f"✅ Logged in as {bot.user}")

bot.run("YOUR_BOT_TOKEN")
