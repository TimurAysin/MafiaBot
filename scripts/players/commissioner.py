from players.player import Player
from players.playerType import PlayerType


class Commissioner(Player):
    """
    Роль комиссара в игре. Умеет узнавать у ведущего, является ли игрок мафией.
    """
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Commissioner, name, screen_name, False, False, PlayerType.Mafia)
