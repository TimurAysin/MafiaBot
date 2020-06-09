from player import Player
from playerType import PlayerType


class Don(Player):
    """
    Роль Дона в игре. Умеет узнавать у ведущего, является ли игрок комиссаром.
    """

    def __init__(self, name, screen_name, id):
        super().__init__(PlayerType.Don, name, screen_name, id, False, False, PlayerType.Commissioner)
