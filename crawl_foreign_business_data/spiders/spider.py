import logging
import re
from abc import ABC
from urllib.parse import unquote

import scrapy
from bs4 import BeautifulSoup

import settings
from items import OtherCountryItem, RussiaCompanyItem, SpainItem
from repositories.redis_repositories import RedisRepositories

logger = logging.getLogger(__name__)

redis_repositories = RedisRepositories()


# Russia Spider
def extract_russian_company_links(response):
    """
    extract_russian_company_links
    :param response:
    :return:
    """
    company_list = []
    category_list = []

    tag_a = response.xpath('//a')
    for a in tag_a:
        url = a.css('a::attr(href)').get()
        if 'ip' in url and len(re.sub(r'\D', "", url.split('ip/')[1])) > 5:
            if 'https://www.rusprofile.ru' not in url:
                url = 'https://www.rusprofile.ru' + url
                company_list.append(url)
        if unquote(response.url).split('https://www.rusprofile.ru')[1] in url:
            if 'https://www.rusprofile.ru' not in url:
                url = 'https://www.rusprofile.ru' + url
                category_list.append(url)

    return company_list, category_list


class RussiaCrawlIndex(scrapy.Spider):
    """
    抓取俄罗斯首字母分类链接
    """
    name = 'RussiaCrawlIndex'
    start_urls = settings.RUSSIA_CONFIG.get('start_urls')

    def parse(self, response, **kwargs):
        """
        prase
        :param response:
        :param kwargs:
        :return:
        """
        items = []
        item = RussiaCompanyItem()
        urls_list = response.xpath('//*[@class="letter-list"]//li')

        for url in urls_list:
            u = url.css('a::attr(href)').get()
            try:
                if 'ip' in u and 'https://www.rusprofile.ru' not in u:
                    u = 'https://www.rusprofile.ru' + u
                    items.append(u)
                else:
                    logger.debug('"%s" 不是按首字母分类' % u)
            except TypeError:
                logger.debug('"%s"  does not exist' % u)

        item['index_list'] = items

        return item


class RussiaCrawlCategory(scrapy.Spider, ABC):
    """
    抓取俄罗斯分类页中所有链接
    """
    name = 'RussiaCrawlCategory'
    start_urls = redis_repositories.read_redis('Russia_index_list')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = RussiaCompanyItem()
        parse_results = extract_russian_company_links(response)

        item['company_list'] = parse_results[0]
        item['page_list'] = parse_results[1]

        return item


class RussiaCrawlCompanyLinks(scrapy.Spider, ABC):
    """
    根据每页链接解析出所有公司详情页链接
    """
    name = 'RussiaCrawlCompanyLinks'
    start_urls = redis_repositories.read_redis('Russia_pages')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = RussiaCompanyItem()
        parse_results = extract_russian_company_links(response)

        item['company_list'] = parse_results[0]
        item['page_list'] = parse_results[1]

        return item


class ParseRussiaCompanyInfo(scrapy.Spider, ABC):
    """
    解析公司详情页中公司信息
    """
    name = 'ParseRussiaCompanyInfo'
    start_urls = redis_repositories.read_redis('Russia_company_list')

    # start_urls = ['https://www.rusprofile.ru/ip/304753421200031']

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = RussiaCompanyItem()
        page = response.text
        soup = BeautifulSoup(page, 'html.parser')

        info_list = soup.find_all('dl')

        company_info = {
            'Название компании': response.xpath('//*[@id="main"]/div/div[1]/div[1]/h1/text()').get().replace('\n',
                                                                                                             '').replace(
                ' ', ''),
            'page_code': page
        }
        for info in info_list:
            company_info[info.find('dt').text] = info.find('dd').text.replace('\n', '').replace(' ', '')

        item['russia_company_infos'] = company_info

        return item


# Spain Spider
class SpainCrawlCityIndex(scrapy.Spider, ABC):
    """
    抓取西班牙网站中分类部分链接
    """

    name = 'SpainCrawlCityIndex'
    start_urls = settings.SPAIN_CONFIG.get('start_urls')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        items = []
        item = SpainItem()

        tag_a = response.xpath('//a')
        for a in tag_a:
            items.append(a.css('a::attr(href)').get())

        item['city'] = items

        return item


class SpainCrawlPageLink(scrapy.Spider, ABC):
    """
    根据分类链接抓取所有页面链接 做区分
    """
    name = 'SpainCrawlPageLink'
    start_urls = redis_repositories.read_redis('Spain_city')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        items = []
        item = SpainItem()
        link_list = response.xpath('//li')
        for link in link_list:
            items.append(link.css('a::attr(href)').get())

        item['company_links'] = items

        return item


class ParseSpainCompanyInfo(scrapy.Spider, ABC):
    """
    解析所有公司详情页
    """
    name = 'parse_spain_company_info'
    start_urls = redis_repositories.read_redis('Spain_company_links')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = SpainItem()
        page = response.text

        company_info = {
            'page_code': page
        }
        num = len(response.xpath('//*[@class="list06 adr"]//li'))
        for i in range(1, num + 1):
            content = response.xpath('//*[@id="datos-externos1"]/ul/li[%s]//text()' % i).getall()
            company_info[content[0]] = ''.join(content[1:]).split('\n')[0].replace(': ', '')

        item['spain_company_infos'] = company_info

        return item


# New Zealand and Australia

def extract_tags_links(response):
    """
    extract tags links
    提取页面中所有链接
    :param response:
    :return:
    """
    items = []
    tag_a = response.xpath('//a')
    for a in tag_a:
        items.append(a.css('a::attr(href)').get())

    return items


class CrawlOtherCountryIndex(scrapy.Spider, ABC):
    """
    抓取页面中所有Company List分类 索引链接
    """

    name = 'CrawlOtherCountryIndex'

    start_urls = settings.OTHER_COUNTRY_CONFIG.get('start_urls')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = OtherCountryItem()

        item['index'] = extract_tags_links(response)

        return item


class CrawlOtherCompanyLinks(scrapy.Spider, ABC):
    """Crawl Company Links"""
    name = 'CrawlOtherCompanyLinks'
    start_urls = redis_repositories.read_redis('NewZealand_index') + redis_repositories.read_redis('Australia_index')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = OtherCountryItem()

        item['index'] = extract_tags_links(response)

        return item


class ParseOtherCountryCompanyInfo(scrapy.Spider):
    """Parse Other Country Company Info"""
    name = 'ParseOtherCountryCompanyInfo'
    start_urls = redis_repositories.read_redis('Australia_company_link') + redis_repositories.read_redis(
        'NewZealand_company_link')
    country = None

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = OtherCountryItem()

        if 'nzlbusiness' in response.url:
            self.country = 'NewZealand'

        if 'aus61business' in response.url:
            self.country = 'Australia'

        company_info = {
            'country': self.country,
            'page_code': response.text,

        }
        info_title = response.xpath('''//*[@class="col-xs-12 col-sm-3 row_label"]''')
        info_value = response.xpath('''//*[@class="col-xs-12 col-sm-9"]''')

        for title, value in zip(info_title, info_value):
            company_info[title.extract().split('</')[0].split('>').pop().strip()] = \
                value.extract().split('</')[0].split('>').pop().strip()

        item['company_info'] = company_info

        return item
