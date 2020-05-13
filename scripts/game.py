from state import State
from player import Player
from playerType import PlayerType


class Game:
    def __init__(self):
        self.state = State.StartGame
        self.__greet = "Здравствуйте! Рад, что вы собрались сегодня, чтобы поиграть в мафию. \
                               Я буду вашим ведущим. Для того, чтобы начать, сделайте меня администратором и напишите команду: /start. \
                               Желаю приятной игры!"
        self.__start = "Начинаем!"
        self.__participants = []
        self.__players = []

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

    def printParticipants(self):
        n = len(self.__participants)
        s = "Количество участников: " + str(n) + "\n"
        i = 1
        for elem in self.__participants:
            s += str(i) + ": @" + elem["screen_name"] + " " + elem["name"] + "\n"
            i += 1
        return s

    # Finish later
    def makeRoles(self):
        if (len(self.__participants) == 0):
            print("Wrong participants pack")
            raise
        n = len(self.__participants)
        self.__players = []
        for participant in self.__participants:
            self.__players.append(Player(PlayerType.Civilian, participant["name"], participant["screen_name"]))

    # For testing
    def makeMafia(self, ind):
        pass
