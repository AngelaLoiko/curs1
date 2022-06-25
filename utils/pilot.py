import configparser
import json
import sys

from tqdm import tqdm
from classes.YaUploader import YaUploader

def get_from_settings():

    settings = configparser.ConfigParser()  # создаём объекта парсера
    settings.read("settings.ini")  # читаем конфиг

    owner_id = settings['user_record']['id']
    username = settings['user_record']['username']
    url = settings['user_record']['URL']
    access_token = settings['user_record']["TOKEN_VK"]
    version_api_vk = settings['user_record']["version_api_vk"]
    urlug = settings['user_record']["URLUSERGET"]
    token_yd = settings['yandex_disk']["TOKEN_YANDEX_DISK"]
    path_yd = settings['yandex_disk']["disk_file_path"]
    numb_of_photos = int(settings['yandex_disk']["number_of_photoes"])

    try:
        if not (owner_id or username):
            raise ValueError
    except ValueError:
        print("Введите либо имя пользователя, либо его цифровой идентификатор!")
        sys.exit()

    try:
        if not(access_token):
            raise ValueError
    except ValueError:
        print("Вы не ввели токен Вконтакте!")
        sys.exit()

    try:
        if not(token_yd):
            raise ValueError
    except ValueError:
        print("Вы не ввели токен Яндекс-диска!")
        sys.exit()



    return owner_id, username, url, access_token, version_api_vk, token_yd, path_yd, numb_of_photos, urlug

def create_json(user_id, list_result_json):
    file = json.dumps(list_result_json, indent=4)
    with open(f'{user_id}.json', 'w', encoding='utf-8') as f:
       f.write(file)

def create_json_on_disk(result_list_obj, numb_of_photos, token_yd, path_yd, owner_id):

    if numb_of_photos > len(result_list_obj):
        numb_of_photos = len(result_list_obj)

    ya_ = YaUploader(token=token_yd)
    path_yd = (f"{path_yd}vk_{owner_id}/")
    ya_.create_folder(path_yd)
    names = set()
    list_result_json = []
    for i in tqdm(range(0, numb_of_photos)):
        if result_list_obj[i].count_of_likes in names:
            filename = (f'{path_yd}{result_list_obj[i].count_of_likes}_{result_list_obj[i].date}.jpg')
        else:
            filename = (f'{path_yd}{result_list_obj[i].count_of_likes}.jpg')
            names.add(result_list_obj[i].count_of_likes)

        ya_.get_upload_file(file_link=result_list_obj[i].url, disk_file_path=filename)

        list_result_json.append({
            'file_name': filename,
            'size': f'{result_list_obj[i].height}x{result_list_obj[i].width}'
        })

    create_json(owner_id, list_result_json)
