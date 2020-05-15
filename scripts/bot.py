import vk_api
import random
from game import Game, State, PlayerType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot:
    def __init__(self):
        self.__token = "55d54859bfc02268950c448c91fe6c95e1261b94e960bea620907555863ed31ed7bc9ca462dd619e1bfed"
        self.__group_id = "195261716"

        self.__vk_session = vk_api.VkApi(token=self.__token)
        self.__longpoll = VkBotLongPoll(self.__vk_session, self.__group_id)
        self.__vk = self.__vk_session.get_api()
        self.__groups = dict()

    def start_polling(self):
        for event in self.__longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                group = event.message["peer_id"] - 2000000000
                if group not in self.__groups.keys():
                    print("New group id:", group)
                    self.__add_group(group, event)
                else:
                    self.__handle_events(group, event)

    def __handle_events(self, group, event):
        game = self.__groups[group]
        if game.state == State.StartGame:
            self.__handle_start_game(group, event)

    def __send_message_to_chat(self, event, text):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            chat_id=event.message["peer_id"] - 2000000000,
            message=text
        )

    def __send_message_to_person(self, d, text):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            domain=d,
            message=text
        )

    def __add_group(self, group, event):
        game = Game()
        self.__groups[group] = game
        # Добавление бота в беседу
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"] == "":
            self.__send_message_to_chat(event, game.greet())
        # Бот уже в беседе
        elif event.type == VkBotEventType.MESSAGE_NEW:
            self.__handle_start_game(group, event)
            
    def __handle_start_game(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"] == "/start":
            self.__groups[group].state = State.InGame
            self.__send_message_to_chat(event, self.__groups[group].start())

            profiles = self.__vk.messages.getConversationMembers(
                peer_id=event.message["peer_id"]
            )["profiles"]

            participants = []

            for info in profiles:
                participants.append({
                    "screen_name": info["screen_name"],
                    "name": info["first_name"] + " " + info["last_name"]
                })

            self.__groups[group].participants = participants

            self.__send_message_to_chat(event, self.__groups[group].print_participants())
            self.__send_message_to_chat(event, "Распределяю роли...")
            self.__groups[group].make_roles()
            self.send_invitation_to_players(self.__groups[group].players)
        elif event.message["text"] != "/start":
            self.__send_message_to_chat(event, "Я не знаю этой команды.")

    def send_invitation_to_players(self, players):
        for player in players:
            self.__send_message_to_person(player.screen_name, "Поздравляем, вы - невиновный.")
