import vk_api
import time
import os
import requests
import logging
from django.utils import timezone

from django.conf import settings
from listanimal.models import NewestLogFileContent

logger = logging.getLogger('commands.createnews')

"""
Сервис предоставляет функции для размещения 
новостей, объявлений а также каждая функция просматривает
наличие или отсутствие основоного текста(main_text)
"""

group_id = settings.GROUP_ID
vk_session = vk_api.VkApi(token=settings.ACESS_TOKEN_ATTACHEMENT)
upload_url = vk_session.method('photos.getWallUploadServer',
                               {'group_id': group_id,
                                'v': 5.95})['upload_url']


def vk_wall_news(animal_news):
    """
    осуществляет определение через какую функцию
    будет обрабатываться новость
    """
    try:
        if animal_news.get('url_media', None) is not None:
            if animal_news['url_media'].endswith('.mp4'):
                _vk_wall_news_with_mp4(animal_news)
            else:
                _vk_wall_news_with_photo(animal_news)
        elif animal_news.get('gallery_img', None) is not None:
            _vk_wall_news_with_gallery_img(animal_news)
        else:
            _vk_wall_without_media_file(animal_news)
    except vk_api.VkApiError:
        logger.error(msg='Ошибка отправки новости в '
                         'вк {},{}'.format(animal_news['description_news'],
                                           str(timezone.now())))
        log_db = open('logger/advertisement.log', 'r')
        NewestLogFileContent.objects.update_or_create(
            log_filename='commands.createnews',
            defaults={'content': log_db.read()[-100:-1]})
        log_db.close()


def vk_wall_advertisement(one_animal, animal_type):
    """
    функция отправляет созданное ОБЪЯВЛЕНИЯ в новостную ленту сообщества
    """
    try:
        message = 'Номер животного:{}\nТип животного:{}\n' \
                  'Возраст:{}\nПол:{}\nГабариты:{}\nИмя:{}\n' \
                  'Статус поиска:{}\nЦвет:{}\n' \
                  'Фотографии{}'.format(
                                        one_animal.get('number', None),
                                        animal_type,
                                        one_animal['age'],
                                        one_animal['gender'],
                                        one_animal['size'],
                                        one_animal['name'],
                                        one_animal['status'],
                                        one_animal.get('color', None),
                                        one_animal.get('photos', None))
        _vk_wall_post_for_group(message)

    except vk_api.VkApiError:
        message = 'Ошибка отправки объявления ' \
                  'в вк:{},{}'.format(one_animal['name'],
                                      timezone.now())
        logger.error(msg=message)
        log_db = open('logger/advertisement.log', 'r')
        NewestLogFileContent.objects.update_or_create(
            log_filename='commands.advertisement',
            defaults={'content': log_db.readlines()[-100:-1]})
        log_db.close()


def _vk_wall_news_with_mp4(animal_news):
    """
    выкладывает новость, если в ней есть
    mp4 файл в новости
    """

    message = '{}\nСсылка на оригинал:{}\n Вложение:{}\n{}\n{}\n' \
              'Ссылка на видео:{}'.format(animal_news['time_post'],
                                          animal_news['url_news'],
                                          animal_news.get('main_text', ''),
                                          animal_news['description_news'],
                                          animal_news['heading'],
                                          animal_news['url_media'])

    _vk_wall_post_for_group(message)


def _vk_wall_news_with_photo(animal_news):
    """
    выкладывает новость, при наличии в ней
    1-й фотографии в новости
    """
    photo = requests.get(animal_news['url_media'])
    images = open('images.jpg', 'wb')
    images.write(photo.content)
    request = requests.post(upload_url,
                            files={'file': open('images.jpg', 'rb')})
    save_wall_photo = vk_session.method('photos.saveWallPhoto',
                                        {'group_id': group_id, 'v': 5.95,
                                         'photo': request.json()['photo'],
                                         'server': request.json()['server'],
                                         'hash': request.json()['hash']})
    saved_photo = 'photo' + str(save_wall_photo[0]['owner_id']) \
                  + '_' + str(save_wall_photo[0]['id'])

    message = '{}\nСсылка на оригинал:{}\nВложение:{}\n{}\n{}'.format(
        animal_news['time_post'],
        animal_news['url_news'],
        animal_news.get('main_text', ''),
        animal_news['description_news'],
        animal_news['heading'])

    post_for_group = {'owner_id': -group_id,
                      'from_group': 1,
                      'message': message,
                      'attachments': saved_photo}

    vk_session.method('wall.post', post_for_group)
    os.remove('images.jpg')


def _vk_wall_news_with_gallery_img(animal_news):
    """
    выкладывает новость при наличии
    галлереи фотографий в новости
    """
    saved_gallery = ''
    for one_img in animal_news['gallery_img']:
        photo = requests.get(one_img.replace(' ', ''))
        images = open('images.jpg', 'wb')
        images.write(photo.content)
        time.sleep(5)
        request = requests.post(upload_url,
                                files={'file': open('images.jpg', 'rb')})
        data = {'group_id': group_id, 'v': 5.95,
                'photo': request.json()['photo'],
                'server': request.json()['server'],
                'hash': request.json()['hash']}
        save_wall_photo = vk_session.method('photos.saveWallPhoto', data)
        saved_photo = 'photo' + str(save_wall_photo[0]['owner_id']) \
                      + '_' + str(save_wall_photo[0]['id'])
        saved_gallery += saved_photo + ','
        os.remove('images.jpg')

    message = '{}\nСсылка на оригинал:{}\nВложение:{}\n{}\n{}'.format(
        animal_news['time_post'],
        animal_news['url_news'],
        animal_news.get('main_text', ''),
        animal_news['description_news'],
        animal_news['heading'])

    _vk_wall_post_for_group(message)


def _vk_wall_without_media_file(animal_news):
    """
    выкладывает новость при
    отсутствии медиафайлов
    """
    message = '{}\nСсылка на оригинал:{}\nВложение:{}\n{}\n{}'.format(
        animal_news['time_post'],
        animal_news['url_news'],
        animal_news.get('main_text', ""),
        animal_news['description_news'],
        animal_news['heading'])

    _vk_wall_post_for_group(message)


def _vk_wall_post_for_group(message):
    post_for_group = {'owner_id': -group_id, 'from_group': 1, 'message': message}
    vk_session.method('wall.post', post_for_group)
