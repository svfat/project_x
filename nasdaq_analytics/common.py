import re
from typing import Dict, Iterable, List
from uuid import UUID

from sqlalchemy.dialects import postgresql

from config import Config
from db import session, Ticker


def canonical_symbol(symbol: str) -> str:
    return re.sub(r'[^A-Z]', '', symbol.upper())


def load_tickers() -> List[str]:
    with open(Config.TICKERS_FILE, 'r') as tickers_file:
        return [
            canonical_symbol(line)
            for line in tickers_file.readlines()
        ]

def get_ticker_uuids(symbols: Iterable[str]) -> Dict[str, UUID]:
    for symbol in symbols:
        session.execute(
            postgresql.insert(Ticker.__table__).values(
                symbol=symbol
            ).on_conflict_do_nothing()
        )

    return {
        ticker.symbol: ticker.id
        for ticker in session.query(Ticker).all()
    }
