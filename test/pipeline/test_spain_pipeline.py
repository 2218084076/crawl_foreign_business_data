"""Test spain pipeline"""
import pytest

from crawl_foreign_business_data.pipelines.spain_pipeline import SpainPipeline
from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories


@pytest.mark.parametrize(
    'item_key,item',
    [
        ('city', ['provincia', 'Actividad']),
        ('city', None),
        ('city', ['test']),
        ('company_links', ['/FOO-TEST.html']),
        ('company_links', ['/PgNum.html']),
        ('company_links', [None]),
        ('spain_company_infos', {'foo': 'bar'}),
    ]
)
def test_spain_process_item(mocker, item, item_key):
    """
    test_spain_process_item
    :param mocker:
    :param item:
    :param item_key:
    :return:
    """
    test_item = {
        item_key: item
    }

    mock_write_to_redis = mocker.patch.object(
        RedisRepositories, 'write_to_redis'
    )
    mock_increase = mocker.patch.object(
        MongoRepositories, 'increase'
    )

    if item_key == 'city' and item is None:
        with pytest.raises(TypeError):
            SpainPipeline().process_item(test_item, mocker.MagicMock())

    if item_key == 'city' and item == ['test']:
        result = SpainPipeline().process_item(test_item, mocker.MagicMock())
        assert result == {'city': ['test']}

    if item_key == 'city' and item == ['provincia', 'Actividad']:
        result = SpainPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called()
        assert result.get(item_key) == item

    if item_key == 'company_links' and item == ['/FOO-TEST.html']:
        result = SpainPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called_with(
            'SpainCrawlCompanyLink',
            '/FOO-TEST.html')
        assert result.get(item_key) == item

    if item_key == 'company_links' and item == ['/PgNum.html']:
        result = SpainPipeline().process_item(test_item, mocker.MagicMock())
        mock_write_to_redis.assert_called_with('SpainCrawlCityIndex', '/PgNum.html')
        assert result.get(item_key) == item

    if item_key == 'company_link' and item == [None]:
        with pytest.raises(AttributeError):
            SpainPipeline().process_item(test_item, mocker.MagicMock())

    if item_key == 'spain_company_infos':
        result = SpainPipeline().process_item(test_item, mocker.MagicMock())
        mock_increase.assert_called_with({'foo': 'bar'})
        assert result.get(item_key) == item
