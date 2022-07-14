"""Test other country pipeline"""
import pytest

from crawl_foreign_business_data.pipelines.other_pipeline import OtherPipeline
from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories


@pytest.mark.parametrize(
    'item_key,item',
    [
        ('index', ['nzlbusiness/browse']),
        ('index', ['nzlbusiness/company']),
        ('index', ['aus61business/browse']),
        ('index', ['aus61business/company']),
        ('company_info', {'country': 'NewZealand'}),
        ('company_info', {'country': 'Australia'}),
    ]
)
def test_process_item(mocker, item_key, item):
    """
    test_process_item
    :param mocker:
    :param item_key:
    :param item:
    :return:
    """
    test_item = {
        item_key: item
    }

    mock_mongo_increase = mocker.patch.object(MongoRepositories, 'increase')
    mock_write_to_redis = mocker.patch.object(RedisRepositories, 'write_to_redis')

    if 'nzlbusiness/browse' in item:
        OtherPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called_with('CrawlOtherCountryIndex', 'nzlbusiness/browse')

    if 'nzlbusiness/company' in item:
        OtherPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called_with('CrawlOtherCompanyLinks', 'nzlbusiness/company')

    if 'aus61business/browse' in item:
        OtherPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called_with('CrawlOtherCountryIndex', 'aus61business/browse')

    if 'aus61business/company' in item:
        OtherPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called_with(
            'CrawlOtherCompanyLinks', 'aus61business/company')

    if item_key == 'company_info' and item.get('country') == 'NewZealand':
        OtherPipeline().process_item(test_item, mocker.MagicMock())
        mock_mongo_increase.assert_called_with({'country': 'NewZealand'})
    if item_key == 'company_info' and item.get('country') == 'Australia':
        OtherPipeline().process_item(test_item, mocker.MagicMock())
        mock_mongo_increase.assert_called_with({'country': 'Australia'})
