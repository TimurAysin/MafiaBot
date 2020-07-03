import random
from player import Player


class PlayerPack:
    __players = []
    __role_count = None
    __role_dist = False

    def __init__(self, participants):
        self.players = participants

    def count_players(self):
        return len(self.__players)

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, participants):
        for elem in participants:
            if not (isinstance(elem, dict) and "name" in elem.keys()
                    and "screen_name" in elem.keys() and "player_id" in elem.keys()):
                print("Wrong participants pack: ", end='')
                print(participants)
                return
        self.__players = participants

    def make_roles(self, role_count):
        if self.__role_dist:
            return

        if self.__wrong_role_count(role_count):
            return

        if len(self.__players) == 0:
            print("PlayerPack has no players in it.")
            return

        self.__role_count = role_count

        for player_type, count in role_count.items():
            self.__make_type(player_type, count)

        self.__role_dist = True

    def __make_type(self, player_type, count):
        i = 0
        while i < count:
            ind = random.randint(0, self.count_players() - 1)
            if not isinstance(self.__players[ind], Player):
                self.__players[ind] = player_type(self.__players[ind]["name"],
                                                  self.__players[ind]["screen_name"],
                                                  self.__players[ind]["player_id"])
                i += 1

    def __wrong_role_count(self, role_count):
        for player_type, count in role_count.items():
            if not (issubclass(player_type, Player) and isinstance(count, int)):
                return True
        return False
