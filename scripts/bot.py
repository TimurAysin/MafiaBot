from metaSingleton import MetaSingleton
import vk_api
import random
from game import Game, State, PlayerType, PlayerPack
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from message import *
from math import ceil


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
        if event.type != VkBotEventType.MESSAGE_NEW:
            return

        text = event.message["text"].split(' ')[-1].strip()

        if peer_id not in self.__groups and text != "Старт":
            self.__send_message_to_chat(peer_id, CREATE_NEW_GAME, "keyboards/intro.json")
            return
        elif text == "Старт":
            self.__start_game(event, peer_id)
            return

    def __send_message_to_chat(self, peer_id, text, keyboard=None):
        print("Sending " + text)
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

    def __do_head_count(self, event, peer_id):
        info = self.__vk.messages.getConversationMembers(
            peer_id=event.message["peer_id"]
        )

        participants = []
        for participant in info["profiles"]:
            participants.append({
                "screen_name": participant["screen_name"],
                "name": participant["first_name"] + " " + participant["last_name"]
            })

        new_player_pack = PlayerPack(participants)
        return new_player_pack

    def __start_game(self, event, peer_id):
        self.__groups[peer_id] = Game

        self.__send_message_to_chat(peer_id, START)
        self.__send_message_to_chat(peer_id, HEAD_COUNT)

        new_player_pack = self.__do_head_count(event, peer_id)

        self.__send_message_to_chat(peer_id, new_player_pack.pretty_print())

        self.__make_roles(event, peer_id, new_player_pack)

    def __make_roles(self, event, peer_id, new_player_pack):
        self.__send_message_to_chat(peer_id, ROLES_PROMPT)

        number_of_players = len(new_player_pack.players)
        default_mafia_count = ceil(number_of_players / 4.0)

        self.__send_message_to_chat(peer_id, suggest_default(default_mafia_count))
        self.__send_message_to_chat(peer_id, CUSTOM_PACK, keyboard="keyboards/role_type.json")
