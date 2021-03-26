from rest_framework.views import APIView
from rest_framework.response import Response

from listanimal.models import AnimalType
from rest.serializer import AnimalTypeSerializer


class AnimalAdvertisementTypeView(APIView):

    def get(self, request):

        type = AnimalType.objects.all()
        serializer = AnimalTypeSerializer(type, many=True)
        return Response(serializer.data)
