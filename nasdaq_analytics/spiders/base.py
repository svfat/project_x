""""""
from typing import List

from scrapy.spiders import Spider


class BaseSpider(Spider):
    symbols: List[str]

    def __init__(self, symbols: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.symbols = symbols
