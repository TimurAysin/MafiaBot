from bot import Bot
from playerPack import PlayerPack
from playerType import PlayerType
from players import *


def main():
    # bot = Bot()
    # bot.start_polling()
    arr = [
        {
            "name": "Timur Aysin",
            "screen_name": "aysint",
            "player_id": 1
        },
        {
            "name": "Timur Aysin",
            "screen_name": "aysint",
            "player_id": 2
        },
        {
            "name": "Timur Aysin",
            "screen_name": "aysint",
            "player_id": 3
        },
    ]

    pack = PlayerPack(arr)
    print(pack.players)

    role_count = {
        Mafia: 1,
        Don: 1,
        Civilian: 1
    }
    pack.make_roles(role_count)
    print(pack.players)


if __name__ == "__main__":
    main()
