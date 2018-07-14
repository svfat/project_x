from flask import Flask

from db import session
from views import init_app as init_views

app = Flask(__name__)
init_views(app)

@app.teardown_appcontext
def remove_session(_: Exception) -> None:
    session.remove()
