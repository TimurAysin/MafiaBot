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
        elif game.state == State.GroupChat:
            self.__handle_vote_start(group, event)
        elif game.state == State.Vote:
            self.__handle_vote(group, event)

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
            self.__groups[group].state = State.GroupChat
            self.__send_message_to_chat(event, self.__groups[group].start())

            info = self.__vk.messages.getConversationMembers(
                peer_id=event.message["peer_id"]
            )

            profiles = info["profiles"]
            participants = []

            ids = dict()

            for profile in profiles:
                participants.append({
                    "screen_name": profile["screen_name"],
                    "name": profile["first_name"] + " " + profile["last_name"]
                })

                ids[profile["id"]] = profile["screen_name"]

            self.__groups[group].participants = participants
            self.__groups[group].ids = ids

            self.__send_message_to_chat(event, self.__groups[group].print_participants())
            self.__send_message_to_chat(event, "Распределяю роли...")
            self.__groups[group].make_roles()
            self.__send_invitation_to_players(self.__groups[group].players)

            # Потом добавлю изменение и контроль времени
            self.__send_message_to_chat(event,
                                        "Распределение ролей завершено! У игроков активных ролей будет по 1 минуте для того, чтобы сделать выбор.")
            self.__send_message_to_chat(event,
                                        "Время на общий разговор - 10 минут.")
            self.__send_message_to_chat(event,
                                        "Можете начинать обсуждение. Чтобы закончить обсуждение и начать голосование, введите команду: /vote")
        elif event.message["text"] != "/start":
            self.__send_message_to_chat(event, "Я не знаю этой команды.")

    def __send_invitation_to_players(self, players):
        for player in players:
            if player.role == PlayerType.Civilian:
                self.__send_message_to_person(player.screen_name, "Поздравляем, вы - невиновный. Остерегайтесь мафии.")
            elif player.role == PlayerType.Doctor:
                self.__send_message_to_person(player.screen_name,
                                              "Поздравляем, вы - доктор. Только вы можете спасти жителей города.")
            elif player.role == PlayerType.Commissioner:
                self.__send_message_to_person(player.screen_name,
                                              "Поздравляем, вы - коммисар. Ваш долг - поймать мафию и спасти невинных.")
            else:
                self.__send_message_to_person(player.screen_name,
                                              "Поздравляем, вы - мафия. Убейте всех!")

    def __handle_vote_start(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"] == "/vote":
            self.__send_message_to_chat(event, "Обсуждение закончено. Начинается голосование.")
            self.__send_message_to_chat(event,
                                        "Каждый игрок должен написать номер другого игрока, за которого он голосует, или 0, если воздерживается.")

            self.__groups[group].state = State.Vote
        else:
            self.__send_message_to_chat(event, "Вы хотите начать голосование? Тогда введите команду /vote.")

    def __handle_vote(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"].isnumeric():
            vote = int(event.message["text"])
            user = self.__groups[group].ids[event.message["from_id"]]

            if user in self.__groups[group].votes.keys():
                self.__send_message_to_chat(event, "Пользователь " + user + " уже проголосовал.")
                return

            if vote == 0:
                msg = "Игрок @" + user + " воздержался от голосования."
                self.__send_message_to_chat(event, msg)
                self.__groups[group].votes[user] = vote
            elif len(self.__groups[group].players) >= vote > 0:
                msg = "Игрок @" + user + " проголосовал за удаление игрока @" + self.__groups[group].players[
                    vote - 1].screen_name + "."
                self.__send_message_to_chat(event, msg)

                if user == self.__groups[group].players[vote - 1].screen_name:
                    self.__send_message_to_chat(event, "Оригинально.")

                self.__groups[group].votes[user] = vote
            else:
                msg = "Игрок @" + user + " ввел неправильный номер. Он может снова проголосовать."
                self.__send_message_to_chat(event, msg)

            if len(self.__groups[group].votes.keys()) == len(self.__groups[group].players):
                self.__groups[group].state = State.Sleep
        elif event.type == VkBotEventType.MESSAGE_NEW:
            self.__send_message_to_chat(event, "Не могу понять. Введите еще раз.")