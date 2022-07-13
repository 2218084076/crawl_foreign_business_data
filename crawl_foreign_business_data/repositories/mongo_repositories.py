"""Mongo Repositories"""
import logging

import pymongo
from itemadapter import ItemAdapter
from scrapy.crawler import Crawler


class MongoRepositories:
    logger = logging.getLogger(__name__)

    def __init__(self, mongo_uri, mongo_db):
        self.db = None
        self.client = None
        self.collection_name = ''
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """
        from crawler
        :param crawler:
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.MONGO_CONFIG.get('mongo_uri'),
            mongo_db=crawler.settings.MONGO_CONFIG.get('mongo_db')
        )

    def open_mongo(self):
        """
        open mongo
        :param:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.logger.info('open mongo')

    def close_mongo(self):
        """
        close mongo
        :param:
        :return:
        """
        self.client.close()
        self.logger.info('close mongo')

    def increase(self, item_content: dict):
        """
        increase
        :param item_content:
        :return:
        """
        self.db[self.collection_name].insert_one(ItemAdapter(item_content).asdict())
