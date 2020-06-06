from players.player import Player
from players.playerType import PlayerType


class Civilian(Player):
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Mafia, name, screen_name, True, False, None)
