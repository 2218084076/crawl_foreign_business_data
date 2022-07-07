import re
from abc import ABC
from urllib.parse import unquote

import scrapy
import settings
from bs4 import BeautifulSoup
from items import RussiaCompanyItem
from repositories.redis_repositories import RedisRepositories

# logger = logging.getLogger(__name__)

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
                    self.logger.debug('"%s" 不是按首字母分类' % u)
            except TypeError:
                self.logger.debug('"%s"  does not exist' % u)

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
    # start_urls = redis_repositories.read_redis('Russia_company_list')
    #
    start_urls = ['https://www.rusprofile.ru/ip/304753421200031']

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
