from django.db.models import Q
from listanimal.models import AnimalInfo


def filter_advert(self):
    validated_data = self.validated_data
    val = Q()
    if validated_data['size'] is not None:
        val &= Q(size=validated_data['size'])
    if validated_data['color'] != []:
        val &= Q(color__in=validated_data['color'])
    if validated_data['animaltype'] != []:
        val &= Q(animal_type__in=validated_data['animaltype'])

    return AnimalInfo.objects.filter(val)
