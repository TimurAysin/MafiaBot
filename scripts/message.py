PROPOSITION_TO_CREATE_GAME = "Чтобы начать игру, создайте беседу и добавьте туда меня."
CREATE_NEW_GAME = "Здравствуйте! Я MafiaBot, буду исполнять роль ведущего в игре. Чтобы начать, " \
                  "сделайте меня администратором и нажмите \"Старт\". "
START = "Начинаем!"
HEAD_COUNT = "Добавляю игроков..."
ROLES_PROMPT = "Пора определить, какие роли будут в игре!"
CUSTOM_PACK = "Чтобы настроить роли, выберите настроить."
CONFIG_EXPLAIN = "Чтобы создать определенное количество персонажей какой-то роли, нажмите на соответствующую кнопку и " \
                 "потом введите число."

DEFAULT_ROLES_ERROR = "В стандартном режиме должно быть не меньше 3 игроков."
ROLE_VALUE = "Сколько?"
ROLE_VALUE_ERROR = "Введите значение еще раз."
ROLE_VALUE_SUCCESS = "Принято."
ROLE_VALUE_CHECK = "Выбранный состав ролей:"
ROLE_CONFIG_SUCCESS = "Отлично! Роли подобраны, игра начинается!"
ROLE_INFO = "Текущий состав ролей:\n"

CHAT_BEGIN = "Сейчас происходит общение. Вы можете обмениваться мыслями сколько угодно, чтобы закончить и перейти к " \
             "голосованию, нажмите на соответствующую кнопку."

MAFIA_DESC = "Вы - мафия. Убивайте несогласных и подчините себе весь город!"
CIVILIAN_DESC = "Вы - мирный житель. Остерегайтесь мафии и других плохих людей."
COMMISSIONER_DESC = "Вы - коммиссар. Удачной охоты."
DOCTOR_DESC = "Вы - доктор, спасайте больше жизней. И себя лечить два раза подряд нельзя."
DON_DESC = "Вы - дон, начальник мафии. Вашей целью является коммиссар."
MANIAC_DESC = "Вы - маньяк. Убивайте всех и не подставляйтесь."

VOTE_BEGIN = "Сейчас игроки голосуют, кого исключить. Вы должны написать номер игрока, чтобы проголосовать за его " \
             "исключение. Если вы воздерживаетесь от голосования, нажмите Отказ. Будьте внимательны, права на ошибку " \
             "нет. "
VOTE_ASK = "@{}, пожалуйста проголосуйте."
VOTE_NONE = "Игрок @{} воздержался от голосования."
VOTE = "Игрок @{} проголосовал за исключение игрока @{}."
KILL = "Игрок @{} исключен. До свидания!"


def suggest_default(mafia_count):
    return "Чтобы выбрать стандартный вариант (1 комиссар, 1 доктор, {} мафиози, остальные - мирные жители), " \
           "выберите Стандартный.".format(str(mafia_count))
