from player import Player
from playerType import PlayerType


class Commissioner(Player):
    """
    Роль комиссара в игре. Умеет узнавать у ведущего, является ли игрок мафией.
    """

    def __init__(self, name, screen_name, id):
        super().__init__(PlayerType.Commissioner, name, screen_name, id, False, False, PlayerType.Mafia)
