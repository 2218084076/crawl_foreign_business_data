"""Russia pipeline"""
from scrapy import Spider

from crawl_foreign_business_data.pipelines.base_pipeline import BasePipeline
from crawl_foreign_business_data.repositories.mongo_repositories import \
    MongoRepositories
from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories

redis_repositories = RedisRepositories()
mongo_repositories = MongoRepositories('localhost:27017', 'BusinessInfos')


class RussiaPipeline(BasePipeline):
    """Russia Pipeline"""

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
            for page in page_list:
                redis_repositories.write_to_redis(spider.name, page)

        if 'company_list' in item:
            company_list = dict(item).get('company_list')
            for company in company_list:
                redis_repositories.write_to_redis(spider.name, company)

        if 'russia_company_infos' in item:
            item_content = item.get('russia_company_infos')
            mongo_repositories.collection_name = 'Russia Company Info'
            mongo_repositories.increase(item_content)
            spider.logger.info(f'save {item} to mongo')
        return item
