from abc import ABC


class Player(ABC):
    """
    Абстрактный класс для создания игроков различных типов.
    name, screen_name - имя игрока
    role - роль в игре
    kill - возможность убивать
    heal - возможность лечить
    ask - возможность спрашивать у ведущего, объект задается параметрически
    """
    def __init__(self, role, name, screen_name, id, kill, heal, ask):
        self.role = role
        self.name = name
        self.screen_name = screen_name
        self.id = id
        self.active = True
        self.kill = kill
        self.heal = heal
        self.ask = ask