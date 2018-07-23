"""Модуль, содержащий представления для веб-интерфейса и API."""
from flask import Flask

from .helpers import views_helper
from .routes import *  # noqa


def init_app(app: Flask) -> None:
    """Проинициализировать приложение.

    :param app: объект приложения Flask
    """
    views_helper.init_app(app)


__all__ = ['init_app']
