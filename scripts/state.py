from enum import Enum


class State(Enum):
    StartGame = 1
    MafiaChatBegin = 3
    MafiaChatInProcess = 10
    Doctor = 4
    Commissioner = 5
    GroupChat = 6
    Vote = 7
    LastWord = 9
    EndGame = 8
    Wake = 11
