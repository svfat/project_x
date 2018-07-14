""""""
import logging
import re
from datetime import datetime
from typing import NamedTuple, Optional, Match

from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from .base import BaseSpider
from .common import only_numbers

MAX_PAGE: int = 10


class RawRow(NamedTuple):
    insider_name: str
    insider_id: str
    relation: Optional[str]
    last_date: str
    transaction_type: Optional[str]
    owner_type: Optional[str]
    shares_traded: Optional[str]
    last_price: Optional[str]
    shares_held: Optional[str]
    symbol: str

    @staticmethod
    def from_selector(selector: Selector, symbol: str) -> 'RawRow':
        insider_name: str = selector.xpath('./td[1]/a/text()').extract_first()
        insider_link: str = selector.xpath('./td[1]/a/@href').extract_first()
        insider_id: str = insider_link.strip('/').split('/')[-1] if insider_link else None

        return RawRow(
            insider_name,
            insider_id,
            *(
                td.xpath('./text()').extract_first()
                for td in selector.xpath('./td')[1:]
            ),
            symbol,
        )


class ParsedRow(NamedTuple):
    insider_name: str
    insider_id: str
    relation: Optional[str]
    last_date: str
    transaction_type: Optional[str]
    owner_type: Optional[str]
    shares_traded: Optional[int]
    last_price: Optional[float]
    shares_held: Optional[int]
    symbol: str

    @staticmethod
    def from_raw_row(raw_row: RawRow) -> 'ParsedRow':
        return ParsedRow(
            insider_name=raw_row.insider_name,
            insider_id=raw_row.insider_id,
            relation=raw_row.relation,
            last_date=datetime.strptime(raw_row.last_date.strip(), '%m/%d/%Y').strftime('%Y-%m-%d'),
            transaction_type=raw_row.transaction_type,
            owner_type=raw_row.owner_type,
            shares_traded=int(only_numbers.sub('', raw_row.shares_traded)) if raw_row.shares_traded is not None else None,
            last_price=float(raw_row.last_price) if raw_row.last_price is not None else None,
            shares_held=int(only_numbers.sub('', raw_row.shares_held)) if raw_row.shares_held is not None else None,
            symbol=raw_row.symbol,
        )

    def as_dict(self):
        return self._asdict()

class InsiderTradesSpider(BaseSpider):
    name = 'insider_trades'

    def start_requests(self):
        for symbol in self.symbols:
            yield Request(f'https://www.nasdaq.com/symbol/{symbol.lower()}/insider-trades', meta={'symbol': symbol})

    def parse(self, response: Response):
        symbol = response.meta['symbol']
        link_extractor = LinkExtractor(allow=rf'https://www\.nasdaq\.com/symbol/{symbol.lower()}/insider-trades\?page=\d+')
        link: Link
        for link in link_extractor.extract_links(response):
            match_page_number: Optional[Match] = re.search(r'page=(\d+)', link.url)
            if match_page_number is not None:
                page_number: int = int(match_page_number.group(1))
                if page_number <= MAX_PAGE:
                    yield Request(link.url, meta={'symbol': symbol})

        for row in response.xpath('//div[@id="content_main"]//div[@class="genTable"]/table[@class="certain-width"]/tr'):
            raw_row = RawRow.from_selector(row, symbol)
            try:
                yield ParsedRow.from_raw_row(raw_row).as_dict()
            except ValueError:
                logging.exception('Ошибка при парсинге строки таблицы с инсайдерскими сделками.')
