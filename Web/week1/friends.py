import requests
from datetime import datetime


def key_filter(data: dict, key: str) -> dict:
    new_data = []
    for var in data:
        if key in var:
            new_data.append(var[key])
    return new_data


def valid_data(data: list, age=False) -> list:
    year_date = []
    for var in data:
        if len(var.split(".")) == 3:
            year = var.split(".")[2]
        else:
            continue
        if age:
            year_date.append(datetime.now().year - int(year))
        else:
            year_date.append(int(year))
        year_date.sort(reverse=age)
    return year_date


def unique_filter(data: list) -> list:
    unique_data = {}
    for var in data:
        unique_data[var] = data.count(var)
    new_data = [(key, value) for key, value in unique_data.items()]
    return new_data



def calc_age(uid):
    # сервисный ключ приложения (обновляется раз в 24 часа)
    token_key = "11887d2a11887d2a11887d2a5911fd93801118811887d2a7188cc3b4301a86cb6bdc8b8"
    # получение ответа от API
    user = requests.get(f"https://api.vk.com/method/users.get?v=5.71&access_token={token_key}"
                        f"&user_ids={uid}")

    # получение словаря с данными о пользователе и id пользователя
    user_info = user.json()["response"][0]
    user_id = user_info["id"]

    # получаем друзей
    friends = requests.get(f"https://api.vk.com/method/friends.get?v=5.71&access_token={token_key}"
                           f"&user_id={user_id}&fields=bdate")
    friends_info = friends.json()["response"]["items"]
    # отбираем всех друзей у которых есть дата рождения
    friends_info = key_filter(friends_info, "bdate")
    # проверяем валидность дат рождения наличие года рождения
    date_info = valid_data(friends_info, age=True)
    # подсчёт уникальных элементов
    date_unique = unique_filter(date_info)
    # сортировка списка
    date_unique.sort(key=lambda val: val[0], reverse=False)
    date_unique.sort(key=lambda val: val[1], reverse=True)
    return date_unique

if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
