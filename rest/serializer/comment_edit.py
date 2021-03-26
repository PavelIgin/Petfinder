from rest_framework import serializers

from rest.service import comment_edit


class CommentEdit(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)
    edit_comment = serializers.CharField(max_length=200)

    def comment_edit(self, request):

        return comment_edit(self, request)
