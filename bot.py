@bot.tree.command(name="status", description="Check how long IRLmartin AI has left to warm up")
async def status(interaction: discord.Interaction):
    global end_time_utc
    now = datetime.now(timezone.utc)

    if end_time_utc and now < end_time_utc:
        remaining = end_time_utc - now
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        mins, secs = divmod(remainder, 60)

        # Format ETA in multiple timezones
        from zoneinfo import ZoneInfo

        utc_time = end_time_utc.strftime("%H:%M")
        eastern = end_time_utc.astimezone(ZoneInfo("America/New_York")).strftime("%H:%M")
        central = end_time_utc.astimezone(ZoneInfo("America/Chicago")).strftime("%H:%M")
        mountain = end_time_utc.astimezone(ZoneInfo("America/Denver")).strftime("%H:%M")
        pacific = end_time_utc.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%H:%M")

        await interaction.response.send_message(
            f"🤖 IRLmartin AI is still warming up.\n"
            f"⏱ Time left: **{hours}h {mins}m {secs}s**\n"
            f"🕒 **ETA:**\n"
            f"- UTC: {utc_time}\n"
            f"- Eastern: {eastern}\n"
            f"- Central: {central}\n"
            f"- Mountain: {mountain}\n"
            f"- Pacific: {pacific}"
        )
    elif end_time_utc:
        await interaction.response.send_message("✅ IRLmartin AI is fully warmed up.")
    else:
        await interaction.response.send_message("⚠️ The warm-up timer hasn't started yet.")
