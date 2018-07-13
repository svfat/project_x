from flask import Flask

from db import session
from views import init_app

app = Flask(__name__)
init_app(app)


@app.teardown_appcontext
def remove_session(_: Exception) -> None:
    session.remove()
