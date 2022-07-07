from abc import ABC

import scrapy
import settings
from items import OtherCountryItem
from repositories.redis_repositories import RedisRepositories

redis_repositories = RedisRepositories()


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
