"""Модуль, содержащий вспомогательные классы и функции для представлений."""
import re
from functools import wraps
from typing import Callable, Union, Dict, Any, List

from flask import Flask, Blueprint, render_template, jsonify, Response
from jsonschema import validate
from werkzeug.routing import Rule

_regex_werkzeug_rule_to_openapi_url_template = re.compile(r'<[^>:]*:?([^>]*)>')


def _convert_werkzeug_rule_to_openapi_url_template(rule: Union[str, Rule]) -> str:
    _rule: str = rule.rule if isinstance(rule, Rule) else rule
    return _regex_werkzeug_rule_to_openapi_url_template.sub(r'{\1}', _rule)


class ViewsHelper:
    """Вспомогательный класс для представлений.

    Смысл существования этого класса в том, чтобы не дублировать код для веб-интерфейса и для API.
    Метод `route` создаёт одновременно представление для веб-интерфейса, которое рендерит шаблон и представление для API,
    которое возвращает json.

    Так же этот класс содержит генерацию спецификации к API в формате OpenAPI (aka Swagger).
    """
    #: объект приложения
    app: Flask

    #: Blueprint для веб-интерфейса
    web_blueprint: Blueprint
    #: Blueprint для API
    api_blueprint: Blueprint

    #: спецификация к API в формете OpenAPI 3
    spec: Dict[str, Any]
    #: контекст, который передаётся во все шаблоны
    global_context: Dict[str, Any]

    def __init__(self) -> None:
        """Инициализация."""
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
        self.global_context = {
            'price_types': {
                'open': 'цена открытия',
                'high': 'максимум за день',
                'low': 'минимум за день',
                'close': 'цена закрытия',
            }
        }

    def init_app(self, app: Flask) -> None:
        """Инициализация приложения.

        :param app: объект приложения, который надо проинициализировать
        """
        self.app = app
        self.app.register_blueprint(self.web_blueprint)
        self.app.register_blueprint(self.api_blueprint)

        @self.app.route('/swagger-ui')
        def swagger_ui():
            """Веб-интерфейс, содержащий автогенерированную документацию к API."""
            return render_template('swagger-ui/index.html')

        @self.app.route('/swagger.json')
        def swagger_json():
            """Метод, возвращающий спецификацию API в формате OpenAPI."""
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
    ) -> Callable[[Callable[..., Dict]], Callable[..., Dict]]:
        """Создание декоратора, который регистрирует представление и для API и для веб-интерфейса.

        Аналог `Flask.route` и `Blueprint.route`.

        :param rule: правило для роутинга (строка или Rule)
        :param template_name: название шаблона для веб-интерфейса
        :param schema: jsonschema для валидации ответа для API и генерирования спецификации к API
        :param parameters: параметры, которые принимает этот метод API, нужны для генерирования спецификации к API
        :param description: описание метода API
        :param options: другие параметры, которые будут переданы в `Blueprint.route`
        :return: декоратор
        """
        self._add_path_to_spec(rule, schema, parameters, description)

        def decorator(view_func: Callable[..., Dict]) -> Callable[..., Dict]:
            """Декоратор, который регистрирует представление и для API и для веб-интерфейса.

            :param view_func: представление (view)
            :return: представление (view)
            """
            @self.web_blueprint.route(rule, **options)
            @wraps(view_func)
            def web_view_func(*args, **kwargs) -> Response:
                """Обработчик запроса для веб-интерфейса.

                Вызывает функцию представления и использует её результаты для рендеринга нужного шаблона.

                :return: ответ на запрос
                """
                context = self.global_context.copy()
                context.update(view_func(*args, **kwargs))
                return render_template(template_name, **context)

            @self.api_blueprint.route(rule, **options)
            @wraps(view_func)
            def api_view_func(*args, **kwargs) -> Response:
                """Обработчик запроса для API.

                Вызывает функцию представления, валидирует результат и возвращает JSON-ответ.

                :return: ответ на запрос
                """
                result = view_func(*args, **kwargs)
                validate(result, schema)
                return jsonify(**view_func(*args, **kwargs))

            return view_func

        return decorator


views_helper = ViewsHelper()
