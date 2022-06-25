import requests

class Photo:
    """
    Класс Photo- характеристики фотографий которые сохраняются на яндекс диск.
    Этому классу можно переопределять стандартные методы, чтобы сравнивать, сортировать или распечатывать информацию о фотогррафиях.
    В этой реализации обошлись добавлением объектов класса в список, сортировать можно по любому полю класса методом sortkey(s),
    где s- поле класса
    @staticmethod
    def sort_key(s):
        return s.size
    """


    def __init__(self, file_name, date, count_of_likes, size, height, width, url):
        self.file_name = file_name
        self.date = date
        self.count_of_likes = count_of_likes
        self.size = size
        self.height = height
        self.width = width
        self.url = url

class VkPhoto:
    """
    Класс VkPhoto имеет методы взаимодействия с сетью Вконтакте
    и формирует, сортирует и возвращает список объектов типа Photo
    """

    def __init__(self, url, urlug, owner_id, version_api_vk, token, username=''):
        self.token = token
        self.version = version_api_vk
        self.url = url
        self.urlug = urlug
        self.list_of_photos = []
        self.username = username
        self.owner_id = owner_id
        if username:
            self.owner_id = self.get_owner_id()
        self.params = {
            'owner_id': self.owner_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0,
            'access_token': self.token,
            'v': self.version
    }

    def get_owner_id(self):
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.user_params = {
            'user_ids': self.username,
        }
        result =  requests.get(self.urlug, params={**self.params, **self.user_params})
        result.raise_for_status()
        if result.status_code == 200:
            try:
                if result.json()["error"]["error_code"] == 5:
                    raise ValueError('Ошибка авторизации вконтакте. Проверьте ТОКЕН в файле settings.ini ')
            except ValueError:
                 print('Ошибка авторизации вконтакте. Проверьте ТОКЕН в файле settings.ini ')
                 raise
            except KeyError:
                 return result.json()['response'][0]['id']

    def get_photos(self):
        result = requests.get(self.url, self.params)
        result.raise_for_status()
        if result.status_code == 200:
            try:
                if result.json()["error"]["error_code"] == 5:
                    raise ValueError('Ошибка авторизации вконтакте. Проверьте ТОКЕН в файле settings.ini ')
            except ValueError:
                print('Ошибка авторизации вконтакте. Проверьте ТОКЕН в файле settings.ini ')
                raise
            except KeyError:
                return result.json()




    def json_to_list_obj(self):
        json_result = self.get_photos()
        if json_result['response']['count']:
            photos = json_result['response']['items']
            for rphoto in photos:
                max_size_index = self.max_size(rphoto['sizes'])
                max_size_height = rphoto['sizes'][max_size_index]['height']
                max_size_width = rphoto['sizes'][max_size_index]['width']
                max_size = max_size_height * max_size_width
                max_size_url = rphoto['sizes'][max_size_index]['url']
                photo_object = Photo(file_name=rphoto['likes']['count'], date=rphoto['date'], count_of_likes=rphoto['likes']['count'],\
                                     size=max_size , height = max_size_height, width=max_size_width, url=max_size_url)
                self.list_of_photos.append(photo_object)
            self.list_of_photos = sorted(self.list_of_photos, key=self.sort_key, reverse=True)
        return self.list_of_photos

    def max_size(self, photoalbum):
        res = []
        for pho in photoalbum:
            res.append(pho['width'] * pho['height'])
        return res.index(max(res))

    @staticmethod
    def sort_key(s):
        return s.size
