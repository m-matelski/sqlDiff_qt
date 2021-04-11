from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Dict


class BaseUrlTemplate(ABC):
    @abstractmethod
    def feed(self, args: dict):
        pass

    def __repr__(self):
        return self.template

    def __str__(self):
        return self.template


class MandatoryFieldsUrlTemplate(BaseUrlTemplate):
    """
    JDBC url template with mandatory parameters.
    Fills mandatory parameters between '{}' brackets. Throws KeyError if argument missing
    """

    def __init__(self, template: str):
        self.template = template

    def feed(self, args: Dict):
        url = self.template.format(**args)
        return url


class OptionalFieldsUrlTemplate(BaseUrlTemplate):
    """Fills optional parameters between '[{}]'"""

    def __init__(self, template: str):
        self.template = template

    def feed(self, args: Dict):
        OptionalParameter = namedtuple('OptionalParameter', ['i_from', 'i_to', 'param_string'])
        optional_params = []
        open_bracket_idx = None
        url = self.template
        for i, c in enumerate(self.template):
            if c == '[':
                if not open_bracket_idx:
                    open_bracket_idx = i
                else:
                    raise ValueError('Nested optional parameters are unsupported.')
            if c == ']':
                if open_bracket_idx:
                    optional_params.append(
                        OptionalParameter(open_bracket_idx, i, self.template[open_bracket_idx: i + 1]))
                    open_bracket_idx = None
                else:
                    raise ValueError('Invalid url template format.')

        for p in optional_params:
            try:
                filled_arg = p.param_string.format(**args).replace('[', '').replace(']', '')
                url = url.replace(p.param_string, filled_arg)
            except KeyError:
                url = url.replace(p.param_string, '')

        return url


class JdbcUrlTemplate(BaseUrlTemplate):

    def __init__(self, template: str):
        self.template = template

    def feed(self, args: Dict):
        optional_fields_url_template = OptionalFieldsUrlTemplate(self.template)
        mandatory_fields_url_template = MandatoryFieldsUrlTemplate(optional_fields_url_template.feed(args))
        url = mandatory_fields_url_template.feed(args)
        return url
