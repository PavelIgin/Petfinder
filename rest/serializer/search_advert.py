from rest_framework import serializers

from rest.service import filter_advert

from listanimal.models import AnimalColor, AnimalType
from listanimal.enums import AnimalChoicesEnum


class UrlAnimalAdvertSerializer(serializers.Serializer):
    """
    выводит животных, которые попадают под фильтры : размер,цвет,тип животного
    """
    size = serializers.ChoiceField(default=None,
                                   choices=AnimalChoicesEnum.choices())
    color = serializers.SlugRelatedField(default=None,
                                         queryset=AnimalColor.objects.all(),
                                         slug_field='primary',
                                         many=True)
    animaltype = serializers.PrimaryKeyRelatedField(default=None,
                                                    queryset=AnimalType.objects.all(),
                                                    many=True)

    def search_advert(self):

        return filter_advert(self)
