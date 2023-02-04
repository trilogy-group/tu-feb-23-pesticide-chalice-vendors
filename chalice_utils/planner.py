import json

class PlanEncoder(json.JSONEncoder):
    # pylint false positive overriden below
    # https://github.com/PyCQA/pylint/issues/414
    def default(self, o):  # pylint: disable=E0202
        # type: (Any) -> Any
        if isinstance(o, StringFormat):
            return o.template
        return o

class StringFormat(object):
    def __init__(self, template, variables):
        # type: (str, List[str]) -> None
        self.template = template
        self.variables = variables

    def __repr__(self):
        # type: () -> str
        return 'StringFormat("%s")' % self.template

    def __eq__(self, other):
        # type: (Any) -> bool
        return (
            isinstance(other, StringFormat) and
            self.template == other.template and
            self.variables == other.variables
        )
