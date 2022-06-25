"""
Учебная программа сохранения на яндекс.диск фотографий пользователей ВК
В settings.ini заполните либо имя пользователя вконтакте, либо его цифровой идентификатор (в реальной жизни, пользователь вводил бы это через поля ввода)
Если будет заполнено и то, и другое, предпочтение будет отдаваться имени пользователя
На яндекс диске создается одноименный директорий, в котором будут сохраняться фотографии пользователя
Программа возвращает json-файл, имя которого формируется в зависимости от имени или идентификатора пользователя
Также не забудьте вставить в settings.ini рабочий токен
"""

from classes.vk import VkPhoto
from utils import pilot

if __name__ == '__main__':
    owner_id, username, url, access_token, version_api_vk, token_yd, path_yd, numb_of_photos, urlug  = pilot.get_from_settings()
    vk = VkPhoto(url, urlug, owner_id, version_api_vk, access_token, username)
    if username:
        owner_id = username
    pilot.create_json_on_disk(vk.json_to_list_obj(), numb_of_photos, token_yd, path_yd, owner_id)

