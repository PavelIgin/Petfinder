from rest_framework import serializers

from rest.service import comment_object_create


class CommentObject(serializers.Serializer):

    content_type = serializers.ChoiceField(choices=[('news', 'news'), ('animal', 'animal')])
    object_id = serializers.IntegerField(min_value=1)

    def request_for_comment_create(self):

        return comment_object_create(self)
