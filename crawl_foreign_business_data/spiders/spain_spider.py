"""Spain spider"""
from abc import ABC

import scrapy

from crawl_foreign_business_data import settings
from crawl_foreign_business_data.items import SpainItem
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories

redis_repositories = RedisRepositories()


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
        for tag in tag_a:
            items.append(tag.css('a::attr(href)').get())

        item['city'] = items

        return item


class SpainCrawlPageLink(scrapy.Spider, ABC):
    """
    根据分类链接抓取所有页面链接 做区分
    """
    name = 'SpainCrawlPageLink'
    start_urls = redis_repositories.read_redis('SpainCrawlCityIndex')

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
    start_urls = redis_repositories.read_redis('SpainCrawlPageLink')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = SpainItem()
        try:
            page = response.text
        except AttributeError:
            page = response.get()
        company_info = {
            'page_code': page
        }
        num = len(response.xpath('//*[@class="list06 adr"]//li'))
        for i in range(1, num + 1):
            content = response.xpath(f'//*[@id="datos-externos1"]/ul/li[{i}]//text()').getall()
            company_info[content[0]] = ''.join(content[1:]).split('\n', maxsplit=1)[0]

        item['spain_company_infos'] = company_info

        return item
