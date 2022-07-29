import requests
import vk_api
import configparser


class VK:
    def __init__(self):
        self.token = config["VK"]["token"]
        self.vk = vk_api.VkApi(token=self.token)

    def resolve_username(self, username):
        # username - 'durov'
        id_username = self.vk.method('users.get', {'user_ids': username})[0]['id']
        # id_ - 1
        return id_username

    def photos_get(self, album_id, owner_id, count):
        if not owner_id.isdigit():
            owner_id = self.resolve_username(owner_id)
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id,
                  'album_id': album_id,
                  'access_token': self.token,
                  'extended': 'likes',
                  'photo_sizes': '1',
                  'count': count,
                  'v': '5.131'
                  }
        response = requests.get(url=url, params=params)
        response_json = response.json()
        if list(response_json.keys())[0] == 'error':
            print(response.status_code)
            print(response_json)
            print('Некорректный id')
            return
        elif response.status_code >= 400:
            print('Ошибка запроса.')
        elif response.status_code == 200:
            print('Список фото выгружен.')
        else:
            print('Ошибка выгрузки фото.')
        print(f"В альбоме '{album_id}' {response_json['response']['count']} фото")
        return response_json['response']['items']

config = configparser.ConfigParser()
config.read("settings.ini")

