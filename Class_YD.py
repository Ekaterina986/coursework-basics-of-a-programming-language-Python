import urllib
import requests
import configparser
from pprint import pprint


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
        if response.status_code == 409:
            print(f'Указанная папка уже существует. {response.status_code}')
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

    def get_json(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'media_type': 'image'}
        response = requests.get(url, headers=headers, params=params)
        pprint(response.json())


config = configparser.ConfigParser()
config.read("settings.ini")

