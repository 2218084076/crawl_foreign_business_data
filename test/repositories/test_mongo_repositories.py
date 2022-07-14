"""Test mongo repositories"""
import pymongo

from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories


def test_increase():
    """
    test_increase
    :return:
    """
    test_content = {'foo': 'bar'}

    mongo_repositories = MongoRepositories('localhost:27017', 'test')
    mongo_repositories.collection_name = 'test'

    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = my_client["test"]
    my_col = mydb["test"]
    db_list = my_client.list_database_names()
    if 'test' in db_list:
        my_col.drop()

    mongo_repositories.open_mongo()
    mongo_repositories.increase(test_content)
    mongo_repositories.close_mongo()
    assert my_col.find({'foo': 'bar'})
