from rest_framework import serializers

from rest.service import filter_news
class UrlAnimalNewsSerializer(serializers.Serializer):
    """
    выводит новости в которых есть введенное предложение в search_line
    """
    search_line = serializers.CharField()

    def search_news(self):

        return filter_news(self)
