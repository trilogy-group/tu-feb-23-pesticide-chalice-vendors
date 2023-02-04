from typing import List, Dict, Optional as Opt, Any  # noqa
from typing import cast
from attr import attrs, attrib, Factory


class Model(object):
    def dependencies(self):
        # type: () -> List[Model]
        return []


@attrs
class ManagedModel(Model):
    resource_name = attrib()  # type: str
    # Subclasses must fill in this attribute.
    resource_type = ''        # type: str


@attrs
class RestAPI(ManagedModel):
    resource_type = 'rest_api'
    swagger_doc = attrib()                       # type: DV[Dict[str, Any]]
    minimum_compression = attrib()               # type: str
    api_gateway_stage = attrib()                 # type: str
    endpoint_type = attrib()                     # type: str
    lambda_function = attrib()                   # type: LambdaFunction
    xray = attrib(default=False)                 # type: bool
    policy = attrib(default=None)                # type: Opt[IAMPolicy]
    authorizers = attrib(default=Factory(list))  # type: List[LambdaFunction]
    domain_name = attrib(default=None)           # type: Opt[DomainName]
    vpce_ids = attrib(default=None)              # type: Opt[List[str]]

    def dependencies(self):
        # type: () -> List[Model]
        resources = []  # type: List[Model]
        resources.extend([self.lambda_function] + self.authorizers)
        if self.domain_name is not None:
            resources.append(self.domain_name)
        return cast(List[Model], resources)
