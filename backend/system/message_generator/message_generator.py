from typing import Dict


class MessageGenerator(object):

    default_vocabulary: Dict[str, str] = {

    }

    default_messages: Dict[str, str] = {

    }

    def __init__(self):
        self._vocabulary = self.default_vocabulary.copy()
        self._messages = self.default_messages.copy()

    def get_message(self, key: str, vocabulary: Dict[str, str] = None) -> str:
        context_vocabulary = self._vocabulary
        if vocabulary:
            # if vocabulary is provided, a clone of the original is made and then updated with provided data
            context_vocabulary = self._vocabulary.copy()
            context_vocabulary.update(vocabulary)
        return self._messages.get(key, '').format(**context_vocabulary)

    def load(self, *, messages: Dict[str, str]=dict(), vocabulary: Dict[str, str]=dict()):
        self._messages.update(messages)
        self._vocabulary.update(vocabulary)


message_generator = MessageGenerator()


def get_message(key, vocabulary=None):
    return message_generator.get_message(key, vocabulary)

