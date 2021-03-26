from rest_framework.views import APIView
from rest_framework.response import Response

from listanimal.models import AnimalColor
from rest.serializer import AnimalColorSerializer


class AnimalAdvertisementColorView(APIView):

    def get(self, request):

        color = AnimalColor.objects.all()
        serializer = AnimalColorSerializer(color, many=True)
        return Response(serializer.data)
