from state import State


class Game:
    def __init__(self):
        self.state = State.NotActive
        self.__greet = "Здравствуйте! Рад, что вы собрались сегодня, чтобы поиграть в мафию. \
                               Я буду вашим ведущим. Для того, чтобы начать, напишите команду: /start. \
                               Желаю приятной игры!"
        self.__start = "/start"

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        try:
            if not isinstance(value, State):
                raise ValueError

            self.__state = value
        except ValueError:
            print("Wrong state assigned to game object - ", value)
            raise

    def greet(self):
        return self.__greet

    def start(self):
        return self.__start