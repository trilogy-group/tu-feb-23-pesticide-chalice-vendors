import os
from typing import Any, Callable, Dict, Optional

from chalice.app import Chalice, RouteEntry  # noqa
if 'LAMBDA_TASK_ROOT' in os.environ:
    from chalice_utils.swagger import SwaggerGenerator
    from chalice_utils.models import RestAPI
else:
    from chalice.deploy.swagger import SwaggerGenerator
    from chalice.deploy.models import RestAPI  # noqa

from leangle.leangle import _leangle_schemas

from marshmallow_jsonschema import JSONSchema


original_generate_swagger = SwaggerGenerator.generate_swagger
original_generate_route_method = SwaggerGenerator._generate_route_method


def patch_generate_swagger() -> Callable:
    """Monkey Patch SwaggerGenerator.generate_swagger."""

    def generate_swagger(self,
                         app: Chalice,
                         rest_api: Optional[RestAPI] = None) -> Dict[str, Any]:
        api: Dict[str, Any] = original_generate_swagger(self, app, rest_api)
        _add_leangle_schemas(api)
        return api
    return generate_swagger


def _dict_sweep(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: _dict_sweep(v, key) for k, v in input_dict.items() if k != key}
    elif isinstance(input_dict, list):
        return [_dict_sweep(element, key) for element in input_dict]
    else:
        return input_dict


def _add_leangle_schemas(api: Dict):
    """Add schema dumps to the API."""
    for schema in _leangle_schemas:
        schema_dump = JSONSchema().dump(schema())['definitions']
        api['definitions'].update(_dict_sweep(schema_dump, 'readOnly'))
    return api


def _add_parameters(view: RouteEntry, current: Dict[str, Any]):
    parameters = getattr(
        view.view_function,
        '_leangle_parameters',
        [],
    )

    # Combine existing parameters with leangle defined ones
    current_parameters = current.get('parameters', [])
    current['parameters'] = [*current_parameters, *parameters]

    return current


def _add_tags(view: RouteEntry, current: Dict[str, Any]):
    tags = getattr(
        view.view_function,
        '_leangle_tags',
        [],
    )

    current['tags'] = tags

    return current


def patch_generate_route_method() -> Callable:
    """Monkey Patch SwaggerGenerator._generate_route_method."""

    def _generate_route_method(self, view: RouteEntry) -> Dict[str, Any]:
        current = original_generate_route_method(self, view)
        current['responses'] = getattr(
            view.view_function,
            '_leangle_responses',
            self._generate_precanned_responses(),
        )

        current = _add_parameters(view, current)
        current = _add_tags(view, current)

        return current

    return _generate_route_method
