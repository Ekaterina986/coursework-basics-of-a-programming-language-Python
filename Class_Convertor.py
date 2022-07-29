import json


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

    def convert_json(self, yandex_data):

        yandex_data_json = json.dumps(yandex_data)
        return yandex_data_json
