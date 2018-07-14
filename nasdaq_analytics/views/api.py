from flask import jsonify

from db import session, Ticker
from .blueprints import api_blueprint


@api_blueprint.route('/')
def index():
    return jsonify([ticker.symbol for ticker in session.query(Ticker).all()])
