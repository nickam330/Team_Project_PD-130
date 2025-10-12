from random import randrange
from vk_token import vk_token

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# token = input('Token: ')

vk = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(vk)


def info_check(user_id):
    info = vk.method('users.get', {'user_ids': user_id, 'fields': 'city,sex,bdate'})
    if ('bdate' in info[0]) and ('city' in info[0]) and ('sex' in info[0]):
        return info
    else:
        return False


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # resp = vk.method('users.get', {'user_ids': event.user_id, 'fields': 'city,sex,bdate'})
        # print(resp)
        # name = resp[0]['first_name']  # получение имени
        # city = resp[0]['city']['title']
        # try:
        #     sex = resp[0]['sex']
        # except:
        #     write_msg(event.user_id, f"{name}, укажите ваш пол")
        #     # получить ответ в сообщении
        # try:
        #     bdate = resp[0]['bdate']
        # except


        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                user_info = info_check(event.user_id)
                print(user_info)
                if user_info:
                    write_msg(event.user_id, f"Хай, {user_info[0]['first_name']}")
                else:
                    write_msg(event.user_id, 'Для продолжения, '
                                             'вам необходимо изменить настройки приватности.\n '
                                             'Напротив пунктов "Кто видит основную информацию моей страницы" и '
                                             '"Кто видит мою дату рождения" нужно выбрать пункт "Все пользователи"')
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, 'Мне не знакома данная команда...\n'
                                         'Я знаю такие следующие команды:\n'
                                         '"Привет" - начало работы бота\n'
                                         '"Вариант" - подбор варианта в соответствии с полом, возрастом, городом\n'
                                         '"Добавить" - добавить в список выбранных\n'
                                         '"Показать" - вывести список выбранных вариантов')