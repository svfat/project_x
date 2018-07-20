"""Модуль, содержащий общие вспомогательные функции."""
import re
from typing import List

from .config import Config


def canonize_symbol(symbol: str) -> str:
    """Привести "ticker symbol" (краткое название акции) к каноничному виду.

    :param symbol: краткое название акции
    :return: краткое название акции, приведённое к верхнему регистру и отфильтрованное от лишних символов
    """
    return re.sub(r'[^A-Z]', '', symbol.upper())


def load_tickers_file() -> List[str]:
    """Загрузить файл, содержащий название акции в каждой строчке.

    :return: список называний акций в каноничном виде.
    """
    with open(Config.TICKERS_FILE, 'r') as tickers_file:
        return [
            canonize_symbol(line)
            for line in tickers_file.readlines()
        ]
