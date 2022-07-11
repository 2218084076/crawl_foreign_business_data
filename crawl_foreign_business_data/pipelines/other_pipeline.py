from repositories.mongo_repositories import MongoRepositories
from repositories.redis_repositories import RedisRepositories
from scrapy import Spider

redis_repositories = RedisRepositories()
mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class OtherPipeline:

    def open_spider(self, spider):
        mongo_repositories.open_mongo()
        spider.logger.info('Open Spider')

    def close_spider(self, spider):
        mongo_repositories.close_mongo()
        spider.logger.info('Close Spider')

    def process_item(self, item: dict, spider: Spider):
        """
        other pipeline
        :param item:
        :param spider:
        :return:
        """
        if 'index' in item:
            for url in dict(item).get('index'):
                if 'nzlbusiness' in url:
                    if 'browse' in url:
                        redis_repositories.write_to_redis('CrawlOtherCountryIndex', url)
                    if 'company' in url:
                        redis_repositories.write_to_redis('CrawlOtherCompanyLinks', url)

                if 'aus61business' in url:
                    if 'browse' in url:
                        redis_repositories.write_to_redis('CrawlOtherCountryIndex', url)

                    if 'company' in url:
                        redis_repositories.write_to_redis('CrawlOtherCompanyLinks', url)

                else:
                    spider.logger.debug('"%s" does not meet the rules!' % url)

        if 'company_info' in item:

            company_info = dict(item).get('company_info')

            if 'NewZealand' in company_info.get('country'):
                mongo_repositories.collection_name = 'NewZealand'
                mongo_repositories.increase(company_info)
                spider.logger.info('save %s to mongo' % item)

            if 'Australia' in company_info.get('country'):
                mongo_repositories.collection_name = 'Australia'
                mongo_repositories.increase(company_info)
                spider.logger.info('save %s to mongo' % item)
