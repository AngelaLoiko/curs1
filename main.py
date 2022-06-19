import json
from tqdm import tqdm
import settings
from classes.YaUploader import YaUploader
from classes.vk import VkPhoto

if __name__ == '__main__':
    owner_id = settings.user_record["id"]
    url = settings.user_record["URL"]
    access_token = settings.user_record["TOKEN_VK"]
    version_api_vk = settings.user_record["version_api_vk"]
    token_yd = settings.yandex_disk["TOKEN_YANDEX_DISK"]
    path_yd = settings.yandex_disk["disk_file_path"]
    numb_of_photos = settings.yandex_disk["number_of_photoes"]

    def create_json(user_id, list_result_json):
        file = json.dumps(list_result_json, indent=4)
        with open(f'{owner_id}.json', 'w', encoding='utf-8') as f:
            f.write(file)

    vk = VkPhoto(url, owner_id, version_api_vk, access_token)
    result_list_obj = vk.json_to_list_obj()
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
