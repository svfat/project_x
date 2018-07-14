import re
from typing import List

from config import Config


def canonical_symbol(symbol: str) -> str:
    return re.sub(r'[^A-Z]', '', symbol.upper())


def load_tickers_file() -> List[str]:
    with open(Config.TICKERS_FILE, 'r') as tickers_file:
        return [
            canonical_symbol(line)
            for line in tickers_file.readlines()
        ]