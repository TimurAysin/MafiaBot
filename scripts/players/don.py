from players.player import Player
from players.playerType import PlayerType


class Don(Player):
    """
    Роль Дона в игре. Умеет узнавать у ведущего, является ли игрок комиссаром.
    """
    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Don, name, screen_name, False, False, PlayerType.Commissioner)
