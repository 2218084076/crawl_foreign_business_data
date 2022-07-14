"""Other country spider"""
from abc import ABC

import scrapy

from crawl_foreign_business_data import settings
from crawl_foreign_business_data.items import OtherCountryItem
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories

redis_repositories = RedisRepositories()


# New Zealand and Australia

def extract_links(response):
    """
    extract tags links
    提取页面中所有链接
    :param response:
    :return:
    """
    items = []
    tag_a = response.xpath('//a')
    for tag in tag_a:
        items.append(tag.css('a::attr(href)').get())

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

        item['index'] = extract_links(response)

        return item


class CrawlOtherCompanyLinks(scrapy.Spider, ABC):
    """Crawl Company Links"""
    name = 'CrawlOtherCompanyLinks'
    # start_urls = redis_repositories.read_redis('CrawlOtherCountryIndex')

    start_urls = ['https://www.aus61business.com/browse/A/8333/']

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        item = OtherCountryItem()

        item['index'] = extract_links(response)

        return item


class ParseOtherCountryCompanyInfo(scrapy.Spider):
    """Parse Other Country Company Info"""
    name = 'ParseOtherCountryCompanyInfo'
    # start_urls = redis_repositories.read_redis('CrawlOtherCompanyLinks')

    start_urls = ['https://www.aus61business.com/company/A-A-Ham-Pty-Ltd']

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

        info_title = response.xpath('''
            //*[@class="col-xs-12 col-sm-3 row_label"]
        ''')
        info_value = response.xpath('''//*[@class="col-xs-12 col-sm-9"]''')

        for title, value in zip(info_title, info_value):
            company_info[title.css('::text').get()] = value.css('::text').get()

        item['company_info'] = company_info

        return item
