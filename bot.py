import discord
print("Discord library version:", discord.__version__)

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

@bot.command(name="quickcheck", help="Check text for TikTok Shop violations")
async def quickcheck(ctx, *, text: str):
    prompt = (
        "You are a TikTok compliance checker. Analyze the following text for TikTok Shop violations, banned words, "
        "health claims, or manipulative language. Respond with a risk level (Safe, Risky, Violation) and suggest fixes.\n\n"
        f"Text: {text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.3,
    )
    result = response.choices[0].message.content.strip()
    await ctx.send(f"**Compliance Check Result:**\n{result}")

@bot.command(name="status", help="Check if the bot is online and running")
async def status(ctx):
    await ctx.send("✅ IRLmartin AI Bot is online and operational.")

bot.run(DISCORD_TOKEN)
