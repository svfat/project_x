from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

# create engine and session
engine = create_engine(Config.DB_CONNECTION_STRING)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

# create automap base
Base = automap_base()

# import pre-declared models here:
from .models import Ticker, HistoricalPrice, InsiderTuple, Insider, InsiderTrade  # noqa

# reflect
Base.prepare(engine, reflect=True)
