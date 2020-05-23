import logging
from collections import namedtuple
import datetime
from time import sleep
from math import ceil
import random

import requests
import bs4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kinopoisk')

InnerBlock = namedtuple(
    'Block',
    'url'
)


class Block(InnerBlock):

    def __str__(self):
        return f'{self.url}'


class KinopoiskParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    def get_page(self, url: str, query: str):
        params = {}  # это параметры get запроса
        if query:
            params['kp_query'] = query

        url = 'https://www.kinopoisk.ru/' + url
        # url = 'https://www.kinopoisk.ru/index.php?kp_query=%D0%B2%D0%B5%D0%BD%D0%BE%D0%BC'
        r = self.session.get(url, params=params)
        # logger.info(r)
        return r.text

    """    
    def parse_block(self, item: bs4.element.Tag):

    logger.info(f'%s, %s, %s, %s, %s', url, title, price, currency, date)
   
    return Block(
        url=url,
    )"""

    def get_block(self, link: str):
        text = self.get_page(link, '')
        soup = bs4.BeautifulSoup(text, 'lxml')

        # logger.info(tags)
        # logger.info(text)
        # logger.info(soup)

        # Запрос Css селектора, состоящего из множества классов, производится через select

        inform = {}
        # если сериал
        container = soup.select('._2H4PAdm6bkbri4XRE7Y7H4')
        if len(container):
            container = soup.select('.table-col-years__years')
            inform['year'] = container[0].get_text()
            container = soup.select('.table-col-basic-link-list__value')
            inform['country'] = container[0].get_text()
            container = soup.select('._27B2_r_SnH5ZlIyaj0FCMF')
            inform['link'] = str('https://www.kinopoisk.ru' + container[0].get('href'))
            try:
                container = soup.select('.table-col-plain-text__value')
                inform['slogan'] = container[0].get_text()
            except:
                inform['slogan'] = '-'

            container = soup.select('.film-poster.image-partial-component.image-partial-component_loaded')
            inform['image_link'] = str('https:' + container[0].get('src').replace('https:', ''))
            logger.info(inform)

        # если фильм.select('.tabl
        else:
            container = soup.select('.js-rum-hero.movie-info__table')
            # logger.debug(container[0].get_text())
            # logger.info(container)
            # logger.info(container)
            logger.info(len(container))

            inform['year'] = container[0].find_all('td')[1].get_text().replace('\n', '')
            inform['country'] = container[0].find_all('td')[3].get_text().replace('\n', '')
            inform['slogan'] = container[0].find_all('td')[5].get_text()

            container = soup.select('.kinopoisk-watch-online-button-partial-component.'
                                    'kinopoisk-watch-online-button-partial-component_theme_desktop.'
                                    'kinopoisk-watch-online-button-partial-component_size_h40.'
                                    'kinopoisk-watch-online-button-partial-component_color-schema_orange')

            try:
                inform['link'] = str('https://www.kinopoisk.ru' + container[0].get('href'))
            except:
                inform['link'] = str('Ссылка на просмотр отсутствует')

            container = soup.select('.popupBigImage')[0]
            logger.info(container)
            logger.info(container.find('img'))
            inform['image_link'] = container.find('img').get('src')
        return inform

    def get_link(self, url: str, query: str):
        text = self.get_page(url, query)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # Запрос Css селектора, состоящего из множества классов, производится через select
        container = soup.select(
            'div.element.most_wanted')
        logger.info(container)
        # logger.debug(container[0].get_text())
        # logger.info(type(container))
        href = container[0].select_one('p.pic a.js-serp-metrika').get('href')
        # logger.info(href)
        link_list = href.split('/')
        logger.info(link_list)
        link = link_list[1] + '/' + link_list[2]
        logger.info(link)
        return link

    def parse_all(self, query: str):
        url = 'index.php'
        link = self.get_link(url=url, query=query)
        sleep(1 + random.randint(0, 10) / 10)
        res = self.get_block(link=link)
        return res


def main():
    p = KinopoiskParser()
    p.parse_all('Дэдпул')


if __name__ == "__main__":
    main()
