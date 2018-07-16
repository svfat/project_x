#!/usr/bin/env python
import json
from tempfile import NamedTemporaryFile
from typing import Dict, Set, IO
from uuid import UUID

from more_itertools import chunked
from scrapy.crawler import CrawlerProcess

from common import load_tickers_file
from config import Config
from db import session, HistoricalPrice, Ticker
from spiders import HistoricalPricesSpider


def get_historical_prices(tmp_file: IO):
    process = CrawlerProcess({
        'CONCURRENT_REQUESTS': Config.CONCURRENT_REQUESTS,
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': f'file://{tmp_file.name}',
    })

    process.crawl(HistoricalPricesSpider, load_tickers_file())
    process.start()


def save_historical_prices(tmp_file: IO):
    for chunk in chunked(tmp_file.readlines(), Config.CHUNK_SIZE):
        historical_prices = [json.loads(line) for line in chunk]

        symbols: Set[str] = set(historical_price['symbol'] for historical_price in historical_prices)
        Ticker.insert_tickers(symbols)
        symbol_to_uuid: Dict[str, UUID] = Ticker.get_uuids_by_symbol()

        HistoricalPrice.bulk_insert(
            [
                dict(
                    ticker_id=symbol_to_uuid[historical_price['symbol']],
                    **{
                        k: v
                        for k, v in historical_price.items() if k != 'symbol'
                    }
                )
                for historical_price in historical_prices
            ]
        )

        session.commit()


if __name__ == '__main__':
    with NamedTemporaryFile() as historical_prices_file:
        get_historical_prices(historical_prices_file)
        save_historical_prices(historical_prices_file)
