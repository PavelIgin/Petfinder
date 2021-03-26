from rest_framework import serializers

from rest.service import delete_comment


class CommentDelete(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)

    def delete_comment(self, request):

        return delete_comment(self, request)
