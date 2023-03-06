import tiktoken


# Encoder to count tokens - https://github.com/openai/tiktoken
token_encoder = tiktoken.encoding_for_model('gpt-3.5-turbo-0301')


# https://platform.openai.com/docs/guides/chat/managing-tokens
def num_tokens_from_string(string: str) -> int:
    '''
    Returns the number of tokens a string will consume in ChatGPT.
    '''
    return len(token_encoder.encode(string))

# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_message(message: dict) -> int:
    '''
    Returns the number of tokens a message will consume in ChatGPT.
    '''
    total_tokens = 0
    for value in message.values():
        # My best guess is 'im_start' + 'im_end' = 4 tokens
        # It must not be counted like <im_start> or <|im_start|>?
        # This isn't clearly documented at all...
        total_tokens += num_tokens_from_string(value) + 4

    # I think this something from the API when it replies?
    # token_count += 2
    return total_tokens

class RoleType:
    '''
    Enum for the role of a message.
    '''
    SYSTEM    = 'system'
    USER      = 'user'
    ASSISTANT = 'assistant'

class Message:
    '''
    Wrapper around message to and from ChatGPT.
    '''
    def __init__(self, role: RoleType, content: str):
        self._role        = role
        self._content     = content
        self._message     = {'role': role, 'content': content}
        self._token_count = num_tokens_from_message(self.message)

    @property
    def message(self) -> dict:
        return self._message

    @property
    def token_count(self) -> int:
        return self._token_count
