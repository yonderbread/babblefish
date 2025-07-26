import json
import os

import discord
from discord import app_commands
import openai

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
else:
    config = {
        "discord_token": "YOUR_DISCORD_TOKEN",
        "openai_api_key": "YOUR_OPENAI_KEY",
        "channels": {}
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    raise SystemExit(
        f"Please fill out {CONFIG_FILE} with your tokens and restart the bot.")

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

openai.api_key = config.get("openai_api_key")

def get_token():
    token = config.get("discord_token")
    if not token:
        raise RuntimeError("discord_token not configured in config.json")
    return token

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

async def translate(text: str, lang_a: str, lang_b: str) -> str:
    system_prompt = (
        f"You are a translator between {lang_a} and {lang_b}. "
        f"When the user writes in {lang_a}, reply only with the most empathetic "
        f"{lang_b} translation. When they write in {lang_b}, reply only with "
        f"the equivalent {lang_a} translation. Do not add explanations or notes."
    )
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return response['choices'][0]['message']['content'].strip()

@tree.command(name="start", description="Configure translation languages for this channel")
@app_commands.describe(lang_a='First language', lang_b='Second language')
async def start(interaction: discord.Interaction, lang_a: str, lang_b: str):
    channel_id = str(interaction.channel_id)
    config.setdefault("channels", {})[channel_id] = {
        "lang_a": lang_a,
        "lang_b": lang_b,
    }
    save_config()
    await interaction.response.send_message(
        f"Translation started between {lang_a} and {lang_b} in this channel.",
        ephemeral=True,
    )

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    channel_id = str(message.channel.id)
    channels = config.get("channels", {})
    if channel_id not in channels:
        return

    lang_a = channels[channel_id]["lang_a"]
    lang_b = channels[channel_id]["lang_b"]
    translation = await translate(message.content, lang_a, lang_b)
    embed = discord.Embed(description=translation)
    await message.reply(embed=embed)
    try:
        await message.add_reaction("\U0001f5e3")  # speech balloon
    except discord.HTTPException:
        pass

def main():
    bot.run(get_token())

if __name__ == '__main__':
    main()
