from typing import Callable
import os

_leangle_schemas = []

# Patches
from .chalice_patches import patch_generate_route_method, patch_generate_swagger  # NOQA
if 'LAMBDA_TASK_ROOT' in os.environ:
    from chalice_utils.swagger import SwaggerGenerator # NOQA
else:
    from chalice.deploy.swagger import SwaggerGenerator # NOQA

SwaggerGenerator.generate_swagger = patch_generate_swagger()
SwaggerGenerator._generate_route_method = patch_generate_route_method()


def add_schema() -> Callable:
    """Add a model to chalice from a schema.

    Example:
        import leangle


        @leangle.add_schema()
        class PetSchema(Schema):
            name = fields.Str()

    """
    def wrapper(cls: Callable) -> Callable:
        _leangle_schemas.append(cls)
        return cls

    return wrapper
