from typing import Dict, Any

from sqlalchemy.orm import joinedload

from db import session, Ticker, HistoricalPrice
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
})
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
                        'type': 'number',
                    },
                }
            },
        },
    },
})
def historical_prices(symbol: str) -> Dict[str, Any]:
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
