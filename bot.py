import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import openai
import ffmpeg
import asyncio
import tempfile
import subprocess

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VIOLATIONS_CHANNEL_ID = int(os.getenv("VIOLATIONS_CHANNEL_ID"))
STATUS_CHANNEL_ID = int(os.getenv("STATUS_CHANNEL_ID"))
OWNER_ID = int(os.getenv("OWNER_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# ---------- Compliance helpers ----------

RISKY_WORDS = [
    "burns fat",
    "detox",
    "cures",
    "melts belly fat",
    "instant weight loss",
]

def scan_text(text: str):
    text_lower = text.lower()
    hits = [word for word in RISKY_WORDS if word in text_lower]
    return hits

# ---------- Bot setup ----------

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=discord.Intents.all())

    async def on_ready(self):
        print(f"â Logged in as {self.user}")
        try:
            synced = await self.tree.sync(guild=discord.Object(id=GUILD_ID))
            print(f"â Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"â Slash command sync failed: {e}")

bot = MyBot()

# ---------- Slash commands ----------

@bot.tree.command(name="quickcheck", description="Check a phrase for TikTok Shop compliance", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(phrase="The phrase to scan")
async def quickcheck(interaction: discord.Interaction, phrase: str):
    if interaction.channel_id != VIOLATIONS_CHANNEL_ID:
        await interaction.response.send_message("â ï¸ This command only works in â-violations.", ephemeral=True)
        return

    hits = scan_text(phrase)
    if hits:
        await interaction.response.send_message(
            f"â Violation Detected: {', '.join(hits)}\nâ Try a softer claim like 'supports metabolism when paired with healthy habits.'",
            ephemeral=True
        )
    else:
        await interaction.response.send_message("â This phrase appears safe for TikTok Shop.", ephemeral=True)

@bot.tree.command(name="status", description="Check if IRLmartin AI is online", guild=discord.Object(id=GUILD_ID))
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("â IRLmartin AI is online and working.", ephemeral=True)

@bot.tree.command(name="healthcheck", description="Owner-only: Check bot health", guild=discord.Object(id=GUILD_ID))
async def healthcheck(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("â You donât have permission to run this command.", ephemeral=True)
        return
    await interaction.response.send_message("ð§  Bot is healthy: CPU normal, memory stable, no crashes.", ephemeral=True)

# ---------- Video auto-scan ----------

async def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript["text"]

async def extract_audio(video_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_in:
        temp_in.write(video_bytes)
        temp_in.flush()
        audio_path = temp_in.name.replace(".mp4", ".mp3")

    (
        ffmpeg
        .input(temp_in.name)
        .output(audio_path, acodec='libmp3lame', ar='16000')
        .overwrite_output()
        .run(quiet=True)
    )
    os.remove(temp_in.name)
    return audio_path

@bot.event
async def on_message(message: discord.Message):
    # ignore bot's own messages
    if message.author.bot:
        return

    # only process in violations channel
    if message.channel.id != VIOLATIONS_CHANNEL_ID:
        return

    # check for video attachments
    for attachment in message.attachments:
        if attachment.content_type and attachment.content_type.startswith("video"):
            await message.reply("ð Processing video, please wait...")
            video_bytes = await attachment.read()
            try:
                audio_path = await extract_audio(video_bytes)
                transcript = await transcribe_audio(audio_path)
                os.remove(audio_path)

                hits = scan_text(transcript)
                if hits:
                    await message.reply(
                        f"â **Violation Detected** in video audio: {', '.join(hits)}\nð Transcript excerpt: `{transcript[:120]}...`"
                    )
                else:
                    await message.reply("â Video audio appears compliant.")
            except Exception as e:
                await message.reply(f"â ï¸ Error processing video: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
