from typing import Dict, Iterable
from uuid import UUID

from sqlalchemy.dialects import postgresql

from db import session, Symbols


def get_symbols_uuids(symbols: Iterable[str]) -> Dict[str, UUID]:
    for symbol in symbols:
        session.execute(
            postgresql.insert(Symbols.__table__).values(
                symbol=symbol
            ).on_conflict_do_nothing()
        )

    return {
        symbol.symbol: symbol.id
        for symbol in session.query(Symbols).all()
    }
