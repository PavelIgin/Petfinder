from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest.serializer import CommentSerializer

from users.models import Comment


class CommentAnimal(APIView):

    def get(self, request, pk):

        queryset = Comment.objects.filter(object_id=pk)
        comments = CommentSerializer(queryset, many=True).data
        return Response(comments)
