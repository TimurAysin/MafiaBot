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
                    and "screen_name" in elem.keys()):
                print("Wrong participants pack: ", end='')
                print(participants)
                return
        self.__players = participants

    @property
    def role_count(self):
        return self.__role_count

    @role_count.setter
    def role_count(self, new_rc):
        if self.__players is None:
            return

        if self.__role_count is not None or PlayerPack.wrong_role_count(new_rc):
            return

        num = 0
        for player_type, count in new_rc.items():
            num += count

        if num != len(self.__players):
            print("Number of players doesn't match.")
            return

        self.__role_count = new_rc

    def make_roles(self):
        if self.__role_dist:
            return

        if len(self.__players) == 0:
            print("PlayerPack has no players in it.")
            return

        for player_type, count in self.__role_count.items():
            self.__make_type(player_type, count)

        self.__role_dist = True

    def __make_type(self, player_type, count):
        i = 0
        while i < count:
            ind = random.randint(0, self.count_players() - 1)
            if not isinstance(self.__players[ind], Player):
                self.__players[ind] = player_type(self.__players[ind]["name"],
                                                  self.__players[ind]["screen_name"])
                i += 1

    @staticmethod
    def wrong_role_count(role_count):
        for player_type, count in role_count.items():
            if not (issubclass(player_type, Player) and isinstance(count, int)):
                return True

        return False

    def heal_player(self, ind):
        if ind < 0 or ind >= len(self.__players):
            print("Wrong index for heal:", ind)
            return
        self.__players[ind].active = True

    def kill_player(self, ind):
        if ind < 0 or ind >= len(self.__players):
            print("Wrong index for kill:", ind)
            return
        self.__players[ind].active = False

    def compare_player_type(self, ind, player_type):
        if ind < 0 or ind >= len(self.__players):
            print("Wrong index for comparison:", ind)
            return

        if not issubclass(player_type, Player):
            print("Wrong type for comparison:", player_type)
            return

        return isinstance(self.__players[ind], player_type)