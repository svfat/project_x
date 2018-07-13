from flask import jsonify

from db import session, Symbols
from .blueprints import api_blueprint


@api_blueprint.route('/')
def index():
    return jsonify([symbol.symbol for symbol in session.query(Symbols).all()])
