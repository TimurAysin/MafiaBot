import random
from players.player import Player
from players.playerType import PlayerType
from state import State


class Game:
    def __init__(self):
        self.__state = State.StartGame
        self.__participants = []
        self.__players = []
        self.mafia = []
        self.__commissioner = -1
        self.__doctor = -1
        self.votes = dict()
        self.ids = []
        self.last_breath = -1
        self.mafia_vote = dict()
        self.to_kill = []
        self.was_mafia_found = False
        self.__chat_id = -1
        self.heal = -1
        # Зависит от количества игроков, потом сделаю
        self.__number_of_mafias = 1

    @property
    def chat_id(self):
        return self.__chat_idpment


    @chat_id.setter
    def chat_id(self, val):
        if self.__chat_id == -1:
            self.__chat_id = val

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        try:
            if not isinstance(value, State):
                raise ValueError

            self.__state = value
        except ValueError:
            print("Wrong state assigned to game object -", value)
            raise

    def greet(self):
        return self.__greet

    def start(self):
        return self.__start

    @property
    def participants(self):
        return self.__participants

    @participants.setter
    def participants(self, value):
        try:
            if not (isinstance(value, list)):
                raise ValueError

            for elem in value:
                if not (isinstance(elem, dict) and 'screen_name' in elem and 'name' in elem):
                    raise ValueError

            self.__participants = value
        except ValueError:
            print("Wrong participants object -", value)
            raise

    @property
    def players(self):
        return self.__players

    def print_participants(self):
        n = len(self.__participants)
        s = "Количество участников: " + str(n) + "\n"
        i = 1
        for elem in self.__participants:
            s += str(i) + ": @" + elem["screen_name"] + " " + elem["name"] + "\n"
            i += 1
        return s

    def print_players(self):
        n = len(self.__participants)
        s = "Количество участников: " + str(n) + "\n"
        i = 1
        for elem in self.__players:
            if elem.active:
                s += str(i) + ": @" + elem.screen_name + " " + elem.name + "\n"
            i += 1
        return s

    # Finish later
    def make_roles(self):
        if len(self.__participants) == 0:
            print("Wrong participants pack")
            raise
        n = len(self.__participants)
        self.__players = []

        for participant in self.__participants:
            self.__players.append(Player(PlayerType.Civilian, participant["name"], participant["screen_name"]))

        i = 0
        while i < self.__number_of_mafias:
            ind = random.randint(0, len(self.__participants) - 1)
            if self.__players[ind].role == PlayerType.Civilian:
                self.__players[ind].role = PlayerType.Mafia
                self.mafia.append(ind)
                i += 1

        while self.__commissioner == -1:
            ind = random.randint(0, len(self.__participants) - 1)
            if self.__players[ind].role == PlayerType.Civilian:
                self.__players[ind].role = PlayerType.Commissioner
                self.__commissioner = ind

        while self.__doctor == -1:
            ind = random.randint(0, len(self.__participants) - 1)
            if self.__players[ind].role == PlayerType.Civilian:
                self.__players[ind].role = PlayerType.Doctor
                self.__doctor = ind

    def delete_player(self, ind):
        self.__players[ind].active = False
        if self.__players[ind].role == PlayerType.Mafia:
            self.mafia.remove(ind)
        self.last_breath = self.__players[ind].screen_name

    def print_mafia(self):
        s = "Оставшиеся мафии:\n"
        for player in self.__players:
            if player.role == PlayerType.Mafia and player.active:
                s += "@" + player.screen_name + "\n"
        return s

    def reset(self):
        self.votes = dict()
        self.last_breath = -1
        self.mafia_vote = dict()
        self.to_kill = []
        self.was_mafia_found = False
        self.heal = -1