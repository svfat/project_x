import sys
from io import FileIO

from scrapy.crawler import CrawlerProcess

# from common import load_tickers
from config import Config
from spiders import InsiderTradesSpider


def get_insider_trades(tmp_file: FileIO):
    process = CrawlerProcess({
        'CONCURRENT_REQUESTS': Config.CONCURRENT_REQUESTS,
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': f'stdout:',
    })

    process.crawl(InsiderTradesSpider, ['AAPL', 'MSFT', 'CVX'])
    process.start()


if __name__ == '__main__':
    get_insider_trades(sys.stdout)
