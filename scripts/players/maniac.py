from player import Player
from playerType import PlayerType


class Maniac(Player):
    """
    Роль Маньяка в игре. Умеет убивать ночью.
    """

    def __init__(self, name, screen_name, id):
        super().__init__(PlayerType.Maniac, name, screen_name, id, True, False, None)
