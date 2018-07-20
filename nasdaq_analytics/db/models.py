from typing import Dict, List, Iterable, Any, NamedTuple
from uuid import UUID

from sqlalchemy import func, text
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.dialects import postgresql

from ..common import canonize_symbol
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

    @staticmethod
    def get_intervals(attribute_name: str, min_delta: float):
        historical_price_from = aliased(HistoricalPrice, name='historical_price_from')
        historical_price_to = aliased(HistoricalPrice, name='historical_price_to')

        # подзапрос, получающий все интервалы, с дельтой больше либо равной заданной
        intervals_with_delta = session.query(
            historical_price_from.date.label('date_from'),
            historical_price_to.date.label('date_to'),
            (
                getattr(historical_price_to, attribute_name) - getattr(historical_price_from, attribute_name)
            ).label('delta'),
            (historical_price_to.date - historical_price_from.date).label('duration'),
            func.min(historical_price_to.date - historical_price_from.date).over().label('min_duration'),
        ).filter(
            historical_price_from.ticker_id == historical_price_to.ticker_id,
            historical_price_from.date < historical_price_to.date,
            func.abs(
                getattr(historical_price_from, attribute_name) - getattr(historical_price_to, attribute_name)
            ) >= min_delta,
        )

        return session.query(
            intervals_with_delta.subquery('intervals_with_delta')
        ).filter(
            text('duration = min_duration')
        ).all()


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
