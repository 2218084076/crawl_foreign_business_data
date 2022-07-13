from scrapy import Spider

from crawl_foreign_business_data.pipelines.base_pipeline import BasePipeline
from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories

redis_repositories = RedisRepositories()
mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class SpainPipeline(BasePipeline):

    def process_item(self, item: dict, spider: Spider):
        """
        Spain pipeline
        :param item:
        :param spider:
        :return:
        """
        if 'city' in item:
            city_list = dict(item).get('city')
            for i in city_list:
                try:
                    if 'provincia' in i or 'Actividad' in i:
                        redis_repositories.write_to_redis(spider.name, i)
                    else:
                        spider.logger.debug('"%s" does not meet the rules!' % i)
                except TypeError:
                    spider.logger.debug('"%s" does not exist' % i)
            spider.logger.info('Spain city list')

        # 保存公司主页链接
        if 'company_links' in item:
            company_links = dict(item).get('company_links')
            for link in company_links:
                try:
                    key = link.split('/').pop().split('.html')[0]
                    if key.isupper() and '-' in key:
                        redis_repositories.write_to_redis('SpainCrawlPageLink', link)

                    if 'PgNum' in link:
                        redis_repositories.write_to_redis('SpainCrawlCityIndex', link)
                    else:
                        spider.logger.debug('"%s" does not meet the rules!' % link)
                except AttributeError:
                    spider.logger.debug('"%s" does not meet the rules!' % link)

        if 'spain_company_infos' in item:
            item_content = item.get('spain_company_infos')
            mongo_repositories.increase(item_content)
            spider.logger.info('save %s to mongo' % item)

        return item
