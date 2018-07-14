""""""
from typing import List

from scrapy.spiders import Spider


class BaseSpider(Spider):
    ticker: List[str]

    def __init__(self, ticker: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ticker = ticker
