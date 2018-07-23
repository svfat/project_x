"""Модуль, содержащий "паука" для сбора информации о торгах инсайдеров."""
import logging
import re
from datetime import datetime
from typing import NamedTuple, Optional, Match, Iterator, Union, Dict

from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from .base import BaseSpider
from .common import only_numbers

#: сколько страниц нужно спарсить
MAX_PAGE: int = 10


class RawRow(NamedTuple):
    """Именнованный кортеж для хранения строки таблицы в "сыром виде"."""
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
        """Метод, получающий из селектора именнованный кортеж с нужными нам значениями.

        :param selector: селектор, из которого можно получить строку таблицы
        :return: результат парсинга этой строки таблицы
        """
        insider_name: Optional[str] = selector.xpath('./td[1]/a/text()').extract_first()
        insider_link: Optional[str] = selector.xpath('./td[1]/a/@href').extract_first()
        insider_id: Optional[str] = insider_link.strip('/').split('/')[-1] if insider_link else None

        if insider_id is None or insider_name is None:
            raise ValueError()

        relation, last_date, transaction_type, owner_type, shares_traded, last_price, shares_held, *_ = (
            td.xpath('./text()').extract_first()
            for td in selector.xpath('./td')[1:8]
        )

        return RawRow(
            insider_name,
            insider_id,
            relation, last_date, transaction_type, owner_type, shares_traded, last_price, shares_held,
            symbol,
        )


class ParsedRow(NamedTuple):
    """Именнованный кортеж, для хранения строки таблицы в распарсенном виде."""
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
        """Метод, получающий из "сырых" данных обработанные.

        :param raw_row: именнованный кортеж с нужными нам данными в сыром виде
        :param symbol: название акции ("символ"), к которым относятся эти данные
        :return: именнованный кортеж с нужными данными в нужном формате, готовыми к отправке "наружу"
        """
        return ParsedRow(
            insider_name=raw_row.insider_name,
            insider_id=raw_row.insider_id,
            relation=raw_row.relation,
            last_date=datetime.strptime(raw_row.last_date.strip(), '%m/%d/%Y').strftime('%Y-%m-%d'),
            transaction_type=raw_row.transaction_type,
            owner_type=raw_row.owner_type,
            shares_traded=(
                int(only_numbers.sub('', raw_row.shares_traded)) if raw_row.shares_traded is not None else None
            ),
            last_price=float(raw_row.last_price) if raw_row.last_price is not None else None,
            shares_held=int(only_numbers.sub('', raw_row.shares_held)) if raw_row.shares_held is not None else None,
            symbol=raw_row.symbol,
        )

    def as_dict(self) -> Dict:
        """Прокси для приватного метода `_asdict`.

        :return: именнованный кортеж, преобразованный в словарь
        """
        return self._asdict()


class InsiderTradesSpider(BaseSpider):
    """"Паук", для получения данных о торгах инсайдеров."""
    name = 'insider_trades'

    def start_requests(self) -> Iterator[Request]:
        """Итератор по первоначальным запросам.

        Делает запрос к странице с историческими ценам для каждой переданной акции.
        """
        for symbol in self.symbols:
            yield Request(f'https://www.nasdaq.com/symbol/{symbol.lower()}/insider-trades', meta={'symbol': symbol})

    def parse(self, response: Response) -> Iterator[Union[Request, Dict]]:
        """Обработчик http ответа от сайта.

        Парсит таблицы с данными и делает запросы к следующим страницам.

        :param response: ответ, получаемый из Scrapy
        :return: итератор по словарям с результатами парсинга и по запросам к следующим страницам
        """
        symbol = response.meta['symbol']
        link_extractor = LinkExtractor(
            allow=rf'https://www\.nasdaq\.com/symbol/{symbol.lower()}/insider-trades\?page=\d+'
        )
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
