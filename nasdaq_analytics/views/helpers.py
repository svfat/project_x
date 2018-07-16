import re
from functools import wraps
from typing import Callable, Union, Dict, Any, List

from flask import Flask, Blueprint, render_template, jsonify
from jsonschema import validate
from werkzeug.routing import Rule

_regex_werkzeug_rule_to_openapi_url_template = re.compile(r'<[^>:]*:?([^>]*)>')


def _convert_werkzeug_rule_to_openapi_url_template(rule: Union[str, Rule]) -> str:
    _rule: str = rule.rule if isinstance(rule, Rule) else rule
    return _regex_werkzeug_rule_to_openapi_url_template.sub(r'{\1}', _rule)


class ViewsHelper:
    app: Flask

    web_blueprint: Blueprint
    api_blueprint: Blueprint

    spec: Dict[str, Any]

    def __init__(self):
        self.web_blueprint = Blueprint('web_blueprint', __name__, url_prefix='/')
        self.api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api')
        self.spec = {
            'openapi': '3.0.1',
            'info': {
                'title': 'NASDAQ Analytics',
                'version': '0.0.1',
            },
            'paths': {},
        }

    def init_app(self, app: Flask):
        self.app = app
        self.app.register_blueprint(self.web_blueprint)
        self.app.register_blueprint(self.api_blueprint)

        @self.app.route('/swagger-ui')
        def swagger_ui():
            return render_template('swagger-ui/index.html')

        @self.app.route('/swagger.json')
        def swagger_json():
            return jsonify(self.spec)

    def _add_path_to_spec(
        self,
        rule: Union[str, Rule],
        schema: Dict[str, Any],
        parameters: List[Dict],
        description: str = '',
    ):
        path_url = _convert_werkzeug_rule_to_openapi_url_template(rule)
        path_object = {
            'get': {
                'parameters': parameters,
                'description': description,
                'responses': {
                    200: {
                        'description': 'Успешное получение данных.',
                        'content': {
                            "application/json": {
                                'schema': schema
                            }
                        },
                    },
                },
            },
        }
        self.spec['paths'][f'/api{path_url}'] = path_object

    def route(
        self,
        rule: Union[str, Rule],
        template_name: str,
        schema: Dict[str, Any],
        parameters: List[Dict],
        description: str = '',
        **options,
    ):
        self._add_path_to_spec(rule, schema, parameters, description)

        def decorator(view_func: Callable[..., Dict]):
            @self.web_blueprint.route(rule, **options)
            @wraps(view_func)
            def web_view_func(*args, **kwargs):
                return render_template(template_name, **view_func(*args, **kwargs))

            @self.api_blueprint.route(rule, **options)
            @wraps(view_func)
            def api_view_func(*args, **kwargs):
                result = view_func(*args, **kwargs)
                validate(result, schema)
                return jsonify(**view_func(*args, **kwargs))

            return view_func

        return decorator


views_helper = ViewsHelper()
