from flask import render_template

from db import session, Symbols
from .blueprints import web_blueprint


@web_blueprint.route('/')
def index():
    return render_template('index.html', symbols=session.query(Symbols).all())
