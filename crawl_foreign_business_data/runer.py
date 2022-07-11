import logging

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.other_country_spider import (CrawlOtherCompanyLinks,
                                          CrawlOtherCountryIndex,
                                          ParseOtherCountryCompanyInfo)
from spiders.russia_spider import (ParseRussiaCompanyInfo, RussiaCrawlCategory,
                                   RussiaCrawlCompanyLinks, RussiaCrawlIndex)
from spiders.spain_spider import (ParseSpainCompanyInfo, SpainCrawlCityIndex,
                                  SpainCrawlPageLink)
from twisted.internet import reactor

logger = logging.getLogger(__name__)


def russia_runer():
    configure_logging()
    settings = get_project_settings()

    runner = CrawlerRunner(settings)

    runner.crawl(RussiaCrawlIndex)
    runner.crawl(RussiaCrawlCategory)
    runner.crawl(RussiaCrawlCompanyLinks)
    runner.crawl(ParseRussiaCompanyInfo)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


def spain_runer():
    configure_logging()
    settings = get_project_settings()

    runner = CrawlerRunner(settings)

    runner.crawl(SpainCrawlCityIndex)
    runner.crawl(SpainCrawlPageLink)
    runner.crawl(ParseSpainCompanyInfo)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


def australia_runer():
    configure_logging()
    settings = get_project_settings()

    runner = CrawlerRunner(settings)

    runner.crawl(CrawlOtherCountryIndex)
    runner.crawl(CrawlOtherCompanyLinks)
    runner.crawl(ParseOtherCountryCompanyInfo)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


russia_runer()
