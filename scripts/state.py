from enum import Enum


class State(Enum):
    NotActive = 0
    StartGame = 1
    InGame = 2
    EndGame = 3
