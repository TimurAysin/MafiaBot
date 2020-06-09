from player import Player
from playerType import PlayerType


class Civilian(Player):
    """
    Роль мирного в игре. Ничего не умеет, но очень важен.
    """

    def __init__(self, name, screen_name, id):
        super().__init__(PlayerType.Civilian, name, screen_name, id, False, False, None)
