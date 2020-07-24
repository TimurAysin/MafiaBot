from metaSingleton import MetaSingleton
import vk_api
import random
from game import Game, State, PlayerType, PlayerPack
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from message import *
from math import ceil
from players import *


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
        # Для настройки ролей
        self.__role = dict()
        # Для голосований
        self.__vote = dict()

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
        text = event.message["text"].split(' ')[-1].strip()

        if peer_id not in self.__groups and text != "Старт":
            self.__send_message_to_chat(peer_id, CREATE_NEW_GAME, "keyboards/intro.json")
        elif peer_id not in self.__groups and text == "Старт":
            self.__start_game(event, peer_id)
        elif self.__groups[peer_id].state == State.Init:
            if text == "Стандартный":
                self.__create_standard_roles(peer_id)
            elif text == "Настроить":
                self.__configure_roles(peer_id)
        elif self.__groups[peer_id].state == State.Config:
            self.__config_role(peer_id, text)
        elif self.__groups[peer_id].state == State.SetRole:
            self.__set_role(peer_id, text)
        elif self.__groups[peer_id].state == State.GroupChat and text == "Закончить":
            self.__start_vote(peer_id)
        elif self.__groups[peer_id].state == State.Vote:
            user = self.__groups[peer_id].ids[event.message["from_id"]]
            self.__add_vote(peer_id, text, user)

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

    def __send_message_to_person(self, d, text):
        id = self.__vk.users.get(
            user_ids=d
        )

        info = self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            message=text,
            user_ids=id[0]["id"]
        )
        return info

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
            self.__groups[peer_id].ids[participant["id"]] = participant["screen_name"]

        new_player_pack = PlayerPack(participants)
        return new_player_pack

    def __start_game(self, event, peer_id):
        self.__groups[peer_id] = Game()

        self.__send_message_to_chat(peer_id, START)
        self.__send_message_to_chat(peer_id, HEAD_COUNT)

        new_player_pack = self.__do_head_count(event, peer_id)
        self.__groups[peer_id].player_pack = new_player_pack

        self.__send_message_to_chat(peer_id, new_player_pack.pretty_print())

        self.__prompt_roles(peer_id, new_player_pack)

    def __prompt_roles(self, peer_id, new_player_pack):
        self.__send_message_to_chat(peer_id, ROLES_PROMPT)

        number_of_players = len(new_player_pack.players)

        # According to Wikipedia rules
        default_mafia_count = ceil(number_of_players / 4.0)

        self.__send_message_to_chat(peer_id, suggest_default(default_mafia_count))
        self.__send_message_to_chat(peer_id, CUSTOM_PACK, keyboard="keyboards/role_type.json")

        self.__groups[peer_id].state = State.Init

    def __create_standard_roles(self, peer_id):
        number_of_players = len(self.__groups[peer_id].player_pack.players)
        default_mafia_count = ceil(number_of_players / 4.0)

        if number_of_players < 3:
            self.__send_message_to_chat(peer_id, DEFAULT_ROLES_ERROR)
            return

        role_count = {
            Mafia: default_mafia_count,
            Doctor: 1,
            Commissioner: 1,
            Civilian: number_of_players - default_mafia_count - 2
        }

        self.__groups[peer_id].add_role_count(role_count)
        self.__groups[peer_id].start_game()
        self.__start_chat(peer_id)

    def __configure_roles(self, peer_id):
        self.__send_message_to_chat(peer_id, CONFIG_EXPLAIN, keyboard="keyboards/role_config.json")
        self.__groups[peer_id].state = State.Config
        self.__groups[peer_id].player_pack.role_count = {}

    def __config_role(self, peer_id, text):
        if text == "Маньяк":
            self.__role[peer_id] = Maniac
        elif text == "Мирный":
            self.__role[peer_id] = Civilian
        elif text == "Коммиссар":
            self.__role[peer_id] = Commissioner
        elif text == "Доктор":
            self.__role[peer_id] = Doctor
        elif text == "Дон":
            self.__role[peer_id] = Don
        elif text == "Мафия":
            self.__role[peer_id] = Mafia
        elif text == "Готово":
            self.__check_roles(peer_id)

        if peer_id in self.__role.keys():
            self.__groups[peer_id].state = State.SetRole
            self.__send_message_to_chat(peer_id, ROLE_VALUE, keyboard="keyboards/cancel.json")

    def __set_role(self, peer_id, text):
        if not text.isnumeric() and text != "Отмена":
            self.__send_message_to_chat(peer_id, ROLE_VALUE_ERROR)
        elif text == "Отмена":
            del self.__role[peer_id]
            self.__groups[peer_id].state = State.Config
            self.__send_message_to_chat(peer_id, "Ок", keyboard="keyboards/role_config.json")
        else:
            self.__groups[peer_id].player_pack.role_count[self.__role[peer_id]] = int(text)
            current_roles = self.__get_current_roles(peer_id)
            del self.__role[peer_id]
            self.__groups[peer_id].state = State.Config

            self.__send_message_to_chat(peer_id, ROLE_VALUE_SUCCESS, keyboard="keyboards/role_config.json")
            self.__send_message_to_chat(peer_id, current_roles, keyboard="keyboards/role_config.json")

    def __check_roles(self, peer_id):
        self.__send_message_to_chat(peer_id, ROLE_VALUE_CHECK)
        self.__send_message_to_chat(peer_id, self.__groups[peer_id].player_pack.pretty_print_role_count())

        if not self.__groups[peer_id].player_pack.make_roles():
            self.__send_message_to_chat(peer_id, text="Количество участников не совпадает с общим количеством ролей.")
        else:
            self.__start_chat(peer_id)

    def __start_chat(self, peer_id):
        self.__send_message_to_chat(peer_id, ROLE_CONFIG_SUCCESS)
        self.__groups[peer_id].state = State.GroupChat
        self.__send_message_to_chat(peer_id, CHAT_BEGIN, keyboard="keyboards/chat.json")
        self.__send_info(peer_id)
        self.__print_mafia(peer_id)

    def __send_info(self, peer_id):
        for player in self.__groups[peer_id].player_pack.players:
            text = ""

            if player.role == PlayerType.Civilian:
                text = CIVILIAN_DESC
            elif player.role == PlayerType.Commissioner:
                text = COMMISSIONER_DESC
            elif player.role == PlayerType.Mafia:
                text = MAFIA_DESC
            elif player.role == PlayerType.Doctor:
                text = DOCTOR_DESC
            elif player.role == PlayerType.Maniac:
                text = MANIAC_DESC
            elif player.role == PlayerType.Don:
                text = DON_DESC

            self.__send_message_to_person(player.screen_name, text)

    def __print_alive(self, peer_id):
        p = self.__groups[peer_id].player_pack.players

        info = "Активные игроки:\n"
        i = 1
        for player in p:
            if not player.active:
                i += 1
                continue
            info += "{}. @{} {}\n".format(str(i), player.screen_name, player.name)
            i += 1

        self.__send_message_to_chat(peer_id, info)

    def __print_mafia(self, peer_id):
        bad_people = self.__groups[peer_id].players_by_type(Mafia)
        bad_people += self.__groups[peer_id].players_by_type(Don)

        info = "Активные мафии и доны:\n"
        i = 1
        for player in bad_people:
            if not player.active:
                i += 1
                continue
            if player.role == PlayerType.Mafia:
                info += "{}. @{} {} - Мафия.\n".format(str(i), player.screen_name, player.name)
            elif player.role == PlayerType.Don:
                info += "{}. @{} {} - Дон.\n".format(str(i), player.screen_name, player.name)
            i += 1

        for player in bad_people:
            if player.active:
                self.__send_message_to_person(player.screen_name, info)

    def __start_vote(self, peer_id):
        self.__send_message_to_chat(peer_id, VOTE_BEGIN, keyboard="keyboards/vote.json")
        self.__print_alive(peer_id)
        self.__groups[peer_id].state = State.Vote
        self.__vote[peer_id] = 0
        self.__ask_for_vote(peer_id, 0)

    def __ask_for_vote(self, peer_id, ind):
        players = self.__groups[peer_id].player_pack.players
        while ind < len(players) and not players[ind].active:
            ind += 1

        if ind >= len(players):
            return -1

        self.__send_message_to_chat(peer_id, VOTE_ASK.format(players[ind].screen_name))
        return ind

    def __add_vote(self, peer_id, text, user):
        if user != self.__groups[peer_id].player_pack.players[self.__vote[peer_id]].screen_name:
            return

        if text == "Воздерживаюсь":
            self.__groups[peer_id].votes[user] = -1
            self.__send_message_to_chat(peer_id, VOTE_NONE.format(user))
            ind = self.__ask_for_vote(peer_id, self.__vote[peer_id] + 1)
            if ind != -1:
                self.__vote[peer_id] = ind
            else:
                self.__end_vote(peer_id)
        else:
            if not text.isnumeric():
                return

            n = int(text)

            if n < 1 or n > len(self.__groups[peer_id].player_pack.players):
                return

            if not self.__groups[peer_id].player_pack.players[n - 1].active:
                return

            self.__groups[peer_id].votes[user] = n - 1
            self.__send_message_to_chat(peer_id,
                                        VOTE.format(user, self.__groups[peer_id].player_pack.players[
                                            self.__vote[peer_id]].screen_name))
            ind = self.__ask_for_vote(peer_id, self.__vote[peer_id] + 1)
            if ind != -1:
                self.__vote[peer_id] = ind
            else:
                self.__end_vote(peer_id)

    def __end_vote(self, peer_id):
        del self.__vote[peer_id]
        temp = dict()
        m = -1

        for key, value in self.__groups[peer_id].votes.items():
            if value != -1:
                temp[value] += 1
                m = max(m, temp[value])

        self.__send_message_to_chat()

    def __get_current_roles(self, peer_id):
        return ROLE_INFO + self.__groups[peer_id].player_pack.pretty_print_role_count()
