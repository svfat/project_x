""""""
from typing import List

from scrapy.spiders import Spider


class BaseSpider(Spider):
    symbols: List[str]
    allowed_domains = ['nasdaq.com', 'www.nasdaq.com']

    def __init__(self, symbols: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.symbols = symbols
