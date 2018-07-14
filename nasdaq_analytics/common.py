from typing import Dict, Iterable
from uuid import UUID

from sqlalchemy.dialects import postgresql

from db import session, Ticker


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
