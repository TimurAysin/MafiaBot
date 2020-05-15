from enum import Enum


class State(Enum):
    StartGame = 1
    Sleep = 2
    MafiaChat = 3
    Doctor = 4
    Commissioner = 5
    GroupChat = 6
    Vote = 7
    EndGame = 8
