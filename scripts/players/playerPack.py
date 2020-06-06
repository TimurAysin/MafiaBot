class PlayerPack:
    __players = []

    def __init__(self, participants):
        self.__players = participants

    def count_players(self):
        return len(self.__players)

