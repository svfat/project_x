from typing import Dict, Any

from flask import abort, redirect, url_for, request
from sqlalchemy.orm import joinedload

from common import canonize_symbol
from db import session, Ticker, InsiderTrade, Insider
from .helpers import views_helper


@views_helper.route('/', template_name='index.html', schema={
    'type': 'object',
    'properties': {
        'tickers': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
    },
}, parameters=[], description='Получить список всех акций, доступных в базе данных.')
def index() -> Dict[str, Any]:
    return {
        'tickers': [
            ticker.symbol
            for ticker in session.query(Ticker).order_by(Ticker.symbol).all()
        ]
    }


@views_helper.route('/<string:symbol>', template_name='historical_prices.html', schema={
    'type': 'object',
    'properties': {
        'ticker': {
            'type': 'string',
        },
        'historical_prices': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'date': {
                        'type': 'string',
                    },
                    'open': {
                        'type': 'number',
                    },
                    'high': {
                        'type': 'number',
                    },
                    'low': {
                        'type': 'number',
                    },
                    'close': {
                        'type': 'number',
                    },
                    'volume': {
                        'type': 'integer',
                    },
                },
            },
        },
    },
}, parameters=[
    {
        'name': 'symbol',
        'in': 'path',
        'required': True,
        'schema': {
            'type': 'string',
        },
    },
], description='Получить цены на акцию за 3 месяца.')
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


@views_helper.route('/<string:symbol>/insider', template_name='insider_trades.html', schema={
    'type': 'object',
    'properties': {
        'ticker': {
            'type': 'string',
        },
        'insider_trades': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'insider_name': {
                        'type': 'string',
                    },
                    'relation': {
                        'type': 'string',
                    },
                    'last_date': {
                        'type': 'string',
                    },
                    'transaction_type': {
                        'type': 'string',
                    },
                    'owner_type': {
                        'type': 'string',
                    },
                    'shares_traded': {
                        'type': 'integer',
                    },
                    'last_price': {
                        'type': 'number',
                    },
                    'shares_held': {
                        'type': 'integer',
                    },

                },
            },
        },
    },
}, parameters=[
    {
        'name': 'symbol',
        'in': 'path',
        'required': True,
        'schema': {
            'type': 'string',
        },
    },
], description='Получить данные о торгах инсайдеров.')
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
