import vk_api
import logging

from django.utils import timezone
from django.conf import settings
from listanimal.models import NewestLogFileContent

logger = logging.getLogger('commands.createanimal')


class VkWallPostAnimal():

    def vk_wall_post(self, one_animal, animal_type):
        """
        функция отправляет созданное объявление в новостную ленту сообщества
        """
        vk_session = vk_api.VkApi(settings.LOGIN, settings.PASSWORD,
                                  token=settings.ACESS_TOKEN_ATTACHEMENT)
        try:
            message = 'Номер животного:{}' \
                      '\nТип животного:{}\n' \
                      'Возраст:{}\nПол:{}\n' \
                      'Габариты:{}\nИмя:{}\n' \
                      'Статус поиска:{}\n' \
                      'Цвет:{}\n' \
                      'Фотографии{}'.format(
                                            one_animal.get('number', None),
                                            animal_type,
                                            one_animal['age'],
                                            one_animal['gender'],
                                            one_animal['size'],
                                            one_animal['name'],
                                            one_animal['status'],
                                            one_animal.get('color', None),
                                            one_animal.get('photos', None)
                                            )

            vk_session.method('wall.post', {'owner_id': -settings.GROUP_ID,
                                            'from_group': 1,
                                            'message': message})

        except vk_api.VkApiError:
            logger.error(msg='Ошибка отправки объявления '
                             'в вк:{},{}'.format(one_animal['name'],
                                                 timezone.now()))
            log_db = open('logger/advertisement.log', 'r')
            NewestLogFileContent.objects.update_or_create(
                            log_filename='commands.advertisement',
                            defaults={'content': log_db.readlines()[-100:-1]})
            log_db.close()
