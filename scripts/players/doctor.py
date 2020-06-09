from player import Player
from playerType import PlayerType


class Doctor(Player):
    """
    Роль доктора в игре. Умеет лечить других игроков.
    """

    def __init__(self, name, screen_name, id):
        super().__init__(PlayerType.Doctor, name, screen_name, id, False, True, None)
