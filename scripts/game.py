import random
from playerPack import PlayerPack
from playerType import PlayerType
from players import *
from state import State


class Game:
    __player_pack = None
    ids = dict()
    state = None
    votes = dict()

    @property
    def player_pack(self):
        return self.__player_pack

    @player_pack.setter
    def player_pack(self, new_pack):
        if self.__player_pack is not None:
            print("Player Pack is already set.")
            return

        if not isinstance(new_pack, PlayerPack):
            print(new_pack, "can't be a Player Pack.")
            return

        if new_pack.players is None:
            print("Can's assign Player Pack.")
            return

        self.__player_pack = new_pack

    def add_role_count(self, role_count):
        self.__player_pack.role_count = role_count

    def start_game(self):
        self.__player_pack.make_roles()
        self.state = State.Vote

    def players_by_type(self, player_type):
        if not (issubclass(player_type, Player)):
            print("Wrong player type -", player_type)
            return None

        result = []

        for player in self.__player_pack.players:
            if isinstance(player, player_type):
                result.append(player)

        return result

    def heal(self, ind):
        self.__player_pack.heal_player(ind)

    def kill(self, ind):
        self.__player_pack.kill_player(ind)

    def ask_about_type(self, ind, player_type):
        return self.__player_pack.compare_player_type(ind, player_type)
