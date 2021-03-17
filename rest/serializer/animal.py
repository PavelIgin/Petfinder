from listanimal.models import AnimalInfo, AnimalColor, AnimalType
from rest_framework import serializers


class AnimalTypeSerializer (serializers.ModelSerializer):
    """
    Сериализует все объекты объявленией животных
    """
    class Meta:
        model = AnimalType
        fields = '__all__'


class AnimalColorSerializer (serializers.ModelSerializer):
    """
    Сериализует все цвета животных
    """
    primary = serializers.CharField(max_length=200)

    class Meta:
        model = AnimalColor
        fields = '__all__'


class AnimalInfoSerializer(serializers.ModelSerializer):
    color = AnimalColorSerializer().serializer_related_field(read_only=True)
    animal_type = AnimalTypeSerializer().serializer_related_field(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = AnimalInfo
        fields = '__all__'




