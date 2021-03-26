from django.contrib.contenttypes.models import ContentType
from listanimal.models import AnimalInfo, AnimalNews
from users.models.comment import Comment


def comment_object_create(self):
    validated_data = self.validated_data
    if validated_data['content_type'] == 'animal':
        object_animal = AnimalInfo.objects.get(id=validated_data['object_id'])
        object_type = ContentType.objects.get_for_model(object_animal)
        comment = Comment.objects.filter(content_type__pk=object_type.id, object_id=object_animal.id)
    if validated_data['content_type'] == 'news':
        object_news = AnimalNews.objects.get(id=validated_data['object_id'])
        object_type = ContentType.objects.get_for_model(object_news)
        comment = Comment.objects.filter(content_type__pk=object_type.id, object_id=object_news.id)

    return comment