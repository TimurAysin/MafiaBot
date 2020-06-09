from player import Player
from playerType import PlayerType


class Mafia(Player):
    """
    Роль мафии в игре. Умеет убивать ночью.
    """
    def __init__(self, name, screen_name, id):
        super().__init__(PlayerType.Mafia, name, screen_name, id, True, False, None)
