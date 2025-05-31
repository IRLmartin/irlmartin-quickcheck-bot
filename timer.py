import asyncio
import discord
from discord import app_commands
from discord.ext import commands

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timer", description="Set a countdown timer (in minutes)")
    async def timer(self, interaction: discord.Interaction, minutes: int):
        if minutes <= 0:
            await interaction.response.send_message("⛔ Please enter a time greater than 0 minutes.")
            return

        await interaction.response.send_message(f"⏳ Timer set for {minutes} minute(s)...")
        await asyncio.sleep(minutes * 60)
        await interaction.followup.send(f"⏰ Time's up! {minutes} minutes have passed.")

async def setup(bot):
    await bot.add_cog(Timer(bot))
