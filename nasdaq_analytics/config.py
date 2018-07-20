"""Модуль, содержащий конфигурационные параметры."""
from os import getenv


class Config:
    """Класс, содержащий конфигурационные параметры."""

    #: тип базы данных
    DB_TYPE: str = 'postgres'
    #: используемый драйвер базы данных
    DB_ENGINE: str = 'psycopg2'

    #: хост базы данных
    DB_HOST: str = getenv('POSTGRES_HOST', '')
    #: хост базы данных
    DB_PORT: int = int(getenv('POSTGRES_PORT', 5432))
    #: хост базы данных
    DB_USER: str = getenv('POSTGRES_USER', '')
    #: хост базы данных
    DB_DB: str = getenv('POSTGRES_DB', '')
    #: хост базы данных
    DB_PASSWORD: str = getenv('POSTGRES_PASSWORD', '')

    #: строка для подключения к базе данных, может быть переопределена с помощью переменной среды
    DB_CONNECTION_STRING: str = getenv(
        'DB_CONNECTION_STRING',
        f'{DB_TYPE}+{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}'
    )

    #: размер чанка, используемый при сохранении данных в базу. Может использоваться для тюнинга производительности
    CHUNK_SIZE = int(getenv('CHUNK_SIZE', 1000))
    #: максимальное количество параллельных запросов при скрапинге
    CONCURRENT_REQUESTS = getenv('CONCURRENT_REQUESTS', 16)

    #: путь к файлу с названиями акций (тикерами), по одной в каждой строке
    TICKERS_FILE: str = getenv('TICKERS_FILE', '/var/input/tickers.txt')
