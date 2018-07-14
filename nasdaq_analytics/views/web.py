from flask import render_template

from db import session, Ticker
from .blueprints import web_blueprint


@web_blueprint.route('/')
def index():
    return render_template('index.html', tickers=session.query(Ticker).all())
