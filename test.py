import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

token = "55d54859bfc02268950c448c91fe6c95e1261b94e960bea620907555863ed31ed7bc9ca462dd619e1bfed"
group = "195261716"

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group)
vk = vk_session.get_api()

for event in longpoll.listen():
    print("Print")
    chat_id = vk.messages.createChat(
                title="Мафии",
                group_id=group,
                user_ids="timuraysin"
       )

    print(chat_id)

    vk.messages.send(
                random_id=random.randint(1, 1000000000000),
                chat_id=chat_id,
                message="Hello there"
            )