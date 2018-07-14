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

# reflect
Base.prepare(engine, reflect=True)

# assign auto-generated models here:
Ticker = Base.classes.ticker
HistoricalPrice = Base.classes.historical_price
