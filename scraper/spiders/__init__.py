"""Модуль, содержащий "пауков" для Scrapy."""
from .historical_prices import HistoricalPricesSpider
from .insider_trades import InsiderTradesSpider

__all__ = ['HistoricalPricesSpider', 'InsiderTradesSpider']
