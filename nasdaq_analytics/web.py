"""Модуль, содержащий WSGI интерфейс для запуска веб-приложения.

Веб-приложение можно запустить с помощью встроенного во Flask сервера (для разработки),
либо с помощью любого сервера, который поддерживает WSGI интерфейс (например: gunicorn, uWSGI).
"""
from flask import Flask

from db import session
from views import init_app as init_views

app = Flask(__name__)
init_views(app)


@app.teardown_appcontext
def remove_session(_: Exception) -> None:
    """Эта функция вызывается при завершении обработки запроса и закрывает сессию SQLAlchemy.

    :param _: ошибка, которая могла возникнуть при обработке запроса, игнорируется
    """
    session.remove()
