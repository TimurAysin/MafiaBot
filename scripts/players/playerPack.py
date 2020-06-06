import random
from players.playerType import PlayerType
from players.player import Player
from players.mafia import Mafia
from players.civilian import Civilian
from players.don import Don
from players.commissioner import Commissioner
from players.doctor import Doctor
from players.maniac import Maniac


class PlayerPack:
    __players = []
    __role_count = None
    __role_dist = False

    def __init__(self, participants):
        self.__players = participants

    def count_players(self):
        return len(self.__players)

    def make_roles(self, role_count):
        if self.__role_dist:
            return
        # Уже проверен, можно использовать
        self.__role_count = role_count

        for player_type, count in role_count.items():
            self.__make_type(player_type, count)

        self.__role_dist = True

    def __make_type(self, player_type, count):
        i = 0
        while i < count:
            ind = random.randint(0, self.count_players() - 1)
            if not isinstance(self.__players[ind], Player):
                self.__players[ind] = player_type(self.__players[ind]["name"], self.__players[ind]["screen_name"])
                i += 1
