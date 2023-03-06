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
@bot.slash_command()
async def prompt_text(interaction, prompt):
    await commands.prompt_text(interaction, prompt)

@bot.slash_command()
async def prompt_image(interaction, prompt):
    await commands.prompt_image(interaction, prompt)

@bot.slash_command()
async def start_chat(interaction, directive):
    await commands.start_chat(interaction, directive)

@bot.event
async def on_message(message):
    await commands.on_message(message)

bot.run(discord_token)
