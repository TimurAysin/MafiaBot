import vk_api
import random
from game import Game
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Server:
    def __init__(self):
        self.__token = "55d54859bfc02268950c448c91fe6c95e1261b94e960bea620907555863ed31ed7bc9ca462dd619e1bfed"
        self.__group_id = "195261716"

        self.__vk_session = vk_api.VkApi(token=self.__token)
        self.__longpoll = VkBotLongPoll(self.__vk_session, self.__group_id)
        self.__vk = self.__vk_session.get_api()
        self.__intro_string = "Здравствуйте! Рад, что вы собрались сегодня, чтобы поиграть в мафию. \
                                Я буду вашим ведущим. Для того, чтобы начать, напишите команду: /start. \
                                Желаю приятной игры!"

    def startPolling(self):
        for event in self.__longpoll.listen():
            self.handleEvents(event)

    def handleEvents(self, event):
        if (event.type == VkBotEventType.MESSAGE_NEW):
            if (event.message["text"].lower() == "начать"):
                self.sendMessage(event, self.__intro_string)
            elif (event.message["text"] == "/start"):
                self.sendMessage(event, "Начинаем!")

    def sendMessage(self, event, text):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            chat_id=event.message["peer_id"] - 2000000000,
            message=text
        )
