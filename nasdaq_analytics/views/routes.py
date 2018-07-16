from typing import Dict, Any

from flask import abort, redirect, url_for, request
from sqlalchemy.orm import joinedload

from common import canonize_symbol
from db import session, Ticker, InsiderTrade
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

    ticker = session.query(Ticker).options(
        joinedload(Ticker.historical_price_ordered_by_date)
    ).filter(
        Ticker.symbol == symbol
    ).first()
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
            for historical_price in ticker.historical_price_ordered_by_date
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
