import pytest
from scrapy import Selector
from scrapy.http import TextResponse

from crawl_foreign_business_data.spiders.other_country_spider import (
    CrawlOtherCompanyLinks, CrawlOtherCountryIndex,
    ParseOtherCountryCompanyInfo, extract_links)


def test_extract_australia_links():
    """
    test_extract_australia_links
    :return:
    """
    with open('data/australia_page.html', 'r', encoding='utf-8') as f:
        response = Selector(text=f.read())

        result = extract_links(response)
        assert result == ['test1', 'test2', 'test3']


def test_crawl_country_index(mocker):
    """
    test_crawl_country_index
    :param mocker:
    :return:
    """
    mock_extract_links = mocker.patch(
        'crawl_foreign_business_data.spiders.other_country_spider.extract_links'
    )

    response = mocker.MagicMock()
    CrawlOtherCountryIndex().parse(response)

    mock_extract_links.assert_called_with(response)


def test_crawl_company_links(mocker):
    """
    test_crawl_company_links
    :param mocker:
    :return:
    """
    mock_extract_links = mocker.patch(
        'crawl_foreign_business_data.spiders.other_country_spider.extract_links'
    )
    response = mocker.MagicMock()
    CrawlOtherCompanyLinks().parse(response)

    mock_extract_links.assert_called_with(response)


@pytest.mark.parametrize(
    'url',
    (
            'aus61business',
            'nzlbusiness'
    )
)
def test_parse_other_country_company_info(url):
    """
    test_parse_other_country_company_info
    :param url:
    :return:
    """

    with open('data/australia_company_info_page.html', 'r', encoding='utf-8') as f:

        resp = TextResponse(url=url, body=f.read().encode('utf-8'))

        if url == 'aus61business':
            result = ParseOtherCountryCompanyInfo().parse(resp)
            assert result.get('company_info').get('country') == 'Australia'
            assert 'foo' in result.get('company_info').keys()

        if url == 'nzlbusiness':
            result = ParseOtherCountryCompanyInfo().parse(resp)
            assert result.get('company_info').get('country') == 'NewZealand'
            assert 'foo' in result.get('company_info').keys()
