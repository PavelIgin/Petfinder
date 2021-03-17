from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from users.serializer import CreateCommentSerializer
from django.core.exceptions import ObjectDoesNotExist


class CommentViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=True, permission_classes=['IsAuthenticated'])
    def create(self, request):
        try:
            serializer = CreateCommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(request)
            return Response({'status': 'comment was created'})
        except ObjectDoesNotExist:
            return Response({'status': 'object is not existing'})
