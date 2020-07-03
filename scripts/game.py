import random
from playerPack import PlayerPack
from playerType import PlayerType
from players import *
from state import State


class Game:
    __host = None
    __player_pack = None
    state = None

    def __init__(self, host):
        self.host = host

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, obj):
        if not isinstance(obj, dict):
            print("Wrong host:", obj)
            return

        if not ("name" in obj.keys() and "screen_name" in obj.keys() and "player_id" in obj.keys()):
            return
        self.__host = obj

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

        if new_pack.role_count is None or new_pack.players is None:
            print("Can's assign Player Pack.")
            return

        self.__player_pack = new_pack

    def start_game(self):
        self.__player_pack.make_roles()
        self.state = State.Greet

    def alive_players(self):
        alive_players = []

        for player in self.__player_pack.players:
            if player.active:
                alive_players.append(player)

        return alive_players

    def players_by_type(self, type):
        if not (issubclass(type, Player)):
            print("Wrong player type -", type)
            return None

        result = []

        for player in self.__player_pack.players:
            if isinstance(player, type):
                result.append(player)

        return result
