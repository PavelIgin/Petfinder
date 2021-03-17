from unittest.mock import patch
from unittest import TestCase
from listanimal.management.service.parseranimal import RtNewsAnimalParser


class MockTestParserAnimal(TestCase):
    parser = RtNewsAnimalParser()

    @patch('listanimal.parseranimal.RtNewsAnimalParser.request_news')
    def test_add_main_text(self, mock_rt_news_animal):
        soup_url_new = open('listanimal/test/html_file_test/news.html').read()
        mock_rt_news_animal.return_value = soup_url_new
        result = self.parser.start_parser()

    @patch('listanimal.parseranimal.RtNewsAnimalParser.request_news')
    def test_add_url_media(self, mock_rt_news_animal):
        soup_url_new = open('listanimal/test/html_file_test/url_media.html').read()
        mock_rt_news_animal.return_value = soup_url_new
        result = self.parser.start_parser()

    @patch('listanimal.parseranimal.RtNewsAnimalParser.request_news')
    def test_add_mediaplayer_mp4(self, mock_rt_news_animal):
        soup_url_new = open('listanimal/test/html_file_test/news_mp4.html').read()
        mock_rt_news_animal.return_value = soup_url_new
        result = self.parser.start_parser()

    @patch('listanimal.parseranimal.RtNewsAnimalParser.request_news')
    def test_add_galery_media(self, mock_rt_news_animal):
        soup_url_new = open('listanimal/test/html_file_test/news_gallery_img.html').read()
        mock_rt_news_animal.return_value = soup_url_new
        result = self.parser.start_parser()

    @patch('listanimal.parseranimal.RtNewsAnimalParser.request_news')
    def test_add_news_different_format(self, mock_rt_news_animal):
        soup_usr_new = open('listanimal/test/html_file_test/news_diff_format.html').read()
        mock_rt_news_animal.return_value = soup_usr_new
        result = self.parser.start_parser()

