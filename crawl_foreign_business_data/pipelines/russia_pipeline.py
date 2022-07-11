from scrapy import Spider

from repositories.mongo_repositories import MongoRepositories
from repositories.redis_repositories import RedisRepositories

redis_repositories = RedisRepositories()
mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class RussiaPipeline:

    def open_spider(self, spider):
        mongo_repositories.open_mongo()
        spider.logger.info('Open Spider')

    def close_spider(self, spider):
        mongo_repositories.close_mongo()
        spider.logger.info('Close Spider')

    def process_item(self, item, spider: Spider):
        """
        russia pipeline
        :param item:
        :param spider:
        :return:
        """
        if 'index_list' in item:
            index_list = dict(item).get('index_list')
            for i in index_list:
                redis_repositories.write_to_redis(spider.name, i)

            spider.logger.info('Russia index list')

        if 'page_list' in item:
            page_list = dict(item).get('page_list')
            for p in page_list:
                redis_repositories.write_to_redis(spider.name, p)

        if 'company_list' in item:
            company_list = dict(item).get('company_list')
            for company in company_list:
                redis_repositories.write_to_redis(spider.name, company)

        if 'russia_company_infos' in item:
            item_content = item.get('russia_company_infos')
            mongo_repositories.collection_name = 'Russia Company Info'
            mongo_repositories.increase(item_content)
            spider.logger.info('save %s to mongo' % item)
        return item
