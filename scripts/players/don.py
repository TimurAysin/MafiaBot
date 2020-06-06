from players.player import Player
from players.playerType import PlayerType


class Civilian(Player):
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Don, name, screen_name, False, False, PlayerType.Commissioner)
