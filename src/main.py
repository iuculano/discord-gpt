import os
import disnake, disnake.ext.commands
import commands

# Mandatory environment variables
discord_token  = os.environ['DISCORD_BOT_TOKEN']

# The bot needs the message intent to read conversations
# This must be enabled on your bot its Discord application
intents                 = disnake.Intents.default()
intents.message_content = True
bot                     = disnake.ext.commands.InteractionBot(intents = intents)

# Wrapper stuff is nasty
@bot.slash_command(description='Make a one-off request to ChatGPT. This maintains no memory of past requests or replies.')
async def prompt_text(interaction, prompt = disnake.ext.commands.Param(description = 'The prompt to send to ChatGPT.')):
    await commands.prompt_text(interaction, prompt)

@bot.slash_command(description='Request Dall-E to generate an image from a prompt.')
async def prompt_image(interaction, prompt = disnake.ext.commands.Param(description = 'The prompt to send to ChatGPT.')):
    await commands.prompt_image(interaction, prompt)

@bot.slash_command(description='Start a thread to use as a container for a conversation.')
async def start_chat(interaction, directive = disnake.ext.commands.Param(default = '', description = 'The base directive/personality to inject into the conversation.')):
    await commands.start_chat(interaction, directive)

@bot.event
async def on_message(message):
    await commands.on_message(message)

bot.run(discord_token)
