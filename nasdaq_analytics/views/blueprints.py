from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api')
web_blueprint = Blueprint('web_blueprint', __name__, url_prefix='/')
