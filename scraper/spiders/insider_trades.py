""""""
from .base import BaseSpider


class InsiderTradesSpider(BaseSpider):
    name = 'insider_trades'
    allowed_domains = 'nasdaq.com'

    def parse(self, response):
        pass
