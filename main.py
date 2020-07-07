from bot import Bot
from playerPack import PlayerPack
from playerType import PlayerType
from players import *
from game import Game


def main():
    bot = Bot()
    bot.start_polling()
    # arr = [
    #     {
    #         "name": "Timur Aysin",
    #         "screen_name": "aysint",
    #         "player_id": 1
    #     },
    #     {
    #         "name": "Timur Aysin",
    #         "screen_name": "aysint",
    #         "player_id": 2
    #     },
    #     {
    #         "name": "Timur Aysin",
    #         "screen_name": "aysint",
    #         "player_id": 3
    #     },
    #     {
    #         "name": "New name",
    #         "screen_name": "aoaoa",
    #         "player_id": 4
    #     },
    #     {
    #         "name": "New name",
    #         "screen_name": "aoaoa",
    #         "player_id": 5
    #     },
    #     {
    #         "name": "New name",
    #         "screen_name": "aoaoa",
    #         "player_id": 6
    #     }
    # ]
    #
    # pack = PlayerPack(arr)
    # print(pack.players)
    #
    # role_count = {
    #     Mafia: 2,
    #     Don: 1,
    #     Civilian: 1,
    #     Commissioner: 1,
    #     Doctor: 1
    # }
    # pack.role_count = role_count
    #
    # game = Game(arr[0])
    # game.player_pack = pack
    # game.start_game()

if __name__ == "__main__":
    main()
