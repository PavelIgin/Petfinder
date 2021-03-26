import logging
from listanimal.service import rt_news_animal
from django.core.management.base import BaseCommand
from listanimal.models import AnimalNews

from listanimal.service.vk_wall_post import vk_wall_news
from listanimal.service.send_mail import send_news

logger = logging.getLogger('commands.create_news')
log_db = open('logger/news.log', 'r')


class Command(BaseCommand):
    def handle(self, *args, **options):

        self.create_news()

    def create_news(self):

        sum_new_news = ''
        news = rt_news_animal()
        for animal_news in news:
            create_object, is_created = AnimalNews.objects.get_or_create(
                heading=animal_news['heading'], defaults=animal_news)
            if is_created:
                vk_wall_news(animal_news)
                sum_new_news += '\n' + ' Заголовок статьи:' + \
                                animal_news['heading']
        send_news(sum_new_news, animal_news)
