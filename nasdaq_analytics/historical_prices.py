import json
from io import FileIO
from typing import Dict
from uuid import UUID

from more_itertools import chunked
from scrapy.crawler import CrawlerProcess
from sqlalchemy.dialects import postgresql

from common import get_ticker_uuids
from config import Config
from db import session, HistoricalPrice
from spiders import HistoricalPricesSpider


def get_historical_prices(tmp_file: FileIO):
    process = CrawlerProcess({
        'CONCURRENT_REQUESTS': Config.CONCURRENT_REQUESTS,
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': f'file://{tmp_file.name}',
    })

    process.crawl(HistoricalPricesSpider, ['AAPL', 'MSFT'])
    process.start()


def save_historical_prices(tmp_file: FileIO):
    for chunk in chunked(tmp_file.readlines(), Config.CHUNK_SIZE):
        historical_prices = [json.loads(line) for line in chunk]
        symbols = set(historical_price['symbol'] for historical_price in historical_prices)

        symbol_to_uuid: Dict[str, UUID] = get_ticker_uuids(symbols)

        session.execute(
            postgresql.insert(HistoricalPrice.__table__).on_conflict_do_nothing(),
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
