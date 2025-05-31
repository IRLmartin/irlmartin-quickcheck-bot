import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta, timezone

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# === SETTINGS ===
TARGET_CHANNEL_ID = 1333932173354340362  # ✅ Your Discord channel ID
TIMER_DURATION_HOURS = 5
UPDATE_INTERVAL_HOURS = 1

end_time_utc = None  # Store the target end time globally

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ IRLmartin AI is live.")
    await start_precise_timer()

async def start_precise_timer():
    global end_time_utc
    total_duration = timedelta(hours=TIMER_DURATION_HOURS)
    interval = timedelta(hours=UPDATE_INTERVAL_HOURS)

    end_time_utc = datetime.now(timezone.utc) + total_duration
    channel = bot.get_channel(TARGET_CHANNEL_ID)

    if not channel:
        print("❌ Could not find the target channel.")
        return

    while True:
        now = datetime.now(timezone.utc)
        remaining = end_time_utc - now

        if remaining.total_seconds() <= 0:
            await channel.send("✅ IRLmartin AI warm-up complete. Ready to assist.")
            break

        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        mins, _ = divmod(remainder, 60)

        await channel.send(f"⏳ IRLmartin AI update: **{hours}h {mins}m remaining...**")

        # Calculate sleep until the next exact update time (rounded to the hour)
        next_post_time = now + interval
        time_until_next = (next_post_time - datetime.now(timezone.utc)).total_seconds()
        await asyncio.sleep(min(time_until_next, remaining.total_seconds()))

# Slash command: /status
@bot.tree.command(name="status", description="Check how long IRLmartin AI has left to warm up")
async def status(interaction: discord.Interaction):
    global end_time_utc
    now = datetime.now(timezone.utc)

    if end_time_utc and now < end_time_utc:
        remaining = end_time_utc - now
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        mins, secs = divmod(remainder, 60)
        await interaction.response.send_message(
            f"🤖 IRLmartin AI is still warming up.\n⏱ Time left: **{hours}h {mins}m {secs}s**"
        )
    elif end_time_utc:
        await interaction.response.send_message("✅ IRLmartin AI is fully warmed up.")
    else:
        await interaction.response.send_message("⚠️ The warm-up timer hasn't started yet.")

bot.run(os.environ["DISCORD_TOKEN"])
