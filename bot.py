import discord
from discord.ext import commands
import openai
import os

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="quickcheck", description="Check text for TikTok Shop violations")
async def quickcheck(ctx, *, text: str):
    await ctx.defer()
    prompt = (
        "You are a TikTok compliance checker. Analyze the following text for TikTok Shop violations, banned words, "
        "health claims, or manipulative language. Respond with a risk level (Safe, Risky, Violation) and suggest fixes.\n\n"
        f"Text: {text}"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.3,
    )
    result = response.choices[0].text.strip()
    await ctx.respond(f"**Compliance Check Result:**\n{result}")

@bot.slash_command(name="status", description="Check if the bot is online and running")
async def status(ctx):
    await ctx.respond("✅ IRLmartin AI Bot is online and operational.")

bot.run(DISCORD_TOKEN)
