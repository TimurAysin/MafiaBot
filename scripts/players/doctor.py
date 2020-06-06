from players.player import Player
from players.playerType import PlayerType


class Doctor(Player):
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Doctor, name, screen_name, False, True, None)
