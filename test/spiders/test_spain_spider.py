"""Test spain spider"""
from scrapy import Selector

from crawl_foreign_business_data.spiders.spain_spider import (
    ParseSpainCompanyInfo, SpainCrawlCityIndex, SpainCrawlPageLink)


def test_spain_crawl_city_index():
    """
    test_spain_crawl_city_index
    :return:
    """
    page_text = '''
<!DOCTYPE HTML   >
<html lang='es'>

<ul class="list02">
    <li><a href="test1" title></a>
    <li><a href="test2" title></a>
    <li><a href="test3" title></a>
</ul>
</html>
    '''
    response = Selector(text=page_text)

    result = SpainCrawlCityIndex().parse(response)
    assert result.get('city') == ['test1', 'test2', 'test3']


def test_spain_crawl_page_link():
    """
    test_spain_crawl_page_link
    :return:
    """
    page_text = '''
<!DOCTYPE HTML   >
<html lang='es'>

<li>
    <div>
        <a href="test1">test1</a>
    </div>
</li>

<li>
    <div>
        <a href="test2">test2</a>
    </div>
</li>
</html>
    '''
    response = Selector(text=page_text)

    result = SpainCrawlPageLink().parse(response)
    assert result.get('company_links') == ['test1', 'test2']


def test_parse_spain_company_info():
    """
    test_parse_spain_company_info
    :return:
    """
    page_text = '''
<!DOCTYPE HTML   >
<html lang='es'>

<section class="list06 adr"
         id="datos-externos1">
    <ul>
        <li><strong>testA</strong><span>a</span></li>
        <li><strong>testB</strong><span>b</span></li>
    </ul>
</section>
</html>
    '''
    response = Selector(text=page_text)

    result = ParseSpainCompanyInfo().parse(response)
    assert 'testA' in result.get('spain_company_infos')
