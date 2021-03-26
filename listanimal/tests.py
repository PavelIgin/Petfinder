from unittest.mock import patch
from django.test import TestCase
from listanimal.service import rt_news_animal


class MockTestParserAnimal(TestCase):


    @patch('listanimal.service.parseranimal.request_news')
    @patch('listanimal.service.parseranimal.request_page_news')
    def test_rt_news_animal(self, mock_rt_news_animal, request_news):
        soup_url_new = open('listanimal/test_html_file/html_file_test/list_news.html').read()
        mock_rt_news_animal.return_value = soup_url_new
        request_news.return_value = soup_url_new
        result = rt_news_animal()
