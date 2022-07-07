# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo as pymongo
from itemadapter import ItemAdapter
from scrapy import Spider
from scrapy.crawler import Crawler

from crawl_foreign_business_data.repositories.redis_repositories import RedisRepositories

redis_repositories = RedisRepositories()


class CrawlForeignBusinessDataPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.db = None
        self.client = None
        self.collection_name = 'example'
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

    def open_spider(self, spider: Spider):
        """
        open spider
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        spider.logger.info('open spider')

    def close_spider(self, spider):
        """
        close spider
        :param spider:
        :return:
        """
        self.client.close()
        spider.logger.info('close spider')

    def process_item(self, item, spider: Spider):
        """
        process item
        :param item:
        :param spider:
        :return:
        """
        spider_name = spider.name
        item_content = dict(item)
        if 'Russia' in spider_name:
            self.collection_name = 'Russia'

            self.russia_pipeline(item_content, spider)

        if 'Spain' in spider_name:
            self.collection_name = 'Spain'

            self.spain_pipeline(item_content, spider)

        if 'Other' in spider.name:
            self.collection_name = 'OtherCountry'

            self.other_pipeline(item_content, spider)

        return item

    def russia_pipeline(self, item: dict, spider: Spider):
        """
        russia pipeline
        :param item:
        :param spider:
        :return:
        """
        if 'index_list' in item:
            index_list = dict(item).get('index_list')
            for i in index_list:
                redis_repositories.write_to_redis('Russia_index_list', i)

            spider.logger.info('Russia index list')

        if 'page_list' in item:
            page_list = dict(item).get('page_list')
            for p in page_list:
                redis_repositories.write_to_redis('Russia_pages', p)

        if 'company_list' in item:
            company_list = dict(item).get('company_list')
            for company in company_list:
                redis_repositories.write_to_redis('Russia_company_list', company)

        if 'russia_company_infos' in item:
            self.db[self.collection_name].insert_one(ItemAdapter(item.get('russia_company_infos')).asdict())
            spider.logger.info('save %s to mongo' % item)

    def spain_pipeline(self, item: dict, spider: Spider):
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
            company_info = dict(item).get('spain_company_infos')
            self.db[self.collection_name].insert_one(ItemAdapter(company_info).asdict())
            spider.logger.info('save %s to mongo' % company_info)

    def other_pipeline(self, item: dict, spider: Spider):
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
                        redis_repositories.write_to_redis('NewZealand_index', url)
                    if 'company' in url:
                        redis_repositories.write_to_redis('NewZealand_company_link', url)

                if 'aus61business' in url:
                    if 'browse' in url:
                        redis_repositories.write_to_redis('Australia_index', url)

                    if 'company' in url:
                        redis_repositories.write_to_redis('Australia_company_link', url)

                else:
                    spider.logger.debug('"%s" does not meet the rules!' % url)

        if 'company_info' in item:

            company_info = dict(item).get('company_info')

            if 'NewZealand' in company_info.get('country'):
                self.collection_name = 'NewZealand_business_info'
                self.db[self.collection_name].insert_one(ItemAdapter(company_info).asdict())
                spider.logger.info('save %s to mongo' % company_info)

            if 'Australia''NewZealand' in company_info.get('country'):
                self.collection_name = 'Australia_business_info'
                self.db[self.collection_name].insert_one(ItemAdapter(company_info).asdict())
                spider.logger.info('save %s to mongo' % company_info)
