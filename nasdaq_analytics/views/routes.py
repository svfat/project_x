import logging
from datetime import date, datetime
from typing import Dict, Any

from dateutil.relativedelta import relativedelta
from flask import abort, redirect, url_for, request
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import joinedload

from ..common import canonize_symbol
from ..db import session, Ticker, InsiderTrade, HistoricalPrice, Insider
from .helpers import views_helper
from .schemas import *


@views_helper.route(
    '/',
    template_name='index.html',
    schema=tickers_list_schema,
    parameters=[],
    description='Получить список всех акций, доступных в базе данных.',
)
def index() -> Dict[str, Any]:
    return {
        'tickers': [
            ticker.symbol
            for ticker in session.query(Ticker).order_by(Ticker.symbol).all()
        ]
    }


@views_helper.route(
    '/<string:symbol>',
    template_name='historical_prices.html',
    schema=historical_prices_schema,
    parameters=[
        {
            'name': 'symbol',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'string',
            },
        },
    ],
    description='Получить цены на акцию за 3 месяца.',
)
def historical_prices(symbol: str) -> Dict[str, Any]:
    canonical_symbol = canonize_symbol(symbol)
    if symbol != canonical_symbol:
        abort(redirect(url_for(request.endpoint, symbol=canonical_symbol), 301))

    ticker = session.query(Ticker).filter(
        Ticker.symbol == symbol
    ).first()

    if ticker is None:
        abort(404)

    return {
        'ticker': ticker.symbol,
        'historical_prices': [
            {
                'date': historical_price.date.isoformat(),
                'open': historical_price.open,
                'high': historical_price.high,
                'low': historical_price.low,
                'close': historical_price.close,
                'volume': historical_price.volume,
            }
            for historical_price in ticker.historical_price_ordered_by_date.filter(
                HistoricalPrice.date >= date.today() - relativedelta(months=3)
            )
        ]
    }


@views_helper.route(
    '/<string:symbol>/insider',
    template_name='insider_trades.html',
    schema=insider_trades_schema,
    parameters=[
        {
            'name': 'symbol',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'string',
            },
        },
    ],
    description='Получить данные о торгах инсайдеров.',
)
def insider_trades(symbol: str) -> Dict[str, Any]:
    canonical_symbol = canonize_symbol(symbol)
    if symbol != canonical_symbol:
        abort(redirect(url_for(request.endpoint, symbol=canonical_symbol), 301))

    ticker = session.query(Ticker).options(
        joinedload(Ticker.insider_trades_ordered_by_date, InsiderTrade.insider),
    ).filter(
        Ticker.symbol == symbol
    ).first()

    return {
        'ticker': ticker.symbol,
        'insider_trades': [
            {
                'insider_name': insider_trade.insider.name,
                'relation': insider_trade.relation,
                'last_date': insider_trade.last_date,
                'transaction_type': insider_trade.transaction_type,
                'owner_type': insider_trade.owner_type,
                'shares_traded': insider_trade.shares_traded,
                'last_price': insider_trade.last_price,
                'shares_held': insider_trade.shares_held,
            }
            for insider_trade in ticker.insider_trades_ordered_by_date
        ]
    }


@views_helper.route(
    '/<string:symbol>/insider/<string:insider_name>',
    template_name='insider_trades_for_insider.html',
    schema=insider_trades_schema,
    parameters=[
        {
            'name': 'symbol',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'string',
            },
        },
        {
            'name': 'insider_name',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'string',
            },
        },
    ],
    description='Получить данные о торгах инсайдеров.',
)
def insider_trades_by_insider_name(symbol: str, insider_name: str) -> Dict[str, Any]:
    canonical_symbol = canonize_symbol(symbol)
    if symbol != canonical_symbol:
        abort(redirect(url_for(request.endpoint, symbol=canonical_symbol), 301))

    ticker = session.query(Ticker).filter(
        Ticker.symbol == symbol
    ).first()

    if ticker is None:
        abort(404)

    query = session.query(InsiderTrade).options(
        joinedload(InsiderTrade.insider),
    ).filter(
        InsiderTrade.ticker_id == Ticker.id,
        InsiderTrade.insider.has(name=insider_name),
    ).order_by(InsiderTrade.last_date.desc())

    return {
        'ticker': ticker.symbol,
        'insider_trades': [
            {
                'insider_name': insider_trade.insider.name,
                'relation': insider_trade.relation,
                'last_date': insider_trade.last_date,
                'transaction_type': insider_trade.transaction_type,
                'owner_type': insider_trade.owner_type,
                'shares_traded': insider_trade.shares_traded,
                'last_price': insider_trade.last_price,
                'shares_held': insider_trade.shares_held,
            }
            for insider_trade in query.all()
        ]
    }


@views_helper.route(
    '/<string:symbol>/analytics',
    template_name='analytics.html',
    schema=analytics_schema,
    parameters=[
        {
            'name': 'symbol',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'string',
            },
        },
        {
            'name': 'date_from',
            'in': 'query',
            'required': False,
            'schema': {
                'type': 'string',
                'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
            },
        },
        {
            'name': 'date_to',
            'in': 'query',
            'required': False,
            'schema': {
                'type': 'string',
                'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
            },
        },
    ],
    description='Получить аналитические данные об исторических ценах.',
)
def analytics(symbol: str):
    canonical_symbol = canonize_symbol(symbol)
    if symbol != canonical_symbol:
        abort(redirect(url_for(request.endpoint, symbol=canonical_symbol), 301))

    ticker = session.query(Ticker).filter(
        Ticker.symbol == symbol
    ).first()

    if ticker is None:
        abort(404)

    date_from_arg = request.args.get('date_from', '')
    date_to_arg = request.args.get('date_to', '')

    try:
        date_from = datetime.strptime(date_from_arg, '%Y-%m-%d').date()
    except ValueError:
        date_from = None

    try:
        date_to = datetime.strptime(date_to_arg, '%Y-%m-%d').date()
    except ValueError:
        date_to = None

    if date_from is not None and date_to is not None and date_from > date_to:
        date_to, date_from = date_from, date_to

    historical_price_from_query = session.query(HistoricalPrice).filter(
        HistoricalPrice.ticker_id == ticker.id
    )
    if date_from is not None:
        historical_price_from_query = historical_price_from_query.order_by(
            asc(func.abs(HistoricalPrice.date - date_from)),
        )
    else:
        historical_price_from_query = historical_price_from_query.order_by(
            asc(HistoricalPrice.date),
        )
    historical_price_from = historical_price_from_query.first()
    logging.error(historical_price_from_query)

    historical_price_to_query = session.query(HistoricalPrice).filter(
        HistoricalPrice.ticker_id == ticker.id
    )
    if date_to is not None:
        historical_price_to_query = historical_price_to_query.order_by(
            asc(func.abs(HistoricalPrice.date - date_to)),
        )
    else:
        historical_price_to_query = historical_price_to_query.order_by(
            desc(HistoricalPrice.date),
        )
    historical_price_to = historical_price_to_query.first()
    logging.error(historical_price_to_query)

    if historical_price_from is None or historical_price_to is None:
        abort(404)

    date_from_iso = historical_price_from.date.isoformat()
    date_to_iso = historical_price_to.date.isoformat()

    if date_from_iso != date_from_arg or date_to_iso != date_to_arg:
        abort(redirect(url_for(
            request.endpoint,
            symbol=canonical_symbol,
            date_from=date_from_iso,
            date_to=date_to_iso,
        ), 302))

    return {
        'ticker': ticker.symbol,
        'date_from': date_from_iso,
        'date_to': date_to_iso,
        'open_delta': historical_price_to.open - historical_price_from.open,
        'high_delta': historical_price_to.high - historical_price_from.high,
        'low_delta': historical_price_to.low - historical_price_from.low,
        'close_delta': historical_price_to.close - historical_price_from.close,
    }
