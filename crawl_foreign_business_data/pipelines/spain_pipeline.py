from repositories.mongo_repositories import MongoRepositories
from repositories.redis_repositories import RedisRepositories
from scrapy import Spider

redis_repositories = RedisRepositories()
mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class SpainPipeline:

    def open_spider(self, spider):
        mongo_repositories.open_mongo()
        spider.logger.info('Open Spider')

    def close_spider(self, spider):
        mongo_repositories.close_mongo()
        spider.logger.info('Close Spider')

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
                        redis_repositories.write_to_redis('Spain_city', i)
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
                        redis_repositories.write_to_redis('Spain_company_links', link)

                    if 'PgNum' in link:
                        redis_repositories.write_to_redis('Spain_city', link)
                    else:
                        spider.logger.debug('"%s" does not meet the rules!' % link)
                except AttributeError:
                    spider.logger.debug('"%s" does not meet the rules!' % link)

        if 'spain_company_infos' in item:
            item_content = item.get('spain_company_infos')
            mongo_repositories.increase(item_content)
            spider.logger.info('save %s to mongo' % item)
