from rest_framework import serializers

from rest.service import CommentService


class CommentEdit(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)
    edit_comment = serializers.CharField(max_length=200)

    def comment_edit(self, request):
        edit_comment = CommentService
        return edit_comment.comment_edit(self, request)

    def delete_comment(self, request):
        delete_comment = CommentService
        return delete_comment.delete_comment(self,request)
