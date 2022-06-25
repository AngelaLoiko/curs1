import requests

class YaUploader:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, folder_name):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_name}
        req = requests.put(folder_url, headers=headers, params=params)

    def get_upload_file(self, file_link, disk_file_path): #Метод класса для записи файла на яндес.
        headers = self.get_headers()
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = { "url": file_link, "path": disk_file_path, "overwrite": True}
        response = requests.post(url=upload_url, params=params, headers=headers)
        response.raise_for_status()
        # TODO: обработать исключения
