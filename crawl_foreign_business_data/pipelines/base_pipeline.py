"""Base pipeline"""

from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories

mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class BasePipeline:
    """Base pipline"""

    def open_spider(self, spider):
        """
        open_spider
        :return:
        """
        mongo_repositories.open_mongo()
        spider.logger.info('Open Spider')

    def close_spider(self, spider):
        """
        close_spider
        :return:
        """
        mongo_repositories.close_mongo()
        spider.logger.info('Close Spider')
