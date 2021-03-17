from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest.serializer import AnimalNewsSerializer, UrlAnimalNewsSerializer

from django.shortcuts import render


class AnimalNewsView(APIView):
    serializer_class = UrlAnimalNewsSerializer

    def get(self, request):

        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        response = serializer.search_news()
        return Response(AnimalNewsSerializer(response, many=True).data)
