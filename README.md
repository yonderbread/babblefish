# Babblefish

A Discord bot that automatically translates messages between two configured languages using ChatGPT.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `config.json` file (ignored by git) containing your tokens and any
   preset channel language pairs:

```json
{
  "discord_token": "your_discord_bot_token",
  "openai_api_key": "your_openai_key",
  "channels": {}
}
```

3. Run the bot:

```bash
python bot.py
```

## Usage

In any Discord channel where the bot is present, run the slash command:

```
/start LANG_A LANG_B
```

Replace `LANG_A` and `LANG_B` with the languages you want to translate between (e.g. `English` and `Portuguese`). After starting, any message sent in that channel in either of the two languages will receive a reply with its translation into the other language.

Example:

- Sending `Oi, eu te amo` will make the bot reply `Hi, I love you`.
- Sending `Hi, how are you?` will make the bot reply `Oi, tudo bem?`.

Channel and token information is stored locally in `config.json`, which is ignored by git so your secrets stay on your machine.
