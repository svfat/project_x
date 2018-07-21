"""Модуль, содержащий схемы в формате jsonschema"""

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
        'insider_name': {
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

analytics_schema = {
    'type': 'object',
    'properties': {
        'ticker': {
            'type': 'string',
        },
        'date_from': {
            'type': 'string',
            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
        },
        'date_to': {
            'type': 'string',
            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
        },
        'open_delta': {
            'type': 'number',
        },
        'high_delta': {
            'type': 'number',
        },
        'low_delta': {
            'type': 'number',
        },
        'close_delta': {
            'type': 'number',
        },
    },
}

types_enum = ['open', 'high', 'low', 'close']

delta_schema = {
    'type': 'object',
    'properties': {
        'ticker': {
            'type': 'string',
        },
        'min_duration': {
            'type': ['integer', 'null'],
        },
        'delta': {
            'type': ['number', 'null'],
        },
        'type': {
            'type': ['string', 'null'],
            'enum': types_enum,
        },
        'intervals': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'date_from': {
                        'type': 'string',
                        'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
                    },
                    'date_to': {
                        'type': 'string',
                        'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
                    },
                    'delta': {
                        'type': 'number',
                    },
                },
            },
        },
    },
}
