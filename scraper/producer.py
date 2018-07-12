import os

from scrapy.crawler import CrawlerProcess

from spiders import HistoricalPricesSpider

process = CrawlerProcess({
    'CONCURRENT_REQUESTS': os.getenv('CONCURRENT_REQUESTS', 16),
    'FEED_FORMAT': 'jsonlines',
    'FEED_URI': 'stdout:',
})

process.crawl(HistoricalPricesSpider, ['AAPL', 'MSFT'])
process.start()
