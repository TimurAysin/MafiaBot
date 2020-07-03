from enum import Enum, auto


class State(Enum):
    Greet = auto()
    MafiaChatBegin = auto()
    MafiaChatInProcess = auto()
    Doctor = auto()
    Commissioner = auto()
    GroupChat = auto()
    Vote = auto()
    LastWord = auto()
    EndGame = auto()
    Wake = auto()
