"""Test russia spider"""
from typing import Any

import pytest
from scrapy import Selector

from crawl_foreign_business_data.spiders.russia_spider import (
    ParseRussiaCompanyInfo, RussiaCrawlIndex, extract_russian_company_links)


def test_extract_russian_links():
    """
    test_extract_russian_links
    :return:
    """
    page_text = '''
<!DOCTYPE html>
<html lang="ru">

<li><a href="/ip/"></a></li>
<li><a href="/ip/305233215000190"></a></li>
<li><a href="/ip/М">page1</a></li>

</html>
   '''
    response = Selector(text=page_text)
    url = 'https://www.rusprofile.ru/ip/М'

    result = extract_russian_company_links(url, response)
    assert result == (
        ['https://www.rusprofile.ru/ip/305233215000190'],
        ['https://www.rusprofile.ru/ip/М']
    )


@pytest.mark.parametrize(
    'url',
    [
        "/ip/A",
        "test",
        None,
        "https://www.rusprofile.ru/TEST"
    ]
)
def test_russia_crawl_index(url: Any):
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

    if url == "/ip/A":
        result = RussiaCrawlIndex().parse(response)
        assert result == {'index_list': [f'https://www.rusprofile.ru{url}']}

    else:
        result = RussiaCrawlIndex().parse(response)
        assert result == {'index_list': []}


def test_parse_russia_company_info(mocker):
    """
    test_parse_russia_company_info
    :param mocker:
    :return:
    """
    page_text = '''
<html>
<meta content="text/html; charset=utf-8">
<div id="main">
    <div class="container">
        <div class="company-header">
            <div>
                <h1 itemprop="name" class="">company-name</h1>
                <div class="tile-item">
                    <dl>
                        <dt>foo</dt>
                        <dd>bar</dd>
                    </dl>
                </div>
            </div>
        </div>
    </div>
</div>
</html>
    '''
    response = mocker.MagicMock(text=page_text)
    result = ParseRussiaCompanyInfo().parse(response)

    assert result.get('russia_company_infos').get('foo') == 'bar'
