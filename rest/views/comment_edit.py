from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest.serializer.comment_edit import CommentEdit


class CommentEditView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request):
        serializer = CommentEdit(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.comment_edit(request)
        return Response(result)

    def destroy(self, request):
        serializer = CommentEdit(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.delete_comment(request)
        return Response(result)
