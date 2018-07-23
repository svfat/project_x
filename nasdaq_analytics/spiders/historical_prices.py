"""Модуль, содержащий "паука" для сбора исторических цен."""
import logging
from datetime import datetime
from typing import NamedTuple, Dict, Iterator

from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.selector import Selector

from .base import BaseSpider
from .common import only_numbers


class RawRow(NamedTuple):
    """Именнованный кортеж для хранения строки таблицы в "сыром виде"."""
    date: str
    open: str
    high: str
    low: str
    close: str
    volume: str

    @staticmethod
    def from_selector(selector: Selector) -> 'RawRow':
        """Метод, получающий из селектора именнованный кортеж с нужными нам значениями.

        :param selector: селектор, из которого можно получить строку таблицы
        :return: результат парсинга этой строки таблицы
        """
        return RawRow(*selector.xpath('./td/text()').extract())


class ParsedRow(NamedTuple):
    """Именнованный кортеж, для хранения строки таблицы в распарсенном виде."""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    symbol: str

    @staticmethod
    def from_raw(raw_row: RawRow, symbol: str) -> 'ParsedRow':
        """Метод, получающий из "сырых" данных обработанные.

        :param raw_row: именнованный кортеж с нужными нам данными в сыром виде
        :param symbol: название акции ("символ"), к которым относятся эти данные
        :return: именнованный кортеж с нужными данными в нужном формате, готовыми к отправке "наружу"
        """
        return ParsedRow(
            date=datetime.strptime(raw_row.date.strip(), '%m/%d/%Y').strftime('%Y-%m-%d'),
            open=float(raw_row.open.strip()),
            high=float(raw_row.high.strip()),
            low=float(raw_row.low.strip()),
            close=float(raw_row.close.strip()),
            volume=int(only_numbers.sub('', raw_row.volume)),
            symbol=symbol,
        )

    def as_dict(self) -> Dict:
        """Прокси для приватного метода `_asdict`.

        :return: именнованный кортеж, преобразованный в словарь
        """
        return self._asdict()


class HistoricalPricesSpider(BaseSpider):
    """"Паук", для получения данных об исторических ценах."""
    name = 'historical_prices'

    def start_requests(self) -> Iterator[Request]:
        """Итератор по первоначальным запросам.

        Делает запрос к странице с историческими ценам для каждой переданной акции.
        """
        for symbol in self.symbols:
            yield Request(f'https://www.nasdaq.com/symbol/{symbol.lower()}/historical', meta={'symbol': symbol})

    def parse(self, response: Response) -> Iterator[Dict]:
        """Обработчик http ответа от сайта.

        :param response: ответ, получаемый из Scrapy
        :return: итератор по словарям с результатами парсинга таблицы с нужными данными
        """
        symbol = response.meta['symbol']
        for row in response.xpath('//div[@id="historicalContainer"]//table/tbody/tr'):
            raw_row = RawRow.from_selector(row)
            try:
                yield ParsedRow.from_raw(raw_row, symbol).as_dict()
            except ValueError:
                logging.exception('Ошибка при парсинге строки таблицы с историческими данными.')
