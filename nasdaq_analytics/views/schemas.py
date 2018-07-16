tickers_list_schema = {
    'type': 'object',
    'properties': {
        'tickers': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
    },
}

historical_prices_schema = {
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
}

insider_trades_schema = {
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
}
