from tqdm import tqdm
import configparser
from pprint import pprint
from Class_VK import VK
from Class_Convertor import Convertor
from Class_YD import YD

if __name__ == '__main__':



    def help_upload():
        """
        для корректной работы программы необходимо внести в файл settings.ini следующие параметры:

        [VK]
        token - токен для доступа к VK
        owner_id - id или username пользователя, чьи фото необходимо загрузить
        count - количество загружаемых фото

        [YD]
        token - токен для доступа к яндекс диску
        path - дирректория на яндекс диске
        """
        print(help_upload.__doc__)


    help_upload()

    config = configparser.ConfigParser()
    config.read("settings.ini")

    vk = VK()
    photo_list_vk = vk.photos_get(config["VK"]["album_id"], config["VK"]["owner_id"], config["VK"]["count"])

    convertor = Convertor()
    yandex_data = convertor.convert_vk(photo_list_vk)
    pprint(convertor.convert_json(yandex_data))

    yd = YD()
    yd.put_directory(path=config["YD"]["path"])
    yd.get_upload(disk_file_path=config["YD"]["path"])

    for file, url in tqdm(yandex_data.items()):
        yd.upload_link(disk_file_path= config["YD"]["path"] + file, url=url)
