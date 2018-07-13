from flask import Flask

from .blueprints import api_blueprint, web_blueprint
from .api import index
from .web import index


def init_app(app: Flask) -> None:
    app.register_blueprint(api_blueprint)
    app.register_blueprint(web_blueprint)
