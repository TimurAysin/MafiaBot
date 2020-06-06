from players.player import Player
from players.playerType import PlayerType


class Civilian(Player):
    """
    Роль мирного в игре. Ничего не умеет, но очень важен.
    """
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Civilian, name, screen_name, False, False, None)
