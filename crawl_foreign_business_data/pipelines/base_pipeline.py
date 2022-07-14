"""Base pipeline"""
import logging

from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories

mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class BasePipeline:
    """Base pipline"""

    logger = logging.getLogger(__name__)

    def open_spider(self):
        """
        open_spider
        :return:
        """
        mongo_repositories.open_mongo()
        self.logger.info('Open Spider')

    def close_spider(self):
        """
        close_spider
        :return:
        """
        mongo_repositories.close_mongo()
        self.logger.info('Close Spider')
