from typing import Dict, List, Iterable, Any, NamedTuple
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from common import canonize_symbol
from . import Base, session


class Ticker(Base):  # type: ignore
    __tablename__ = 'ticker'

    historical_price_ordered_by_date = relationship(
        'HistoricalPrice',
        order_by='desc(HistoricalPrice.date)',
        lazy='dynamic',
    )
    insider_trades_ordered_by_date = relationship('InsiderTrade', order_by='desc(InsiderTrade.last_date)')

    @staticmethod
    def insert_tickers(symbols: Iterable[str]) -> None:
        for symbol in symbols:
            session.execute(
                postgresql.insert(Ticker.__table__).values(
                    symbol=canonize_symbol(symbol)
                ).on_conflict_do_nothing()
            )

    @staticmethod
    def get_uuids_by_symbol() -> Dict[str, UUID]:
        return {
            ticker.symbol: ticker.id
            for ticker in session.query(Ticker).all()
        }


class HistoricalPrice(Base):  # type: ignore
    __tablename__ = 'historical_price'

    @staticmethod
    def bulk_insert(historical_prices: List[Dict[str, Any]]):
        session.execute(
            postgresql.insert(HistoricalPrice.__table__).on_conflict_do_nothing(),
            historical_prices,
        )


class InsiderTuple(NamedTuple):
    id: str
    name: str


class Insider(Base):  # type: ignore
    __tablename__ = 'insider'

    @staticmethod
    def insert_insiders(insiders: Iterable[InsiderTuple]):
        for insider in insiders:
            session.execute(
                postgresql.insert(Insider.__table__).values(
                    id=insider.id,
                    name=insider.name,
                ).on_conflict_do_nothing()
            )


class InsiderTrade(Base):  # type: ignore
    __tablename__ = 'insider_trade'

    @staticmethod
    def bulk_insert(insider_trades: List[Dict[str, Any]]):
        session.execute(
            postgresql.insert(InsiderTrade.__table__).on_conflict_do_nothing(),
            insider_trades,
        )
