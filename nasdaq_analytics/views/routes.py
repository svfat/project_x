from db import session, Ticker
from .helpers import views_helper


@views_helper.route('/', template_name='index.html')
def index():
    return {
        'tickers': [
            ticker.symbol
            for ticker in session.query(Ticker).order_by(Ticker.symbol).all()
        ]
    }
