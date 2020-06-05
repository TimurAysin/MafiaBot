from messageType import MessageType
from metaSingleton import MetaSingleton


class Message(metaclass=MetaSingleton):
    __messages = {
        MessageType.Info: "info",
        MessageType.Greeting: "greeting"
    }

    def __init__(self):
        print("Message system is active.")

    def get(self, key):
        if not isinstance(key, MessageType):
            print("Wrong message type -" + key)
        else:
            return self.__messages[key]
