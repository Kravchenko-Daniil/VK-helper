import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from decouple import config
from datetime import datetime


token = config('TOKEN', default='')

def main():
    vk_session = vk_api.VkApi(token=token)

    try:
        vk = vk_session.get_api()
    except vk_api.AuthError as error_msg:
        print(error_msg)

        return

    longpoll = VkLongPoll(vk_session)

    values_in_message = ['поехали', "погнали", "начинаем", "стартуем", "вперед", "го", "начали"]
    message = input("Write the message to send: ")

    for event in longpoll.listen():
         if event.type == VkEventType.MESSAGE_NEW:
             if event.to_me:
                if any(value in str(event.message).lower() for value in values_in_message):
                    print(f'{datetime.now().strftime("%H:%M:%S")} & {event.peer_id}: ', str(event.message))
                    vk.messages.send(user_id=event.peer_id, message=message, random_id=0)

                    break

    print("Done")

if __name__ == '__main__':
    main()