import json
import requests
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from listanimal.models import AnimalInfo, AnimalColor, AnimalType
from listanimal.service.vk_wall_post import vk_wall_advertisement
from listanimal.service import send_animal
logger = logging.getLogger('commands.create_animal')


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_animal()

    def create_animal(self):
        """

        """
        data = {'grant_type': 'client_credentials',
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET}
        r = requests.post('https://api.petfinder.com/v2/oauth2/token',
                          data=json.dumps(data), verify=False)
        token_petfinder = json.loads(r.text)['access_token']
        headers = {'Authorization': 'Bearer ' + token_petfinder}
        r = requests.get('https://api.petfinder.com/v2/animals?page=1',
                         headers=headers, verify=False)
        json_file = json.loads(r.text)
        dict_animal = json_file.get('animals')
        self.create_animal_objects(dict_animal)

    def create_animal_objects(self, dict_animal):
        sum_new_animals = ''
        for one_animal in dict_animal:
            animal_type = AnimalType.objects.get_or_create(
                                animal_type=one_animal['type'])[0]
            if one_animal['colors']['primary'] is not None:
                animal_color = AnimalColor.objects.get_or_create(
                                primary=one_animal['colors']['primary'])[0]
            url_animals = []
            for i in one_animal['photos']:
                url_animals.append(i['full'])
            defaults = {'animal_type': animal_type,
                        'color': animal_color,
                        'age': one_animal['age'],
                        'gender': one_animal['gender'],
                        'size': one_animal['size'],
                        'photos': url_animals,
                        'name': one_animal['name'],
                        'status': one_animal['status']}
            create_object, is_created = AnimalInfo.objects.update_or_create(
                                                    number=one_animal['id'],
                                                    defaults=defaults)
            if is_created:
                sum_new_animals += '\n' + 'Новое объявление:' \
                                    + str(animal_type) + '' + defaults['name']
                vk_wall_advertisement(one_animal, animal_type)
        send_animal(sum_new_animals, one_animal)
