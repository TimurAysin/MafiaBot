from messageType import MessageType
from metaSingleton import MetaSingleton


class Message(metaclass=MetaSingleton):
    __messages = {
        MessageType.Bot_Cond: "Для того, чтобы я мог функционировать, сделайте несколько вещей:\n"
                              "1. Назначьте меня администратором группы.\n"
                              "2. Каждый игрок, если играет впервые, должен отправить мне сообщение."
                              " Иначе я не смогу отправлять ему сообщения.\nНа этом всё!",
        MessageType.Greeting: "Здравствуйте! Рад, что вы собрались сегодня, чтобы поиграть в мафию. "
                              "Я буду вашим ведущим!",
        MessageType.Start: "Начинаем!",
    }

    def __init__(self):
        print("Message system is active.")

    def get(self, key):
        if not isinstance(key, MessageType):
            print("Wrong message type -" + key)
        else:
            return self.__messages[key]
