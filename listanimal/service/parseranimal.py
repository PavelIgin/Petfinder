from bs4 import BeautifulSoup as bs
import requests

headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; '
                         'Linux x86_64; rv:70.0) '
                         'Gecko/20100101 Firefox/70.0'}
base_url = 'https://russian.rt.com'
tag_animal = base_url + '/tag/zhivotnye'
session = requests.Session()
articles = []


def rt_news_animal():
    """
    Эта функция парсит https://russian.rt.com/tag/zhivotnye
    all_list_news = последние 15 новостей
    url_new = ссылка на конкретную новость
    heading= заголовок статьи
    time_post = время публикации статьи
    description_news= краткое описание статьи , которое находится
    как в статье ,так и в ее кратном описании на общей странице статей
    """
    request = request_page_news()
    soup = bs(request, 'html.parser')
    page_news = soup.find_all('div', 'card__heading_all-new')
    for news_instance in page_news:
        link = news_instance('a', 'link_color')
        for news in link:
            url_news = base_url + news['href']
            request_url_news = request_news(url_news)
            soup_url_new = bs(request_url_news, 'html.parser')
            _gathering_news(soup_url_new, news_instance, url_news)
    return articles


def request_news(url_news):
    request = session.get(url_news, headers=headers).content
    return request


def request_page_news():
    request = session.get(tag_animal, headers=headers).content
    return request


def _gathering_news(soup_url_new, news_instance, url_news):
    if soup_url_new.find('div', 'article__summary') is None:
        _add_news_different_format(soup_url_new, news_instance, url_news)
    else:
        heading = soup_url_new.find('div', 'article__summary').text
        time_post = soup_url_new.find('time', 'date')['datetime']
        set_news = {'url_news': url_news,
                    'description_news': news_instance.text.strip(),
                    'heading': heading.strip(),
                    'time_post': time_post}
        _add_main_text(set_news, soup_url_new)
        _add_url_media(set_news, soup_url_new)
        _add_mediaplayer_mp4(set_news,
                             time_post, soup_url_new)
        _add_mediaplayer_you_tube(soup_url_new,
                                  set_news)
        _add_galery_media(soup_url_new, set_news)
        articles.append(set_news)


def _add_main_text(set_news, soup_url_new):
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


def _add_url_media(set_news, soup_url_new):
    """
    url_media= принимает в значение картинки, видео
    (может быть как mp4 так и с youtube)
    """
    url_media = soup_url_new.find('img', 'article__cover-image')
    if url_media is not None:
        return set_news.update({'url_media': url_media['src']})


def _add_mediaplayer_mp4(set_news, time_post, soup_url_new):
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


def _add_mediaplayer_you_tube(soup_url_new, set_news):
    """
    url_media = видео(youtube)
    """
    mediaplayer_you_tube = soup_url_new.find_all('div', 'slide')
    if mediaplayer_you_tube is []:
        url_media = soup_url_new.find('iframe', 'cover__video')
        if url_media is not None:
            you_tube_url = 'https:' + url_media['src']
            return set_news.update({'url_media': you_tube_url})


def _add_galery_media(soup_url_new, set_news):
    """
    galery_media = при наличии в статье нескольких фотографий,
    вместо url_media принимаются все фотографии в galery_media
    """
    galery_media = soup_url_new.find_all('div', 'slide')
    summ_gallery = []
    for gallery in galery_media:
        summ_gallery += {str(gallery['data-src'] + ' ')}
    return set_news.update({'gallery_img': summ_gallery})


def _add_news_different_format(soup_usr_new, news_instance, url_new):
    """
    парсинг статей отличного от большинства статей
    https://russian.rt.com/russia/article/808880-rebyonok-opeka-dom-podzhog
    :param soup_usr_new:
    :param news_instance:
    :param url_new:
    :return:
    """
    image = soup_usr_new.find('div', 'main-cover')['style']
    first_element = image.find('(') + 1
    last_element = image.rfind(')')
    url_image = image[first_element:last_element]
    time_post = news_instance.parent.find('time', 'date')['datetime']
    heading = soup_usr_new.find('h1', 'main-page-heading__title').text
    text_news = soup_usr_new.find('div', 'page-content')
    description = text_news.find_all('p')[0].text
    main_text = text_news.find_all('p')[1:]
    full_text = ''
    for part_text in main_text:
        full_text += part_text.text
    set_news = {'url_news': url_new,
                'description_news': description,
                'heading': heading,
                'main_text': full_text,
                'time_post': time_post,
                'url_media': url_image}
    articles.append(set_news)
