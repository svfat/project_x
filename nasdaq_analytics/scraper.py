#!/usr/bin/env python
from tempfile import NamedTemporaryFile

from historical_prices import get_historical_prices, save_historical_prices

if __name__ == '__main__':
    with NamedTemporaryFile() as historical_prices_file:
        get_historical_prices(historical_prices_file)
        save_historical_prices(historical_prices_file)
