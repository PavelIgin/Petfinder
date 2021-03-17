from bs4 import BeautifulSoup as bs
import requests


class RtNewsAnimalParser:

    headers = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; '
                             'Linux x86_64; rv:70.0) '
                             'Gecko/20100101 Firefox/70.0'}
    base_url = 'https://russian.rt.com'
    tag_zhivotnie = base_url + '/tag/zhivotnye'
    session = requests.Session()
    articles = []

    def rt_news_animal(self):
        """
        Эта функция парсит https://russian.rt.com/tag/zhivotnye
        all_list_news = последние 15 новостей
        url_new = ссылка на конкретную новость
        heading= заголовок статьи
        time_post = время публикации статьи
        description_news= краткое описание статьи , которое находится
        как в статье ,так и в ее кратном описании на общей странице статей
        """
        self.start_parser()
        return self.articles

    def request_news(self):
        request = self.session.get(self.tag_zhivotnie, headers=self.headers)
        return request.content

    def start_parser(self):
        request = self.request_news()
        soup = bs(request, 'html.parser')
        all_list_news = soup.find_all('div', 'card__heading_all-new')
        for list_news in all_list_news:
            url_news = list_news('a', 'link_color')
            for url_new in url_news:
                url_new = self.base_url + url_new['href']
                request_url_new = self.session.get(url_new,
                                                   headers=self.headers)
                soup_url_new = bs(request_url_new.content, 'html.parser')
                self.gathering_news(self, soup_url_new,
                                                  list_news, url_new)
        return soup_url_new

    def gathering_news(self, soup_url_new, list_news, url_new):

        if soup_url_new.find('div', 'article__summary') is None:
            self.add_news_different_format(self, soup_url_new,
                                                         list_news, url_new)
        else:
            heading = soup_url_new.find('div', 'article__summary').text
            time_post = soup_url_new.find('time', 'date')['datetime']
            set_news = {'url_news': url_new,
                        'description_news': list_news.text.strip(),
                        'heading': heading.strip(),
                        'time_post': time_post}
            self.add_main_text(self, set_news, soup_url_new)
            self.add_url_media(self, set_news, soup_url_new)
            self.add_mediaplayer_mp4(self, set_news,
                                     time_post, soup_url_new)
            self.add_mediaplayer_you_tube(self, soup_url_new,
                                                        set_news)
            self.add_galery_media(self, soup_url_new, set_news)
            self.articles.append(set_news)

    def add_main_text(self, set_news, soup_url_new):
        """
        main_text= основной текст находящийся на странице статьи
        """
        main_text = soup_url_new.find('div', 'article__text')
        if main_text is not None:
            main_text_find_all = main_text.find_all('p')
            full_text = ''
            for main_text_p in main_text_find_all:
                full_text += main_text_p.text
            return set_news.update({'main_text': full_text})

    def add_url_media(self, set_news, soup_url_new):
        """
        url_media= принимает в значение картинки, видео
        (может быть как mp4 так и с youtube)
        """
        url_media = soup_url_new.find('img', 'article__cover-image')
        if url_media is not None:
            return set_news.update({'url_media': url_media['src']})

    def add_mediaplayer_mp4(self, set_news, time_post, soup_url_new):
        """
        url_media = видео(mp4)
        """
        optimal_date = time_post.split('-')[0] + '.' + time_post.split('-')[1]
        mediaplayer_mp4 = soup_url_new.find('div', 'mediaplayer')
        if mediaplayer_mp4 is not None:
            url_media = mediaplayer_mp4.find('div').attrs['id']
            kod_video = url_media.split('-')[-1]
            url_media_new = 'https://cdnv.rt.com/russian/video/' + \
                            optimal_date + "/" + kod_video + '.mp4'
            return set_news.update({'url_media': url_media_new})

    def add_mediaplayer_you_tube(self, soup_url_new, set_news):
        """
        url_media = видео(youtube)
        """
        mediaplayer_you_tube = soup_url_new.find_all('div', 'slide')
        if mediaplayer_you_tube is []:
            url_media = soup_url_new.find('iframe', 'cover__video')
            if url_media is not None:
                you_tube_url = 'https:' + url_media['src']
                return set_news.update({'url_media': you_tube_url})

    def add_galery_media(self, soup_url_new, set_news):
        """
        galery_media = при наличии в статье нескольких фотографий,
        вместо url_media принимаются все фотографии в galery_media
        """
        galery_media = soup_url_new.find_all('div', 'slide')
        summ_gallery = []
        for gallery in galery_media:
            summ_gallery += {str(gallery['data-src'] + ' ')}
        return set_news.update({'gallery_img': summ_gallery})

    def add_news_different_format(self, soup_usr_new, list_news, url_new):
        image = soup_usr_new.find('div', 'main-cover')['style']
        first_char = image.find('(')+1
        last_char = image.rfind(')')
        url_image = image[first_char:last_char]
        time_post = list_news.parent.find('time', 'date')['datetime']
        description_news = soup_usr_new.find('h1',
                                             'main-page-heading__title').text
        all_text = soup_usr_new.find('div', 'page-content')
        heading = all_text.find_all('p')[0].text
        main_text = all_text.find_all('p')[1:]
        full_text = ''
        for parth_text in main_text:
            full_text += parth_text.text
        set_news = {'url_news': url_new,
                    'description_news': description_news,
                    'heading': heading,
                    'main_text': full_text,
                    'time_post': time_post,
                    'url_media': url_image}
        self.articles.append(set_news)
