from os import getenv


class Config:
    # specify db type and db engine
    DB_TYPE: str = 'postgres'
    DB_ENGINE: str = 'psycopg2'

    # get credentials
    DB_HOST: str = getenv('POSTGRES_HOST', '')
    DB_PORT: int = int(getenv('POSTGRES_PORT', 5432))
    DB_USER: str = getenv('POSTGRES_USER', '')
    DB_DB: str = getenv('POSTGRES_DB', '')
    DB_PASSWORD: str = getenv('POSTGRES_PASSWORD', '')

    # it is possible to override the connection string
    #   with an environment variable
    DB_CONNECTION_STRING: str = getenv(
        'DB_CONNECTION_STRING',
        f'{DB_TYPE}+{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}'
    )

    CHUNK_SIZE = int(getenv('CHUNK_SIZE', 1000))
    CONCURRENT_REQUESTS = getenv('CONCURRENT_REQUESTS', 16)
