import os
import openai
import disnake
from chat_gpt_state    import ThreadState
from chat_gpt_messages import RoleType, Message


# Mandatory environment variables
openai.api_key = os.environ['OPENAI_API_KEY']

# Describe the base personality
chatgpt_base_personality = 'You are a helpful assistant. Use Discord style markdown when appropriate.'

# ChatGPT state for conversations
chatgpt_global_thread_state = {}


async def prompt_text(
    interaction: disnake.ApplicationCommandInteraction,
    prompt: str
):
    '''
    Slash command to make a one-off request to ChatGPT, optionally with a
    context to inject some personality into the reply.

    This does not retain any memory of the request or reply.
    '''

    await interaction.response.defer()
    response = openai.ChatCompletion.create(
        model    = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': chatgpt_base_personality},
            {'role': 'user', 'content': prompt}
        ]
    )

    await interaction.edit_original_response(response['choices'][0]['message']['content'].strip())

async def prompt_image(
    interaction: disnake.ApplicationCommandInteraction,
    prompt: str
):
    await interaction.response.defer()
    response = openai.Image.create(
        prompt = prompt,
        n      = 1,
        size   = '1024x1024'
    )

    url = response['data'][0]['url']
    await interaction.edit_original_response(url)

async def start_chat(
    interaction: disnake.ApplicationCommandInteraction,
    directive: str = None
):
    '''
    Slash command to start a thread to use as a container for a conversation.
    Optionally, a directive can be provided to inject some personality into the
    conversation.

    ChatGPT will maintain a buffer of messages to act as the conversation's
    memory. The buffer is rolling and will older messsages will be purged to
    make room for new ones.

    This is dependent on the token limit of ChatGPT. Longer requests and
    responses will consume more tokens, leading to quicker memory loss.
    This floats somewhere in the ballpark of 3000~ words.
    '''

    await interaction.response.defer()

    channel = interaction.channel
    thread  = await channel.create_thread(
        name                  = directive if directive else 'Just another ChatGPT conversation!',
        type                  = disnake.ChannelType.public_thread,
        auto_archive_duration = 60
    )

    # Define a thread's state
    # The context is considered permanent in the conversation and is always
    # the first message. We keep of the current and previous token counts
    # to determine the delta between messages -
    directive                              = directive if directive else chatgpt_base_personality
    chatgpt_global_thread_state[thread.id] = ThreadState(thread.id, directive)

    await interaction.edit_original_response('Registered.')

async def on_message(discord_message):
    # No idea if this is a good way to do this...

    # Threads that the bot started are tracked in the state
    # If we can match the channel id, we're talking in a bot thread
    state: ThreadState = chatgpt_global_thread_state.get(discord_message.channel.id)
    if state and discord_message.author.name != 'ChatGPT':
        # Purge history to stay under the token limit, if needed
        # This counts the tokens for the user's message to ensure it fits on
        # the message queue - this isn't perfect but will true-up after the
        # API call
        state.update(Message(RoleType.USER, discord_message.content))

        response = openai.ChatCompletion.create(
            model    = 'gpt-3.5-turbo',
            messages = state.messages
        )

        # Push the response, possibly sacrificing more messages
        content = response['choices'][0]['message']['content']

        # Cleared enough space to push the latest message
        state.update(Message(RoleType.ASSISTANT, content))
        await discord_message.channel.send(content.strip())
