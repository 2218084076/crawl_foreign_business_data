"""Items"""
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RussiaCompanyItem(scrapy.Item):
    """Russia Company Item"""

    company_list = scrapy.Field()
    page_list = scrapy.Field()
    index_list = scrapy.Field()
    russia_company_infos = scrapy.Field()


class SpainItem(scrapy.Item):
    """Spain Item"""

    city = scrapy.Field()
    company_links = scrapy.Field()
    spain_company_infos = scrapy.Field()


class OtherCountryItem(scrapy.Item):
    """Other Country Item"""

    index = scrapy.Field()
    company_info = scrapy.Field()
