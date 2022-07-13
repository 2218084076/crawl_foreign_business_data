from scrapy import Spider

from crawl_foreign_business_data.pipelines.base_pipeline import BasePipeline
from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories

redis_repositories = RedisRepositories()
mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class OtherPipeline(BasePipeline):

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
