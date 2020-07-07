from metaSingleton import MetaSingleton
import vk_api
import random
from game import Game, State, PlayerType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from message import *


class Bot(metaclass=MetaSingleton):
    def __init__(self):
        # VK_API
        self.__token = "55d54859bfc02268950c448c91fe6c95e1261b94e960bea620907555863ed31ed7bc9ca462dd619e1bfed"
        self.__group_id = "195261716"
        self.__vk_session = vk_api.VkApi(token=self.__token)
        self.__longpoll = VkBotLongPoll(self.__vk_session, self.__group_id)
        self.__vk = self.__vk_session.get_api()

        # Группы, в которых бот запущен
        self.__groups = dict()

    def start_polling(self):
        for event in self.__longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id, from_us = Bot.get_peer_id(event)

                if from_us:
                    self.__handle_user_msg(event, peer_id)
                else:
                    self.__handle_group_msg(event, peer_id)

    def __handle_user_msg(self, event, peer_id):
        self.__send_message_to_peer(peer_id, PROPOSITION_TO_CREATE_GAME)

    def __handle_group_msg(self, event, peer_id):
        if peer_id not in self.__groups:
            self.__send_message_to_chat(peer_id, CREATE_NEW_GAME, "keyboards/intro.json")
            return

    def __send_message_to_chat(self, peer_id, text, keyboard=None):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            chat_id=peer_id,
            message=text,
            keyboard=None if (keyboard is None) else open(keyboard, "r", encoding="UTF-8").read()
        )

    def __send_message_to_peer(self, peer_id, text, keyboard=None):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            peer_id=peer_id,
            message=text,
            keyboard=None if (keyboard is None) else open(keyboard, "r", encoding="UTF-8").read()
        )

    @staticmethod
    def get_peer_id(event):
        peer_id = event.message["peer_id"] - 2000000000
        from_us = False
        if peer_id < 0:
            from_us = True
            peer_id += 2000000000
        return [peer_id, from_us]
