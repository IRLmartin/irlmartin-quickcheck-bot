import discord
from discord.ext import commands
import openai
import os

print("Discord library version:", discord.__version__)  # For debugging

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()  # Sync slash commands with Discord

@bot.tree.command(name="quickcheck", description="Check text for TikTok Shop violations")
async def quickcheck(interaction: discord.Interaction, *, text: str):
    await interaction.response.defer()
    print("Received quickcheck request with text:", text)
    prompt = (
        "You are a TikTok compliance checker. Analyze the following text for TikTok Shop violations, banned words, "
        "health claims, or manipulative language. Respond with a risk level (Safe, Risky, Violation) and suggest fixes.\n\n"
        f"Text: {text}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3,
            timeout=15  # 15 seconds timeout (adjust as needed)
        )
        result = response.choices[0].message.content.strip()
        print("OpenAI response:", result)
        await interaction.followup.send(f"**Compliance Check Result:**\n{result}")
    except Exception as e:
        print("Error calling OpenAI API:", e)
        await interaction.followup.send("❌ Sorry, something went wrong while checking the text. Please try again later.")

@bot.tree.command(name="status", description="Check if the bot is online and running")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("✅ IRLmartin AI Bot is online and operational.")

bot.run(DISCORD_TOKEN)
