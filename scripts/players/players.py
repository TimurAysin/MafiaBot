from player import Player
from playerType import PlayerType


class Maniac(Player):
    """
    Роль Маньяка в игре. Умеет убивать ночью.
    """

    def __init__(self, name, screen_name, player_id):
        super().__init__(PlayerType.Maniac, name, screen_name, player_id, True, False, None)


class Civilian(Player):
    """
    Роль мирного в игре. Ничего не умеет, но очень важен.
    """

    def __init__(self, name, screen_name, player_id):
        super().__init__(PlayerType.Civilian, name, screen_name, player_id, False, False, None)


class Commissioner(Player):
    """
    Роль комиссара в игре. Умеет узнавать у ведущего, является ли игрок мафией.
    """

    def __init__(self, name, screen_name, player_id):
        super().__init__(PlayerType.Commissioner, name, screen_name, player_id, False, False, PlayerType.Mafia)


class Doctor(Player):
    """
    Роль доктора в игре. Умеет лечить других игроков.
    """

    def __init__(self, name, screen_name, player_id):
        super().__init__(PlayerType.Doctor, name, screen_name, player_id, False, True, None)


class Don(Player):
    """
    Роль Дона в игре. Умеет узнавать у ведущего, является ли игрок комиссаром.
    """

    def __init__(self, name, screen_name, player_id):
        super().__init__(PlayerType.Don, name, screen_name, player_id, False, False, PlayerType.Commissioner)


class Mafia(Player):
    """
    Роль мафии в игре. Умеет убивать ночью.
    """

    def __init__(self, name, screen_name, player_id):
        super().__init__(PlayerType.Mafia, name, screen_name, player_id, True, False, None)
