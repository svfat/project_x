from functools import wraps
from typing import Callable, Union, Any, Dict

from flask import Flask, Blueprint, render_template, jsonify
from werkzeug.routing import Rule


class ViewsHelper:
    app: Flask

    web_blueprint: Blueprint
    api_blueprint: Blueprint

    def __init__(self):
        self.web_blueprint = Blueprint('web_blueprint', __name__, url_prefix='/')
        self.api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api')

    def init_app(self, app: Flask):
        self.app = app
        self.app.register_blueprint(self.web_blueprint)
        self.app.register_blueprint(self.api_blueprint)

    def route(self, rule: Union[str, Rule], template_name: str, **options):
        def decorator(view_func: Callable[..., Dict]):
            @self.web_blueprint.route(rule, **options)
            @wraps(view_func)
            def web_view_func(*args, **kwargs):
                return render_template(template_name, **view_func(*args, **kwargs))

            @self.api_blueprint.route(rule, **options)
            @wraps(view_func)
            def api_view_func(*args, **kwargs):
                return jsonify(**view_func(*args, **kwargs))

            return view_func

        return decorator


views_helper = ViewsHelper()
