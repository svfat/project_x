"""Модуль, содержащий модели и сессию для работы с БД.

Используется `sqlalchemy.ext.automap`, что позволяет не описывать модели полностью.
Все свойства классов будут созданы динамически, исходя из структуры БД.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

engine = create_engine(Config.DB_CONNECTION_STRING)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

Base = automap_base()

from .models import Ticker, HistoricalPrice, InsiderTuple, Insider, InsiderTrade  # noqa

Base.prepare(engine, reflect=True)
