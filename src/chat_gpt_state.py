import time
import queue
from   chat_gpt_messages import RoleType, Message, num_tokens_from_message


class ThreadState:
    '''
    Wrapper around the state of a conversation thread.
    '''
    def __init__(self, thread_id: int, directive: str):
        self._last_updated = int(time.time())
        self._thread_id    = thread_id
        self._directive    = Message(RoleType.SYSTEM, directive)
        self._token_count  = self.directive.token_count
        self._token_limit  = 4096 - self.directive.token_count # Since the context is permanent we can subtract it
        self._messages     = queue.Queue()

    @property
    def is_stale(self) -> int:
        return int(time.time()) - self._last_updated > 3600

    @property
    def directive(self) -> str:
        return self._directive

    @property
    def token_count(self) -> int:
        return self._token_count + 2

    @property
    def token_limit(self) -> int:
        return self._token_limit

    @property
    def messages(self) -> list:
        message_buffer = []
        message_buffer.append({'role': 'system', 'content': self.directive.content})
        message_buffer.extend(list(self._messages.queue))
        return message_buffer

    def update(self, message: Message):
        '''
        Pushes a message to the state's message queue, sacrificing messages if
        necessary to keep the token count under the limit, updating the thread
        state.
        '''
        # Push the message to the queue
        while message.token_count  + self.token_count > self.token_limit:
            sacrifice          = self._pop()
            sacrifice_tokens   = num_tokens_from_message(sacrifice)
            self._token_count -= sacrifice_tokens

        # Update the token count
        self._token_count += message.token_count
        self._messages.put(message.message)

    def _pop(self) -> Message:
        '''
        Pops the oldest message from the queue.
        Used to reclaim tokens when over budget.
        '''
        return self._messages.get()
