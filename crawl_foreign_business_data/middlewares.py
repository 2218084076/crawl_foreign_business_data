"""Middlewares"""

import random

from scrapy import Request, Spider, signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from crawl_foreign_business_data.repositories.redis_repositories import \
    RedisRepositories

redis_repositories = RedisRepositories()


class CrawlForeignBusinessDataSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlForeignBusinessDataDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider: Spider):
        """
        spider_opened
        :param spider:
        :return:
        """
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlForeignBusinessDataRetryMiddleware(RetryMiddleware):
    """CrawlForeign Business Data Retry Middleware"""

    def process_response(self, request, response, spider):
        """
        process_response
        :param request:
        :param response:
        :param spider:
        :return:
        """
        if request.meta.get('dont_retry', False):
            return response

        if (response.status not in self.retry_http_codes and
                response.status != '200'):
            redis_repositories.rewrite(spider.name, request.url)

        if response.status in self.retry_http_codes:
            reason = response.status
            spider.logger.info(f'retry_http_code {response.status}')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        """
        process_exception
        :param request:
        :param exception:
        :param spider:
        :return:
        """

        if (
                isinstance(exception, self.EXCEPTIONS_TO_RETRY)
                and not request.meta.get('dont_retry', False)
        ):
            redis_repositories.rewrite(spider.name, request.url)
            return self._retry(request, exception, spider)


class CrawlForeignBusinessDataProxyMiddleware(object):
    """Spain Proxy Middleware"""

    def __init__(self, proxy):
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        """
        from_crawler
        :param crawler:
        :return:
        """
        proxy_ip = crawler.settings.get('PROXY')

        return cls(proxy_ip)

    def process_request(self, request: Request, spider: Spider):
        """
        process_request
        :param request:
        :param spider:
        :return:
        """

        if request.url.startswith('http://'):
            request.meta['proxy'] = f'http://{self.proxy}'
            spider.logger.info(f'proxy {self.proxy}')

        elif request.url.startswith('https://'):
            request.meta['proxy'] = f'https://{self.proxy}'
            spider.logger.info(f'proxy {self.proxy}')


class DefineHeadersMiddleware:
    """
    Define Headers Middleware
    """

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        """
        from_crawler
        :param crawler:
        :return:
        """

        return cls(user_agent=crawler.settings.get('USER_AGENT'))

    def process_request(self, request, spider):
        """
        process_request
        :param request:
        :param spider:
        :return:
        """
        spider_name = spider.name
        spider.logger.info(f'spider.name: {spider_name}')
        if 'Russia' in spider_name:
            request.headers['User-Agent'] = random.choice(self.user_agent.get('RUSSIA'))

        if 'Spain' in spider_name:
            request.headers['User-Agent'] = random.choice(self.user_agent.get('SPAIN'))

        if 'Other' in spider.name:
            request.headers['User-Agent'] = random.choice(self.user_agent.get('OTHER_COUNTRY'))
