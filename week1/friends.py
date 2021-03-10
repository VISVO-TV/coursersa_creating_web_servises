"""
Задание по программированию: Практика по requests

Данное задание изначально было простым. Было принято
решение изменить изначальную архитектуру и сделать его в
ООП стиле, без привязки интерфейса к конкретному
API VK (исключительно для тренировки навыка!)
"""

import requests
import datetime
from collections import Counter


class RequestFactoryVK:
    def get_info(sefl, token, id, username):
        raise ValueError


class RequestForMakeLikes(RequestFactoryVK):
    pass


class RequestForTwiceFriendOld(RequestFactoryVK):
    # Функция требуемая в задании
    def get_info(self, token, id, username):
        if id == username == None:
            print('Please, add id or username')
            return None

        if id == None:
            url = f"https://api.vk.com/method/users.get?user_ids={username}&access_token={token}&v=5.71"
            r = requests.get(url).json()
            id = r['response'][0]['id']

        url = f'https://api.vk.com/method/friends.get?user_id={id}&fields=bdate&access_token={token}&v=5.71'
        r = requests.get(url).json()
        all_friends = r['response']['items']
        result_list = []

        for friend in all_friends:
            try:
                date = friend['bdate']
                a = date.split('.')
                if len(a) < 3:
                    raise KeyError
                birthday = datetime.date(int(a[2]),int(a[1]),int(a[0]))
                diff = datetime.datetime.now().date() - birthday
                year = diff.days // 365
                result_list.append(year)
            except KeyError:
                date = None

        my_dict = Counter(result_list).most_common()
        return my_dict


class Api:
    def definition_method(self, obj):
        raise ValueError


class ApiFacebook(Api):
    # пример добавления другого api в архитектуру
    def definition_method(self, obj, id, username):
        pass


class ApiVk(Api):
    # определяем требуемые переменные и передаем их в определенный метод
    def definition_method(self, obj, id, username):
        self.TOKEN = 'd51491cbd51491cbd51491cbeed5625e40dd514d51491cbb55c08fb476b262b1d37bf8f'

        if obj.method == 'twice':
            self._method = RequestForTwiceFriendOld()
            return self._method.get_info(self.TOKEN, id, username)


class User:
    # Основной класс в котором инициализируются требуемые api и данные.
    def __init__(self, config=None):
        self._config = config or ApiVk()

    def get_info(self, method, id=None, username=None):
        self.method = method
        if method == 'twice':
            return self._config.definition_method(self, id, username)


# Запрашиваем требуемую информацию
a = User()
print(a.get_info('twice', username='goodvaer31'))
# [(22, 5), ...]
