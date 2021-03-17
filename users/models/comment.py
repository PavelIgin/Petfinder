from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    """
    Комментарии к объявлениям или новостям, создаются пользователями сервиса
    """
    user = models.ForeignKey('CustomUser',
                             related_name='comment',
                             on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.CharField(max_length=200)
    date_create = models.DateTimeField(auto_now=True, editable=False)
