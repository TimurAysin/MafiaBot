class Player:
    def __init__(self, role, name, screen_name, kill, heal, ask):
        self.role = role
        self.name = name
        self.screen_name = screen_name
        self.active = True
        self.kill = kill
        self.heal = heal
        self.ask = ask