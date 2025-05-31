import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta, timezone

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TIMER_DURATION = 5 * 60  # 5 minutes (change as needed)
end_time_utc = None  # Global time tracker

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ IRLmartin AI is live.")
    await start_warmup_timer()

async def start_warmup_timer():
    global end_time_utc
    now = datetime.now(timezone.utc)
    end_time_utc = now + timedelta(seconds=TIMER_DURATION)

    # No need to announce — timer just runs in background
    await asyncio.sleep(TIMER_DURATION)

# Slash command: /status
@bot.tree.command(name="status", description="Check how long IRLmartin AI has left to warm up")
async def status(interaction: discord.Interaction):
    global end_time_utc
    now = datetime.now(timezone.utc)

    if end_time_utc and now < end_time_utc:
        remaining = end_time_utc - now
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        await interaction.response.send_message(
            f"🤖 IRLmartin AI is still warming up.\n⏱ Time left: **{mins} minutes {secs} seconds**"
        )
    elif end_time_utc:
        await interaction.response.send_message("✅ IRLmartin AI is fully warmed up and ready.")
    else:
        await interaction.response.send_message("⚠️ The warm-up timer hasn't started yet.")

bot.run(os.environ["DISCORD_TOKEN"])
