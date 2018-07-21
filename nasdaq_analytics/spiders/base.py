"""Модуль, содержащий базовый класс для "пауков" Scrapy."""
from typing import List

from scrapy.spiders import Spider


class BaseSpider(Spider):
    """Базовый класс для "пауков", содержащий общие методы."""

    #: список "символов" (наваний акций)
    symbols: List[str]
    #: разрешённые домены
    allowed_domains = ['nasdaq.com', 'www.nasdaq.com']

    def __init__(self, symbols: List[str], *args, **kwargs) -> None:
        """Инициализация, сохраняем список "символов" (наваний акций) в свойстве объекта.

        :param symbols: список "символов" (наваний акций)
        :param args: аргументы, передаются в `__init__` родительского класса
        :param kwargs: аргументы, передаются в `__init__` родительского класса
        """
        super().__init__(*args, **kwargs)
        self.symbols = symbols
