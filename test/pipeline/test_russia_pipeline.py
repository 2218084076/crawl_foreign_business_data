"""Test russia pipeline"""

import pytest

from crawl_foreign_business_data.pipelines.russia_pipeline import \
    RussiaPipeline
from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories


@pytest.mark.parametrize(
    'key,value',
    [
        ('index_list', {'foo': 'bar'}),
        ('page_list', {'foo': 'bar'}),
        ('company_list', {'foo': 'bar'}),
        ('russia_company_infos', {'foo': 'bar'})
    ]
)
def test_russia_process_item(mocker, key: str, value: str):
    """
    test_russia_process_item
    :param mocker:
    :param key:
    :param value:
    :return:
    """
    test_item = {
        key: value
    }
    mock_increase = mocker.patch.object(
        MongoRepositories, 'increase'
    )
    test_spider = mocker.MagicMock()

    result = RussiaPipeline().process_item(test_item, test_spider)

    if key == 'russia_company_infos':
        mock_increase.assert_called()
        assert result.get(key) == value
    else:
        assert result.get(key) == value
