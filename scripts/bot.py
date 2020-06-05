from typing import Type

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
                from_us = False
                if group < 0:
                    from_us = True
                    group += 2000000000
                    if group in self.__groups.keys():
                        group = self.__groups[group]
                    else:
                        self.__send_message_to_peer(event, "Вы не зарегестрированы ни в одной игре. Хотите начать?")
                        self.__send_message_to_peer(event, "Просто добавьте меня в беседу с вашими друзьями,"
                                                           " и мы начнем.")
                        continue

                if group not in self.__groups.keys():
                    print("New group id:", group)
                    self.__add_group(group, event)
                else:
                    self.__handle_events(group, event, from_us)

    def __handle_events(self, group, event, from_us):
        game = self.__groups[group]
        if game.state == State.StartGame:
            self.__handle_start_game(group, event)
        else:
            if not game.state == State.LastWord:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if not self.__check_alive(group, event):
                        return

            if game.state == State.GroupChat:
                self.__handle_vote_start(group, event)
            elif game.state == State.Vote:
                self.__handle_vote(group, event)
            elif game.state == State.LastWord:
                self.__handle_last_word(group, event)
            elif game.state == State.MafiaChatInProcess and from_us:
                self.__handle_mafia_chat_process(group, event)
            elif game.state == State.Commissioner and from_us:
                self.__handle_commissioner_query(group, event)
            elif game.state == State.Doctor and from_us:
                self.__handle_doctor_query(group, event)

    def __send_message_to_chat(self, peer_id, text):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            chat_id=peer_id - 2000000000,
            message=text
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

    def __send_message_to_peer(self, event, text):
        self.__vk.messages.send(
            random_id=random.randint(1, 1000000000000),
            peer_id=event.message["peer_id"],
            message=text
        )

    def __add_group(self, group, event):
        game = Game()
        self.__groups[group] = game
        self.__groups[group].chat_id = event.message["peer_id"]
        # Добавление бота в беседу
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"] == "":
            self.__send_message_to_chat(event.message["peer_id"].message["peer_id"], game.greet())
        # Бот уже в беседе
        elif event.type == VkBotEventType.MESSAGE_NEW:
            self.__handle_start_game(group, event)

    def __handle_start_game(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"] == "/start":
            self.__groups[group].state = State.GroupChat
            self.__send_message_to_chat(event.message["peer_id"], self.__groups[group].start())

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

            self.__send_message_to_chat(event.message["peer_id"], self.__groups[group].print_participants())
            self.__send_message_to_chat(event.message["peer_id"], "Распределяю роли...")
            self.__groups[group].make_roles()
            self.__send_invitation_to_players(self.__groups[group].players)

            # Потом добавлю изменение и контроль времени
            self.__send_message_to_chat(event.message["peer_id"],
                                        "Распределение ролей завершено! "
                                        "У игроков активных ролей будет по 1 минуте для того, чтобы сделать выбор.")
            self.__send_message_to_chat(event.message["peer_id"],
                                        "Время на общий разговор - 10 минут.")
            self.__send_message_to_chat(event.message["peer_id"],
                                        "Можете начинать обсуждение. "
                                        "Чтобы закончить обсуждение и начать голосование, введите команду: /vote")
        elif event.message["text"] != "/start":
            self.__send_message_to_chat(event.message["peer_id"], "Я не знаю этой команды.")

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
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message["text"] == "/vote":
                self.__send_message_to_chat(event.message["peer_id"], "Обсуждение закончено. Начинается голосование.")
                self.__send_message_to_chat(event.message["peer_id"],
                                            "Каждый игрок должен написать номер другого игрока, "
                                            "за которого он голосует, или 0, если воздерживается.")

                self.__groups[group].state = State.Vote
        else:
            self.__send_message_to_chat(event.message["peer_id"],
                                        "Вы хотите начать голосование? Тогда введите команду /vote.")

    def __handle_vote(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW and event.message["text"].isnumeric():
            vote = int(event.message["text"])
            user = self.__groups[group].ids[event.message["from_id"]]

            if user in self.__groups[group].votes.keys():
                self.__send_message_to_chat(event.message["peer_id"], "Игрок " + user + " уже проголосовал.")
                return

            if vote == 0:
                msg = "Игрок @" + user + " воздержался от голосования."
                self.__send_message_to_chat(event.message["peer_id"], msg)
                self.__groups[group].votes[user] = vote
            elif len(self.__groups[group].players) >= vote > 0:
                msg = "Игрок @" + user + " проголосовал за удаление игрока @" + self.__groups[group].players[
                    vote - 1].screen_name + "."
                self.__send_message_to_chat(event.message["peer_id"], msg)

                if user == self.__groups[group].players[vote - 1].screen_name:
                    self.__send_message_to_chat(event.message["peer_id"], "Оригинально.")

                self.__groups[group].votes[user] = vote
            else:
                msg = "Игрок @" + user + " ввел неправильный номер. Он может снова проголосовать."
                self.__send_message_to_chat(event.message["peer_id"], msg)

            if len(self.__groups[group].votes.keys()) == len(self.__groups[group].players):
                self.__handle_sleep(group, event)

        elif event.type == VkBotEventType.MESSAGE_NEW:
            self.__send_message_to_chat(event.message["peer_id"], "Не могу понять. Введите еще раз.")

    def __handle_sleep(self, group, event):
        self.__send_message_to_chat(event.message["peer_id"], "Голосование завершено.")
        lst = list(self.__groups[group].votes.values())
        self.__groups[group].votes = dict()

        d = dict()
        m1 = -1
        m2 = -1

        for i in range(1, len(self.__groups[group].participants) + 1):
            d[i] = lst.count(i)
            if d[i] == 0:
                continue
            if m1 == -1:
                m1 = i
            elif d[i] > d[m1]:
                m1, m2 = i, m1
            elif m2 == -1 or d[i] > d[m2]:
                m2 = i

        if m1 == -1:
            self.__send_message_to_chat(event.message["peer_id"], "Сегодня никого не исключаем.")
            self.__start_night(group, event)
        elif m2 != -1 and d[m1] == d[m2] and d[m1] != 0:
            self.__send_message_to_chat(event.message["peer_id"], "Похоже, голосов поровну. Надо переголосовать.")
        else:
            self.__send_message_to_chat(event.message["peer_id"], "Прощаемся с игроком: " + str(m1))
            self.__send_message_to_chat(event.message["peer_id"],
                                        "Игрок " + str(m1) + " имеет право на последнее слово. "
                                                             "Для завершения напишите команду: /done.")
            self.__groups[group].delete_player(m1 - 1)
            self.__groups[group].last_breath = self.__groups[group].players[m1 - 1]
            self.__groups[group].state = State.LastWord

    def __start_night(self, group, event):
        self.__groups[group].state = State.MafiaChatBegin
        self.__send_message_to_chat(event.message["peer_id"], "Город засыпает. Просыпается мафия и делает свой выбор.")
        self.__handle_mafia_chat_begin(group, event)

    def __check_alive(self, group, event):
        name = self.__groups[group].ids[event.message["from_id"]]

        user = None
        for player in self.__groups[group].players:
            if player.screen_name == name:
                user = player
                break

        if not user.active:
            self.__send_message_to_chat(event.message["peer_id"],
                                        "Игрок " + user.screen_name + " не может говорить, так как он мертв.")
            return False
        return True

    def __handle_last_word(self, group, event):
        name = self.__groups[group].ids[event.message["from_id"]]

        if name == self.__groups[group].last_breath.screen_name:
            self.__send_message_to_chat(event.message["peer_id"], "Спасибо за игру.")
            self.__start_night(group, event)

    def __handle_mafia_chat_begin(self, group, event):
        mafias = self.__groups[group].mafia

        for index in mafias:
            mafia = self.__groups[group].players[index]
            self.__send_message_to_person(mafia.screen_name, self.__groups[group].print_players())
            self.__send_message_to_person(mafia.screen_name, self.__groups[group].print_mafia())
            info = self.__send_message_to_person(mafia.screen_name, "Чтобы выдвинуть человека на голосование, "
                                                                    "введите команду: !q, где q - номер игрока.")
            print(info)
            self.__groups[info[0]["peer_id"]] = group

        if len(mafias) == 0:
            self.__groups[group].state = State.Commissioner
            self.__comissioner_chat(group, event)
        else:
            self.__groups[group].state = State.MafiaChatInProcess

    def __handle_mafia_chat_process(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not (event.message["text"].startswith("!") and event.message["text"][1:].isnumeric()):
                self.__send_message_to_peer(event, "Неправильный формат ввода.")
                return
            ind = int(event.message["text"][1:])
            if ind > len(self.__groups[group].players) or ind < 0:
                self.__send_message_to_peer(event, "Недопустимый номер игрока.")
                return

            if ind > 0 and not self.__groups[group].players[ind - 1].active:
                self.__send_message_to_peer(event, "Этого человека уже убили.")
                return

            if not event.message["peer_id"] in self.__groups[group].mafia_vote.keys():
                self.__groups[group].mafia_vote[event.message["peer_id"]] = ind
                self.__send_message_to_peer(event, "Ответ записан. Дождитесь остальных игроков.")

                if len(self.__groups[group].mafia_vote.keys()) == len(self.__groups[group].mafia):
                    self.__end_mafia_vote(group, event)
            else:
                self.__send_message_to_peer(event, "Вы уже проголосовали.")

    def __end_mafia_vote(self, group, event):
        s = set(self.__groups[group].mafia_vote.values())

        if len(s) == 1:
            mafias = self.__groups[group].mafia
            ind = list(s)[0]
            for index in mafias:
                mafia = self.__groups[group].players[index]

                if ind != 0:
                    self.__send_message_to_person(mafia.screen_name,
                                                  "Отлично! Удаляем игрока под номером " + str(ind) + ".")
                else:
                    self.__send_message_to_person(mafia.screen_name,
                                                  "Отлично! Никого не удаляем.")
            if ind != 0:
                self.__groups[group].to_kill.append(ind - 1)
            self.__groups[group].state = State.Commissioner
            self.__commissioner_chat(group, event)
        else:
            mafias = self.__groups[group].mafia
            s = list(map(str, list(s)))

            for index in mafias:
                mafia = self.__groups[group].players[index]
                self.__send_message_to_person(mafia.screen_name,
                                              "Похоже, появились разногласия! Мафии проголосовали за: " + ', '.join(
                                                  s)) + "."
                self.__send_message_to_person(mafia.screen_name,
                                              "Проголосуйте еще раз.")
            self.__groups[group].mafia_vote = dict()

    def __commissioner_chat(self, group, event):
        commissioner = None
        self.__send_message_to_chat(self.__groups[group].chat_id, "Мафия засыпает. Просыпается коммисар.")

        for player in self.__groups[group].players:
            if player.role == PlayerType.Commissioner and player.active:
                commissioner = player

        if commissioner is None:
            self.__groups[group].state = State.Doctor
            self.__doctor_chat(group, event)
        else:
            self.__send_message_to_person(commissioner.screen_name, self.__groups[group].print_players())
            info = self.__send_message_to_person(commissioner.screen_name, "Чтобы проверить человека, "
                                                                           "введите команду: !q, где q - номер игрока.")
            print(info)
            self.__groups[info[0]["peer_id"]] = group

    def __doctor_chat(self, group, event):
        self.__send_message_to_chat(self.__groups[group].chat_id, "Коммисар засыпает. Просыпается доктор.")
        doctor = None

        for player in self.__groups[group].players:
            if player.role == PlayerType.Doctor and player.active:
                doctor = player

        if doctor is None:
            self.__groups[group].state = State.Wake
            self.__wake(group, event)
        else:
            self.__send_message_to_person(doctor.screen_name, self.__groups[group].print_players())
            info = self.__send_message_to_person(doctor.screen_name, "Чтобы вылечить человека, "
                                                                     "введите команду: !q, где q - номер игрока.")
            print(info)
            self.__groups[info[0]["peer_id"]] = group

    def __handle_commissioner_query(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not (event.message["text"].startswith("!") and event.message["text"][1:].isnumeric()):
                self.__send_message_to_peer(event, "Неправильный формат ввода.")
                return
            ind = int(event.message["text"][1:])
            if ind > len(self.__groups[group].players) or ind < 1:
                self.__send_message_to_peer(event, "Недопустимый номер игрока.")
                return

            if not self.__groups[group].players[ind - 1].active:
                self.__send_message_to_peer(event, "Этого человека уже убили.")
                return

            if self.__groups[group].players[ind - 1].role == PlayerType.Mafia:
                self.__send_message_to_peer(event, "Этот игрок - мафия!")
                self.__groups[group].was_mafia_found = True
            else:
                self.__send_message_to_peer(event, "Этот игрок - мирный!")
            self.__groups[group].state = State.Doctor
            self.__doctor_chat(group, event)

    def __handle_doctor_query(self, group, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not (event.message["text"].startswith("!") and event.message["text"][1:].isnumeric()):
                self.__send_message_to_peer(event, "Неправильный формат ввода.")
                return
            ind = int(event.message["text"][1:])
            if ind > len(self.__groups[group].players) or ind < 1:
                self.__send_message_to_peer(event, "Недопустимый номер игрока.")
                return

            if not self.__groups[group].players[ind - 1].active:
                self.__send_message_to_peer(event, "Этого человека уже убили.")
                return

            self.__groups[group].heal = ind - 1
            self.__send_message_to_peer(event, "Вылечен игрок " + str(ind) + ".")

            self.__groups[group].state = State.Wake
            self.__wake(group, event)

    def __wake(self, group, event):
        self.__send_message_to_chat(self.__groups[group].chat_id, "Доктор засыпает. Просыпается город.")

        def_dead = []
        for dead in self.__groups[group].to_kill:
            if dead != self.__groups[group].heal:
                def_dead.append(dead)

        if self.__groups[group].was_mafia_found:
            self.__send_message_to_chat(self.__groups[group].chat_id, "Ночью был обнаружен мафия.")
        for ind in def_dead:
            self.__send_message_to_chat(self.__groups[group].chat_id, "Убит игрок: " + str(ind + 1) + ".")
            self.__groups[group].delete_player(ind)

        non_mafia = 0
        mafia = 0

        for player in self.__groups[group].players:
            if player.role == PlayerType.Mafia and player.active:
                mafia += 1
            elif player.role != PlayerType.Mafia and player.active:
                non_mafia += 1

        self.__groups[group].reset()
        if mafia >= non_mafia:
            self.__groups[group].state = State.EndGame
            self.__finish(group, event)
        else:
            self.__groups[group].state = State.Vote

    def __finish(self, group, event):
        non_mafia = 0
        mafia = 0

        for player in self.__groups[group].players:
            if player.role == PlayerType.Mafia and player.active:
                mafia += 1
            elif player.role != PlayerType.Mafia and player.active:
                non_mafia += 1
        if mafia >= non_mafia:
            self.__send_message_to_chat(self.__groups[group].chat_id, "Мафия выиграла!")
        else:
            self.__send_message_to_chat(self.__groups[group].chat_id, "Добро победило!")

        self.__send_message_to_chat(self.__groups[group].chat_id, "Великолепная игра!")
        self.__clean(group)

    def __clean(self, group):
        keys = []
        for key in self.__groups.keys():
            if key < 2000000000:
                if key == group:
                    keys.append(key)
                elif self.__groups[key] == group:
                    keys.append(key)
            else:
                if key == group:
                    keys.append(key)

        for key in keys:
            del self.__groups[key]