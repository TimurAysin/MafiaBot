import vk_api
import random
from game import Game, State
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot:
    def __init__(self):
        self.__token = "55d54859bfc02268950c448c91fe6c95e1261b94e960bea620907555863ed31ed7bc9ca462dd619e1bfed"
        self.__group_id = "195261716"

        self.__vk_session = vk_api.VkApi(token=self.__token)
        self.__longpoll = VkBotLongPoll(self.__vk_session, self.__group_id)
        self.__vk = self.__vk_session.get_api()
        self.__groups = dict()

    def startPolling(self):
        for event in self.__longpoll.listen():
            group = event.message["peer_id"] - 2000000000
            if (group in self.__groups.keys()):
                self.__handleEvents(group, event)
            else:
                print("New group id:", group)
                self.__addGroup(group, event)

    def __handleEvents(self, group, event):
        game = self.__groups[group]
        if (game.state == State.NotActive):
            self.handleNotActive(self, group, event)

    def __sendMessage(self, event, text):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            chat_id=event.message["peer_id"] - 2000000000,
            message=text
        )

    def __addGroup(self, group, event):
        game = Game()
        self.__groups[group] = game
        self.__sendMessage(event, game.greet())

    def __handleNotActive(self, group, event):
        if (event.type == VkBotEventType.MESSAGE_NEW and event.message["text"].lower == "/start"):
            