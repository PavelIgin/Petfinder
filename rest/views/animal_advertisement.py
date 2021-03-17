from rest.serializer import UrlAnimalAdvertSerializer
from listanimal.models import AnimalInfo
from rest.serializer import AnimalInfoSerializer

from rest_framework import viewsets
from drf_yasg.views import get_schema_view


import logging
logger = logging.getLogger('rest.views')
SchemaView = get_schema_view()


class AnimalAdvertisementView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnimalInfoSerializer
    queryset = AnimalInfo.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = UrlAnimalAdvertSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        self.queryset = serializer.search_advert()
        return super().list(self, request, *args, **kwargs)
