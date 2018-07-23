"""Модели."""
from typing import Dict, List, Iterable, Any, NamedTuple
from uuid import UUID

from sqlalchemy import func, text
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.dialects import postgresql

from common import canonize_symbol
from . import Base, session


class Ticker(Base):  # type: ignore
    """Акция."""

    __tablename__ = 'ticker'

    #: исторические цены на эту акцию, отсортированные по дате
    historical_price_ordered_by_date = relationship(
        'HistoricalPrice',
        order_by='desc(HistoricalPrice.date)',
        lazy='dynamic',
    )
    #: инсайдерские торги, связанные с этой акцией, отсортированные по дате
    insider_trades_ordered_by_date = relationship('InsiderTrade', order_by='desc(InsiderTrade.last_date)')

    @staticmethod
    def insert_tickers(symbols: Iterable[str]) -> None:
        """Вставить акции в базу данных, не делать ничего, если такая акция уже есть.

        :param symbols: названия акций (CVX, AAPL, GOOG, etc...)
        """
        for symbol in symbols:
            session.execute(
                postgresql.insert(Ticker.__table__).values(
                    symbol=canonize_symbol(symbol)
                ).on_conflict_do_nothing()
            )

    @staticmethod
    def get_uuids_by_symbol() -> Dict[str, UUID]:
        """Получить соответствие названий акций и их внутренних идентификаторов.

        :return: словарь, содержащий соответствие названий акций и их внутренних идентификаторов
        """
        return {
            ticker.symbol: ticker.id
            for ticker in session.query(Ticker).all()
        }


class HistoricalPrice(Base):  # type: ignore
    """Исторические цены на акцию."""

    __tablename__ = 'historical_price'

    @staticmethod
    def bulk_insert(historical_prices: List[Dict[str, Any]]):
        """Массовая вставка исторических цен в базу, с игнорированием конфликтов.

        :param historical_prices: список словарей, содержащих исторические цены
        """
        session.execute(
            postgresql.insert(HistoricalPrice.__table__).on_conflict_do_nothing(),
            historical_prices,
        )

    @staticmethod
    def get_intervals(ticker: Ticker, attribute_name: str, min_delta: float):
        """Получить список минимальных интервалов, когда цена на акцию изменилась более чем на min_delta.

        :param ticker: акция
        :param attribute_name: тип цены (open/high/low/close)
        :param min_delta: минимальное изменение цены акции
        """
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
            historical_price_from.ticker_id == ticker.id,
            historical_price_to.ticker_id == ticker.id,
            historical_price_from.ticker_id == historical_price_to.ticker_id,
            historical_price_from.date < historical_price_to.date,
            func.abs(
                getattr(historical_price_from, attribute_name) - getattr(historical_price_to, attribute_name)
            ) > min_delta,
        ).order_by(historical_price_from.date)

        return session.query(
            intervals_with_delta.subquery('intervals_with_delta')
        ).filter(
            text('duration = min_duration')
        ).all()


class InsiderTuple(NamedTuple):
    """Именнованный кортеж, содержащий данные об инсайдере."""

    id: str
    name: str


class Insider(Base):  # type: ignore
    """Инсайдер."""

    __tablename__ = 'insider'

    @staticmethod
    def insert_insiders(insiders: Iterable[InsiderTuple]) -> None:
        """Сохранить инсайдеров в базу данных.

        :param insiders: итератор по инсайдерам
        """
        for insider in insiders:
            session.execute(
                postgresql.insert(Insider.__table__).values(
                    id=insider.id,
                    name=insider.name,
                ).on_conflict_do_nothing()
            )


class InsiderTrade(Base):  # type: ignore
    """Данные об инсайдерских торгах."""

    __tablename__ = 'insider_trade'

    @staticmethod
    def bulk_insert(insider_trades: List[Dict[str, Any]]) -> None:
        """Массовая вставка данных о торгах инсайдеров в базу, с игнорированием конфликтов.

        :param insider_trades: список словарей, содержащих данные о торгах инсайдеров
        """
        session.execute(
            postgresql.insert(InsiderTrade.__table__).on_conflict_do_nothing(),
            insider_trades,
        )
