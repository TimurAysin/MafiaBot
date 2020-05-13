import sys

sys.path.append("./scripts")

from bot import Bot, Game


def main():
    bot = Bot()
    bot.startPolling()


if __name__ == "__main__":
    main()
