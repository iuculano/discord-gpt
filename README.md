# Discord ChatGPT Bot
Extremely simple Discord bot for ChatGPT and DALL-E.

## Getting started
Create an OpenAI API key. You may need to put a card on file.
* [OpenAI API Keys](https://platform.openai.com/account/api-keys)

Create a Discord application.
* [Discord Applications](https://discord.com/developers/applications/)

1. Enable the `MESSAGE CONTENT INTENT` feature under `Bot`.
2. Grant the `bot` and `applications.commands` scope under OAuth.
3. Grant the `Send Messages`, `Create Public Threads`, and `Send Messages in Threads` permissions.
4. Copy the URL and navigate to it to join it to your server.

Set the `OPENAI_API_KEY` and `DISCORD_BOT_TOKEN` environment variables and run.

## Docker
One of the easiest ways to run the bot is with Docker.

```bash
docker build . --tag discord-gpt:latest
docker run -d -e OPENAI_API_KEY='KEY_HERE' -e DISCORD_BOT_TOKEN='TOKEN_HERE' discord-gpt:latest
```
