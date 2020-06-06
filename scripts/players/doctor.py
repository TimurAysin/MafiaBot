from players.player import Player
from players.playerType import PlayerType


class Doctor(Player):
    """
    Роль доктора в игре. Умеет лечить других игроков.
    """
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Doctor, name, screen_name, False, True, None)
