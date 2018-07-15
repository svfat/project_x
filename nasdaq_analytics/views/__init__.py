from flask import Flask

from .helpers import views_helper
from .routes import index, insider_trades # noqa


def init_app(app: Flask):
    views_helper.init_app(app)


__all__ = ['init_app']
