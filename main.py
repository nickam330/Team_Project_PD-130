from dataclasses import fields
from random import randrange

import requests

from table_function.give_information import give_age
from table_function.selected_add import add_selected, link_list
from table_function.user_add_inf import *
from create_table.base_information import *
from create_table.create_session import *
from vk_token import vk_token, clien_token
from datetime import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# token = input('Token: ')

vk_session = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

user_that_we_find = {}

genders = {
    2: "male",
    1: "female",
    0: "Any"
}


# def uid_info():
#     photos = vk_user.photos.get(
#         owner_id=uid,
#         album_id='profile',
#         extended=1,
#         count=3
#     )['items']
#     top_photos = sorted(
#         photos,
#         key=lambda x: x['likes']['count'],
#         reverse=True)[
#         :3]
#
#     attachments = [
#         f"photo{
#             p['owner_id']}_{
#             p['id']}" for p in top_photos]
#     first_name, last_name, ages, city_id, city_user, sex =information_user(uid)
#     vk.messages.send(
#         user_id=user_id,
#         message=f"{first_name} {last_name}\nhttps://vk.com/id{uid}",
#         attachment=",".join(attachments),
#         random_id=randrange(10 ** 7),
#         keyboard=open(
#             "keyboard_start.json", "r", encoding="UTF-8").read()
#     )
#

# def expire_key(user_id):
#     user = session.query(Users).filter_by(id=user_id).first()
#     if not user:
#         return None
#     time = datetime.now()
#     time_key = user.date_of_key
#     hours = user.expires_in/3600
#     difference_hours = (time - time_key).total_seconds() / 3600
#     if difference_hours < hours:
#         return True
#     else:
#         r = requests.post(f'https://flask-bot-lu45.onrender.com/ping/{user_id}')
#     return False


def refresh_token(user_id):
    r = requests.post(f'https://flask-bot-lu45.onrender.com/ping/{user_id}')
    print(r.status_code, r.text)

def information_user(id):
    fields = "first_name,last_name,bdate,city,sex"
    user_info = vk.users.get(user_ids=id, fields=fields)[0]
    sex = user_info["sex"]
    first_name = user_info["first_name"]
    last_name = user_info["last_name"]
    date_today = datetime.today()
    date_birth = user_info["bdate"]
    bdate = datetime.strptime(date_birth, "%d.%m.%Y")
    ages = date_today.year - bdate.year
    city_info = user_info["city"]
    city_id = city_info["id"]
    city_user = city_info["title"]
    return first_name, last_name, ages, city_id, city_user, sex



while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                session = Session()
                user_id = event.user_id

                first_name, last_name, ages, city_id, city_user, sex = information_user(
                    user_id)
                gender = genders[sex]

                user = session.query(Users).filter_by(id=user_id).first()

                if not user:
                    add_user_id(user_id, session)
                    add_age(user_id, ages, session)
                    add_gender(user_id, gender, session)
                    add_city_name_int(user_id, city_user, city_id, session)
                    add_status(user_id, 2, session)
                    session.commit()
                    user = session.query(Users).filter_by(
                        id=user_id).first()
                status = user.status
                print(f"{status}")

                # if event.text.lower() == "привет":
                #     print(first_name, last_name, ages, city_id, city_user, sex)
                #     gender = genders[sex]

                # if user.expires_in:
                #     time = datetime.now()
                #     time_key = user.date_of_key
                #     hours = user.expires_in / 3600
                #     print(time_key,time , hours)
                #     difference_hours = (time - time_key).total_seconds() / 3600
                #     print(time_key, time, hours,difference_hours)
                #     if difference_hours > hours:
                #         refresh_token(user_id)
                #         user.date_of_key = datetime.now()
                #         session.commit()

                if event.text == "Дать согласие" and status == 2:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=url,
                            keyboard=open(
                                "keyboard.json", "r", encoding="UTF-8", ).read(),
                            random_id=randrange(10 ** 7)
                        )

                elif event.text == "Показать Избранное":
                    people = link_list(user_id,session)
                    for person in people:
                        access_token = user.access_token
                        vk_session_user = vk_api.VkApi(token=access_token)
                        vk_user = vk_session_user.get_api()
                        # if user_that_we_find.get(user_id) and len(user_that_we_find[user_id]) > 0:
                        uid = person
                        user.last_user = uid
                        session.commit()
                        photos = vk_user.photos.get(
                            owner_id=uid,
                            album_id='profile',
                            extended=1,
                            count=3
                        )['items']
                        top_photos = sorted(
                            photos,
                            key=lambda x: x['likes']['count'],
                            reverse=True)[
                                     :3]

                        attachments = [f"photo{p['owner_id']}_{p['id']}" for p in top_photos]

                        first_name, last_name, ages, city_id, city_user, sex = information_user(uid)
                        vk.messages.send(
                            user_id=user_id,
                            message=f"{first_name} {last_name}\nhttps://vk.com/id{uid}",
                            attachment=",".join(attachments),
                            random_id=randrange(10 ** 7),
                            keyboard=open(
                                "keyboard_start.json", "r", encoding="UTF-8").read()
                        )
                elif status == 2:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Привет, чтобы начать дайте соглассие,нажмите кнопку'Дать согласие'",
                        keyboard=open(
                            "keyboard.json",  "r", encoding="UTF-8", ).read(),
                        random_id=randrange(10 ** 7)
                    )

                elif status == 1 and event.text == "Начать поиск":
                    user_found = []
                    target_sex = 2 if sex == 1 else 1
                    user = session.query(Users).filter_by(id=user_id).first()

                    age = give_age(user.id, session)
                    access_token = user.access_token
                    # vk_session_user = vk_api.VkApi(token=clien_token)
                    vk_session_user = vk_api.VkApi(token=access_token)
                    vk_user = vk_session_user.get_api()

                    users = vk_user.users.search(
                        age_from=age - 2,
                        age_to=age + 2,
                        sex=target_sex,
                        city=city_id,
                        has_photo=1,
                        count=20,
                        fields = "is_closed,can_access_closed"
                    )['items']
                    girls = set(link_list(user_id, session))
                    for people in users:
                        print(people )
                        uid = people["id"]
                        if uid in girls:
                            continue
                        if people.get('is_closed') and not people.get('can_access_closed', False):
                            continue
                        user_found.append(uid)
                    user_that_we_find[user_id] = user_found
                    user.status = 4
                    session.commit()
                    vk.messages.send(
                        user_id=user_id,
                        message="Начинаем",
                        random_id=randrange(10 ** 7),
                        keyboard=open("keyboard_show_people.json", "r", encoding="UTF-8").read()

                    )

                elif event.text == "Добавить в Избранное" and status == 4:

                    last_user = user.last_user
                    link = f"https://vk.com/id{last_user}"
                    add_selected(user_id, last_user,link, session)
                    vk.messages.send(
                        user_id=user_id,
                        message=f"{first_name} {last_name}\nДобавлена, 'Следующий'",
                        random_id=randrange(10 ** 7),
                        keyboard=open(
                            "keyboard_start.json", "r", encoding="UTF-8").read())


                elif status == 4:

                    vk_session_user = vk_api.VkApi(token=clien_token)
                    vk_user = vk_session_user.get_api()
                    if user_that_we_find.get(user_id) and len(user_that_we_find[user_id]) > 0:
                        uid = user_that_we_find[user_id].pop(0)
                        user.last_user = uid
                        session.commit()
                        photos = vk_user.photos.get(
                            owner_id=uid,
                            album_id='profile',
                            extended=1,
                            count=3
                        )['items']
                        top_photos = sorted(
                            photos,
                            key=lambda x: x['likes']['count'],
                            reverse=True)[
                                     :3]

                        attachments = [
                            f"photo{
                            p['owner_id']}_{
                            p['id']}" for p in top_photos]
                        first_name, last_name, ages, city_id, city_user, sex = information_user(uid)
                        vk.messages.send(
                            user_id=user_id,
                            message=f"{first_name} {last_name}\nhttps://vk.com/id{uid}",
                            attachment=",".join(attachments),
                            random_id=randrange(10 ** 7),
                            keyboard=open(
                                "keyboard_start.json", "r", encoding="UTF-8").read()
                        )
                    else:
                        vk.messages.send(
                            user_id=user_id,
                            message="Больше анкет нет.",
                            random_id=randrange(10 ** 7),
                            keyboard=open("keyboard_new.json", "r", encoding="UTF-8").read()
                        )
                        user.status = 1
                        session.commit()

                elif status == 1:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Начать?",
                        keyboard=open(
                            "keyboard_search.json", "r", encoding="UTF-8", ).read(),
                        random_id=randrange(10 ** 7)
                    )
                elif status == 0:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Я не знаю эту команду, Введите 'Привет'",
                        keyboard=open(
                            "keyboard.json", "r", encoding="UTF-8", ).read(),
                        random_id=randrange(10 ** 7)
                    )
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Я не знаю эту команду, Введите 'Привет'",
                        keyboard=open(
                            "keyboard.json", "r", encoding="UTF-8", ).read(),
                        random_id=randrange(10 ** 7)
                    )
    except Exception as error:
        print(error)
        continue
