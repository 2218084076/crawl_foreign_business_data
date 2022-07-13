from scrapy import Selector

from crawl_foreign_business_data.spiders.spain_spider import (
    ParseSpainCompanyInfo, SpainCrawlCityIndex, SpainCrawlPageLink)


def test_spain_crawl_city_index():
    """
    test_spain_crawl_city_index
    :return:
    """
    with open('data/spain_city_page.html', 'r', encoding='utf-8') as f:
        response = Selector(text=f.read())

        result = SpainCrawlCityIndex().parse(response)
        assert result.get('city') == ['test1', 'test2', 'test3']


def test_spain_crawl_page_link():
    """
    test_spain_crawl_page_link
    :return:
    """
    with open('data/spain_pages.html', 'r', encoding='utf-8') as f:
        response = Selector(text=f.read())

        result = SpainCrawlPageLink().parse(response)
        assert result.get('company_links') == ['test1', 'test2']


def test_parse_spain_company_info():
    """
    test_parse_spain_company_info
    :return:
    """
    with open('data/spain_company_info.html', 'r', encoding='utf-8') as f:
        response = Selector(text=f.read())

        result = ParseSpainCompanyInfo().parse(response)
        assert 'testA' in result.get('spain_company_infos')
