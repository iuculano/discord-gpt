import os
import openai
import disnake
from disnake.ext import commands

openai.api_key = os.getenv('OPENAI_API_KEY')

# The bot needs the message intent to read conversations
# This must be enabled on your bot its Discord application
intents                 = disnake.Intents.default()
intents.message_content = True
bot                     = commands.InteractionBot(intents = intents)

# State of conversations - tracks live conversations
chatgpt_state = {}

@bot.slash_command(description = 'Asks ChatGPT a one-off question.')
async def query(interaction: disnake.ApplicationCommandInteraction, query: str):
    response = openai.ChatCompletion.create(
        model    = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': query}]
    )

    await interaction.send(response['choices'][0]['message']['content'].strip())

@bot.slash_command(description = 'Starts a thread to use as a container for a conversation.')
async def start_chat(interaction: disnake.ApplicationCommandInteraction, context: str = None):
    channel = interaction.channel
    thread  = await channel.create_thread(
        name                  = context if context else 'Just another ChatGPT conversation!',
        type                  = disnake.ChannelType.public_thread,
        auto_archive_duration = 60
    )

    chatgpt_state[thread.id] = {
        'name':     thread.name,
        'messages': [{'role': 'system', 'content': context if context else 'You are a helpful assistant.'},]
    }


@bot.event
async def on_message(message):
    chatgpt_thread = chatgpt_state.get(message.channel.id)
    if chatgpt_thread and message.author.name != 'ChatGPT':
        chatgpt_thread['messages'].append({'role': 'user', 'content': message.content})

        response = openai.ChatCompletion.create(
            model    = 'gpt-3.5-turbo',
            messages = chatgpt_thread['messages']
        )

        content = response['choices'][0]['message']['content'].strip()
        chatgpt_thread['messages'].append({'role': 'assistant', 'content': content})

        await message.channel.send(content)

discord_token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(discord_token)
