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
