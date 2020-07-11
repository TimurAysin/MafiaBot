from player import Player
from playerType import PlayerType


class Maniac(Player):
    """
    Роль Маньяка в игре. Умеет убивать ночью.
    """

    role_name = "Маньяк"

    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Maniac, name, screen_name, True, False, None)


class Civilian(Player):
    """
    Роль мирного в игре. Ничего не умеет, но очень важен.
    """

    role_name = "Мирный"

    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Civilian, name, screen_name, False, False, None)


class Commissioner(Player):
    """
    Роль комиссара в игре. Умеет узнавать у ведущего, является ли игрок мафией.
    """

    role_name = "Коммиссар"

    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Commissioner, name, screen_name, False, False, PlayerType.Mafia)


class Doctor(Player):
    """
    Роль доктора в игре. Умеет лечить других игроков.
    """

    role_name = "Доктор"

    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Doctor, name, screen_name, False, True, None)


class Don(Player):
    """
    Роль Дона в игре. Умеет узнавать у ведущего, является ли игрок комиссаром.
    """

    role_name = "Дон"

    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Don, name, screen_name, False, False, PlayerType.Commissioner)


class Mafia(Player):
    """
    Роль мафии в игре. Умеет убивать ночью.
    """

    role_name = "Мафия"

    def __init__(self, name, screen_name):
        super().__init__(PlayerType.Mafia, name, screen_name, True, False, None)
