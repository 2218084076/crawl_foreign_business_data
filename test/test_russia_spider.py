import pytest
from scrapy import Selector

from crawl_foreign_business_data.spiders.russia_spider import extract_russian_company_links, RussiaCrawlIndex, \
    ParseRussiaCompanyInfo


def test_extract_russian_links():
    """
    test_extract_russian_links
    :return:
    """
    with open('data/russia_page.html', 'r', encoding='utf-8') as f:
        response = Selector(text=f.read())
        url = 'https://www.rusprofile.ru/ip/М'

        result = extract_russian_company_links(url, response)
        assert result == (['https://www.rusprofile.ru/ip/305233215000190'], ['https://www.rusprofile.ru/ip/М'])


@pytest.mark.parametrize(
    'url',
    [
        "ip/A",
        "test",
        None,
        "https://www.rusprofile.ru/TEST"
    ]
)
def test_russia_crawl_index(url):
    """
    test_russia_crawl_index
    :param url:
    :return:
    """
    page_text = f'''
<html lang="ru">
    <ul class="letter-list">
    <li><a href="{url}">А</a></li>
    </ul>
</html>
    '''
    response = Selector(text=page_text)

    if url == "ip/A":
        result = RussiaCrawlIndex().parse(response)
        assert result == {'index_list': ['https://www.rusprofile.ru/%s' % url]}

    else:
        result = RussiaCrawlIndex().parse(response)
        assert result == {'index_list': []}


def test_parse_russia_company_info(mocker):
    """
    test_parse_russia_company_info
    :param mocker:
    :return:
    """
    with open('data/ruaaia_company_info.html', 'r', encoding='utf-8') as f:
        response = mocker.MagicMock(text=f.read())
        result = ParseRussiaCompanyInfo().parse(response)

        assert result.get('russia_company_infos').get('OGRNIP') == '319508100170320'
