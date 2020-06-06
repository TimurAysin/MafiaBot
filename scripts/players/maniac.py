from players.player import Player
from players.playerType import PlayerType


class Maniac(Player):
    """
    Роль Маньяка в игре. Умеет убивать ночью.
    """
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Maniac, name, screen_name, True, False, None)
