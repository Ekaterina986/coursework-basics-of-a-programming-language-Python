import urllib
import requests
from tqdm import tqdm
import configparser


class VK:
    def __init__(self):
        self.token = config["VK"]["token"]

    def photos_get(self, album_id, owner_id, count):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id,
                  'album_id': album_id,
                  'access_token': self.token,
                  'extended': 'likes',
                  'photo_sizes': '1',
                  'count': count,
                  'v': '5.131'
                  }
        response = requests.get(url=url, params=params).json()
        if response.status_code != 200:
            print('Ошибка get запроса.')
        print(f"В альбоме '{album_id}' {response['response']['count']} фото")
        return response['response']['items']


class Convertor:
    def convert_vk(self, photo_list_vk):
        size_sort = {'s': 0, 'm': 1, 'x': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'y': 7, 'z': 8, 'w': 9}
        yandex_data_list = {}
        for photo_list_vk_item in photo_list_vk:
            # Создание уникального имени файла
            file_name = str(photo_list_vk_item['likes']['count'])
            if file_name + '.jpg' in yandex_data_list:
                file_name = file_name + '-' + str(photo_list_vk_item['date'])
            file_name = file_name + '.jpg'
            # Добавление ключей сортировки
            for size_item in photo_list_vk_item['sizes']:
                size_item['type_int'] = size_sort[size_item['type']]
            # Сортировка
            sizes_sorted = sorted(photo_list_vk_item['sizes'], key=lambda x: x['type_int'])

            yandex_data_list[file_name] = sizes_sorted[-1]['url']
        return yandex_data_list


class YD:
    def __init__(self):
        self.token = config["YD"]["token"]

    def put_directory(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {'Content - Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'OAuth {self.token}'
                   }
        res = requests.put(f'{url}?path={path}', headers=headers)
        if res == 201:
            print('Папка создана успешно.')
        return res

    def get_upload(self, disk_file_path: str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Authorization': f'OAuth {self.token}',
            'Content - Type': 'application/json'
        }
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f'Ошибка резервирования. {response.status_code}')
            print(headers)
            print(params)
            print(response.json())
        return response.json()

    def upload_link(self, disk_file_path, url):
        response_href = self.get_upload(disk_file_path=disk_file_path)
        href = response_href.get('href', '')
        data = urllib.request.urlopen(url)
        response = requests.put(href, data=data)
        response.raise_for_status()
        if response.status_code == 201:
            print('Загружено успешно.')
        else:
            print('Ошибка загрузки на Яндекс Диск.')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")

    vk = VK()
    photo_list_vk = vk.photos_get(config["VK"]["album_id"], config["VK"]["owner_id"], config["VK"]["count"])

    convertor = Convertor()
    yandex_data = convertor.convert_vk(photo_list_vk)

    yd = YD()
    yd.put_directory(path=config["YD"]["path"])
    yd.get_upload(disk_file_path=config["YD"]["path"])

    for file, url in tqdm(yandex_data.items()):
        yd.upload_link(disk_file_path=config["YD"]["path"] + file, url=url)
