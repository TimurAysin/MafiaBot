import sys

sys.path.append("./scripts")

from bot import Bot


def main():
    bot = Bot()
    bot.start_polling()


if __name__ == "__main__":
    main()
